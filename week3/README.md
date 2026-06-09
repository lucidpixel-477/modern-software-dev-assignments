# Week 3 - Weather MCP Server

本项目实现了一个本地 STDIO MCP server，用来封装 Open-Meteo API。
MCP client 可以通过城市名称调用天气和空气质量相关工具。

## 注意事项

- 本周的作业需要另外创建一个conda虚拟环境week3-mcp。
- 任何命令行均在anaconda prompt中运行。
- 使用 MCP Inspector 命令行之前需要先进入 week3/server 目录。
- 使用的MCP client为官方的MCP Inspector以及Claude Code。
- 需要提前安装 Poetry，用于安装依赖和运行 server。

## 使用的外部 API

- Open-Meteo Geocoding API：将城市名称转换为纬度和经度。
- Open-Meteo Forecast API：返回当前天气和每日天气预报。
- Open-Meteo Air Quality API：返回当前 AQI 和污染物指标。

这些 API 不需要 API key。

## 环境设置（如果已有这个环境可以跳过）

在anaconda prompt中进入项目server目录，并确保当前环境为base，运行以下命令行。

```anaconda prompt
conda create -n week3-mcp python=3.12
conda activate week3-mcp
cd week3/server
poetry install --no-interaction
```

此外，还需前往

```
https://nodejs.org/zh-cn/download
```

下载node.js到本地，并在命令行中分别运行

```anaconda prompt
node -v
npm -v
npx -v
```

检查是否下载成功

## 本地运行

在anaconda prompt中进入项目server目录，并确保当前环境为week3-mcp，运行main.py文件

```anaconda prompt
cd week3/server
conda activate week3-mcp
poetry run python main.py
```

这个 server 使用 STDIO transport，因此应该由 MCP client 启动，而不是像普通
HTTP server 一样直接访问，所以不建议直接运行。

## MCP Inspector

在 `week3/server` 目录下运行：

```
npx @modelcontextprotocol/inspector poetry run python main.py
```

或者在```任意目录```下运行：

```
npx @modelcontextprotocol/inspector poetry -C D:\modern-software-dev-assignments\week3\server run python main.py
```

然后终端就会自动打开浏览器进入MCP Inspector页面，可以在此页面调用MCP工具进行使用。

点击```Connect```后点击上方的```Tools```即可使用已经定义好的MCP Tools。

## Claude Code

在```anaconda prompt```中进入```week3-mcp```环境后输入：

```
claude mcp add --transport stdio week3-weather -- poetry -C D:\modern-software-dev-assignments\week3\server run python main.py
```

后面的路径注意替换成自己的 `week3/server` 文件夹绝对路径。

这个命令会把 MCP server 添加到 Claude Code 的用户级配置中。本机实际保存位置为：

```text
C:\Users\lenovo\.claude.json
```

其中 `mcpServers` 里的配置名称是 `week3-weather`，启动方式是：

```text
poetry -C D:\modern-software-dev-assignments\week3\server run python main.py
```

随后直接输入

```
claude
```

进入 Claude Code。

注意：进入 Claude Code 前需要保证当前环境为 `week3-mcp`。


## 工具

### `get_current_weather`

获取某个城市的当前天气。

#### 在 MCP Inspector 中

输入：

```json
{
  "city": "Shanghai"
}
```

示例输出：

```text
Current weather for Shanghai, China:
Temperature: 23.1 C
Wind speed: 12.4 km/h
Weather: Partly cloudy
Time: 2026-05-28T21:45
```

#### 在 Claude Code 中

输入

```prompt
Use the week3-weather MCP tool to get current weather for Shanghai.
```

### `get_weather_forecast`

获取某个城市未来 1 到 7 天的天气预报。

#### 在 MCP Inspector 中

输入：

```json
{
  "city": "Shanghai",
  "days": 3
}
```

示例输出：

```text
3-day forecast for Shanghai, China:
2026-05-28: 19.2 C - 25.4 C, precipitation probability 20%, Partly cloudy
2026-05-29: 20.1 C - 27.0 C, precipitation probability 10%, Clear sky
2026-05-30: 21.3 C - 28.2 C, precipitation probability 30%, Slight rain
```

#### 在 Claude Code 中

输入

```prompt
Call get_weather_forecast for Tokyo for 3 days.
```

### `get_air_quality`

获取某个城市的当前空气质量指标。

#### 在 MCP Inspector 中

输入：

```json
{
  "city": "Shanghai"
}
```

示例输出：

```text
Current air quality for Shanghai, China:
US AQI: 72
PM2.5: 21.4 ug/m3
PM10: 42.8 ug/m3
Carbon monoxide: 180.0 ug/m3
Nitrogen dioxide: 18.5 ug/m3
Ozone: 93.2 ug/m3
Time: 2026-05-28T21:00
```

#### 在 Claude Code 中

输入

```prompt
Use week3-weather to get air quality for Beijing.
```

## 错误处理

遇到以下情况时，server 会返回用户可读的错误信息：

- 城市名称为空。
- Geocoding API 找不到对应城市。
- 上游 API 返回 HTTP 错误。
- 上游 API 返回限流错误。
- 请求超时。
- 天气或空气质量结果为空。
- 天气预报天数不在支持的 1 到 7 天范围内。

每个上游 HTTP 请求都设置了 10 秒超时。Open-Meteo 可能会对高频使用进行限流，
所以如果上游服务返回限流或临时失败状态，client 应稍后再重试。
