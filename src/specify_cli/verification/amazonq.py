"""Lightweight sample AmazonQ-like validation module.

This module is intentionally tiny and safe: it demonstrates how a simple
query-based validation could be performed against a known structure and
returns a serializable result suitable for reporting.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class AmazonQQuery:
    key: str
    value: Any

    def to_dict(self) -> Dict[str, Any]:
        return {"key": self.key, "value": self.value}


def simple_validate(data: dict) -> dict:
    """A tiny validator that checks required fields exist in data."""
    required = ["name", "version"]
    missing = [k for k in required if k not in data]
    return {
        "valid": len(missing) == 0,
        "missing": missing,
        "data": data,
    }
