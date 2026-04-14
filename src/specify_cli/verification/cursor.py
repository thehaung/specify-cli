"""Minimal Cursor-like context manager for verification runs."""

from __future__ import annotations

from pathlib import Path
import json


class CursorContext:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.steps = []  # list of (step_name, completed_bool)

    def add_step(self, name: str, completed: bool = False) -> None:
        self.steps.append({"name": name, "completed": completed})

    def mark_complete(self, name: str) -> None:
        for s in self.steps:
            if s["name"] == name:
                s["completed"] = True
                break

    def to_json(self) -> str:
        return json.dumps({"path": str(self.path), "steps": self.steps}, indent=2)

    def persist(self) -> Path:
        manifest = self.path / "cursor-manifest.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(self.to_json(), encoding="utf-8")
        return manifest
