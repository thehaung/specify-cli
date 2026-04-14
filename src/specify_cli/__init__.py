"""Specify CLI - Command-line interface for Specify."""

from typing import Optional

import typer
from rich.console import Console

app = typer.Typer(help="Specify CLI")
console = Console()

# Import check command and register it
from specify_cli.commands.check import check as check_command

app.command()(check_command)

# Import init command and register it
try:
    from specify_cli.commands.init import init as init_command

    app.command()(init_command)
except ImportError as e:
    console.print(f"[yellow]Warning: init command unavailable: {e}[/yellow]")


@app.command()
def version():
    """Print version information."""
    console.print("0.1.0")


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
