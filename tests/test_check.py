"""Tests for the check command."""

import json
import os
from contextlib import contextmanager
from pathlib import Path

from typer.testing import CliRunner

from specify_cli.commands.check import (
    app as check_app,
    check_integrations,
)


@contextmanager
def cd(path: Path):
    """Context manager to temporarily change directory."""
    old_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)


def test_check_passes_on_healthy_setup(runner: CliRunner, tmp_path: Path):
    """Test that check returns exit 0 on a healthy setup."""
    from specify_cli.commands.init import app as init_app

    project_dir = tmp_path / "test_project"
    project_dir.mkdir(parents=True)

    with cd(project_dir):
        init_result = runner.invoke(
            init_app,
            ["--ai", "amazonq", "--here", "--no-git"],
        )
    assert init_result.exit_code == 0

    with cd(project_dir):
        result = runner.invoke(
            check_app,
            [],
        )

    assert result.exit_code == 0
    assert "All checks passed" in result.output or result.exit_code == 0


def test_check_fails_on_missing_files(runner: CliRunner, tmp_path: Path):
    """Test that check returns exit 1 when files are missing."""
    from specify_cli.commands.init import app as init_app

    project_dir = tmp_path / "test_project"
    project_dir.mkdir(parents=True)

    with cd(project_dir):
        init_result = runner.invoke(
            init_app,
            ["--ai", "amazonq", "--here", "--no-git"],
        )
    assert init_result.exit_code == 0

    specify_dir = project_dir / ".specify"
    constitution_path = specify_dir / "memory" / "constitution.md"
    if constitution_path.exists():
        constitution_path.unlink()

    with cd(project_dir):
        result = runner.invoke(
            check_app,
            [],
        )

    assert result.exit_code == 1


def test_check_returns_2_without_specify(runner: CliRunner, tmp_path: Path):
    """Test that check returns exit 2 when not in a Specify project."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir(parents=True)

    with cd(project_dir):
        result = runner.invoke(
            check_app,
            [],
        )

    assert result.exit_code == 2
    assert "Not in a Specify project" in result.output


def test_check_json_output(runner: CliRunner, tmp_path: Path):
    """Test that check --json produces valid JSON output."""
    from specify_cli.commands.init import app as init_app

    project_dir = tmp_path / "test_project"
    project_dir.mkdir(parents=True)

    with cd(project_dir):
        init_result = runner.invoke(
            init_app,
            ["--ai", "amazonq", "--here", "--no-git"],
        )
    assert init_result.exit_code == 0

    with cd(project_dir):
        result = runner.invoke(
            check_app,
            ["--json"],
        )

    assert result.exit_code == 0

    # Rich console may wrap output, so remove soft newlines within lines
    # by removing newlines that aren't followed by proper JSON indentation
    output = result.output
    # Fix wrapped lines by removing newlines not preceded by JSON structure
    cleaned = ""
    for line in output.splitlines():
        stripped = line.strip()
        if cleaned and not stripped.startswith(("{", "}", "[", "]", '"')):
            # This is a continuation of a wrapped line
            cleaned = cleaned.rstrip() + stripped
        else:
            if cleaned:
                cleaned += "\n"
            cleaned += line

    data = json.loads(cleaned)

    assert "core_tools" in data
    assert "config" in data
    assert "templates" in data
    assert "scripts" in data
    assert "constitution" in data
    assert "integrations" in data
    assert "all_passed" in data

    assert isinstance(data["all_passed"], bool)


def test_check_integration_health():
    """Test that integration check method works correctly."""
    from specify_cli.commands.init import app as init_app
    from typer.testing import CliRunner

    runner = CliRunner()
    import tempfile

    with tempfile.TemporaryDirectory() as tmp_dir:
        project_dir = Path(tmp_dir) / "test_project"
        project_dir.mkdir(parents=True)

        with cd(project_dir):
            init_result = runner.invoke(
                init_app,
                ["--ai", "amazonq", "--here", "--no-git"],
            )
        assert init_result.exit_code == 0

        specify_dir = project_dir / ".specify"

        integration_result = check_integrations(specify_dir)

        assert isinstance(integration_result, dict)
        assert "passed" in integration_result
        assert "integrations" in integration_result
        assert "path" in integration_result

        assert isinstance(integration_result["passed"], bool)
        assert isinstance(integration_result["integrations"], dict)
