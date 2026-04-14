from __future__ import annotations

from pathlib import Path


def run_check(target_dir: Path) -> dict:
    """Lightweight health check for the verification scaffolding.

    Returns a dict indicating if the scaffold exists and contains basic
    subdirectories. This is a minimal stand-in for a more feature-rich check
    CLI that could be wired into the main command suite.
    """
    base = target_dir / ".specify" / "verification"
    if not base.exists():
        return {"passed": False, "path": str(base)}

    required = [base / "plans", base / "checks", base / "templates"]
    ok = all(p.exists() for p in required)
    return {
        "passed": ok,
        "path": str(base),
        "plans": str(base / "plans"),
        "checks": str(base / "checks"),
        "templates": str(base / "templates"),
    }
