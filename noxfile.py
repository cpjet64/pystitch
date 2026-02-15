"""Nox automation for supported-version quality, packaging, and audit checks."""

import nox

SUPPORTED_PYTHONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]
EXPERIMENTAL_PYTHONS = ["3.14"]

nox.options.default_venv_backend = "uv|virtualenv"
nox.options.error_on_missing_interpreters = True
nox.options.sessions = ["ci"]


def install_dev(session: nox.Session) -> None:
    """Install the project with development dependencies."""
    session.install("--upgrade", "pip")
    session.install("-e", ".[dev]")


def run_lint(session: nox.Session) -> None:
    """Run baseline lint checks that are stable on the current codebase."""
    session.run("ruff", "check", "src", "test")


def run_typecheck(session: nox.Session) -> None:
    """Run baseline static typing checks."""
    session.run("mypy", "src/pystitch")


def run_tests(session: nox.Session) -> None:
    """Run the test suite under pytest (includes unittest tests)."""
    session.run("pytest", "-q")


@nox.session(python=SUPPORTED_PYTHONS)
def ci(session: nox.Session) -> None:
    """Run tests + lint + type checks for supported versions."""
    install_dev(session)
    run_tests(session)
    run_lint(session)
    run_typecheck(session)


@nox.session(python=EXPERIMENTAL_PYTHONS)
def experimental(session: nox.Session) -> None:
    """Run the full quality pipeline for experimental Python versions."""
    install_dev(session)
    run_tests(session)
    run_lint(session)
    run_typecheck(session)


@nox.session(python=["3.13"])
def quick(session: nox.Session) -> None:
    """Fast local iteration on the primary development interpreter."""
    install_dev(session)
    run_tests(session)


@nox.session(python=["3.13"])
def package(session: nox.Session) -> None:
    """Build package artifacts and validate metadata."""
    install_dev(session)
    session.run(
        "python",
        "-c",
        "import shutil; shutil.rmtree('build', ignore_errors=True); shutil.rmtree('dist', ignore_errors=True)",
    )
    session.run("python", "-m", "build")
    session.run(
        "python",
        "-c",
        (
            "from pathlib import Path; "
            "import subprocess, sys; "
            "files=[str(p) for p in Path('dist').glob('*') if p.is_file()]; "
            "assert files, 'dist/ is empty after build'; "
            "raise SystemExit(subprocess.call([sys.executable, '-m', 'twine', 'check', *files]))"
        ),
    )


@nox.session(python=["3.13"])
def audit(session: nox.Session) -> None:
    """Run dependency vulnerability audit with waiver policy."""
    install_dev(session)
    session.run("python", ".ci/audit_with_waivers.py")
