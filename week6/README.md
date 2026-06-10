# Week 6 – Semgrep 漏洞扫描与修复

本项目是一个 FastAPI 应用（包含前后端），使用 Semgrep 进行静态代码安全扫描，发现并修复了三个阻断级（Blocking）安全漏洞。

## 漏洞扫描概览

使用命令：
```bash
semgrep scan --config=p/security-audit --config=p/secrets week6
```

扫描结果共发现 3 个阻断级漏洞，全部位于 `backend/app/routers/notes.py`：

| 漏洞类型 | Semgrep 规则 | 风险等级 |
|---------|--------------|----------|
| `eval()` 任意代码执行 | `eval-detected` |  阻断 |
| `subprocess` 命令注入 | `subprocess-shell-true` |  阻断 |
| `urlopen` 本地文件读取 | `dynamic-urllib-use-detected` |  阻断 |

---

## 修复详情

### 修复 1：禁止 `eval()` 执行任意表达式

**位置**：`backend/app/routers/notes.py` 第 104 行  
**原代码**：
```python
result = str(eval(expr))
```
**修复方式**：使用 `ast` 模块安全解析，仅允许数字常量与白名单运算符（`+` `-` `*` `/` `**` 及一元负号）。  
**效果**：彻底阻断函数调用、模块导入等任意代码执行。

### 修复 2：禁止 `shell=True` 命令注入

**位置**：`backend/app/routers/notes.py` 第 112 行  
**原代码**：
```python
subprocess.run(cmd, shell=True, ...)
```
**修复方式**：
- 改为 `shell=False`，以列表形式接收参数
- 增加命令白名单：`["echo", "date", "whoami", "pwd"]`
- 添加 `timeout=5` 防止资源耗尽

**效果**：消除 shell 元字符注入风险，仅允许执行预定义的安全命令。

### 修复 3：禁止 `urllib` 读取本地文件

**位置**：`backend/app/routers/notes.py` 第 120 行  
**原代码**：
```python
from urllib.request import urlopen
with urlopen(url) as res: ...
```
**修复方式**：
- 替换为 `requests` 库
- 仅允许 `http` / `https` 协议
- 禁用自动重定向、设置超时

**效果**：阻止 `file://` 等危险协议，防止任意文件读取。

---

## 环境搭建与运行

### 1. 创建虚拟环境并激活
```bash
python -m venv venv
# Windows
venv\Scripts\activate.bat
```

### 2. 安装依赖
```bash
cd week6
pip install fastapi uvicorn sqlalchemy pydantic pyyaml Jinja2 MarkupSafe Werkzeug requests python-dotenv aiofiles
pip install -r requirements.txt
```

### 3. 启动应用
```bash
cd backend
uvicorn app.main:app --reload
```
服务默认运行在 `http://127.0.0.1:8000`


## 验证修复

重新运行 Semgrep 扫描，确认三个漏洞已消失：
```bash
semgrep scan --config=p/security-audit --config=p/secrets week6
```
预期输出：`Findings: 0`

### 功能测试用例

| 接口 | 正常请求 | 恶意请求（应被拒绝） |
|------|----------|----------------------|
| `/debug/eval?expr=2+3*4` | 返回 `14` | `expr=__import__('os').system('whoami')` → 400 错误 |
| `/debug/run?args[]=echo&args[]=hello` | 返回 `hello` | `args[]=cat&args[]=/etc/passwd` → 403 错误 |
| `/debug/fetch?url=https://example.com` | 返回页面内容 | `url=file:///etc/passwd` → 400 错误 |