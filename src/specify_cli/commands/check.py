"""Check command for validating Specify setup health."""

import json
import shutil
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

app = typer.Typer(help="Check Specify setup health")
console = Console()

# Expected template files
EXPECTED_TEMPLATES = [
    "agent-file-template.md",
    "checklist-template.md",
    "constitution-template.md",
    "plan-template.md",
    "spec-template.md",
    "tasks-template.md",
]

# Expected bash scripts
EXPECTED_SCRIPTS = [
    "check-prerequisites.sh",
    "common.sh",
    "create-new-feature.sh",
    "setup-plan.sh",
    "update-agent-context.sh",
]


def find_specify_root(start_path: Optional[Path] = None) -> Optional[Path]:
    """Find .specify/ directory by walking up from CWD.

    Args:
        start_path: Path to start searching from. Defaults to CWD.

    Returns:
        Path to .specify/ directory if found, None otherwise.
    """
    if start_path is None:
        start_path = Path.cwd()

    current = start_path.resolve()

    while True:
        specify_dir = current / ".specify"
        if specify_dir.exists() and specify_dir.is_dir():
            return specify_dir

        # Stop at filesystem root
        parent = current.parent
        if parent == current:
            return None
        current = parent


def check_core_tools() -> dict:
    """Check if core tools are available in PATH.

    Returns:
        Dict with check results.
    """
    git_available = shutil.which("git") is not None
    python_available = shutil.which("python3") is not None

    return {
        "passed": git_available and python_available,
        "git": {"available": git_available, "path": shutil.which("git")},
        "python3": {"available": python_available, "path": shutil.which("python3")},
    }


def check_config(specify_dir: Path) -> dict:
    """Check Specify configuration files.

    Args:
        specify_dir: Path to .specify/ directory.

    Returns:
        Dict with check results.
    """
    results = {
        "passed": True,
        "init_options": {
            "exists": False,
            "valid": False,
            "path": str(specify_dir / "init-options.json"),
        },
        "integration": {
            "exists": False,
            "valid": False,
            "path": str(specify_dir / "integration.json"),
        },
    }

    # Check init-options.json
    init_options_path = specify_dir / "init-options.json"
    if init_options_path.exists():
        results["init_options"]["exists"] = True
        try:
            json.loads(init_options_path.read_text(encoding="utf-8"))
            results["init_options"]["valid"] = True
        except json.JSONDecodeError:
            results["passed"] = False
    else:
        results["passed"] = False

    # Check integration.json
    integration_path = specify_dir / "integration.json"
    if integration_path.exists():
        results["integration"]["exists"] = True
        try:
            json.loads(integration_path.read_text(encoding="utf-8"))
            results["integration"]["valid"] = True
        except json.JSONDecodeError:
            results["passed"] = False
    else:
        results["passed"] = False

    return results


def check_templates(specify_dir: Path) -> dict:
    """Check if all template files exist.

    Args:
        specify_dir: Path to .specify/ directory.

    Returns:
        Dict with check results.
    """
    templates_dir = specify_dir / "templates"
    files_found = []
    files_missing = []

    for template_file in EXPECTED_TEMPLATES:
        template_path = templates_dir / template_file
        if template_path.exists():
            files_found.append(template_file)
        else:
            files_missing.append(template_file)

    return {
        "passed": len(files_missing) == 0,
        "found": files_found,
        "missing": files_missing,
        "path": str(templates_dir),
    }


def check_scripts(specify_dir: Path) -> dict:
    """Check if all bash scripts exist and are executable.

    Args:
        specify_dir: Path to .specify/ directory.

    Returns:
        Dict with check results.
    """
    scripts_dir = specify_dir / "scripts" / "bash"
    files_ok = []
    files_missing = []
    files_not_executable = []

    for script_file in EXPECTED_SCRIPTS:
        script_path = scripts_dir / script_file
        if not script_path.exists():
            files_missing.append(script_file)
        elif not script_path.stat().st_mode & 0o111:  # Check executable bit
            files_not_executable.append(script_file)
        else:
            files_ok.append(script_file)

    return {
        "passed": len(files_missing) == 0 and len(files_not_executable) == 0,
        "ok": files_ok,
        "missing": files_missing,
        "not_executable": files_not_executable,
        "path": str(scripts_dir),
    }


def check_constitution(specify_dir: Path) -> dict:
    """Check if constitution file exists and is non-empty.

    Args:
        specify_dir: Path to .specify/ directory.

    Returns:
        Dict with check results.
    """
    constitution_path = specify_dir / "memory" / "constitution.md"

    if not constitution_path.exists():
        return {
            "passed": False,
            "exists": False,
            "empty": True,
            "path": str(constitution_path),
        }

    content = constitution_path.read_text(encoding="utf-8")
    is_empty = len(content.strip()) == 0

    return {
        "passed": not is_empty,
        "exists": True,
        "empty": is_empty,
        "path": str(constitution_path),
    }


def check_integrations(specify_dir: Path) -> dict:
    """Check all installed integrations.

    Args:
        specify_dir: Path to .specify/ directory.

    Returns:
        Dict with check results.
    """
    integrations_dir = specify_dir / "integrations"
    results = {
        "passed": True,
        "integrations": {},
        "path": str(integrations_dir),
    }

    if not integrations_dir.exists():
        return results

    # Find all manifest files
    for manifest_file in integrations_dir.glob("*.manifest.json"):
        integration_name = manifest_file.stem.replace(".manifest", "")

        try:
            manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
            files_status = {}
            all_files_ok = True

            # Check each file in the manifest
            # Handle both dict format {"path": "hash"} and list format [{"path": "", "sha256": ""}]
            files_data = manifest.get("files", {})
            if isinstance(files_data, dict):
                # Dict format: keys are paths, values are hashes
                for file_path, expected_hash in files_data.items():
                    full_path = specify_dir.parent / file_path
                    exists = full_path.exists()
                    files_status[file_path] = {"exists": exists}
                    if not exists:
                        all_files_ok = False
            elif isinstance(files_data, list):
                # List format: each item has "path" and "sha256" keys
                for file_entry in files_data:
                    if isinstance(file_entry, dict):
                        file_path = file_entry.get("path", "")
                        expected_hash = file_entry.get("sha256", "")
                        full_path = specify_dir.parent / file_path
                        exists = full_path.exists()
                        files_status[file_path] = {"exists": exists}
                        if not exists:
                            all_files_ok = False

            integration_passed = all_files_ok
            results["integrations"][integration_name] = {
                "passed": integration_passed,
                "version": manifest.get("version", "unknown"),
                "files": files_status,
            }

            if not integration_passed:
                results["passed"] = False

        except (json.JSONDecodeError, KeyError) as e:
            results["integrations"][integration_name] = {
                "passed": False,
                "error": str(e),
            }
            results["passed"] = False

    return results


def format_check_result(name: str, result: dict, verbose: bool = False) -> Text:
    """Format a single check result for display.

    Args:
        name: Name of the check.
        result: Check result dict with 'passed' key.
        verbose: Whether to show verbose output.

    Returns:
        Rich Text object.
    """
    passed = result.get("passed", False)
    symbol = "✓" if passed else "✗"
    color = "green" if passed else "red"

    text = Text()
    text.append(f"{symbol} ", style=color)
    text.append(name, style="bold")

    if verbose:
        if "path" in result:
            text.append(f"\n    Path: {result['path']}", style="dim")
        if "missing" in result and result["missing"]:
            text.append(f"\n    Missing: {', '.join(result['missing'])}", style="red")
        if "not_executable" in result and result["not_executable"]:
            text.append(
                f"\n    Not executable: {', '.join(result['not_executable'])}",
                style="yellow",
            )
        if "integrations" in result and verbose:
            for integration_name, integration_result in result["integrations"].items():
                status = "✓" if integration_result.get("passed") else "✗"
                style = "green" if integration_result.get("passed") else "red"
                text.append(f"\n    {status} {integration_name}", style=style)

    return text


@app.command()
def check(
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(
        False, "-v", "--verbose", help="Show detailed information"
    ),
):
    """Check Specify setup health."""
    # Find .specify/ directory
    specify_dir = find_specify_root()

    if specify_dir is None:
        if json_output:
            output = {
                "error": "Not in a Specify project",
                "all_passed": False,
            }
            console.print(json.dumps(output, indent=2))
        else:
            console.print("[red]✗ Not in a Specify project[/red]")
            console.print(
                "[dim]Could not find .specify/ directory. Run 'specify init' first.[/dim]"
            )
        sys.exit(2)

    # Run all checks
    results = {
        "core_tools": check_core_tools(),
        "config": check_config(specify_dir),
        "templates": check_templates(specify_dir),
        "scripts": check_scripts(specify_dir),
        "constitution": check_constitution(specify_dir),
        "integrations": check_integrations(specify_dir),
    }

    # Determine overall status
    all_passed = all(result.get("passed", False) for result in results.values())
    results["all_passed"] = all_passed

    if json_output:
        # JSON output
        json_results = {
            "core_tools": results["core_tools"],
            "config": results["config"],
            "templates": results["templates"],
            "scripts": results["scripts"],
            "constitution": results["constitution"],
            "integrations": results["integrations"],
            "all_passed": all_passed,
        }
        console.print(json.dumps(json_results, indent=2))
    else:
        # Rich formatted output
        table = Table(title="Specify Setup Health Check", show_header=False, box=None)
        table.add_column("Check", style="bold")
        table.add_column("Status")

        # Core Tools
        core_tools_text = format_check_result(
            "Core Tools", results["core_tools"], verbose
        )
        if verbose and results["core_tools"]["passed"]:
            core_tools_text.append(
                f"\n    git: {results['core_tools']['git']['path']}", style="dim"
            )
            core_tools_text.append(
                f"\n    python3: {results['core_tools']['python3']['path']}",
                style="dim",
            )
        table.add_row("Core Tools", core_tools_text)

        # Config
        config_text = format_check_result("Configuration", results["config"], verbose)
        table.add_row("Configuration", config_text)

        # Templates
        templates_text = format_check_result("Templates", results["templates"], verbose)
        if verbose and results["templates"]["passed"]:
            templates_text.append(
                f"\n    Found: {len(results['templates']['found'])} files", style="dim"
            )
        table.add_row("Templates", templates_text)

        # Scripts
        scripts_text = format_check_result("Scripts", results["scripts"], verbose)
        if verbose and results["scripts"]["passed"]:
            scripts_text.append(
                f"\n    OK: {len(results['scripts']['ok'])} files", style="dim"
            )
        table.add_row("Scripts", scripts_text)

        # Constitution
        constitution_text = format_check_result(
            "Constitution", results["constitution"], verbose
        )
        table.add_row("Constitution", constitution_text)

        # Integrations
        integrations_text = format_check_result(
            "Integrations", results["integrations"], verbose
        )
        table.add_row("Integrations", integrations_text)

        # Overall status
        console.print()
        console.print(table)
        console.print()

        if all_passed:
            console.print(
                Panel("[green]✓ All checks passed![/green]", border_style="green")
            )
        else:
            failed_checks = [
                name
                for name, result in results.items()
                if name != "all_passed" and not result.get("passed", False)
            ]
            console.print(
                Panel(
                    f"[red]✗ Some checks failed: {', '.join(failed_checks)}[/red]",
                    border_style="red",
                )
            )
        console.print()

    sys.exit(0 if all_passed else 1)
