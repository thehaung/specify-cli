from __future__ import annotations

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


class AmazonQIntegration(SkillsIntegration):
    """Amazon Q integration for Specify CLI (flat-structure skills)."""

    key = "amazonq"
    name = "AmazonQ"
    requires_cli = False
    # Flat skills directory (no per-command SKILL.md folders)
    skills_dir = ".amazonq/skills"
    file_extension = ".md"
    context_file = None

    def __init__(self):
        super().__init__(
            skills_dir=self.skills_dir,
            file_extension=self.file_extension,
            context_file=self.context_file,
        )

    def install(self, target_dir: Path, templates_dir: Path) -> list[Path]:
        """Install Amazon Q skills from flat template files.

        - Creates target_dir/.amazonq/skills/
        - Reads templates_dir/skills/*.md and writes them as
          target_dir/.amazonq/skills/{stem}.md with substitutions
        - Builds a manifest at target_dir/.specify/integrations/amazonq.manifest.json
        - Returns all created files including the manifest
        """
        created_files: list[Path] = []

        skills_path = target_dir / self.skills_dir
        skills_path.mkdir(parents=True, exist_ok=True)
        created_files.append(skills_path)

        templates_skills_dir = templates_dir / "skills"
        if templates_skills_dir.exists():
            for template_file in templates_skills_dir.glob(f"*{self.file_extension}"):
                base_name = template_file.stem
                dest_path = skills_path / f"{base_name}{self.file_extension}"
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

        # Manifest for Amazon Q integration
        manifest_data = {
            "version": "1.0",
            "skills_dir": self.skills_dir,
            "file_extension": self.file_extension,
            "files": [
                {
                    "path": str(p.relative_to(target_dir)),
                    "sha256": _compute_sha256(p),
                }
                for p in created_files[1:]  # skip the skills_path directory
                if p.is_file()
            ],
        }

        manifest_path = self.get_manifest_path(target_dir)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
        created_files.append(manifest_path)

        return created_files

    def check(self, target_dir: Path) -> dict:
        """Check if Amazon Q integration is properly installed."""
        skills_path = target_dir / self.skills_dir
        manifest_path = self.get_manifest_path(target_dir)

        result: dict = {"installed": False, "files": []}

        if not skills_path.exists():
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
            # No manifest; fall back to simple heuristic
            files = [
                str(p.relative_to(target_dir))
                for p in (skills_path).glob(f"**/*{self.file_extension}")
            ]
            result["installed"] = len(files) > 0
            result["files"] = files

        return result

    def get_manifest_path(self, target_dir: Path) -> Path:
        """Get the path to the Amazon Q manifest file."""
        return target_dir / ".specify/integrations/amazonq.manifest.json"
