"""Base integration classes for Specify CLI."""

from abc import ABC, abstractmethod
import hashlib
import json
import shutil
from pathlib import Path

# Placeholder tokens for template substitution
PLACEHOLDER_SCRIPT = "{SCRIPT}"
PLACEHOLDER_ARGS = "{ARGS}"
PLACEHOLDER_AGENT = "__AGENT__"


class IntegrationBase(ABC):
    """Abstract base class for integrations."""

    key: str
    name: str
    requires_cli: bool

    @abstractmethod
    def install(self, target_dir: Path, templates_dir: Path) -> list[Path]:
        """Install the integration into the target directory.

        Args:
            target_dir: Directory to install into.
            templates_dir: Directory containing template files.

        Returns:
            List of Path objects for all created files.
        """
        ...

    @abstractmethod
    def check(self, target_dir: Path) -> dict:
        """Check if the integration is properly installed.

        Args:
            target_dir: Directory to check.

        Returns:
            Dict with 'installed' (bool) and 'files' (list) keys.
        """
        ...

    @abstractmethod
    def get_manifest_path(self, target_dir: Path) -> Path:
        """Get the path to the integration's manifest file.

        Args:
            target_dir: Directory where the integration is installed.

        Returns:
            Path to the manifest file.
        """
        ...


class SkillsIntegration(IntegrationBase):
    """Integration for skills-based workflows."""

    def __init__(
        self,
        skills_dir: str = ".specify/skills",
        file_extension: str = ".md",
        context_file: str | None = None,
    ):
        """Initialize SkillsIntegration.

        Args:
            skills_dir: Relative path to skills directory.
            file_extension: Extension for skill files.
            context_file: Optional name of context file to maintain.
        """
        self.skills_dir = skills_dir
        self.file_extension = file_extension
        self.context_file = context_file

    def install(self, target_dir: Path, templates_dir: Path) -> list[Path]:
        """Install skills from templates.

        Args:
            target_dir: Directory to install into.
            templates_dir: Directory containing template files.

        Returns:
            List of Path objects for all created files.
        """
        created_files: list[Path] = []
        skills_path = target_dir / self.skills_dir

        # Create skills directory
        skills_path.mkdir(parents=True, exist_ok=True)
        created_files.append(skills_path)

        # Find all template files in templates_dir
        if templates_dir.exists():
            for template_file in templates_dir.rglob(f"*{self.file_extension}"):
                # Compute relative path from templates_dir
                rel_path = template_file.relative_to(templates_dir)
                dest_path = skills_path / rel_path

                # Create destination directory if needed
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Read template content
                content = template_file.read_text(encoding="utf-8")

                # Perform substitutions
                processed = process_template(content, {
                    PLACEHOLDER_SCRIPT: rel_path.stem,
                    PLACEHOLDER_ARGS: "",
                    PLACEHOLDER_AGENT: "specify",
                })

                # Write processed file
                dest_path.write_text(processed, encoding="utf-8")
                created_files.append(dest_path)

        # Create manifest
        manifest_data = {
            "version": "1.0",
            "skills_dir": self.skills_dir,
            "file_extension": self.file_extension,
            "files": [
                {
                    "path": str(p.relative_to(skills_path)),
                    "sha256": _compute_sha256(p),
                }
                for p in created_files[1:]  # Skip the skills_path itself
            ],
        }

        manifest_path = self.get_manifest_path(target_dir)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
        created_files.append(manifest_path)

        return created_files

    def check(self, target_dir: Path) -> dict:
        """Check if skills are properly installed.

        Args:
            target_dir: Directory to check.

        Returns:
            Dict with 'installed' (bool) and 'files' (list).
        """
        skills_path = target_dir / self.skills_dir
        manifest_path = self.get_manifest_path(target_dir)

        result: dict = {
            "installed": False,
            "files": [],
        }

        # Check if skills directory exists
        if not skills_path.exists():
            return result

        # Load and validate manifest
        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                expected_files = {f["path"] for f in manifest.get("files", [])}

                # Check all expected files exist
                all_exist = True
                for file_path in expected_files:
                    if not (skills_path / file_path).exists():
                        all_exist = False
                        break

                    # Verify SHA256
                    file_sha = _compute_sha256(skills_path / file_path)
                    stored_sha = next(
                        (f["sha256"] for f in manifest["files"] if f["path"] == file_path),
                        None,
                    )
                    if file_sha != stored_sha:
                        all_exist = False
                        break

                result["installed"] = all_exist
                result["files"] = list(expected_files)
            except (json.JSONDecodeError, KeyError):
                # Manifest invalid - consider not installed
                pass
        else:
            # No manifest - check if skills directory has any files
            files = [str(p.relative_to(skills_path)) for p in skills_path.rglob(f"*{self.file_extension}")]
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
        return target_dir / self.skills_dir / "manifest.json"


def _compute_sha256(file_path: Path) -> str:
    """Compute SHA256 hex digest of a file.

    Args:
        file_path: Path to the file.

    Returns:
        SHA256 hex digest string.
    """
    sha256_hash = hashlib.sha256()
    content = file_path.read_bytes()
    sha256_hash.update(content)
    return sha256_hash.hexdigest()


def process_template(content: str, substitutions: dict) -> str:
    """Process template by replacing placeholders.

    Uses simple str.replace() for substitution. Supports:
    - {SCRIPT} - Script/function name
    - {ARGS} - Arguments string
    - __AGENT__ - Agent identifier

    Args:
        content: Template content string.
        substitutions: Dict mapping placeholder strings to replacement values.

    Returns:
        Processed content with substitutions applied.
    """
    result = content
    for placeholder, replacement in substitutions.items():
        result = result.replace(placeholder, replacement)
    return result
