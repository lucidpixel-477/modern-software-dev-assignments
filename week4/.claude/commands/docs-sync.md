# Docs Sync Workflow

You are helping me keep the project documentation in sync with the current application behavior.

Documentation sync request:
$ARGUMENTS

## Goal

Review the current application routes, schemas, user-facing behavior, and recent code changes. Then update the relevant documentation so it accurately reflects the current state of the starter application.

## Workflow

1. Understand the documentation request.
   - Restate what documentation needs to be checked or updated.
   - Identify whether the request is about API routes, frontend behavior, developer workflow, task progress, or writeup content.

2. Inspect current code and documentation.
   - Check relevant backend files under:
     ```text
     backend/
     ```
   - Check relevant frontend files under:
     ```text
     frontend/
     ```
   - Check existing documentation under:
     ```text
     docs/
     ```
   - Check the current repository changes:
     ```bash
     git status
     git diff
     ```

3. Check API behavior if needed.
   - If the backend API changed, inspect the FastAPI routes and schemas.
   - If the app is running, compare the current API behavior with:
     ```text
     http://localhost:8000/docs
     ```
     or:
     ```text
     http://localhost:8000/openapi.json
     ```
   - If the app is not running, do not assume undocumented routes exist. Use the source code as the main reference.

4. Update documentation.
   - Update `docs/API.md` if API endpoints, request bodies, response bodies, or error behavior changed.
   - Do not edit `docs/TASKS.md` unless I explicitly ask.
   - Update other files under `docs/` only if I explicitly ask or if they are directly required for the current task.
   - Do not edit `writeup.md` unless I explicitly ask.

5. Preserve useful existing content.
   - Do not delete documentation sections unless they are clearly outdated or incorrect.
   - Prefer small, focused edits.
   - Keep the documentation concise and easy to scan.

6. Verify documentation consistency.
   - Compare the updated docs with the relevant code.
   - Make sure endpoint names, paths, HTTP methods, request fields, and response fields are accurate.
   - If examples are included, make sure they match the current implementation.

7. Run checks if documentation changes are related to code changes.
   - If code was changed together with documentation, run:
     ```bash
     make test
     ```
   - If linting is relevant, run:
     ```bash
     make lint
     ```
   - If only Markdown documentation was changed, tests may be skipped, but explain why.

8. Final report.
   - List documentation files changed.
   - Summarize what was updated.
   - Mention any API or behavior changes reflected in the docs.
   - Mention whether tests or lint were run.
   - List any remaining documentation gaps or TODOs.

## Safety rules

- Do not invent API behavior that is not supported by the code.
- Do not edit `writeup.md` unless I explicitly ask.
- Do not make large code changes during documentation sync.
- Do not delete files.
- Do not commit or push changes unless I explicitly ask.
- If documentation and code disagree, report the mismatch clearly before making assumptions.

## Expected output

At the end, provide a report like this:

```text
Documentation files changed:
- docs/API.md
- docs/TASKS.md

Summary:
- Added documentation for the notes search endpoint.
- Marked the notes search task as completed in TASKS.md.

Checks:
- Compared docs against backend routes.
- make test passed.

Remaining TODOs:
- No remaining documentation gaps found.
```