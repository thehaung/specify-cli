# Specify CLI

A command-line tool for bootstrapping and managing development workflows with AI-powered integrations.

## Overview

Specify CLI helps teams establish consistent development practices by providing:

- **Project initialization** with bundled templates and scripts
- **AI integration** support for Amazon Q and Cursor
- **Health checks** to verify your setup is properly configured
- **Constitution-based workflows** for project governance

## Installation

### From PyPI

```bash
pip install specify-cli
```

### Development Installation

#### Option 1: Using the bin/ folder (Recommended for development)

```bash
git clone https://github.com/your-org/specify.git
cd specify
# Add to PATH temporarily
export PATH="$PWD/bin:$PATH"
# Or create a symlink
ln -s "$PWD/bin/specify-cli" /usr/local/bin/specify-cli
```

#### Option 2: Using pip

```bash
git clone https://github.com/your-org/specify.git
cd specify
pip install -e .
```

## Usage

### Initialize a Project

Create a new Specify project in your current directory:

```bash
specify-cli init --ai amazonq --here
```

Or initialize with both Amazon Q and Cursor integrations:

```bash
specify-cli init --ai both --here
```

For interactive mode (prompts for all options):

```bash
specify-cli init
```

Options:
- `--ai {amazonq,cursor,both}` - AI integration to install
- `--here` - Use current directory as project directory
- `--no-git` - Skip git initialization

### Check Setup Health

Verify your Specify project is properly configured:

```bash
specify-cli check
```

For detailed output:

```bash
specify-cli check --verbose
```

For JSON output (useful for CI/CD):

```bash
specify-cli check --json
```

## Supported Integrations

### Amazon Q

Amazon Q integration installs skills into `.amazonq/skills/` with manifest tracking at `.specify/integrations/amazonq.manifest.json`.

```bash
specify-cli init --ai amazonq --here
```

### Cursor

Cursor integration installs skills into `.cursor/skills/` with context rules in `.cursor/rules/`.

```bash
specify-cli init --ai cursor --here
```

### Both Integrations

Install both Amazon Q and Cursor integrations:

```bash
specify-cli init --ai both --here
```

## Project Structure

After initialization, your project will include:

```
.specify/
├── memory/
│   └── constitution.md      # Project governance document
├── scripts/
│   └── bash/                 # Development automation scripts
├── templates/               # Workflow templates
├── init-options.json        # Initialization configuration
└── integration.json         # Installed AI integrations
```

For Cursor integration only:

```
.cursor/
├── skills/                   # Cursor skill definitions
└── rules/
    └── specify-rules.mdc    # Project context rules
```

For Amazon Q integration only:

```
.amazonq/
└── skills/                   # Amazon Q skill definitions
```

Integration manifests are stored at `.specify/integrations/`.

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Requirements

- Python 3.11+
- typer >= 0.9.0
- rich >= 13.0.0

## License

MIT

Verification Scaffolding (New)
- A lightweight verification framework scaffold has been added to the repository under .specify/verification.
- It includes plans, checks, and templates to bootstrap automated verification workflows.
- You can initialize the scaffold in a project directory to start a minimal verification workflow:
- Example: python3 -c 'from specify_cli.verification.runner import init_run; init_run(Path(".").resolve())'
