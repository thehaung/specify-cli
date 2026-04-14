"""Lightweight base classes used by the verification framework scaffold."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any


@dataclass
class VerificationTask(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self) -> bool:
        """Execute the verification task. Return True if successful."""
        raise NotImplementedError


class VerificationCheck(ABC):
    @abstractmethod
    def perform(self) -> Dict[str, Any]:
        """Run a single check and return a serializable result."""
        raise NotImplementedError


@dataclass
class VerificationReport:
    passed: bool
    details: Dict[str, Any]

    def to_json(self) -> str:
        import json

        return json.dumps({"passed": self.passed, "details": self.details}, indent=2)
