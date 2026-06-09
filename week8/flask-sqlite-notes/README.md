# Flask SQLite 笔记管理器

一个用于创建、查看、编辑和删除笔记的小型 Web 应用。笔记会持久化存储在本地 SQLite 数据库中。

## 技术栈

- Python
- Flask
- SQLite
- 使用 Jinja 的 HTML 模板
- CSS

## 环境要求

- Python 3.10 或更高版本
- `pip`

## 安装

可选但推荐：先创建并激活虚拟环境。

```bash
conda create -n week8-flask python=3.12
conda activate week8-flask
```

安装项目依赖（需先进入当前文件夹路径）：

```bash
pip install -r requirements.txt
```

## 本地运行

启动 Flask 应用：

```bash
python app.py
```

打开终端中显示的本地地址，通常是：

```text
http://127.0.0.1:5000
```

应用首次启动时会在项目文件夹中自动创建 `notes.db`。

## 功能

- 创建笔记，标题必填，内容可选
- 列出所有笔记
- 编辑已有笔记
- 在浏览器确认后删除笔记
- 针对验证错误、成功操作和笔记不存在等情况显示提示消息
- 自动生成 `created_at` 和 `updated_at` 时间戳

## 已知限制

- 没有用户账号或身份认证
- 没有搜索、标签或筛选功能
- 时间戳使用服务器本地时间
- SQLite 用作简单的本地数据库，不适合高并发生产环境
