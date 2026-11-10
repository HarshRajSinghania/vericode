"""Project detection and running type-checkers / test runners."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

CheckStatus = Literal["pass", "fail", "skip", "error"]

PROJECT_MARKERS = {
    "python": ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"],
    "node": ["package.json"],
    "go": ["go.mod"],
    "rust": ["Cargo.toml"],
}
ORDER = ("python", "node", "go", "rust")


@dataclass
class CheckResult:
    name: str
    status: CheckStatus
    detail: str = ""
    summary: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "status": self.status,
            "detail": self.detail,
            "summary": self.summary,
        }


def detect_project(root: Path) -> dict[str, bool]:
    return {
        pt: any((root / m).exists() for m in markers) for pt, markers in PROJECT_MARKERS.items()
    }


def detect_primary(root: Path) -> str | None:
    found = detect_project(root)
    for t in ORDER:
        if found.get(t):
            return t
    return None


def _run(cmd: list[str], cwd: Path, timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def run_typecheck(root: Path, ptype: str | None = None) -> CheckResult:
    ptype = ptype or detect_primary(root)
    if ptype is None:
        return CheckResult("typecheck", "skip", "No supported project detected")
    if ptype == "python":
        tool = shutil.which("mypy") or shutil.which("pyright")
        if not tool:
            return CheckResult("typecheck", "skip", "mypy/pyright not installed (pip install mypy)")
        try:
            r = _run([tool, "."], root)
            return CheckResult(
                "typecheck",
                "pass" if r.returncode == 0 else "fail",
                f"{Path(tool).name}: clean" if r.returncode == 0 else (r.stdout + r.stderr)[-2000:],
            )
        except subprocess.TimeoutExpired:
            return CheckResult("typecheck", "error", "timed out")
    if ptype == "node":
        if not (root / "tsconfig.json").exists():
            return CheckResult(
                "typecheck", "skip", "no tsconfig.json (plain JS, nothing to type-check)"
            )
        if not shutil.which("tsc"):
            return CheckResult("typecheck", "skip", "tsc not installed (npm i -g typescript)")
        try:
            r = _run(["tsc", "--noEmit"], root)
            return CheckResult(
                "typecheck",
                "pass" if r.returncode == 0 else "fail",
                "tsc: clean" if r.returncode == 0 else (r.stdout + r.stderr)[-2000:],
            )
        except subprocess.TimeoutExpired:
            return CheckResult("typecheck", "error", "timed out")
    if ptype == "go":
        if not shutil.which("go"):
            return CheckResult("typecheck", "skip", "go not installed")
        try:
            r = _run(["go", "vet", "./..."], root)
            return CheckResult(
                "typecheck",
                "pass" if r.returncode == 0 else "fail",
                "go vet: clean" if r.returncode == 0 else r.stderr[-2000:],
            )
        except subprocess.TimeoutExpired:
            return CheckResult("typecheck", "error", "timed out")
    if ptype == "rust":
        if not shutil.which("cargo"):
            return CheckResult("typecheck", "skip", "cargo not installed")
        try:
            r = _run(["cargo", "check"], root)
            return CheckResult(
                "typecheck",
                "pass" if r.returncode == 0 else "fail",
                "cargo check: clean" if r.returncode == 0 else r.stderr[-2000:],
            )
        except subprocess.TimeoutExpired:
            return CheckResult("typecheck", "error", "timed out")
    return CheckResult("typecheck", "skip", "unsupported project type")


def run_tests(root: Path, ptype: str | None = None) -> CheckResult:
    ptype = ptype or detect_primary(root)
    if ptype is None:
        return CheckResult("tests", "skip", "No supported project detected")
    if ptype == "python":
        has_tests = (
            (root / "tests").is_dir()
            or list(root.glob("test_*.py"))
            or list(root.glob("*_test.py"))
        )
        if not has_tests:
            return CheckResult("tests", "skip", "no tests found")
        if not shutil.which("pytest"):
            return CheckResult("tests", "skip", "pytest not installed")
        try:
            r = _run(["pytest", "-q"], root)
            return CheckResult(
                "tests",
                "pass" if r.returncode == 0 else "fail",
                "pytest: passed" if r.returncode == 0 else (r.stdout + r.stderr)[-2000:],
            )
        except subprocess.TimeoutExpired:
            return CheckResult("tests", "error", "timed out")
    if ptype == "node":
        if not shutil.which("npm"):
            return CheckResult("tests", "skip", "npm not installed")
        try:
            r = _run(["npm", "test", "--", "--silent"], root)
            return CheckResult(
                "tests",
                "pass" if r.returncode == 0 else "fail",
                "npm test: passed" if r.returncode == 0 else (r.stdout + r.stderr)[-2000:],
            )
        except subprocess.TimeoutExpired:
            return CheckResult("tests", "error", "timed out")
    if ptype == "go":
        if not shutil.which("go"):
            return CheckResult("tests", "skip", "go not installed")
        try:
            r = _run(["go", "test", "./..."], root)
            return CheckResult(
                "tests",
                "pass" if r.returncode == 0 else "fail",
                "go test: passed" if r.returncode == 0 else r.stderr[-2000:],
            )
        except subprocess.TimeoutExpired:
            return CheckResult("tests", "error", "timed out")
    if ptype == "rust":
        if not shutil.which("cargo"):
            return CheckResult("tests", "skip", "cargo not installed")
        try:
            r = _run(["cargo", "test"], root)
            return CheckResult(
                "tests",
                "pass" if r.returncode == 0 else "fail",
                "cargo test: passed" if r.returncode == 0 else r.stderr[-2000:],
            )
        except subprocess.TimeoutExpired:
            return CheckResult("tests", "error", "timed out")
    return CheckResult("tests", "skip", "unsupported project type")
