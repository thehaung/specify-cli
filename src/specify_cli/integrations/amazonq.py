from pathlib import Path

from specify_cli.integrations.base import SkillsIntegration


class AmazonQIntegration(SkillsIntegration):
    key = "amazonq"
    name = "AmazonQ"
    requires_cli = False
    skills_dir = ".specify/amazonq/skills"
    file_extension = ".md"
    context_file = None

    def __init__(self):
        super().__init__(
            skills_dir=self.skills_dir,
            file_extension=self.file_extension,
            context_file=self.context_file,
        )

    def get_manifest_path(self, target_dir: Path) -> Path:
        return target_dir / ".specify/amazonq/manifest.json"
