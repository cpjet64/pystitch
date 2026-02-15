# DEVELOPERS.md

This document is the master developer guide for this repository.

## Purpose + Audience
- Audience:
  - New contributors onboarding to the repo.
  - Existing contributors maintaining formats, encoder logic, tests, docs, and release workflows.
- Purpose:
  - Provide one canonical operational guide for development work.
  - Define required workflows, quality gates, and repository contracts.
- Experience paths:
  - New-dev path: follow `Fast Start (15 min)`, `Repo Map`, `Architecture Overview`, then `Daily Workflow Commands`.
  - Experienced-dev path: jump to `Validation Matrix`, `Public API Stability Rules`, `Testing Standards`, and feature-specific sections.

## How To Use This Doc
- Recommended reading order:
  1. `Fast Start (15 min)`
  2. `Supported Python + venvs`
  3. `Repo Map`
  4. `Architecture Overview`
  5. `Daily Workflow Commands`
  6. `Validation Matrix`
  7. Remaining sections based on task type.
- Quick links:
  - Setup: [`Fast Start (15 min)`](#fast-start-15-min)
  - Architecture: [`Architecture Overview`](#architecture-overview)
  - Debugging: [`Debug Harness Guide`](#debug-harness-guide)
  - Docs: [`Sphinx Docs Workflow`](#sphinx-docs-workflow)
  - CI and release: [`CI/CD Contract`](#cicd-contract), [`Release Process`](#release-process)
  - Troubleshooting: [`Troubleshooting Playbook`](#troubleshooting-playbook)
- Use other docs when:
  - `README.md`: user-facing/project overview and API usage.
  - `AGENTS.md`: AI assistant rules/guardrails for agent tooling behavior.
  - `.AGENTS/*.md`: implementation plans and execution roadmaps.

## Source of Truth Hierarchy
- Canonical developer operations document: `DEVELOPERS.md` (this file).
- User-facing project overview: `README.md`.
- AI assistant guardrails: `AGENTS.md`.
- If added in future:
  - `CODING_STYLE.md`: detailed style conventions.
  - `CONTRIBUTING.md`: external contributor process.
  - `CODE_OF_CONDUCT.md`: community behavior standards.
- Relationship rule:
  - `DEVELOPERS.md` is the master workflow contract.
  - Other docs may summarize, but should not conflict with this file.
  - If conflicts occur, update docs together in one change.

## Fast Start (15 min)

### Windows (PowerShell, recommended)
```powershell
Set-Location f:\projects\oss\pystitch

# Install missing Python versions (if needed)
py install 3.9
py install 3.10
py install 3.11
py install 3.12
py install 3.13
# Optional experimental version
py install 3.14

# Create venvs
py -3.9 -m venv .venv39
py -3.10 -m venv .venv310
py -3.11 -m venv .venv311
py -3.12 -m venv .venv312
py -3.13 -m venv .venv313
# Optional experimental venv
py -3.14 -m venv .venv314

# Install the same dev toolchain into all supported venvs
$venvs = @('.venv39', '.venv310', '.venv311', '.venv312', '.venv313')
foreach ($v in $venvs) { .\$v\Scripts\python.exe -m pip install -e .[dev] }
# Optional experimental setup
if (Test-Path .venv314) { .\.venv314\Scripts\python.exe -m pip install -e .[dev] }

# Smoke test one environment
.\.venv313\Scripts\python.exe -m nox -s quick-3.13
```

### macOS (zsh/bash + pyenv recommended)
```bash
cd /path/to/pystitch

# Install versions (if missing)
pyenv install 3.9.21
pyenv install 3.10.16
pyenv install 3.11.11
pyenv install 3.12.9
pyenv install 3.13.2
# Optional experimental version
pyenv install 3.14.0

# Create venvs
PYENV_VERSION=3.9.21  python -m venv .venv39
PYENV_VERSION=3.10.16 python -m venv .venv310
PYENV_VERSION=3.11.11 python -m venv .venv311
PYENV_VERSION=3.12.9  python -m venv .venv312
PYENV_VERSION=3.13.2  python -m venv .venv313

# Install the same dev toolchain into all supported venvs
for v in .venv39 .venv310 .venv311 .venv312 .venv313; do "$v/bin/python" -m pip install -e .[dev]; done
# Optional experimental setup
PYENV_VERSION=3.14.0 python -m venv .venv314
if [ -d .venv314 ]; then .venv314/bin/python -m pip install -e .[dev]; fi

# Smoke test
.venv313/bin/python -m nox -s quick-3.13
```

### Linux (bash + pyenv recommended)
```bash
cd /path/to/pystitch

# Install versions (if missing)
pyenv install 3.9.21
pyenv install 3.10.16
pyenv install 3.11.11
pyenv install 3.12.9
pyenv install 3.13.2
# Optional experimental version
pyenv install 3.14.0

# Create venvs
PYENV_VERSION=3.9.21  python -m venv .venv39
PYENV_VERSION=3.10.16 python -m venv .venv310
PYENV_VERSION=3.11.11 python -m venv .venv311
PYENV_VERSION=3.12.9  python -m venv .venv312
PYENV_VERSION=3.13.2  python -m venv .venv313

# Install the same dev toolchain into all supported venvs
for v in .venv39 .venv310 .venv311 .venv312 .venv313; do "$v/bin/python" -m pip install -e .[dev]; done
# Optional experimental setup
PYENV_VERSION=3.14.0 python -m venv .venv314
if [ -d .venv314 ]; then .venv314/bin/python -m pip install -e .[dev]; fi

# Smoke test
.venv313/bin/python -m nox -s quick-3.13
```

## Supported Python + venvs
- Package support baseline: `requires-python = ">=3.9"` in `pyproject.toml`.
- Supported/gated versions:
  - Python `3.9` through `3.13` on Linux/Windows/macOS.
- Experimental/non-gated version:
  - Python `3.14` (runs in CI as non-blocking until tooling stability is fully confirmed).
- Local development venv names:
  - `.venv39`, `.venv310`, `.venv311`, `.venv312`, `.venv313`, `.venv314`.
- CI/local parity policy:
  - supported local venvs (`.venv39` through `.venv313`) must match the supported CI matrix exactly.
  - experimental versions may exist locally and in CI as non-gated jobs.
- Naming convention:
  - `.venv<major><minor>` for two-digit minor versions.
  - Example: Python 3.12 -> `.venv312`.
- Upgrade policy:
  - When adding/removing supported Python versions, update all of:
    - `pyproject.toml` classifiers and `requires-python` if needed.
    - `.github/workflows/test.yml` matrix.
    - `AGENTS.md` guardrails if version policy/compatibility statements are referenced there.
    - `DEVELOPERS.md` setup and validation sections.
    - `README.md` compatibility statement.

## Repo Map
- `.git/`: git metadata and repository history (internal VCS data).
- `.github/workflows/`: CI workflow definitions (currently `test.yml`).
- `src/pystitch/`: library source code (core model, encoder, readers, writers, helpers).
- `test/`: unittest suite and regression tests.
- `.venv39`, `.venv310`, `.venv311`, `.venv312`, `.venv313`, `.venv314`: local development virtual environments (ignored by git).
- `unittest_venv*.log`: local multi-venv test output logs (ignored by git).
- `.AGENTS/`: local planning/audit artifacts for agent workflows (ignored by git).
- `README.md`: user-facing overview and feature documentation.
- `DEVELOPERS.md`: master developer workflow guide (this file).
- `AGENTS.md`: AI assistant rules/guardrails file used by agent tooling.
- `pyproject.toml`: package metadata and build configuration.
- `LICENSE`: project license file.
- `.gitignore`: ignore rules for local/generated artifacts.

## Architecture Overview
- End-to-end flow:
  - `read -> pattern -> encode -> write`
  - `convert`: `read -> pattern -> encode -> write`
- Core objects:
  - `EmbPattern`: central in-memory representation (stitches, threadlist, extras).
  - `EmbThread`: thread metadata and color behavior.
  - `Transcoder` in `EmbEncoder.py`: normalizes command streams for writer requirements.
- Public entry points:
  - `src/pystitch/__init__.py` exports top-level APIs (`read`, `write`, `convert`, format helpers).
- Extension points:
  - New readers: add `*Reader.py`, implement `read(stream, out_pattern, settings=None)`.
  - New writers: add `*Writer.py`, implement `write(pattern, stream, settings=None)`.
  - Register formats in `supported_formats()` and add corresponding helper wrappers if needed.
  - Add tests for new/changed format behavior under `test/`.

## Daily Workflow Commands

### Install dev toolchain
```powershell
.\.venv313\Scripts\python.exe -m pip install -e .[dev]
```
- The `dev` extra includes: `ruff`, `black`, `mypy`, `coverage`, `debugpy`, `pytest`, `hypothesis`, and `nox`.
- For strict version parity, install the same dev extra in all supported-version venvs:
```powershell
$venvs = @('.venv39', '.venv310', '.venv311', '.venv312', '.venv313')
foreach ($v in $venvs) { .\$v\Scripts\python.exe -m pip install -e .[dev] }
# Optional experimental venv:
if (Test-Path .venv314) { .\.venv314\Scripts\python.exe -m pip install -e .[dev] }
```

### Show available nox sessions
```powershell
.\.venv313\Scripts\python.exe -m nox --list
```
- Nox environment backend policy:
  - prefer `uv` when available for faster virtual environment setup.
  - automatically fall back to `virtualenv` when `uv` is not installed.

### Install git hooks (recommended)
```powershell
.\.githooks\install.ps1
```
- Optional shell alternative: `bash .githooks/install.sh`.
- Hook policy:
  - `pre-commit` is intentionally fast (staged-file syntax + Ruff + Black checks).
  - `pre-push` is intentionally strict (full supported matrix + packaging + blocking audit; experimental remains non-blocking).

### Run default supported-version quality matrix
```powershell
.\.venv313\Scripts\python.exe -m nox
```

### Run full supported-version quality matrix locally
```powershell
.\.venv313\Scripts\python.exe -m nox -s ci
```

### Run specific sessions
```powershell
.\.venv313\Scripts\python.exe -m nox -s ci-3.13
.\.venv313\Scripts\python.exe -m nox -s quick-3.13
.\.venv313\Scripts\python.exe -m nox -s experimental-3.14
.\.venv313\Scripts\python.exe -m nox -s package-3.13
.\.venv313\Scripts\python.exe -m nox -s audit-3.13
```
- `ci-*` sessions run tests, lint, and static typing together for parity with supported CI jobs.

### Run one test module directly (debug fallback)
```powershell
.\.venv313\Scripts\python.exe -m pytest -q test/test_embpattern.py
```

### Build package
```powershell
.\.venv313\Scripts\python.exe -m nox -s package-3.13
```

### Docs checks (Sphinx rollout target)
```powershell
.\.venv313\Scripts\python.exe -m pip install -e .[docs]
.\.venv313\Scripts\python.exe -m sphinx -W --keep-going -b html docs docs/_build/html
.\.venv313\Scripts\python.exe -m sphinx -W --keep-going -b linkcheck docs docs/_build/linkcheck
.\.venv313\Scripts\python.exe scripts/check_docs_coverage.py
```

## Validation Matrix
- Before commit:
  - let `pre-commit` run fast staged-file checks.
  - run targeted tests for touched modules.
  - for refactors, run behavior-equivalence proof tests comparing pre-refactor and post-refactor outputs.
  - run docs build if docs/docstrings/public API changed.
- Before push:
  - let `pre-push` run strict checks:
    - required: `nox -s ci package-3.13 audit-3.13`
    - non-blocking: `nox -s experimental-3.14`
  - add temporary exceptions only in `.ci/audit-waivers.json` with `owner`, `reason`, and `expires`.
- Before PR:
  - run `python -m nox` on the primary dev environment (`.venv313`) to execute supported-version quality parity checks.
  - include proof-test evidence for refactors showing end results are unchanged.
  - for broad-impact changes, run multi-interpreter nox supported sessions (`ci-3.9` through `ci-3.13`).
  - run `experimental-3.14` when changes may impact upcoming interpreter compatibility.
  - include evidence in PR description (commands run, key outputs, risk notes).
- Before release:
  - full nox supported quality matrix across supported versions.
  - run the experimental interpreter session and review failures before broad support expansion.
  - build sdist/wheel and verify integrity.
  - run docs build and coverage checks.
  - confirm release/version/changelog consistency.

## Coding Standards
- Naming:
  - Reader/Writer module filenames use PascalCase (for example `DstReader.py`, `PesWriter.py`).
  - Tests use `test_*.py` naming.
  - Use clear, descriptive names in complex logic.
- Docstrings:
  - Module docstrings required for public modules.
  - Public classes/functions must have docstrings.
  - Complex logic should include concise explanation of intent.
- Type hints:
  - Add or maintain type hints on public APIs and non-trivial internal helpers.
- Comment policy:
  - Prefer "why" comments, not line-by-line narration.
  - Binary/bitmask logic must include explanatory comments.
  - Remove dead/commented debug code.
- Readability rules:
  - Keep functions focused and manageable in size.
  - Break monolithic logic into named helpers.
  - Avoid wildcard imports in new/modified code unless intentionally justified.

## Public API Stability Rules
- Public API is defined by top-level exports in `src/pystitch/__init__.py` and documented public helpers.
- Stability expectations:
  - Avoid breaking public signatures without explicit release notes.
  - Prefer additive changes to preserve compatibility.
- Deprecation expectations:
  - Mark deprecations clearly in docs and release notes.
  - Keep deprecated paths available for at least one minor release cycle when practical.
- Versioning expectations:
  - Update `pyproject.toml` version when releasing behavior/API changes.
  - Breaking changes require explicit versioning and migration notes.

## Debug Harness Guide
- Status:
  - Centralized debug harness is planned (see `.AGENTS/plan-debugharness.md`).
  - Current code includes many direct `print()` statements in tests; migration target is unified harness.
- Target toggles:
  - Global: `set_debug(...)`, `get_debug_config()`, `clear_debug()`.
  - Per-call: `settings["debug"]` for `read`, `write`, `convert`.
  - Env defaults: `PYSTITCH_DEBUG`, `PYSTITCH_DEBUG_FILE`, `PYSTITCH_DEBUG_CONSOLE`.
- Target modes:
  - Console only.
  - File only.
  - Both console and file.
- Migration from `print`:
  - Replace source-level debug `print()` calls with harness emit helpers.
  - Replace test prints with harness/gated helpers.
  - Remove commented-out debug print remnants.
- Troubleshooting:
  - No debug output:
    - confirm debug is enabled and config precedence is correct.
    - confirm component filter is not excluding events.
  - File output missing:
    - confirm writable path and parent directory existence.
    - confirm file mode and append settings.
  - Excessive output:
    - disable verbose mode.
    - set component filters.
    - set max-events cap.

## Testing Standards
- Required tests by change type:
  - Refactor-only changes: add a proof test that demonstrates no end-result behavior change.
  - Reader/writer/encoder changes: add regression coverage for affected formats and command behavior.
  - Public API changes: add tests for signatures, behavior, and error paths.
  - Metadata/thread handling changes: add preservation tests.
  - Matrix/transform changes: add coordinate and command sequence checks.
- Refactor proof-test requirements:
  - Compare old-path and refactored-path outputs for equivalent inputs.
  - Assert output equivalence at the behavior boundary (file bytes, stitch streams, command counts, metadata, or expected invariants).
  - Include at least one representative real-world case and one edge case.
  - Keep proof tests deterministic and automation-friendly.
- Test naming:
  - Module: `test_<feature>.py`
  - Method: `test_<expected_behavior>()`
  - Refactor proofs: prefer `test_refactor_<area>_preserves_<behavior>()`.
- Fixtures/mocking:
  - Prefer deterministic pattern helpers in `test/pattern_for_tests.py`.
  - Use lightweight mocks only when external effects are unavoidable.
- Regression expectations:
  - Every bug fix should include a regression test reproducing prior failure.
  - Avoid weakening assertions to pass unstable behavior.

## Sphinx Docs Workflow
- Status:
  - Full Sphinx workflow is planned in `.AGENTS/plan-docs.md`.
  - `docs/` and `.[docs]` extras are target-state and not fully wired yet in the current repository snapshot.
  - The commands below are future-state examples to use after the docs rollout lands.
- Expected commands:
```powershell
.\.venv313\Scripts\python.exe -m pip install -e .[docs]
.\.venv313\Scripts\python.exe -m sphinx -W --keep-going -b html docs docs/_build/html
.\.venv313\Scripts\python.exe -m sphinx -W --keep-going -b linkcheck docs docs/_build/linkcheck
.\.venv313\Scripts\python.exe scripts/check_docs_coverage.py
```
- Autosummary conventions:
  - Public API pages are generated from source and export boundaries.
  - Private/internal symbols should not pollute public docs.
- API regeneration:
  - Regenerate autosummary when public modules, exports, or docstrings change.
- How to verify everything appears:
  1. Build docs with warnings as errors.
  2. Run docs coverage check and confirm zero missing symbols.
  3. Open `docs/_build/html/index.html`.
  4. Confirm core, reader, writer, and utility sections include expected APIs.

## Docs Contribution Guide
- Docs definition-of-done for code changes:
  - Public API changes include docstring and docs updates.
  - New behavior includes usage examples where useful.
  - Removed/renamed behavior removes stale docs references.
  - Sphinx build passes with warnings as errors.
  - Coverage check passes with no missing public symbols.

## Localization Workflow
- Status:
  - Crowdin workflow is not yet wired in this repository.
- Target Crowdin flow once enabled:
  1. Source docs are authored in English in repo files.
  2. Source strings are synced to Crowdin.
  3. Translators update strings in Crowdin.
  4. Translated files are synced back by automation.
- Do not edit manually (when localization is enabled):
  - Generated translation catalogs (for example `docs/locales/**/LC_MESSAGES/*.po`).
  - Crowdin-managed sync metadata files.
  - Generated build artifacts in `docs/_build/`.

## Commit + PR Standards
- Commit message format:
  - Use conventional style when practical: `<type>: <summary>`
  - Examples: `fix: preserve thread order in vp3 writer`, `docs: add sphinx verification steps`.
- PR checklist:
  - clear description of what changed and why.
  - affected modules/formats listed.
  - compatibility impact noted.
  - validation commands listed with outcomes.
  - docs updated when behavior/API/workflow changed.
- Required evidence/artifacts:
  - test command output summary.
  - for refactors, proof-test output summary demonstrating unchanged end results.
  - docs/build output summary when relevant.
  - migration notes for breaking or user-visible changes.

## CI/CD Contract
- Current CI workflow:
  - `.github/workflows/test.yml`
  - `.github/workflows/dependency-review.yml`
  - `.github/dependabot.yml`
  - Supported matrix job: Linux/Windows/macOS x Python 3.9-3.13 via nox `ci-*`.
  - Packaging verification job: Python 3.13 via nox `package-3.13`.
  - Experimental job: Python 3.14 via nox `experimental-3.14` (non-blocking).
  - Audit job: Python 3.13 via nox `audit-3.13` (blocking, waiver-aware).
  - Dependency review workflow blocks high-severity dependency/workflow risk on pull requests.
  - Dependabot opens weekly update PRs for pip dependencies and GitHub Actions.
- CI validates:
  - editable install with `.[dev]`
  - nox quality session per supported OS/Python matrix target (tests + lint + typing)
  - package build metadata integrity (`twine check`)
- Required checks:
  - all supported matrix jobs, packaging job, and audit job must pass.
  - dependency-review must pass on PRs that modify dependency/workflow files.
  - security exceptions are only allowed through `.ci/audit-waivers.json`.
- Local reproduction:
  - run `python -m nox -s ci` from `.venv313` for full supported-version parity.
  - if you need a single-target repro, run `python -m nox -s ci-3.12` (replace version as needed).
  - run `python -m nox -s experimental-3.14` to reproduce the non-gated job.
  - run `python -m nox -s package-3.13` to reproduce packaging checks.
  - run `python -m nox -s audit-3.13` to reproduce blocking dependency audit checks.
  - install hooks once per clone with `.\.githooks\install.ps1` (or `bash .githooks/install.sh`).
  - use hooks for daily safety rails: `pre-commit` (fast) and `pre-push` (strict).
- Planned CI expansions:
  - docs workflow with warnings-as-errors.
  - debug harness validation checks.

## Release Process
- Pre-release checklist:
  1. Confirm tests pass across supported versions.
  2. Confirm docs/build checks pass.
  3. Confirm changelog/release notes are accurate.
  4. Bump version in `pyproject.toml`.
- Packaging:
```powershell
.\.venv313\Scripts\python.exe -m pip install --upgrade build twine
.\.venv313\Scripts\python.exe -m build
.\.venv313\Scripts\python.exe -m twine check dist/*
```
- Publish (when authorized):
  - publish with trusted release workflow or scoped PyPI token.
- Post-release verification:
  - verify install from package index in clean env.
  - verify core read/write smoke tests.
  - verify docs references match released behavior/version.

## Troubleshooting Playbook
- `ModuleNotFoundError: pystitch` in tests:
  - run editable install in active venv: `python -m pip install -e .`
- Wrong interpreter/venv used:
  - print active interpreter path: `python -c "import sys; print(sys.executable)"`
  - rerun commands using explicit venv python path.
- Test output files colliding:
  - remove stale generated test files in workspace root before rerun.
- CI mismatch vs local:
  - replicate CI version and OS as closely as possible.
  - run the same nox session as CI (`ci-<version>`, `experimental-3.14`, or full `ci`).
- Docs build failures:
  - check import paths in `docs/conf.py`.
  - ensure public symbols are exported intentionally.
  - run coverage checker to identify missing API pages.
- Debug logs missing or incomplete:
  - confirm debug toggles and output path settings.
  - ensure filters are not excluding components.

## Glossary
- Stitch: a movement/operation command in pattern data.
- Jump: non-stitch movement between points.
- Trim: thread cut command.
- Color change: command to switch thread/color sequence.
- Needle set: explicit needle index change command.
- Encoder/Transcoder: normalization step converting high/mid-level commands into writer-compatible streams.
- Reader: module that parses a file format into `EmbPattern`.
- Writer: module that serializes `EmbPattern` into a file format.
- Extras: metadata dictionary stored on `EmbPattern`.

## Decision Record Index (ADR)
- Status: no formal ADR files are currently tracked in this repository.
- Recommended ADR location for future decisions: `docs/adr/`.
- ADR template recommendation:
  - Context
  - Decision
  - Alternatives considered
  - Consequences
- Initial ADR index:
  - `ADR-000`: Reserved for ADR process adoption.

## Maintenance Contract for DEVELOPERS.md
- Owners:
  - Repository maintainers listed in `pyproject.toml` and active code owners.
- Last reviewed:
  - `2026-02-15`
- Mandatory update triggers:
  - Python version policy changes.
  - CI workflow changes.
  - New required developer tool/workflow.
  - Debug harness behavior/toggles changes.
  - Sphinx/docs workflow changes.
  - Release process changes.
- Change log:
  - `2026-02-14`: Replaced with full master guide covering setup, architecture, workflows, CI, release, docs, debug, and governance.
  - `2026-02-15`: Adopted workflow plan with supported CI matrix on Python 3.9-3.13 and experimental non-gated 3.14 checks.

## Security + Secrets Basics
- Credentials/tokens:
  - Never hardcode secrets in source, tests, docs, or scripts.
  - Use environment variables or CI secret stores.
  - Scope tokens to least privilege and shortest practical lifetime.
- Safe logging/debug output:
  - Do not log tokens, credentials, private file paths, or sensitive user data.
  - When debug harness is enabled, sanitize values before emitting.
  - Prefer explicit allowlists for logged context fields.
- Disclosure path:
  - For security issues, report privately to maintainers before public disclosure.
  - Do not open public issue with exploit details until maintainers confirm remediation path.
