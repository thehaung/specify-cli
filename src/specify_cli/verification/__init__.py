"""Verification scaffolding utilities for Specify.

This package provides lightweight helpers to bootstrap a verification
framework structure inside a project's .specify directory. The primary
entry point is scaffold_verification which creates basic folders and
seed files that outline the verification workflow.
"""

from .scaffold import scaffold_verification

__all__ = ["scaffold_verification"]
