"""High-level runner coordinating verification scaffolds."""

from __future__ import annotations

from pathlib import Path

from .scaffold import scaffold_verification


def init_run(target_dir: Path) -> dict:
    """Initialize a minimal verification scaffold in the given directory.

    Returns a dict describing what was created for introspection in tests
    or tooling.
    """
    return scaffold_verification(target_dir)
