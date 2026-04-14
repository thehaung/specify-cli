from pathlib import Path

import pytest

from specify_cli.verification.scaffold import scaffold_verification
from specify_cli.verification.runner import init_run


def test_scaffold_creates_verification_structure(tmp_path: Path):
    project_dir = tmp_path / "proj"
    project_dir.mkdir(parents=True)

    result = scaffold_verification(project_dir)

    verify_root = project_dir / ".specify" / "verification"
    assert verify_root.exists() and verify_root.is_dir()

    plans_dir = verify_root / "plans"
    templates_dir = verify_root / "templates"
    assert plans_dir.exists() and templates_dir.exists()

    plan_file = plans_dir / "example-plan.md"
    template_file = templates_dir / "sample-check.md"
    assert plan_file.exists()
    assert template_file.exists()

    # README for scaffold should exist at .specify/README.md
    readme = project_dir / ".specify" / "README.md"
    assert readme.exists()

    # Result metadata
    assert isinstance(result, dict)
    assert "path" in result
    assert result["plans_seeded"] is True
    assert result["templates_seeded"] is True


def test_init_run_bootstraps_verification(tmp_path: Path):
    project_dir = tmp_path / "proj2"
    project_dir.mkdir(parents=True)

    res = init_run(project_dir)
    assert isinstance(res, dict)
    verify_root = project_dir / ".specify" / "verification"
    assert verify_root.exists()
    assert (verify_root / "plans").exists()
