# Add Feature Workflow

You are helping me add a new feature to this FastAPI + static frontend starter application.

Feature request:
$ARGUMENTS

## Goal

Implement the requested feature safely and systematically.

## Workflow

1. Understand the feature request.
   - Restate the requested feature briefly.
   - Identify whether it affects the backend, frontend, database, tests, or documentation.

2. Inspect the existing project structure.
   - Check relevant files under `backend/`, `frontend/`, `data/`, and `docs/`.
   - Do not make changes before understanding the current implementation.

3. Create or update tests first when possible.
   - For backend API changes, update or add tests under `backend/tests/`.
   - The test should describe the expected behavior of the new feature.

4. Implement the feature.
   - Update backend routes, schemas, models, or services if needed.
   - Update frontend files if the feature should appear in the UI.
   - Update seed data or database-related files only if required.

5. Verify the change.
   - Run:
     ```bash
     make test
     ```
   - If tests fail, analyze the failure and fix the issue.
   - Then run:
     ```bash
     make lint
     ```

6. Summarize the result.
   - List modified files.
   - Explain what feature was added.
   - Mention tests run and whether they passed.
   - Mention any remaining TODOs or limitations.

## Safety rules

- Do not delete existing files unless clearly necessary.
- Prefer small, focused changes.
- Before finishing, show a summary of the diff.
- If the feature request is ambiguous, ask for clarification before editing many files.