# Verify Change Workflow

You are helping me verify whether the current code changes are safe, correct, and ready to submit.

Verification request:
$ARGUMENTS

## Goal

Review the current repository changes, run the appropriate checks, and provide a clear summary of whether the changes are ready to keep or need more work.

## Workflow

1. Inspect the current changes.
   - Run:
     ```bash
     git status
     ```
   - Run:
     ```bash
     git diff
     ```
   - Identify which files were changed.
   - Summarize the likely purpose of the changes.

2. Check whether the changes are focused.
   - Determine whether the modified files match the requested task.
   - Point out any unrelated or suspicious changes.
   - Do not revert anything automatically unless I explicitly ask.

3. Run the test suite.
   - Run:
     ```bash
     make test
     ```
   - If tests fail:
     - Summarize the failing tests.
     - Explain the likely cause.
     - Suggest the smallest fix.
     - Ask before making large changes.

4. Run linting.
   - Run:
     ```bash
     make lint
     ```
   - If linting fails:
     - Summarize the lint errors.
     - Fix simple formatting or import issues if safe.
     - Do not make large refactors during verification.

5. Optional formatting check.
   - If formatting issues are reported, run:
     ```bash
     make format
     ```
   - After formatting, run:
     ```bash
     make test
     make lint
     ```

6. Review documentation impact.
   - If API routes, schemas, or user-facing behavior changed, check whether docs should be updated.
   - Mention whether `docs/API.md`, `docs/TASKS.md`, or `writeup.md` may need updates.
   - Do not edit `writeup.md` unless I explicitly ask.

7. Final report.
   - List modified files.
   - Summarize what changed.
   - Report test results.
   - Report lint results.
   - Mention any remaining TODOs, risks, or limitations.
   - Give a clear recommendation:
     - Ready to keep
     - Needs minor fixes
     - Needs major revision

## Safety rules

- Do not delete files.
- Do not reset, checkout, commit, or push changes unless I explicitly ask.
- Do not run destructive commands.
- Prefer analysis and small fixes over large rewrites.
- If rollback is needed, suggest commands instead of running them automatically.

## Rollback guidance

If the changes are not acceptable, suggest one of the following:

```bash
git restore <file>
```

to restore a specific file, or:

```bash
git restore .
```

to discard all unstaged changes.

Only provide rollback commands as suggestions. Do not execute them unless I explicitly request it.