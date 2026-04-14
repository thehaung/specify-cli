"""Pytest fixtures for specify-cli tests."""

import os
import subprocess
from pathlib import Path

import pytest
from typer.testing import CliRunner

from specify_cli.commands.init import app as init_app


@pytest.fixture
def runner():
    """Return a CliRunner for testing Typer apps."""
    return CliRunner()


@pytest.fixture
def tmp_project_dir(tmp_path):
    """Create a temporary project directory with git initialized.

    Returns:
        Path to the temporary project directory.
    """
    project_dir = tmp_path / "test_project"
    project_dir.mkdir(parents=True, exist_ok=True)

    # Initialize git repo
    subprocess.run(
        ["git", "init"],
        cwd=str(project_dir),
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Configure git user for commits
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=str(project_dir),
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=str(project_dir),
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return project_dir


@pytest.fixture
def initialized_project(tmp_project_dir, runner):
    """Create a temporary project and run init with amazonq integration.

    Returns:
        Path to the initialized project directory.
    """
    # Change to the temp directory and run init
    result = runner.invoke(
        init_app,
        ["--ai", "amazonq", "--here", "--no-git"],
        cwd=str(tmp_project_dir),
    )

    # Check init succeeded
    assert result.exit_code == 0, f"Init failed: {result.output}"

    return tmp_project_dir
