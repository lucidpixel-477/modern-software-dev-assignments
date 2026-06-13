# Week 6 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## Brief findings overview 
Semgrep扫描共发现3个阻塞级高风险代码漏洞，全部位于`week6/backend/app/routers/notes.py`文件中：
1. eval()任意代码执行漏洞：攻击者可通过恶意输入执行任意Python代码
2. subprocess shell=True命令注入漏洞：攻击者可通过恶意输入执行任意系统命令
3. 动态urllib任意文件读取漏洞：攻击者可通过构造file://协议URL读取服务器任意文件


## Fix #1
a. File and line(s)
> week6\backend\app\routers\notes.py 第102-105行
>（@router.get("/debug/eval") 中的 result = str(eval(expr))）


b. Rule/category Semgrep flagged
>python.lang.security.audit.eval-detected.eval-detected`


c. Brief risk description
>代码使用`eval()`函数直接执行用户输入的表达式。攻击者可以构造包含系统命令的恶意输入（如`__import__('os').system('rm -rf /')`），在服务器上执行任意Python代码，完全控制整个系统。


d. Your change (short code diff or explanation, AI coding tool usage)
>用 ast 模块构建安全的表达式求值器：
>仅解析数学表达式，限制节点类型为 Constant（仅整数/浮点数）、BinOp、UnaryOp。
>使用白名单操作符字典（+、-、*、/、**、取负），拒绝任何未定义的运算。
>所有非白名单的 AST 节点均抛出 HTTPException，防止执行任意代码。
>将原始 eval(expr) 替换为 eval_node(tree.body)，其中 tree = ast.parse(expr, mode='eval')。


e. Why this mitigates the issue
>不再依赖 Python 的 eval() 动态执行任意代码，而是将用户输入限制在纯粹的数学表达式范围内。
>通过白名单机制，彻底阻断函数调用、属性访问、导入模块等危险操作
>即使攻击者构造复杂 payload 也会因操作符或节点类型不在白名单而被拒绝，从根本上消除代码注入风险。


## Fix #2
a. File and line(s)
> `week6/backend/app/routers/notes.py` 第108-113行


b. Rule/category Semgrep flagged
> python.lang.security.audit.subprocess-shell-true.subprocess-shell-true`


c. Brief risk description
> subprocess.run(cmd, shell=True) 将用户输入的字符串直接传递给系统 shell 执行
> 攻击者可利用 shell 元字符（;、|、&& 等）注入任意命令，例如 cmd=echo; cat /etc/passwd，导致服务器被完全控制。


d. Your change (short code diff or explanation, AI coding tool usage)
>将接口参数从 cmd: str 改为 args: list[str] = Query(...)，强制接收列表形式的命令及参数。
>设置 shell=False，禁止通过 shell 执行。
>引入命令白名单 allowed_commands = ["echo", "date", "whoami", "pwd"]，仅允许执行列表内命令。
>添加超时设置 timeout=5 防止资源耗尽，并对异常分类处理。


e. Why this mitigates the issue
> shell=False 使命令直接由系统调用执行，不会经过 shell 解析，因此无法利用 shell 元字符注入额外命令。
> 参数以列表传递，杜绝了字符串拼接带来的注入可能。
> 命令白名单进一步限制了可执行程序的种类，即便攻击者能控制 args 内容也无法调用危险命令，实现了纵深防御。

## Fix #3
a. File and line(s)
> `week6/backend/app/routers/notes.py` 第116-122行


b. Rule/category Semgrep flagged
> `python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected`


c. Brief risk description
> urllib 的 urlopen 支持 file:// 协议
> 攻击者如果控制 URL 参数（如 url=file:///etc/passwd），可以读取服务器上的任意文件，导致敏感信息泄露。


d. Your change (short code diff or explanation, AI coding tool usage)
> 使用 requests 库替代 urllib.request.urlopen。
> 通过 urllib.parse.urlparse 解析用户输入的 URL，检验 scheme 必须为 http 或 https，否则返回 400 错误。
> 添加超时、禁止重定向、自定义 User‑Agent 头，防止被目标服务器反爬或 SSRF 探测内网。
> 异常统一捕获并返回友好错误信息。


e. Why this mitigates the issue
> requests 库默认不支持 file:// 协议，从根本上杜绝了本地文件读取。
> 对 URL scheme 的白名单校验（仅允许 http/https）进一步确保只能发起对外部 Web 资源的请求，有效阻止利用 file://、gopher:// 等危险协议进行内网探测或文件读取。
> 附加的超时和禁止重定向也降低了 SSRF 攻击的利用可能性。