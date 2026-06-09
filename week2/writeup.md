# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **王昱晅** \
SUNet ID: **302024674006** \
Citations: **使用Codex辅助完成了TODO任务中的代码生成与重构工作。**

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
分析现有的在week2/app/services/extract.py中的extract_action_items()函数，分析这个函数的功能。这个函数目前是通过预先定义好的启发式规则来提取行动项的。我需要你实现一个由大语言模型ollama驱动的替代版本extract_action_items_llm()函数。你可以参考https://ollama.com/blog/structured-outputs这个文档来使模型输出字符串组成的JSON数组，还可以参考https://ollama.com/library这个文档看有哪些可以调用的ollama模型，建议先从小一点的模型开始。extract_action_items_llm()函数直接写在week2/app/services/extract.py文件的最后
``` 

Generated Code Snippets:
```
Modified files:
1. `week2/app/services/extract.py`
   - Lines 92-93: 新增了 `extract_action_items_llm()` 函数定义和函数说明。
   - Lines 94-95: 新增了空输入处理逻辑，如果输入文本为空或只包含空格，就直接返回空列表。
   - Lines 97-101: 新增了模型选择和 JSON Schema 设置。函数默认使用 `llama3.1:8b`，同时支持通过函数参数或 `OLLAMA_ACTION_ITEMS_MODEL` 环境变量切换模型。
   - Lines 103-124: 新增了对 Ollama `chat()` 的调用，包括 system/user prompt，以及要求模型按照结构化输出格式返回字符串组成的 JSON 数组。
   - Lines 126-130: 新增了对不同版本 Ollama Python 返回格式的兼容处理。
   - Lines 132-137: 新增了 JSON 解析和异常处理，用来处理模型返回内容不是合法 JSON 的情况。
   - Lines 139-153: 新增了对模型返回结果的清理、过滤和去重逻辑，最后返回整理后的行动项列表
```

### Exercise 2: Add Unit Tests
Prompt: 
```
- 1. 在week2/tests/test_extract.py文件中写一段测试代码，要求可以直接运行用来测试extract_action_items_llm()函数是否能够成功运行，注意只能添加代码，非必要不删除或修改原有的代码。
- 2. 测试代码中给的sample_text可以稍微长一点，不要直接根据sample_text限定模型的输出，主要是使用extract_action_items_llm()函数进行关键内容的提取
- 3. 在week2/tests/test_extract.py文件中继续加入测试，测试的内容要包含以下场景：

   1. bullet lists：像 - [ ] write tests、* fix API
   2. keyword-prefixed lines：像 TODO: update README、Action: call Bob 
   3. empty input：空字符串 "" 或只有空格的输入

   要求：
   1. 在运行测试文件夹的时候需要将这些测试项目全部包含
   2. 非必要不要修改原有的代码
   3. 完成后列出修改文件、主要改动、关键行号和测试方法
   4. 在week2的README.md文件中按照添加的代码，修改运行测试部分相应的描述
``` 

Generated Code Snippets:
```
Modified files:
1. `week2/tests/test_extract.py`
   - Lines 1-6: 新增了直接运行测试文件时的包路径处理逻辑，使 `python week2/tests/test_extract.py` 也能正确使用相对导入。
   - Lines 29-36: 新增了 `test_extract_bullet_list_variants()`，覆盖 `- [ ] write tests` 和 `* fix API` 两种 bullet list 输入，并断言提取结果为 `["write tests", "fix API"]`。
   - Lines 39-47: 新增了 `test_extract_keyword_prefixed_lines()`，覆盖 `TODO: update README` 和 `Action: call Bob` 两种 keyword-prefixed lines，同时确认普通背景句不会被提取。
   - Lines 50-52: 新增了 `test_extract_empty_or_whitespace_input()`，使用 `pytest.mark.parametrize` 覆盖空字符串、只有空格以及只有换行/制表符的输入，断言结果为空列表。
   - Lines 55-71: 新增了 `_sample_text_for_llm()` 测试样本文本。文本内容较长，混合了会议背景、自然语言行动项、`Action:` 和 `TODO:` 前缀任务，用来测试 LLM 是否能从真实一点的文本中提取关键行动项。
   - Lines 74-82: 新增了 `test_extract_action_items_llm_runs_and_returns_action_items()` 测试函数，调用 `extract_action_items_llm()` 并检查返回结果是非空字符串列表，同时检查结果没有重复项；测试没有把模型输出限定为固定句子。
   - Lines 85-95: 新增了 `__main__` 入口，允许直接运行该测试文件并打印 `extract_action_items_llm()` 的提取结果，同时用断言确认函数成功返回可用的行动项列表。
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
请先阅读 week2/app 的后端代码，然后完成 TODO 3 的小范围重构：整理 API schemas、数据库层、配置项和错误处理。

要求：
- 不要改变现有功能、API 路径或返回含义。
- 不要大改项目结构。
- 不要删除原有函数或功能。
- 尽量保持修改范围小而清晰。
- 修改后确保现有测试可以通过。

完成后请列出：
1. 修改了哪些文件；
2. 每个文件的主要改动；
3. 关键代码的大致行号；
4. 我应该运行哪些命令来测试。
``` 

Generated/Modified Code Snippets:
```
Modified files:
1. `week2/app/config.py`
   - Lines 12-19: 新增 `Settings` 配置类，集中保存应用标题、项目基础路径和 `OLLAMA_ACTION_ITEMS_MODEL` 默认模型配置。
   - Lines 21-35: 新增 `data_dir`、`db_path`、`frontend_dir`、`index_html_path` 属性，把数据库路径和前端静态文件路径统一放到配置层管理。
   - Line 38: 新增全局 `settings` 实例，供数据库层、主应用和服务层复用。

2. `week2/app/schemas.py`
   - Lines 8-17: 新增 note 创建请求和 note 响应 schema，明确 `/notes` 接口的输入输出结构。
   - Lines 20-34: 新增 action item extract 请求和响应 schema，保持原有返回字段 `note_id` 和 `items` 不变。
   - Lines 37-53: 新增 action item 列表响应和 done 更新请求/响应 schema，明确 `done` 返回为布尔值。

3. `week2/app/errors.py`
   - Lines 6-11: 新增通用 `bad_request()` 和 `not_found()` helper，集中创建 `HTTPException`。
   - Lines 14-23: 新增 `content_required()`、`text_required()`、`note_not_found()`，保留原有 status code 和 detail 文案。

4. `week2/app/db.py`
   - Lines 5-17: 改为从 `settings` 读取数据库路径，并新增 `DatabaseRow` 类型别名。
   - Lines 57-101: 保留原有数据库查询和写入函数，只整理类型标注，使数据库层边界更清晰。
   - Lines 114-129: 新增 `note_to_dict()` 和 `action_item_to_dict()`，把 sqlite row 到 API 字典的转换集中在数据库层附近。

5. `week2/app/main.py`
   - Lines 14-20: 新增 FastAPI lifespan，在应用启动时调用 `init_db()`，替代模块导入时直接初始化数据库。
   - Lines 23-32: 首页 HTML 和静态文件目录改为使用 `settings` 中的路径配置，API 路由和功能保持不变。

6. `week2/app/routers/notes.py`
   - Lines 12-19: `create_note()` 改用 `NoteCreateRequest` 和 `NoteResponse`，并使用 `content_required()` 处理空内容错误。
   - Lines 22-27: `get_single_note()` 改用 `NoteResponse` 和 `note_not_found()`，返回内容仍然是 `id`、`content`、`created_at`。

7. `week2/app/routers/action_items.py`
   - Lines 19-31: `/action-items/extract` 改用 request/response schema 和 `text_required()`，返回结构仍然是 `note_id` 与 `items`。
   - Lines 34-37: `/action-items` 列表接口使用 `ActionItemResponse`，并复用 `db.action_item_to_dict()` 做行转换。
   - Lines 40-44: `/action-items/{action_item_id}/done` 改用 done 请求/响应 schema，返回字段仍然是 `id` 和 `done`。

8. `week2/app/services/extract.py`
   - Lines 9 and 95: LLM 默认模型改为从 `settings.ollama_action_items_model` 读取，避免服务层直接读取环境变量。
   - Lines 32-64 and 90-151: 保持原有提取逻辑不变，只整理类型标注为 Python 3.10+ 的 `list[str]` 写法。
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
请完成 week2/assignment.md 的 TODO 4。

要求：
1. 新增一个后端 endpoint，调用 extract_action_items_llm()，例如 POST /action-items/extract-llm。
2. 在前端新增 “Extract LLM” 按钮，点击后调用该 endpoint 并显示结果。
3. 新增一个获取所有 notes 的后端 endpoint，例如 GET /notes。
4. 在前端新增 “List Notes” 按钮，点击后获取并显示所有 notes。
5. 保持现有功能不变，不要删除原有接口或按钮，不要大改项目结构。
6. 完成后列出修改文件、主要改动、关键行号和测试方法。
``` 

Generated Code Snippets:
```
1. `week2/app/routers/action_items.py`
   - Line 14: 新增导入 `extract_action_items_llm()`，用于后端 LLM 提取接口调用。
   - Lines 19-21: 保留原有 `POST /action-items/extract` 接口，并改为复用 `_extract_with_strategy(..., use_llm=False)`，原有 Extract 功能不变。
   - Lines 24-26: 新增 `POST /action-items/extract-llm` 接口，前端点击 “Extract LLM” 后会调用该接口。
   - Lines 29-43: 新增 `_extract_with_strategy()` helper，把普通提取和 LLM 提取共用的参数校验、保存 note、插入 action items、返回结果逻辑集中到一起；Line 42 根据 `use_llm` 决定调用 `extract_action_items_llm()` 或原来的 `extract_action_items()`。
2. `week2/app/routers/notes.py`
   - Lines 22-24: 新增 `GET /notes` 接口 `list_all_notes()`，调用已有的 `db.list_notes()` 获取全部 notes，并用 `db.note_to_dict()` 转成 API 返回格式。
3. `week2/frontend/index.html`
   - Lines 14-17: 新增 note 列表显示相关样式，并让按钮行支持换行，避免新增按钮后布局挤在一起。
   - Lines 29-30: 新增 “Extract LLM” 和 “List Notes” 两个按钮，原有 “Extract” 按钮保留。
   - Lines 39-40: 新增前端按钮元素引用 `extractLlmBtn` 和 `listNotesBtn`。
   - Lines 42-48: 新增 `escapeHtml()`，显示 action items 和 notes 时转义用户文本，避免 HTML 内容被直接插入页面。
   - Lines 50-60: 抽出 `attachDoneHandlers()`，继续支持勾选 action item 后调用原有 `/action-items/{id}/done` 接口。
   - Lines 62-71: 抽出 `renderActionItems()`，普通 Extract 和 LLM Extract 共用同一套结果渲染逻辑。
   - Lines 73-88: 新增通用 `extractActionItems()` 请求函数，根据传入 endpoint 调用普通提取或 LLM 提取接口。
   - Lines 92-98: 原有 “Extract” 按钮继续调用 `/action-items/extract`；新增 “Extract LLM” 按钮调用 `/action-items/extract-llm`。
   - Lines 100-116: 新增 “List Notes” 点击逻辑，调用 `GET /notes` 并把所有 notes 显示在页面上。
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
请完成 week2/assignment.md 的 TODO 5：阅读当前 week2 代码库，并生成一个结构清晰的 README.md。

README 至少包括：
1. 项目简介；
2. 如何安装依赖并运行项目；
3. API endpoints 和主要功能说明；
4. 如何运行测试。

请根据当前实际代码生成，不要编造不存在的接口或命令，可以加入更多内容使得README.md文档更加清晰，但是不要为了加内容而加内容导致出现大段无用的表述，仅生成README.md文件即可，不要动别的文件
``` 

Generated Code Snippets:
```
Modified files:
1. `week2/README.md`
   - Lines 1-11: 新增项目标题和项目简介，说明这是一个 FastAPI + SQLite 的 Action Item Extractor，并概括前端、启发式提取、LLM 提取、笔记存储和行动项状态跟踪等主要功能。
   - Lines 13-32: 新增项目结构说明，列出 `app/`、`routers/`、`services/`、`frontend/` 和 `tests/` 等主要目录及其作用，方便读者快速理解代码组织。
   - Lines 34-58: 新增依赖安装和项目运行说明，包括 `poetry install`、`poetry run uvicorn week2.app.main:app --reload`、访问地址，以及 Ollama LLM endpoint 所需的模型配置说明。
   - Lines 60-92: 新增 API endpoints 表格，按照前端、笔记、行动项三类列出实际存在的路由、请求体或查询参数，以及每个 endpoint 的功能。
   - Lines 77-118: 新增 `curl.exe` 请求示例和典型 JSON 响应示例，用来展示如何调用 note 创建接口和启发式 action items 提取接口。
   - Lines 120-129: 新增提取行为说明，解释启发式提取器识别的 bullet、keyword prefix、checkbox marker 和 fallback imperative starter，以及 LLM 提取器的返回处理方式。
   - Lines 131-139: 新增测试运行说明，写明使用 `poetry run pytest week2/tests`，并说明当前 LLM 测试需要 Ollama 正在运行且配置模型可用。
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 
