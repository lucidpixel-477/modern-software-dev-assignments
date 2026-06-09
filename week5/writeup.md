# Week 5 Write-up
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
### Automation A: Warp Drive saved prompts, rules, MCP servers

a. Design of each automation, including goals, inputs/outputs, steps
> Automation A: Week5 Task Implementation Assistant
>
> 这是一个 Warp Drive saved prompt，用来辅助完成 `week5/docs/TASKS.md` 中的任务。
>
> 目标：
> 让 Warp Agent 按固定流程完成任务，包括阅读要求、检查代码、制定计划、修改代码、添加测试、运行测试并总结结果。
>
> 输入：
> 选定的任务编号和任务描述
> `week5/` 目录下的项目代码
> 相关的后端、前端和测试文件
>
> 输出：
> 完成的代码修改
> 新增或更新的测试
> `make test` 的运行结果
> 修改文件和完成情况总结
>
> 步骤：
> 1. 阅读选定任务。
> 2. 检查相关代码文件。
> 3. 修改前先给出计划。
> 4. 在 `week5/` 内完成代码修改。
> 5. 添加或更新测试。
> 6. 运行 `make test`。
> 7. 总结修改内容和测试结果。

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> 使用自动化前，我需要手动阅读任务、查找文件、规划修改、添加测试并运行测试，步骤比较分散，容易遗漏。
>
> 使用自动化后，Warp Agent 会按照 saved prompt 的固定流程完成这些步骤，使任务实现过程更加清晰，也减少了遗漏测试或修改无关文件的风险。

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> 我使用的是 Partial autonomy。Agent 可以读取文件、制定计划和运行低风险命令，但在修改代码或执行敏感命令前需要确认。
>
> 这样既能提高效率，又能避免 Agent 自动进行不合适的修改。我通过检查修改计划、查看改动文件和运行 `make test` 来监督结果。

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> 这个自动化本身是一个 saved prompt，不是 multi-agent workflow。它可以被不同 Warp tab 中的 agent 复用，让多个 agent 使用相同的任务流程。

e. How you used the automation (what pain point it resolves or accelerates)
> 我使用这个自动化来辅助完成 Week 5 中选定的任务2、4。它解决的主要问题是减少重复说明，让 Agent 每次都能按照统一流程完成任务，包括读任务、改代码、加测试和总结结果。



### Automation B: Multi‑agent workflows in Warp 

a. Design of each automation, including goals, inputs/outputs, steps
> Automation B: Multi-Agent Coordination Playbook
>
> 这是一个用于 Warp multi-agent workflow 的协作 playbook，具体内容保存在 `week5/multi-agent-coordination-playbook.md`。
>
> 目标：
> 让多个 Warp Agent 在不同 tab 中并行完成相互独立的任务，同时通过角色分工、文件范围和共享文件规则减少冲突。
>
> 输入：
> `week5/docs/TASKS.md` 中选定的任务
> 每个 agent 的角色和负责范围
> `week5/` 目录下的后端、前端和测试文件
>
> 输出：
> 各 agent 完成的代码修改
> 新增或更新的测试
> 每个 agent 的任务完成总结
> 最终的集成测试结果
>
> 步骤：
> 1. 为每个 agent 分配清晰角色和任务。
> 2. 每个 agent 在修改前说明正在做的任务和计划修改的文件。
> 3. 如果涉及共享文件，先说明修改原因、修改区域和潜在影响。
> 4. 两个 agent 分别并行实现 Task 8 和 Task 9。
> 5. 完成后汇总各自修改内容和测试结果。
> 6. 由集成检查确认 `make test` 是否通过。

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> 使用自动化前，我需要按顺序完成 Task 8 和 Task 9：先改列表分页，再加索引和性能测试。这样虽然安全，但速度较慢，而且需要自己持续记住每个任务会影响哪些文件。
>
> 使用自动化后，我可以让两个 Warp Agent 在不同 tab 中并行工作。一个 agent 负责 Task 8 的列表分页，另一个 agent 负责 Task 9 的索引和 query performance 测试。playbook 明确了每个 agent 的负责范围和共享文件规则，因此并行开发时更容易发现潜在冲突，也减少了互相覆盖修改的风险。

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> 我使用的是 Partial autonomy。Agent 可以读取文件、检查相关代码和运行低风险命令，但在修改代码、修改共享文件或运行可能影响文件状态的命令前需要说明计划并等待确认。
>
> 我这样设置是因为 Task 8 和 Task 9 都会接触后端路由、模型和测试文件，其中部分文件可能被多个任务同时使用。我通过检查每个 agent 的文件修改计划、确认共享文件是否冲突、查看最终 diff，并运行 `make test` 来监督结果。

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> 我使用两个 agent 并行完成任务：
>
> Agent 1 负责 Task 8: List endpoint pagination for all collections。它主要处理 `GET /notes` 和 `GET /action-items` 的分页参数、分页返回结构，以及对应的前端分页控件和后端测试。
>
> Agent 2 负责 Task 9: Query performance and indexes。它主要处理 SQLite 索引，例如 notes title/id 排序索引和 action items completed filter 索引，并添加 larger dataset 和 query plan 相关测试。
>
> 协调策略是让两个 agent 先声明任务和计划修改文件。如果两个 agent 都需要修改共享文件，例如 `backend/app/models.py`、`backend/app/schemas.py`、`frontend/app.js` 或测试文件，就先停下来确认修改范围。并行的主要收益是 Task 8 和 Task 9 可以同时推进；主要风险是两个 agent 可能同时修改 schema、测试或前端状态管理，所以需要人工检查 diff 和测试结果。

e. How you used the automation (what pain point it resolves or accelerates)
> 我使用这个 multi-agent playbook 来并行推进 Task 8 和 Task 9。它解决的主要问题是多任务开发时的协调成本：每个 agent 都知道自己的角色、可修改文件和完成标准，不需要每次重新说明规则。
>
> 这个自动化加快了实现列表分页和性能索引的过程，同时让最终结果更容易检查，因为每个 agent 都需要总结自己完成了什么、运行了哪些测试，以及是否还有风险。
>
> 当然由于两个任务在进行过程中会修改同一个或者同几个文件，所以在实际执行的时候agnet窗口会大量地询问我是否继续它的操作，这就需要人时刻关注当前的运行情况，所以在实际进行并行运行的时候最好是对不同的项目进行修改，否则执行效率可能并不会提高太多，除非提示词写的特别好。

### (Optional) Automation C: Any Additional Automations
a. Design of each automation, including goals, inputs/outputs, steps
> TODO

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> TODO

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> TODO

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> TODO

e. How you used the automation (what pain point it resolves or accelerates)
> TODO

