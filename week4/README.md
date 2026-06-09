# Week 4

Week 4 是一个用于练习 Claude Code 自动化工作流的 FastAPI + SQLite starter application。本周重点是在已有应用基础上创建可复用的自动化，并用这些自动化扩展和验证应用功能。

- FastAPI backend with SQLite
- Static frontend served by FastAPI
- Notes and action items workflow
- Pytest tests
- Ruff/Black formatting and linting
- Claude Code slash command automations

## Quickstart

1. 在仓库根目录安装依赖

```powershell
poetry install
```

2. 运行应用

```powershell
cd week4
make run
```

打开：

```text
http://127.0.0.1:8000
```

API 文档：

```text
http://127.0.0.1:8000/docs
```

## Structure

```text
week4/
  .claude/commands/       # Claude Code slash command automations
  backend/                # FastAPI app, routers, schemas, services, tests
  frontend/               # Static HTML/CSS/JS frontend
  data/                   # SQLite seed data
  docs/                   # API docs and task notes
  assignment.md           # Assignment description
  writeup.md              # Automation write-up
```

## Automations

本周实现了三个 Claude Code slash commands：

- `/add-feature`：按固定流程添加或修改功能，并运行测试和 lint。
- `/verify-change`：检查当前 diff，运行 `make test` 和 `make lint`，判断修改是否可以保留。
- `/docs-sync`：对照当前后端 API 和前端行为同步文档。

这些自动化文件位于：

```text
week4/.claude/commands/
```

## Tests

在 `week4/` 目录下运行：

```powershell
make test
```

## Formatting/Linting

在 `week4/` 目录下运行：

```powershell
make format
make lint
```

## Documentation

- 作业说明见 `assignment.md`
- 自动化说明和使用记录见 `writeup.md`
- API 文档见 `docs/API.md`
