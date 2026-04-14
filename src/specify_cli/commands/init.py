import json
import os
import shutil
import stat
import subprocess
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from specify_cli.integrations import INTEGRATION_REGISTRY
from importlib import resources


app = typer.Typer(help="Initialize a new Specify project with bundled assets.")
console = Console()


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.mkdir(parents=True, exist_ok=True)


def _copy_asset_tree(src_root: Path, dest_root: Path) -> None:
    # Copy all files from src_root to dest_root, preserving structure
    for root, dirs, files in os.walk(src_root):
        rel = Path(root).relative_to(src_root)
        dest_dir = dest_root / rel
        dest_dir.mkdir(parents=True, exist_ok=True)
        for f in files:
            s = Path(root) / f
            d = dest_dir / f
            if not d.exists():
                shutil.copy2(s, d)


@app.command()
def init(
    ai: Optional[str] = typer.Option(
        None, "--ai", help="AI integration to install: amazonq, cursor, or both."
    ),
    here: bool = typer.Option(
        False, "--here", help="Use current directory as project directory"
    ),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git initialization"),
):
    """Create a new Specify project in a directory with bundled assets."""

    # Resolve target project directory
    target_dir = Path.cwd()
    if here:
        target_dir = Path.cwd()

    # Interactive wizard when no --ai provided
    if ai is None:
        console.print(Panel("Specify Init Wizard", title="Init", expand=False))
        # Project dir
        dir_input = typer.prompt("Project directory (empty for current)", default="")
        if dir_input:
            target_dir = Path(dir_input).expanduser().resolve()
        else:
            target_dir = Path.cwd()

        # AI selection
        console.print("Select AI integration:")
        console.print("  1) AmazonQ")
        console.print("  2) Cursor")
        console.print("  3) Both (AmazonQ + Cursor)")
        choice = typer.prompt("Enter choice [1-3]", type=int, default=1)
        if choice == 1:
            ai = "amazonq"
        elif choice == 2:
            ai = "cursor"
        else:
            ai = "both"

        # Branch numbering (stub, only for UI parity)
        console.print("Branch numbering:")
        console.print("  1) Sequential")
        console.print("  2) Timestamp")
        branch_choice = typer.prompt("Enter choice [1-2]", type=int, default=1)
        # store on disk for future runs
        _branch = "sequential" if branch_choice == 1 else "timestamp"

        # Script type (v1 defaults to Bash; skip prompt per requirements)
        # Git init
        git_choice = typer.prompt("Initialize git repository? (y/n)", default="y")
        _git = git_choice.lower() in ("y", "yes", "true")

    else:
        _git = not no_git

    # Check for existing .specify in target_dir
    spec_path = target_dir / ".specify"
    if spec_path.exists():
        console.print(
            Panel(
                f"Detected existing .specify/ at {str(spec_path)}. What would you like to do?",
                title="Existing project",
            )
        )
        console.print("1) Overwrite (start fresh)")
        console.print("2) Merge with existing (preserve files)")
        console.print("3) Abort")
        action = typer.prompt("Choose an option [1-3]", type=int, default=3)
        if action == 1:
            shutil.rmtree(spec_path)
        elif action == 2:
            pass
        else:
            console.print("Init aborted by user.")
            raise typer.Abort()

    # Create directory structure
    _ensure_dir(spec_path / "memory")
    _ensure_dir(spec_path / "scripts" / "bash")
    _ensure_dir(spec_path / "templates")

    # Copy bundled assets (bash scripts and templates) into the new project
    # Use importlib.resources to access bundled assets
    # Bash scripts
    pkg_root = None
    try:
        pkg_root = resources.files("specify_cli")
        src_bash = pkg_root.joinpath("scripts").joinpath("bash")
        if src_bash.exists():
            _copy_asset_tree(Path(src_bash), spec_path / "scripts" / "bash")
    except Exception:
        # Fallback: rely on local repo copies (non-fatal)
        console.print("Warning: could not copy bundled bash scripts.")

    # Templates
    try:
        if pkg_root is not None:
            src_templates = pkg_root.joinpath("templates")
            if src_templates.exists():
                _copy_asset_tree(Path(src_templates), spec_path / "templates")
    except Exception:
        console.print("Warning: could not copy bundled templates.")

    # Constitution: initialize memory/constitution.md from constitution-template.md
    constitution_template = spec_path / "templates" / "constitution-template.md"
    constitution_path = spec_path / "memory" / "constitution.md"
    if constitution_template.exists():
        text = constitution_template.read_text(encoding="utf-8")
        # Simple substitutions
        proj_name = target_dir.name
        text = text.replace("[PROJECT_NAME]", proj_name)
        text = text.replace("[PRINCIPLE_1_NAME]", "I. Library-First")
        text = text.replace(
            "[PRINCIPLE_1_DESCRIPTION]",
            "Libraries must be self-contained and independently testable.",
        )
        text = text.replace("[PRINCIPLE_2_NAME]", "II. CLI Interface")
        text = text.replace(
            "[PRINCIPLE_2_DESCRIPTION]", "Clear and predictable command-line usage."
        )
        text = text.replace("[PRINCIPLE_3_NAME]", "III. Test-Driven Development")
        text = text.replace(
            "[PRINCIPLE_3_DESCRIPTION]", "Tests drive design and ensure stability."
        )
        text = text.replace("[PRINCIPLE_4_NAME]", "IV. Integration Testing")
        text = text.replace(
            "[PRINCIPLE_4_DESCRIPTION]",
            "Contracts and interfaces must be exercised end-to-end.",
        )
        text = text.replace("[PRINCIPLE_5_NAME]", "V. Observability")
        text = text.replace(
            "[PRINCIPLE_5_DESCRIPTION]", "Logging and metrics for reliability."
        )
        text = text.replace("[SECTION_2_NAME]", "Additional Constraints")
        text = text.replace(
            "[SECTION_2_CONTENT]", "Security, performance, and usability requirements."
        )
        text = text.replace("[SECTION_3_NAME]", "Development Workflow")
        text = text.replace(
            "[SECTION_3_CONTENT]", "Code reviews and testing requirements."
        )
        text = text.replace(
            "[GOVERNANCE_RULES]", "All changes must be documented and reviewed."
        )
        text = text.replace("[CONSTITUTION_VERSION]", "1.0.0")
        text = text.replace("[RATIFICATION_DATE]", "2026-01-01")
        text = text.replace("[LAST_AMENDED_DATE]", "2026-01-01")
        constitution_path.parent.mkdir(parents=True, exist_ok=True)
        constitution_path.write_text(text, encoding="utf-8")

    # Init integrations
    installed = []
    primary_integration = None
    if ai:
        # support multiple options: amazonq, cursor, or both
        if ai == "amazonq" or ai == "both":
            _inst = INTEGRATION_REGISTRY.get("amazonq")
            if _inst:
                primary_integration = _inst
                inst_obj = _inst()
                inst_obj.install(target_dir, spec_path / "templates")
                installed.append("amazonq")
        if ai == "cursor" or ai == "both":
            # Cursor integration is added below after we construct it lazily
            try:
                from specify_cli.integrations.cursor import CursorIntegration

                inst = CursorIntegration()
                inst.install(target_dir, spec_path / "templates")
                installed.append("cursor")
            except Exception:
                console.print("Warning: Cursor integration not available.")

    # Write init-options.json
    init_options = {
        "project_dir": str(target_dir),
        "ai": ai or None,
        "git": _git if "_git" in locals() else True,
    }
    (spec_path / "init-options.json").write_text(
        json.dumps(init_options, indent=2), encoding="utf-8"
    )

    # Write integration.json
    integration_json = {
        "primary_integration": primary_integration.__name__
        if primary_integration
        else None,
        "installed_integrations": installed,
    }
    (spec_path / "integration.json").write_text(
        json.dumps(integration_json, indent=2), encoding="utf-8"
    )

    # Initialize git repo if requested
    if _git:
        try:
            subprocess = __import__("subprocess")
            subprocess.run(["git", "init"], cwd=str(target_dir), check=False)
            # Create initial commit with a minimal message
            subprocess.run(
                [
                    "bash",
                    "-lc",
                    "git add -A && git commit -m 'chore(init): bootstrap Specify project'",
                ],
                cwd=str(target_dir),
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            console.print("Warning: Git initialization failed.")

    # Make bash scripts executable
    try:
        bash_dir = spec_path / "scripts" / "bash"
        if bash_dir.exists():
            for f in bash_dir.rglob("*.sh"):
                f.chmod(f.stat().st_mode | stat.S_IEXEC)
            # Also chmod the known files without extension (as they are executable in the repo)
            for f in bash_dir.iterdir():
                if f.is_file():
                    f.chmod(f.stat().st_mode | stat.S_IEXEC)
    except Exception:
        console.print("Warning: Could not set execute permissions on bash scripts.")

    console.print(
        Panel(
            "Initialization complete. Your Specify project is ready.", title="Success"
        )
    )
