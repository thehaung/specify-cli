"""Tiny scaffold helper for a verification framework.

This module provides a single function to bootstrap a minimal verification
structure under a project's .specify directory. The goal is to offer a
disciplined starting point for GOAL-ORIENTED autonomous verification
workflows without introducing opinionated behavior into the core CLI.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.mkdir(parents=True, exist_ok=True)


def scaffold_verification(target_root: Path) -> Dict[str, object]:
    """Create a minimal verification scaffold inside .specify/verification.

    The layout is intentionally lightweight:
    - .specify/verification/plans/
    - .specify/verification/checks/
    - .specify/verification/templates/
    - .specify/verification/templates/sample-check.md
    - .specify/verification/README.md
    """
    verify_root = target_root / ".specify" / "verification"
    _ensure_dir(verify_root / "plans")
    _ensure_dir(verify_root / "checks")
    _ensure_dir(verify_root / "templates")

    # Seed a minimal plan and a couple of templates
    seed_plan = verify_root / "plans" / "example-plan.md"
    if not seed_plan.exists():
        seed_plan.write_text(
            "# Example verification plan\n\nThis plan outlines the verification steps."
        )

    seed_template = verify_root / "templates" / "sample-check.md"
    if not seed_template.exists():
        seed_template.write_text(
            "# Sample check template\n\n- [ ] Step 1\n- [ ] Step 2\n"
        )

    readme = verify_root.parent / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Verification scaffold\n\nThis directory contains a lightweight verification framework scaffold for the project."
        )

    return {
        "path": str(verify_root),
        "plans_seeded": seed_plan.exists(),
        "templates_seeded": seed_template.exists(),
    }
