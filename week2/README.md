# Week 2 - Action Item Extractor

Action Item Extractor 是一个小型 FastAPI + SQLite 应用，用于将自由格式的笔记转换为可保存的行动项。它包括：

- 位于 `/` 的简洁 HTML 前端
- 基于启发式规则的行动项提取
- 可选的 Ollama LLM 行动项提取
- 笔记存储与查询
- 行动项列表展示与完成状态跟踪

后端数据存储在 `week2/data/app.db` 中，该文件会在 FastAPI 应用启动时自动创建。

## 项目结构

```text
week2/
  app/
    main.py                 # FastAPI 应用设置、前端路由、路由注册
    config.py               # 应用配置和路径
    db.py                   # SQLite 连接、表结构初始化、查询辅助函数
    errors.py               # 共享 HTTP 错误辅助函数
    schemas.py              # Pydantic 请求/响应模型
    routers/
      notes.py              # 笔记 API endpoints
      action_items.py       # 行动项 API endpoints
    services/
      extract.py            # 启发式和 Ollama 提取逻辑
  frontend/
    index.html              # 简洁浏览器界面
  tests/
    test_extract.py         # 提取逻辑测试
```

## 安装依赖

在仓库根目录运行：

```powershell
poetry install
```

如果要使用 LLM 提取 endpoint，还需要确保已经安装并启动 Ollama，并且已拉取配置中的模型。默认模型是 `llama3.1:8b`；可以通过 `OLLAMA_ACTION_ITEMS_MODEL` 环境变量覆盖该配置。

## 运行项目

在仓库根目录运行：

```powershell
poetry run uvicorn week2.app.main:app --reload
```

然后打开：

```text
http://127.0.0.1:8000/
```

前端支持粘贴笔记、选择是否保存笔记、使用启发式提取器提取行动项、使用 LLM 提取器提取行动项，以及查看已保存的笔记。

## API Endpoints

### 前端

| Method | Path | 说明 |
| --- | --- | --- |
| `GET` | `/` | 返回 `week2/frontend/index.html` 中的 HTML 前端。 |
| `GET` | `/static/*` | 提供 `week2/frontend` 目录中的静态文件。 |

### 笔记

| Method | Path | Request Body | 说明 |
| --- | --- | --- | --- |
| `POST` | `/notes` | `{"content": "..."}` | 创建一条笔记。空内容会返回 `400`。 |
| `GET` | `/notes` | none | 列出所有已保存笔记，最新的在前。 |
| `GET` | `/notes/{note_id}` | none | 根据 ID 返回一条笔记。笔记不存在时返回 `404`。 |

示例：

```powershell
curl.exe -X POST http://127.0.0.1:8000/notes `
  -H "Content-Type: application/json" `
  -d "{\"content\":\"TODO: write tests\"}"
```

### 行动项

| Method | Path | Request Body / Query | 说明 |
| --- | --- | --- | --- |
| `POST` | `/action-items/extract` | `{"text": "...", "save_note": true}` | 使用基于规则的启发式逻辑提取行动项。如果 `save_note` 为 true，原始文本也会被保存为笔记。空文本会返回 `400`。 |
| `POST` | `/action-items/extract-llm` | `{"text": "...", "save_note": true}` | 使用 Ollama 提取行动项。使用 `OLLAMA_ACTION_ITEMS_MODEL`，或默认模型 `llama3.1:8b`。 |
| `GET` | `/action-items` | optional `?note_id=1` | 列出所有行动项，也可以只列出关联到某条笔记的行动项。 |
| `POST` | `/action-items/{action_item_id}/done` | `{"done": true}` | 将行动项标记为已完成或未完成。 |

启发式提取请求示例：

```powershell
curl.exe -X POST http://127.0.0.1:8000/action-items/extract `
  -H "Content-Type: application/json" `
  -d "{\"text\":\"- [ ] Set up database\nTODO: write tests\",\"save_note\":true}"
```

典型提取响应：

```json
{
  "note_id": 1,
  "items": [
    {
      "id": 1,
      "text": "Set up database"
    },
    {
      "id": 2,
      "text": "TODO: write tests"
    }
  ]
}
```

## 提取行为

启发式提取器会识别：

- 项目符号行，例如 `- task`、`* task`，以及类似 `1. task` 的编号项
- 以 `todo:`、`action:` 或 `next:` 开头的关键词行
- 类似 `[ ]` 和 `[todo]` 的复选框标记
- 一组简单的祈使句开头词作为兜底规则，例如 `add`、`create`、`fix`、`update` 和 `write`

LLM 提取器会把笔记文本发送给 Ollama，并要求返回一个由可执行任务字符串组成的 JSON 数组。如果 Ollama 返回无效 JSON 或不符合预期的数据结构，提取器会返回空列表。

## 运行测试

在仓库根目录运行：

```powershell
poetry run pytest week2/tests
```

当前测试文件会覆盖启发式提取器的 bullet list、checkbox、keyword-prefixed lines、empty input 等场景，并包含一个 LLM 提取测试。运行 `poetry run pytest week2/tests` 时，这些测试都会被自动收集。LLM 测试会调用 `extract_action_items_llm()`，因此需要 Ollama 正在运行，并且配置的模型可用。
