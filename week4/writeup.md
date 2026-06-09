# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
### Automation #1
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> 灵感来自 Claude Code best practices 中“先探索代码、再计划、再实现”的流程。这个自动化把新增功能拆成理解需求、检查项目结构、补测试、实现、运行测试和总结结果几个固定步骤，减少每次手动重复提示。

b. Design of each automation, including goals, inputs/outputs, steps
> 这是一个用于添加新功能的 slash command，文件位于 `.claude/commands/add-feature.md`。
>
> 目标：让 Claude Code 按固定流程完成新功能开发。
>
> 输入：用户通过 `$ARGUMENTS` 提供的功能需求。
>
> 输出：功能实现、修改文件列表、测试结果和剩余问题。
>
> 步骤：先理解需求，再检查代码结构，必要时补充测试，然后修改后端或前端代码，最后运行 `make test` 和 `make lint` 并总结结果。

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> 运行方式：在 claude code 的对话框中输入类似以下的语句
>
> ```text
> /add-feature Implement the missing frontend search UI for the existing /notes/search/ endpoint.
> ```
>
> 预期输出：Claude Code 会分析相关代码，完成对应功能，运行测试和 lint，并总结修改内容。
>
> 安全说明：该流程要求 Claude Code 不随意删除文件，只做小范围修改。若修改不合适，可以用 `git diff -- .` 查看变化，用 `git restore <file>` 回滚指定文件。

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> 自动化前，需要我手动查找相关文件、提醒 Claude 先看代码、再改功能、再运行测试。
>
> 自动化后，只需要输入 `/add-feature` 加功能描述，Claude Code 就会按固定流程完成开发和检查，减少重复指令。

e. How you used the automation to enhance the starter application
> 我使用 `/add-feature` 来扩展 starter application 的功能。通过这个自动化，我添加并改进了 notes 搜索、删除、编辑、空结果提示、输入校验，以及 action items 的取消完成和删除功能。
>
> 这个自动化帮助我在添加功能前先检查现有代码结构，再根据需要修改前端和后端代码，并在最后总结修改内容。相比直接让 Claude Code 随意改代码，这个流程更稳定，也更容易控制修改范围。


### Automation #2
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> 灵感来自 best practices 中“给 Claude 一个可验证目标”的建议。这个自动化把验证过程固定为检查 `git status`/`git diff`、运行 `make test` 和 `make lint`，最后给出是否可以保留修改的明确结论。

b. Design of each automation, including goals, inputs/outputs, steps
> 这是一个用于验证当前修改的 slash command，文件位于 `.claude/commands/verify-change.md`。
>
> 目标：检查当前代码修改是否安全、聚焦，并且是否可以保留。
>
> 输入：用户通过 `$ARGUMENTS` 提供的验证说明。
>
> 输出：修改文件列表、测试结果、lint 结果、风险说明和最终建议。
>
> 步骤：运行 `git status` 和 `git diff` 查看修改，再运行 `make test` 和 `make lint`，最后给出是否可以保留的结论。

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> 运行方式：在 claude code 的对话框中输入类似以下的语句
>
> ```text
> /verify-change Check whether the current changes are safe to keep.
> ```
>
> 预期输出：Claude Code 会列出当前修改，运行测试和 lint，并给出 “Ready to keep” 或需要修复的建议。
>
> 安全说明：该流程不会自动 commit、push、reset 或删除文件。若需要回滚，只建议使用 `git restore <file>`，不会自动执行。

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> 自动化前，需要我手动查看 diff、运行测试、运行 lint，并自己判断修改是否安全。
>
> 自动化后，`/verify-change` 可以一次性完成这些检查，并给出清晰的验证结论。

e. How you used the automation to enhance the starter application
> 我使用 `/verify-change` 来检查每次功能修改是否安全。每完成一个功能后，我都会运行这个自动化来查看当前 diff，并运行 `make test` 和 `make lint`。
>
> 它帮助我发现并修复了 Windows/Bash 环境下 `make test` 无法正确找到 `backend` 模块的问题。修复 Makefile 后，测试和 lint 都可以正常通过。之后我也用它验证 notes 和 action items 的功能修改是否可以保留。


### *(Optional) Automation #3*
*If you choose to build additional automations, feel free to detail them here!*

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> 灵感来自 best practices 中“提供足够上下文、不要凭空假设”的建议。这个自动化要求先读取 backend、frontend 和 docs，再根据真实 API 行为更新文档，避免文档和代码不一致。

b. Design of each automation, including goals, inputs/outputs, steps
> 这是一个用于同步文档的 slash command，文件位于 `.claude/commands/docs-sync.md`。
>
> 目标：让项目文档，尤其是 API 文档，与当前代码保持一致。
>
> 输入：用户通过 `$ARGUMENTS` 提供的文档同步需求。
>
> 输出：更新后的文档、修改摘要和剩余文档缺口。
>
> 步骤：检查后端 routes、schemas 和现有文档，必要时参考 `/openapi.json`，然后更新 `docs/API.md`，并总结文档变化。

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> 运行方式：在 claude code 的对话框中输入类似以下的语句
>
> ```text
> /docs-sync Create or update docs/API.md based on the current backend API routes. Do not edit docs/TASKS.md or writeup.md.
> ```
>
> 预期输出：Claude Code 会检查当前 API 实现，更新 `docs/API.md`，并说明修改了哪些文档内容。
>
> 安全说明：该流程不会编造不存在的 API，也不会在未要求时修改 `docs/TASKS.md` 或 `writeup.md`。如需回滚，可使用 `git restore docs/API.md`。

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> 自动化前，需要我手动查看后端接口，再对照文档逐项更新。
>
> 自动化后，`/docs-sync` 会按固定流程检查代码和文档，使 API 文档维护更方便。

e. How you used the automation to enhance the starter application
> 我使用 `/docs-sync` 来维护 API 文档。在完成 notes、action items 和 extraction 相关功能后，我让它检查当前后端 routes 和 schemas，并创建或更新 `docs/API.md`。
>
> 这个自动化帮助我把当前 API 的请求方法、路径、请求体、响应格式和常见错误写入文档，避免代码已经变化但文档没有同步的问题。
