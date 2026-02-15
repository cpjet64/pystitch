# Pystitch Repository Guardrails

These rules are mandatory for all contributions in this repository.
If two rules conflict, protect data integrity and project mandates first.

`DEVELOPERS.md` is the canonical developer workflow guide.
This file intentionally contains guardrails only; detailed setup, commands, CI reproduction, docs, and release workflows live in `DEVELOPERS.md`.

## Core Project Mandates (Non-Negotiable)
- Keep mandated embroidery read/write support intact: `PES`, `DST`, `EXP`, `JEF`, `VP3`.
- Keep mandated command support intact: `STITCH`, `JUMP`, `TRIM`, `STOP`, `END`, `COLOR_CHANGE`, `NEEDLE_SET`, `SEQUIN_MODE`, `SEQUIN_EJECT`.
- Follow the project philosophy from `README.md`: minimize information loss wherever practical.
- Do not introduce behavior that silently discards stitch, thread, or metadata information unless explicitly documented and tested.

## Repository Structure and Boundaries
- Source layout is fixed:
  - `src/pystitch/`: library code and format adapters.
  - `test/`: standard `unittest` suite and regression coverage.
  - `.github/workflows/test.yml`: CI matrix, packaging verification, experimental interpreter checks, and dependency audit.
  - `.github/workflows/dependency-review.yml`: dependency risk checks on PR dependency/workflow changes.
  - `.github/dependabot.yml`: scheduled dependency and GitHub Actions update automation.
- Preserve module naming conventions:
  - Readers/Writers use `PascalCase` filenames (`DstReader.py`, `PesWriter.py`).
  - Tests use `test_*.py` snake_case filenames.
- Keep public API stability in mind. Public entry points are exported via `src/pystitch/__init__.py`.

## Python Version Policy
- Package compatibility remains `requires-python = ">=3.9"` unless intentionally changed with full review.
- Supported/gated CI versions are `3.9` through `3.13`.
- Supported local environment names and upgrade policy are defined in `DEVELOPERS.md`.
- Before finalizing non-trivial changes, run validation as defined in `DEVELOPERS.md` (`Validation Matrix`).

## Required Development Commands
- Required setup, test, build, docs, and debug commands are defined in `DEVELOPERS.md`:
  - `Fast Start (15 min)`
  - `Daily Workflow Commands`
  - `Validation Matrix`
  - `Sphinx Docs Workflow`
  - `Debug Harness Guide`
- Install and use repo-local hooks from `.githooks`:
  - `pre-commit`: fast staged-file checks for iteration speed.
  - `pre-push`: strict quality gate before sharing changes.

## Format and Encoder Change Rules
- Any change to readers/writers/encoder behavior must include tests for the affected formats.
- Preserve roundtrip behavior and command counts unless a deliberate breaking change is approved.
- Do not mutate input patterns during write/encode paths unless the API explicitly documents mutation.
- Keep command masking and encoded command semantics consistent with `EmbConstant.py` and `EmbFunctions.py`.

## Documentation and Metadata Consistency
- Keep README format lists in sync with actual supported formats.
- Run metadata consistency validation when touching format support or README lists (command is documented in `DEVELOPERS.md`).
- Keep `pyproject.toml`, README compatibility statements, and CI matrix aligned when changing Python support claims.
- If developer workflow guidance appears in other docs, replace it with a concise reference to `DEVELOPERS.md`.

## CI and Test Guardrails
- CI supported matrix validates Linux/Windows/macOS with Python `3.9` through `3.13`; do not narrow coverage without explicit approval.
- CI packaging verification is required (`build` + `twine check`); do not remove it without explicit approval.
- Dependency audit (`audit-3.13`) is blocking and waiver-aware; approved temporary exceptions must be listed in `.ci/audit-waivers.json` with owner/reason/expiry.
- Dependency review is blocking for dependency/workflow-modifying pull requests.
- Keep nox session contracts aligned with CI:
  - `ci-*` for supported versions
  - `quick-3.13`
  - `package-3.13`
  - `audit-3.13`
- Every behavior change should have a test, especially for:
  - format conversion
  - command preservation
  - metadata/thread retention
  - matrix/transform and trim behavior

## Coding and Change Hygiene
- Follow existing Python style (4 spaces, clear names, focused helpers).
- Avoid unrelated refactors in behavior-changing PRs.
- Keep commits scoped and imperative (for example: `docs: ...`, `ci: ...`, `vp3: ...`).
- PR descriptions should include:
  - what changed
  - why
  - affected formats/modules
  - compatibility impact
