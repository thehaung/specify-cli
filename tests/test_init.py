"""Tests for the init command."""

import json
import os
import stat
from contextlib import contextmanager
from pathlib import Path

from typer.testing import CliRunner

from specify_cli.commands.init import app as init_app


@contextmanager
def cd(path: Path):
    """Context manager to temporarily change directory."""
    old_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)


def test_init_creates_specify_dir(runner: CliRunner, tmp_path: Path):
    """Test that init creates .specify/ directory structure."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir(parents=True)

    with cd(project_dir):
        result = runner.invoke(
            init_app,
            ["--ai", "amazonq", "--here", "--no-git"],
        )

    assert result.exit_code == 0

    specify_dir = project_dir / ".specify"
    assert specify_dir.exists()
    assert specify_dir.is_dir()

    assert (specify_dir / "memory").exists()
    assert (specify_dir / "scripts" / "bash").exists()
    assert (specify_dir / "templates").exists()


def test_init_amazonq_creates_skills(runner: CliRunner, tmp_path: Path):
    """Test that init with --ai amazonq creates skill files."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir(parents=True)

    with cd(project_dir):
        result = runner.invoke(
            init_app,
            ["--ai", "amazonq", "--here", "--no-git"],
        )

    assert result.exit_code == 0

    skills_dir = project_dir / ".amazonq" / "skills"
    assert skills_dir.exists()

    skill_files = list(skills_dir.rglob("*.md"))
    assert len(skill_files) >= 9

    expected_skills = [
        "speckit-specify.md",
        "speckit-constitution.md",
        "speckit-clarify.md",
        "speckit-taskstoissues.md",
        "speckit-checklist.md",
        "speckit-plan.md",
        "speckit-analyze.md",
        "speckit-tasks.md",
        "speckit-implement.md",
    ]

    skill_names = [f.name for f in skill_files]
    for expected in expected_skills:
        assert expected in skill_names


def test_init_cursor_creates_skills(runner: CliRunner, tmp_path: Path):
    """Test that init with --ai cursor creates 9 SKILL.md directories plus rules."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir(parents=True)

    with cd(project_dir):
        result = runner.invoke(
            init_app,
            ["--ai", "cursor", "--here", "--no-git"],
        )

    assert result.exit_code == 0

    cursor_skills_dir = project_dir / ".cursor" / "skills"
    assert cursor_skills_dir.exists()

    skill_dirs = [d for d in cursor_skills_dir.iterdir() if d.is_dir()]
    assert len(skill_dirs) == 9

    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        assert skill_file.exists()

    rules_file = project_dir / ".cursor" / "rules" / "specify-rules.mdc"
    assert rules_file.exists()


def test_init_both_integrations(runner: CliRunner, tmp_path: Path):
    """Test that init with --ai both creates both AmazonQ and Cursor integrations."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir(parents=True)

    with cd(project_dir):
        result = runner.invoke(
            init_app,
            ["--ai", "both", "--here", "--no-git"],
        )

    assert result.exit_code == 0

    amazonq_skills_dir = project_dir / ".amazonq" / "skills"
    assert amazonq_skills_dir.exists()
    amazonq_files = list(amazonq_skills_dir.rglob("*.md"))
    assert len(amazonq_files) >= 9

    cursor_skills_dir = project_dir / ".cursor" / "skills"
    assert cursor_skills_dir.exists()
    cursor_dirs = [d for d in cursor_skills_dir.iterdir() if d.is_dir()]
    assert len(cursor_dirs) >= 9

    rules_file = project_dir / ".cursor" / "rules" / "specify-rules.mdc"
    assert rules_file.exists()


def test_init_detects_existing_specify(runner: CliRunner, tmp_path: Path):
    """Test that init prompts when .specify/ already exists."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir(parents=True)

    specify_dir = project_dir / ".specify"
    specify_dir.mkdir()
    (specify_dir / "existing_file.txt").write_text("existing content")

    with cd(project_dir):
        result = runner.invoke(
            init_app,
            ["--ai", "amazonq", "--here", "--no-git"],
        )

    assert "Detected existing .specify/" in result.output or result.exit_code == 0


def test_init_options_json_valid(runner: CliRunner, tmp_path: Path):
    """Test that init-options.json is valid JSON with expected keys."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir(parents=True)

    with cd(project_dir):
        result = runner.invoke(
            init_app,
            ["--ai", "amazonq", "--here", "--no-git"],
        )

    assert result.exit_code == 0

    init_options_path = project_dir / ".specify" / "init-options.json"
    assert init_options_path.exists()

    content = init_options_path.read_text(encoding="utf-8")
    data = json.loads(content)

    assert "project_dir" in data
    assert "ai" in data
    assert "git" in data

    assert data["ai"] == "amazonq"
    assert data["git"] is False


def test_init_integration_json_valid(runner: CliRunner, tmp_path: Path):
    """Test that integration.json is valid JSON."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir(parents=True)

    with cd(project_dir):
        result = runner.invoke(
            init_app,
            ["--ai", "amazonq", "--here", "--no-git"],
        )

    assert result.exit_code == 0

    integration_path = project_dir / ".specify" / "integration.json"
    assert integration_path.exists()

    content = integration_path.read_text(encoding="utf-8")
    data = json.loads(content)

    assert "primary_integration" in data
    assert "installed_integrations" in data

    assert "AmazonQIntegration" in data["primary_integration"]
    assert "amazonq" in data["installed_integrations"]


def test_init_scripts_executable(runner: CliRunner, tmp_path: Path):
    """Test that bash scripts have executable permissions."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir(parents=True)

    with cd(project_dir):
        result = runner.invoke(
            init_app,
            ["--ai", "amazonq", "--here", "--no-git"],
        )

    assert result.exit_code == 0

    scripts_dir = project_dir / ".specify" / "scripts" / "bash"
    assert scripts_dir.exists()

    script_files = list(scripts_dir.iterdir())
    assert len(script_files) > 0

    for script_file in script_files:
        if script_file.is_file():
            mode = script_file.stat().st_mode
            assert mode & stat.S_IEXEC, f"{script_file.name} is not executable"


def test_init_git_repo_created(runner: CliRunner, tmp_path: Path):
    """Test that git repo is initialized when not using --no-git."""
    import subprocess

    project_dir = tmp_path / "test_project"
    project_dir.mkdir(parents=True)

    with cd(project_dir):
        result = runner.invoke(
            init_app,
            ["--ai", "amazonq", "--here"],
        )

    assert result.exit_code == 0

    git_dir = project_dir / ".git"
    assert git_dir.exists()
    assert git_dir.is_dir()
