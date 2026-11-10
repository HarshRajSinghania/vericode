import shutil
import subprocess

from vericode import projects


def test_detect_python(tmp_path):
    (tmp_path / "requirements.txt").write_text("")
    assert projects.detect_primary(tmp_path) == "python"


def test_detect_node(tmp_path):
    (tmp_path / "package.json").write_text("{}")
    assert projects.detect_primary(tmp_path) == "node"


def test_detect_none(tmp_path):
    assert projects.detect_primary(tmp_path) is None


def test_typecheck_skip_no_project(tmp_path):
    assert projects.run_typecheck(tmp_path).status == "skip"


def test_tests_skip_no_tests(tmp_path):
    (tmp_path / "requirements.txt").write_text("")
    assert projects.run_tests(tmp_path).status == "skip"


def test_python_typecheck_pass(monkeypatch, tmp_path):
    (tmp_path / "requirements.txt").write_text("")
    monkeypatch.setattr(shutil, "which", lambda x: "/bin/" + x)

    class R:
        returncode = 0
        stdout = ""
        stderr = ""

    monkeypatch.setattr(subprocess, "run", lambda *a, **k: R())
    assert projects.run_typecheck(tmp_path).status == "pass"


def test_python_typecheck_fail(monkeypatch, tmp_path):
    (tmp_path / "requirements.txt").write_text("")
    monkeypatch.setattr(shutil, "which", lambda x: "/bin/" + x)

    class R:
        returncode = 1
        stdout = "err"
        stderr = ""

    monkeypatch.setattr(subprocess, "run", lambda *a, **k: R())
    assert projects.run_typecheck(tmp_path).status == "fail"


def test_detect_go(tmp_path):
    (tmp_path / "go.mod").write_text("module x\n")
    assert projects.detect_primary(tmp_path) == "go"


def test_detect_rust(tmp_path):
    (tmp_path / "Cargo.toml").write_text("[package]\n")
    assert projects.detect_primary(tmp_path) == "rust"


def test_node_typecheck_no_tsconfig(tmp_path):
    (tmp_path / "package.json").write_text("{}")
    assert projects.run_typecheck(tmp_path).status == "skip"


def test_go_typecheck_pass(monkeypatch, tmp_path):
    (tmp_path / "go.mod").write_text("module x\n")
    monkeypatch.setattr(shutil, "which", lambda x: "/bin/" + x)

    class R:
        returncode = 0
        stdout = ""
        stderr = ""

    monkeypatch.setattr(subprocess, "run", lambda *a, **k: R())
    assert projects.run_typecheck(tmp_path).status == "pass"


def test_rust_test_skip_no_cargo(monkeypatch, tmp_path):
    (tmp_path / "Cargo.toml").write_text("[package]\n")
    monkeypatch.setattr(shutil, "which", lambda x: None)
    assert projects.run_tests(tmp_path).status == "skip"
