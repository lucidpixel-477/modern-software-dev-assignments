from json import JSONDecodeError

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("week3-weather")

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"  # 地理编码api
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"  # 天气预报api
AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"  # 空气质量api
# 由于ruff限制一行的长度不能超过100，因此将这个字符串单独提出来
DAILY_FORECAST_FIELDS = (
    "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max"
)


def weather_code_to_text(code: int | None) -> str:
    """将Open-Meteo的天气代码转换为简短可读的标签."""
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }
    return weather_codes.get(code, f"Unknown weather code: {code}")


def parse_json_response(response: httpx.Response, api_name: str) -> dict:
    """解析上游 JSON 响应；如果响应无效，则返回用户友好的错误。"""
    try:
        data = response.json()
    except JSONDecodeError as exc:
        raise RuntimeError(f"{api_name} returned invalid JSON.") from exc

    if not isinstance(data, dict):
        raise RuntimeError(f"{api_name} returned an unexpected JSON format.")

    return data


def find_location(city: str) -> dict:
    """根据城市名称查找其纬度、经度、城市名称和国家。"""
    city = city.strip()
    # 确保城市名称不为空
    if not city:
        raise ValueError("City name cannot be empty.")

    # 通过Open-Meteo的地理编码API查找城市
    try:
        response = httpx.get(
            GEOCODING_URL,
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=10,
        )
        response.raise_for_status()
    # 请求超时
    except httpx.TimeoutException as exc:
        raise RuntimeError("Location lookup timed out. Please try again later.") from exc
    # http状态错误
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 429:
            raise RuntimeError("Location lookup was rate limited. Please try again later.") from exc
        raise RuntimeError(
            f"Location lookup failed with HTTP status {exc.response.status_code}."
        ) from exc
    # 其他http错误
    except httpx.HTTPError as exc:
        raise RuntimeError("Location lookup failed because the API is unavailable.") from exc

    # 将api返回的json转换成字典后取出results字段
    results = parse_json_response(response, "Location lookup API").get("results", [])
    if not results:
        raise ValueError(f"No location found for city: {city}")

    location = results[0]
    return {
        "name": location["name"],
        "country": location.get("country", "Unknown country"),
        "latitude": location["latitude"],
        "longitude": location["longitude"],
    }


# 这是一个mcp工具函数
@mcp.tool()
def get_current_weather(city: str) -> str:
    """获取某个城市的当前天气."""
    try:
        location = find_location(city)
        response = httpx.get(
            FORECAST_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": "temperature_2m,wind_speed_10m,weather_code",
                "timezone": "auto",
            },
            timeout=10,
        )
        # 检查http请求有没有失败
        response.raise_for_status()
    except (ValueError, RuntimeError) as exc:
        return f"Error: {exc}"
    except httpx.TimeoutException:
        return "Error: Weather request timed out. Please try again later."
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 429:
            return "Error: Weather API rate limit reached. Please try again later."
        return f"Error: Weather API returned HTTP status {exc.response.status_code}."
    except httpx.HTTPError:
        return "Error: Weather API is unavailable."

    try:
        current = parse_json_response(response, "Weather API").get("current")
    except RuntimeError as exc:
        return f"Error: {exc}"

    if not current:
        return f"Error: No current weather data found for {location['name']}."

    return (
        f"Current weather for {location['name']}, {location['country']}:\n"
        f"Temperature: {current.get('temperature_2m')} C\n"
        f"Wind speed: {current.get('wind_speed_10m')} km/h\n"
        f"Weather: {weather_code_to_text(current.get('weather_code'))}\n"
        f"Time: {current.get('time')}"
    )


# 这是一个mcp工具
@mcp.tool()
def get_weather_forecast(city: str, days: int = 3) -> str:
    """获取某个城市未来1到7天的天气预报."""
    if days < 1 or days > 7:
        return "Error: days must be between 1 and 7."

    try:
        location = find_location(city)
        response = httpx.get(
            FORECAST_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "daily": DAILY_FORECAST_FIELDS,
                "timezone": "auto",
                "forecast_days": days,
            },
            timeout=10,
        )
        # 检查http请求有没有失败
        response.raise_for_status()
    except (ValueError, RuntimeError) as exc:
        return f"Error: {exc}"
    except httpx.TimeoutException:
        return "Error: Weather forecast request timed out. Please try again later."
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 429:
            return "Error: Weather API rate limit reached. Please try again later."
        return f"Error: Weather API returned HTTP status {exc.response.status_code}."
    except httpx.HTTPError:
        return "Error: Weather API is unavailable."

    try:
        daily = parse_json_response(response, "Weather forecast API").get("daily")
    except RuntimeError as exc:
        return f"Error: {exc}"

    if not daily or not daily.get("time"):
        return f"Error: No forecast data found for {location['name']}."

    lines = [f"{days}-day forecast for {location['name']}, {location['country']}:"]
    for index, date in enumerate(daily["time"]):
        lines.append(
            f"{date}: "
            f"{daily['temperature_2m_min'][index]} C - "
            f"{daily['temperature_2m_max'][index]} C, "
            f"precipitation probability {daily['precipitation_probability_max'][index]}%, "
            f"{weather_code_to_text(daily['weather_code'][index])}"
        )

    return "\n".join(lines)


@mcp.tool()
def get_air_quality(city: str) -> str:
    """获取某个城市的当前空气质量."""
    try:
        location = find_location(city)
        response = httpx.get(
            AIR_QUALITY_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": "us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone",
                "timezone": "auto",
            },
            timeout=10,
        )
        response.raise_for_status()
    except (ValueError, RuntimeError) as exc:
        return f"Error: {exc}"
    except httpx.TimeoutException:
        return "Error: Air quality request timed out. Please try again later."
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 429:
            return "Error: Air quality API rate limit reached. Please try again later."
        return f"Error: Air quality API returned HTTP status {exc.response.status_code}."
    except httpx.HTTPError:
        return "Error: Air quality API is unavailable."

    try:
        current = parse_json_response(response, "Air quality API").get("current")
    except RuntimeError as exc:
        return f"Error: {exc}"

    if not current:
        return f"Error: No air quality data found for {location['name']}."

    return (
        f"Current air quality for {location['name']}, {location['country']}:\n"
        f"US AQI: {current.get('us_aqi')}\n"
        f"PM2.5: {current.get('pm2_5')} ug/m3\n"
        f"PM10: {current.get('pm10')} ug/m3\n"
        f"Carbon monoxide: {current.get('carbon_monoxide')} ug/m3\n"
        f"Nitrogen dioxide: {current.get('nitrogen_dioxide')} ug/m3\n"
        f"Ozone: {current.get('ozone')} ug/m3\n"
        f"Time: {current.get('time')}"
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
