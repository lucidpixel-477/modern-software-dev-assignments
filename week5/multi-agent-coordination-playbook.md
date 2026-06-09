# Multi-Agent Coordination Playbook

You are participating in a multi-agent workflow for the Week 5 assignment.

Project scope:
- Work only inside the `week5/` directory.
- Do not modify files outside `week5/`.
- Do not make unrelated refactors.
- Keep changes minimal and focused on your assigned task.

Coordination rules:
1. Each agent must have a clearly assigned role.
2. Each agent must state which task it is working on before editing.
3. Each agent must list the files it plans to modify before making changes.
4. Each agent must avoid modifying files assigned to another agent unless explicitly approved.
5. If two agents need to modify the same file, stop and explain the conflict before editing.
6. Prefer separate backend, frontend, and test changes when possible.
7. Do not overwrite another agent's work.
8. After finishing, summarize what was changed, which tests were run, and whether the task is complete.

Agent roles:

Agent A: Notes Agent
- Responsible for Task 2: Notes search with pagination and sorting.
- May work on:
  - `backend/app/routers/notes.py`
  - `backend/app/main.py` if notes routes are defined there
  - `backend/app/schemas.py`
  - `backend/tests/test_notes.py`
  - `frontend/app.js` only for Notes UI changes
  - `frontend/styles.css` only for Notes UI styling
- Must not modify Action Items behavior unless approved.

Agent B: Action Items Agent
- Responsible for Task 4: Action items filters and bulk complete.
- May work on:
  - `backend/app/routers/action_items.py`
  - `backend/app/main.py` if action item routes are defined there
  - `backend/app/schemas.py`
  - `backend/tests/test_action_items.py`
  - `frontend/app.js` only for Action Items UI changes
  - `frontend/styles.css` only for Action Items UI styling
- Must not modify Notes behavior unless approved.

Agent C: Integration/Test Agent
- Responsible for checking final integration.
- May run:
  - `make test`
  - `make lint`
  - manual browser testing instructions
- May inspect code and suggest fixes.
- Should not modify code unless explicitly asked.

Shared-file rule:
- `frontend/app.js`, `frontend/styles.css`, and `backend/app/schemas.py` are shared files.
- If an agent needs to edit a shared file, it must first state:
  1. Why the file needs to change.
  2. Which section will be changed.
  3. Whether this could affect another agent's task.
- If there is a possible conflict, stop and ask for human approval.

Completion standard:
Each agent must finish with:
1. Task completed or not completed.
2. Files changed.
3. Tests run.
4. Test results.
5. Manual testing steps.
6. Remaining risks or issues.

Use Partial autonomy:
- You may read files and run low-risk commands.
- Ask before making code changes.
- Ask before running commands that may modify files.
