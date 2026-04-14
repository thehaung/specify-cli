"""Cursor integration for Specify CLI."""

import json
from pathlib import Path

from specify_cli.integrations.base import (
    SkillsIntegration,
    PLACEHOLDER_SCRIPT,
    PLACEHOLDER_ARGS,
    PLACEHOLDER_AGENT,
    process_template,
    _compute_sha256,
)


class CursorIntegration(SkillsIntegration):
    """Integration for Cursor IDE."""

    key = "cursor"
    name = "Cursor"
    requires_cli = False
    skills_dir = ".cursor/skills"
    file_extension = ".md"
    context_file = ".cursor/rules/specify-rules.mdc"

    def __init__(self):
        """Initialize CursorIntegration."""
        super().__init__(
            skills_dir=self.skills_dir,
            file_extension=self.file_extension,
            context_file=self.context_file,
        )

    def install(self, target_dir: Path, templates_dir: Path) -> list[Path]:
        """Install Cursor skills from templates.

        Creates .cursor/skills/ directory with subdirectories for each command,
        and creates .cursor/rules/specify-rules.mdc with YAML frontmatter.

        Args:
            target_dir: Directory to install into.
            templates_dir: Directory containing template files.

        Returns:
            List of Path objects for all created files.
        """
        created_files: list[Path] = []

        skills_path = target_dir / self.skills_dir
        skills_path.mkdir(parents=True, exist_ok=True)
        created_files.append(skills_path)

        commands_dir = templates_dir / "commands"
        if commands_dir.exists():
            for template_file in commands_dir.rglob(f"*{self.file_extension}"):
                base_name = template_file.stem
                skill_dir = skills_path / base_name
                skill_dir.mkdir(parents=True, exist_ok=True)
                dest_path = skill_dir / "SKILL.md"
                content = template_file.read_text(encoding="utf-8")
                processed = process_template(
                    content,
                    {
                        PLACEHOLDER_SCRIPT: base_name,
                        PLACEHOLDER_ARGS: "",
                        PLACEHOLDER_AGENT: "specify",
                    },
                )
                dest_path.write_text(processed, encoding="utf-8")
                created_files.append(dest_path)

        rules_dir = target_dir / ".cursor/rules"
        rules_dir.mkdir(parents=True, exist_ok=True)
        created_files.append(rules_dir)

        context_path = target_dir / self.context_file
        agent_template = templates_dir / "agent-file-template.md"

        if agent_template.exists():
            content = agent_template.read_text(encoding="utf-8")
        else:
            content = "# Development Guidelines\n\nAuto-generated configuration.\n"

        frontmatter = """---
description: "Project Development Guidelines"
globs: ["**/*"]
alwaysApply: true
---

"""
        processed_content = frontmatter + content
        processed_content = process_template(
            processed_content,
            {
                PLACEHOLDER_SCRIPT: "specify-rules",
                PLACEHOLDER_ARGS: "",
                PLACEHOLDER_AGENT: "specify",
            },
        )

        context_path.write_text(processed_content, encoding="utf-8")
        created_files.append(context_path)

        manifest_data = {
            "version": "1.0",
            "skills_dir": self.skills_dir,
            "file_extension": self.file_extension,
            "files": [
                {
                    "path": str(p.relative_to(target_dir)),
                    "sha256": _compute_sha256(p),
                }
                for p in created_files[1:]
                if p.is_file()
            ],
        }

        manifest_path = self.get_manifest_path(target_dir)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
        created_files.append(manifest_path)

        return created_files

    def check(self, target_dir: Path) -> dict:
        """Check if Cursor integration is properly installed.

        Args:
            target_dir: Directory to check.

        Returns:
            Dict with 'installed' (bool) and 'files' (list).
        """
        skills_path = target_dir / self.skills_dir
        manifest_path = self.get_manifest_path(target_dir)
        context_path = target_dir / self.context_file

        result: dict = {
            "installed": False,
            "files": [],
        }

        if not skills_path.exists():
            return result

        if not context_path.exists():
            return result

        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                expected_files = {f["path"] for f in manifest.get("files", [])}

                all_exist = True
                for file_path in expected_files:
                    full_path = target_dir / file_path
                    if not full_path.exists():
                        all_exist = False
                        break

                    file_sha = _compute_sha256(full_path)
                    stored_sha = next(
                        (
                            f["sha256"]
                            for f in manifest["files"]
                            if f["path"] == file_path
                        ),
                        None,
                    )
                    if file_sha != stored_sha:
                        all_exist = False
                        break

                result["installed"] = all_exist
                result["files"] = list(expected_files)
            except (json.JSONDecodeError, KeyError):
                pass
        else:
            skill_dirs = [d for d in skills_path.iterdir() if d.is_dir()]
            files = []
            for skill_dir in skill_dirs:
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    files.append(str(skill_file.relative_to(target_dir)))

            if context_path.exists():
                files.append(str(context_path.relative_to(target_dir)))

            result["installed"] = len(files) > 0
            result["files"] = files

        return result

    def get_manifest_path(self, target_dir: Path) -> Path:
        """Get the path to the manifest file.

        Args:
            target_dir: Directory where the integration is installed.

        Returns:
            Path to the manifest file.
        """
        return target_dir / ".specify/integrations/cursor.manifest.json"
