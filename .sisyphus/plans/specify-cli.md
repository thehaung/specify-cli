# Specify CLI — Implementation Plan

## TL;DR

> **Quick Summary**: Build a lightweight pip-installable Python CLI with `init` and `check` commands that set up spec-driven development projects with AmazonQ and Cursor AI agent integrations, inspired by spec-kit.
> 
> **Deliverables**:
> - `specify-cli` Python package installable via pip
> - `specify init` command with interactive wizard
> - `specify check` command validating setup health
> - AmazonQ integration (flat .md skills in `.specify/amazonq/skills/`)
> - Cursor integration (folder-based skills in `.cursor/skills/` + rules)
> - Bundled templates and bash scripts
> - pytest test suite
> 
> **Estimated Effort**: Medium
> **Parallel Execution**: YES - 3 waves
> **Critical Path**: Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6 → Task 7 → Task 8 → Task 9

---

## Context

### Original Request
Build a lightweight specify CLI based on github/spec-kit with only `init` and `check` commands, supporting AmazonQ and Cursor, using Python with pip (not uv).

### Interview Summary
**Key Discussions**:
- AmazonQ: IDE extension (VS Code/IntelliJ), simple flat `.md` skill files inside `.specify/amazonq/skills/`
- Cursor: Follow spec-kit's folder-based pattern (`.cursor/skills/<name>/SKILL.md`)
- Architecture: Simplified spec-kit with IntegrationBase + SkillsIntegration pattern
- pip-installable package with interactive wizard for init
- Bash scripts shelled out to (not ported to Python)
- Tests after implementation with pytest

**Research Findings**:
- spec-kit uses Typer + Rich, Python 3.11+, hatchling build system
- spec-kit has 27+ integrations — we only need 2
- AmazonQ CLI is deprecated — we target the IDE extension with simple markdown files
- Cursor uses SkillsIntegration with `.cursor/skills/` and `.cursor/rules/specify-rules.mdc`
- Bash scripts in existing `.specify/scripts/bash/` are well-tested and can be copied directly
- 9 command templates need placeholder substitution during install

### Metis Review
**Identified Gaps** (addressed):
- AmazonQ format: Resolved — IDE extension uses simple markdown, not JSON agent configs
- AmazonQ deprecation: Resolved — targeting IDE extension, not CLI
- Bash scripts: Resolved — shell out, not port
- Class hierarchy: Kept as designed (user approved Approach A) but simplified
- Template substitution: Simple `str.replace()`, not full 8-step pipeline
- Init wizard: Simple `Prompt.ask()`, not arrow-key picker

---

## Work Objectives

### Core Objective
Build a working pip-installable Python CLI that initializes spec-driven development projects with AmazonQ and Cursor integrations, and validates the setup is healthy.

### Concrete Deliverables
- `src/specify_cli/` package with CLI entry point
- `specify init` — interactive wizard creating `.specify/` + agent integration files
- `specify check` — validates tools, config, templates, scripts, and integrations
- Bundled templates (6 markdown + 9 command templates)
- Bundled bash scripts (5 scripts)
- AmazonQ integration module
- Cursor integration module
- pytest test suite
- pyproject.toml with pip-installable config

### Definition of Done
- [ ] `pip install -e . && specify --version` works
- [ ] `specify init --ai amazonq` creates correct `.specify/` structure with AmazonQ skills
- [ ] `specify init --ai cursor` creates correct `.specify/` + `.cursor/` structure
- [ ] `specify init --ai both` creates both integrations
- [ ] `specify check` reports all checks passed after init
- [ ] `specify check` reports failures for missing files
- [ ] `pytest tests/ -v` passes

### Must Have
- pip-installable package (NOT uv)
- Interactive wizard for init
- AmazonQ: flat `.md` files in `.specify/amazonq/skills/`
- Cursor: folder-based `SKILL.md` in `.cursor/skills/` + `.cursor/rules/specify-rules.mdc`
- Manifest tracking with SHA256 hashes
- Both tool availability AND project structure validation in check
- `importlib.resources` for template access (NOT `__file__`)

### Must NOT Have (Guardrails)
- No `uv` support or references
- No extension system
- No preset system
- No agents beyond AmazonQ and Cursor
- No PowerShell scripts
- No porting of bash scripts to Python
- No Jinja2 or `readchar` dependencies
- No silent overwriting of existing `.specify/` directories
- No `__file__` for template access (must use `importlib.resources`)

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** - ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: NO (creating from scratch)
- **Automated tests**: YES (Tests-after)
- **Framework**: pytest
- **If TDD**: N/A — tests after implementation

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **CLI commands**: Use Bash — Run specify commands, assert exit codes and output
- **File structure**: Use Bash — test -d, test -f, ls, cat
- **Python module**: Use Bash — python -c import, run pytest

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — foundation + scaffolding):
├── Task 1: Project scaffolding + pyproject.toml [quick]
├── Task 2: Integration base classes [quick]
└── Task 3: Bundled templates + bash scripts [quick]

Wave 2 (After Wave 1 — core implementation):
├── Task 4: AmazonQ integration module (depends: 2, 3) [unspecified-high]
├── Task 5: Cursor integration module (depends: 2, 3) [unspecified-high]
├── Task 6: `specify init` command (depends: 1, 2, 4, 5) [deep]
└── Task 7: `specify check` command (depends: 1, 2, 4, 5) [unspecified-high]

Wave 3 (After Wave 2 — testing + polish):
├── Task 8: pytest test suite (depends: 6, 7) [unspecified-high]
└── Task 9: README + integration testing (depends: 8) [quick]

Wave FINAL (After ALL tasks):
├── F1: Plan compliance audit (oracle)
├── F2: Code quality review (unspecified-high)
├── F3: Real manual QA (unspecified-high)
└── F4: Scope fidelity check (deep)
```

### Dependency Matrix

| Task | Depends On | Blocks | Wave |
|------|-----------|--------|------|
| 1 | - | 6, 7 | 1 |
| 2 | - | 4, 5, 6, 7 | 1 |
| 3 | - | 4, 5 | 1 |
| 4 | 2, 3 | 6, 7 | 2 |
| 5 | 2, 3 | 6, 7 | 2 |
| 6 | 1, 2, 4, 5 | 8, 9 | 2 |
| 7 | 1, 2, 4, 5 | 8, 9 | 2 |
| 8 | 6, 7 | 9 | 3 |
| 9 | 8 | F1-F4 | 3 |

### Agent Dispatch Summary

- **Wave 1**: **3** — T1 → `quick`, T2 → `quick`, T3 → `quick`
- **Wave 2**: **4** — T4 → `unspecified-high`, T5 → `unspecified-high`, T6 → `deep`, T7 → `unspecified-high`
- **Wave 3**: **2** — T8 → `unspecified-high`, T9 → `quick`
- **FINAL**: **4** — F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high`, F4 → `deep`

---

## TODOs

- [ ] 1. Project Scaffolding + pyproject.toml

  **What to do**:
  - Create `pyproject.toml` with hatchling build system, Python 3.11+, dependencies (typer>=0.9.0, rich), entry point `specify = "specify_cli:main"`, dev dependencies (pytest>=7.0)
  - Create `src/specify_cli/__init__.py` with Typer app and `main()` function (stub — just `specify --version` for now)
  - Create `src/specify_cli/commands/__init__.py` (empty for now)
  - Create `src/specify_cli/integrations/__init__.py` (empty for now)
  - Verify `pip install -e .` works and `specify --version` prints version
  - Add `.gitignore` for Python (dist, __pycache__, *.egg-info, .pytest_cache)

  **Must NOT do**:
  - Do NOT use uv in any config or documentation
  - Do NOT add dependencies beyond typer and rich (plus pytest for dev)
  - Do NOT use `__file__` for any path resolution

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2, 3)
  - **Blocks**: Tasks 6, 7
  - **Blocked By**: None

  **References**:

  **Pattern References**:
  - `src/specify_cli/__init__.py` pattern from spec-kit — uses Typer app with `@app.command()` decorators and `main()` entry

  **External References**:
  - Typer docs: https://typer.tiangolo.com/tutorial/package/ — entry point setup pattern
  - Hatchling: https://hatch.pypa.io/latest/config/build/ — build system configuration

  **Acceptance Criteria**:

  - [ ] `pyproject.toml` exists with correct metadata (name, version, dependencies, entry point)
  - [ ] `src/specify_cli/__init__.py` exists with Typer app and `main()`
  - [ ] `pip install -e .` succeeds without errors
  - [ ] `specify --version` prints `0.1.0`

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Package installs and CLI entry point works
    Tool: Bash
    Preconditions: Python 3.11+ available, virtual environment active
    Steps:
      1. pip install -e .
      2. specify --version
    Expected Result: Output contains "0.1.0"
    Failure Indicators: pip install fails, command not found, version not printed
    Evidence: .sisyphus/evidence/task-1-install-version.txt

  Scenario: No uv references in project
    Tool: Bash
    Preconditions: pyproject.toml created
    Steps:
      1. grep -r "uv" pyproject.toml src/
    Expected Result: No matches found (exit code 1 from grep)
    Failure Indicators: Any match containing "uv" (not part of another word)
    Evidence: .sisyphus/evidence/task-1-no-uv.txt
  ```

  **Commit**: YES
  - Message: `feat(scaffold): initial project structure with pyproject.toml`
  - Files: `pyproject.toml, src/specify_cli/__init__.py, src/specify_cli/commands/__init__.py, src/specify_cli/integrations/__init__.py, .gitignore`

- [ ] 2. Integration Base Classes

  **What to do**:
  - Create `src/specify_cli/integrations/base.py` with:
    - `IntegrationBase(ABC)` — abstract class with `key`, `name`, `requires_cli` attributes and abstract methods: `install(target_dir, templates_dir) -> list[Path]`, `check(target_dir) -> dict`, `get_manifest_path(target_dir) -> Path`
    - `SkillsIntegration(IntegrationBase)` — concrete subclass with `skills_dir`, `file_extension`, `context_file` attributes. Implements `install()` (create skills dir, copy templates with substitution, write manifest with SHA256 hashes), `check()` (verify skills dir, check files, validate manifest), `get_manifest_path()`
    - Shared helper `_compute_sha256(file_path) -> str` for manifest hashing
    - Shared helper `process_template(content, substitutions) -> str` for placeholder replacement using `str.replace()`
  - Update `src/specify_cli/integrations/__init__.py` with `INTEGRATION_REGISTRY` dict (empty for now, populated by amazonq.py and cursor.py)

  **Must NOT do**:
  - Do NOT implement the full spec-kit 8-step template pipeline — use simple `str.replace()` for `{SCRIPT}`, `{ARGS}`, `__AGENT__`
  - Do NOT add Jinja2 or any templating dependency

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3)
  - **Blocks**: Tasks 4, 5, 6, 7
  - **Blocked By**: None

  **References**:

  **Pattern References**:
  - `.specify/integrations/agy.manifest.json` — manifest format with SHA256 file hashes
  - `.specify/integrations/opencode.manifest.json` — another manifest example

  **External References**:
  - `hashlib.sha256` from Python stdlib for hash computation
  - `importlib.resources` for template file access from within package

  **Acceptance Criteria**:

  - [ ] `IntegrationBase` class exists with all abstract methods defined
  - [ ] `SkillsIntegration` implements `install()`, `check()`, `get_manifest_path()`
  - [ ] `process_template()` handles `{SCRIPT}`, `{ARGS}`, `__AGENT__` substitution
  - [ ] `_compute_sha256()` returns correct SHA256 hex digest
  - [ ] `INTEGRATION_REGISTRY` dict exists in `__init__.py`

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: SkillsIntegration.install creates files with manifest
    Tool: Bash
    Preconditions: base.py created, Python 3.11+ available
    Steps:
      1. python -c "from specify_cli.integrations.base import SkillsIntegration, IntegrationBase; print('import OK')"
      2. python -c "from specify_cli.integrations import INTEGRATION_REGISTRY; print(type(INTEGRATION_REGISTRY))"
    Expected Result: "import OK" and "<class 'dict'>"
    Failure Indicators: ImportError, AttributeError
    Evidence: .sisyphus/evidence/task-2-base-classes.txt

  Scenario: process_template handles all placeholders
    Tool: Bash
    Preconditions: base.py created
    Steps:
      1. python -c "from specify_cli.integrations.base import process_template; r = process_template('Hello {SCRIPT} and __AGENT__', {'{SCRIPT}': '.specify/scripts/bash/', '__AGENT__': 'amazonq'}); assert 'amazonq' in r and '.specify/scripts/bash/' in r; print('PASS')"
    Expected Result: "PASS"
    Failure Indicators: AssertionError or ImportError
    Evidence: .sisyphus/evidence/task-2-template-processing.txt
  ```

  **Commit**: YES
  - Message: `feat(core): integration base classes`
  - Files: `src/specify_cli/integrations/base.py, src/specify_cli/integrations/__init__.py`

- [ ] 3. Bundled Templates + Bash Scripts

  **What to do**:
  - Copy the 6 markdown templates from existing `.specify/templates/` into the package at `templates/`:
    - `constitution-template.md`, `spec-template.md`, `plan-template.md`, `tasks-template.md`, `checklist-template.md`, `agent-file-template.md`
  - Copy the 5 bash scripts from existing `.specify/scripts/bash/` into the package at `scripts/bash/`:
    - `common.sh`, `setup-plan.sh`, `check-prerequisites.sh`, `create-new-feature.sh`, `update-agent-context.sh`
  - Add AmazonQ support to `update-agent-context.sh` (add `amazonq` agent type with `AMAZONQ_FILE` path)
  - Create 9 command template files in `templates/commands/`:
    - `speckit-specify.md`, `speckit-plan.md`, `speckit-tasks.md`, `speckit-implement.md`, `speckit-clarify.md`, `speckit-analyze.md`, `speckit-checklist.md`, `speckit-constitution.md`, `speckit-taskstoissues.md`
  - Each command template has YAML frontmatter with `description`, `handoffs`, `scripts` + markdown body with AI agent instructions
  - Model command templates after the existing ones in `.agent/skills/` and `.opencode/command/`
  - Ensure all files are included in the package via `pyproject.toml` `[tool.hatch.build.targets.wheel]` `artifacts` or `shared-data`

  **Must NOT do**:
  - Do NOT modify the logic of the bash scripts — copy verbatim (except adding AmazonQ to update-agent-context.sh)
  - Do NOT port bash scripts to Python
  - Do NOT use `__file__` to locate templates

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2)
  - **Blocks**: Tasks 4, 5
  - **Blocked By**: None

  **References**:

  **Pattern References**:
  - `.specify/templates/` — all 6 template files to copy
  - `.specify/scripts/bash/` — all 5 bash scripts to copy
  - `.agent/skills/speckit-specify/SKILL.md` — example skill command template format (YAML frontmatter + markdown)
  - `.opencode/command/speckit.specify.md` — another command template format example

  **API/Type References**:
  - `.specify/integrations/agy.manifest.json` — shows how manifest tracks files

  **Acceptance Criteria**:

  - [ ] All 6 templates exist in `templates/`
  - [ ] All 5 bash scripts exist in `scripts/bash/`
  - [ ] All 9 command templates exist in `templates/commands/`
  - [ ] `update-agent-context.sh` includes AmazonQ agent type
  - [ ] Files are accessible via `importlib.resources` after pip install

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: All bundled assets exist and are readable
    Tool: Bash
    Preconditions: Templates and scripts copied to package
    Steps:
      1. ls templates/*.md | wc -l
      2. ls scripts/bash/*.sh | wc -l
      3. ls templates/commands/*.md | wc -l
    Expected Result: 6 templates, 5 scripts, 9 command templates
    Failure Indicators: Wrong counts or missing files
    Evidence: .sisyphus/evidence/task-3-assets-exist.txt

  Scenario: update-agent-context.sh includes AmazonQ
    Tool: Bash
    Preconditions: Scripts copied
    Steps:
      1. grep -c "amazonq" scripts/bash/update-agent-context.sh
    Expected Result: At least 1 match
    Failure Indicators: 0 matches — AmazonQ not added
    Evidence: .sisyphus/evidence/task-3-amazonq-in-script.txt
  ```

  **Commit**: YES
  - Message: `feat(assets): bundled templates and bash scripts`
  - Files: `templates/, scripts/, pyproject.toml`

- [ ] 4. AmazonQ Integration Module

  **What to do**:
  - Create `src/specify_cli/integrations/amazonq.py` with `AmazonQIntegration(SkillsIntegration)` class:
    - `key = "amazonq"`, `name = "AmazonQ"`, `requires_cli = False`
    - `skills_dir = ".specify/amazonq/skills"`, `file_extension = ".md"`, `context_file = None`
  - Implement `install()`:
    - Create `.specify/amazonq/skills/` directory
    - Copy each of the 9 command templates from `templates/commands/` → `.specify/amazonq/skills/speckit-<name>.md` (flat naming)
    - Apply `process_template()` substitution for `{SCRIPT}`, `{ARGS}`, `__AGENT__`
    - Write manifest to `.specify/amazonq/manifest.json` with SHA256 hashes
  - Implement `check()`:
    - Verify `.specify/amazonq/skills/` directory exists
    - Check all 9 expected `.md` skill files exist
    - Validate `manifest.json` is parseable JSON with correct structure
  - Register in `INTEGRATION_REGISTRY` in `__init__.py`

  **Must NOT do**:
  - Do NOT create JSON agent configuration files — AmazonQ IDE extension reads simple markdown
  - Do NOT create a CLI check for AmazonQ — it's an IDE extension
  - Do NOT create files outside `.specify/amazonq/`

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 5 — Cursor)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 6, 7
  - **Blocked By**: Tasks 2, 3

  **References**:

  **Pattern References**:
  - `src/specify_cli/integrations/base.py` — SkillsIntegration base class to extend
  - `.specify/integrations/agy.manifest.json` — manifest format to follow
  - `.agent/skills/speckit-specify/SKILL.md` — skill content format reference

  **Acceptance Criteria**:

  - [ ] `AmazonQIntegration` class exists and extends `SkillsIntegration`
  - [ ] `install()` creates 9 `.md` files in target `.specify/amazonq/skills/`
  - [ ] `install()` writes valid `manifest.json` with SHA256 hashes
  - [ ] `check()` correctly reports installed/missing files
  - [ ] `INTEGRATION_REGISTRY["amazonq"]` maps to `AmazonQIntegration`

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: AmazonQ install creates all skill files
    Tool: Bash
    Preconditions: base.py and templates exist, Python 3.11+
    Steps:
      1. python -c "
import tempfile, pathlib
from specify_cli.integrations.amazonq import AmazonQIntegration
from importlib import resources
td = tempfile.mkdtemp()
pkg_templates = resources.files('specify_cli') / 'templates'
inst = AmazonQIntegration()
inst.install(pathlib.Path(td), pkg_templates)
skills = list((pathlib.Path(td) / '.specify/amazonq/skills').glob('*.md'))
print(len(skills))
"
    Expected Result: 9
    Failure Indicators: Any other number, ImportError, FileNotFoundError
    Evidence: .sisyphus/evidence/task-4-amazonq-install.txt

  Scenario: AmazonQ install creates valid manifest
    Tool: Bash
    Preconditions: AmazonQ install completed
    Steps:
      1. python -c "
import tempfile, pathlib, json
from specify_cli.integrations.amazonq import AmazonQIntegration
from importlib import resources
td = tempfile.mkdtemp()
pkg_templates = resources.files('specify_cli') / 'templates'
inst = AmazonQIntegration()
inst.install(pathlib.Path(td), pkg_templates)
manifest = json.loads((pathlib.Path(td) / '.specify/amazonq/manifest.json').read_text())
print(manifest['integration'])
"
    Expected Result: "amazonq"
    Failure Indicators: JSON parse error, missing integration key
    Evidence: .sisyphus/evidence/task-4-amazonq-manifest.txt

  Scenario: AmazonQ check detects missing files
    Tool: Bash
    Preconditions: AmazonQ install completed
    Steps:
      1. python -c "
import tempfile, pathlib
from specify_cli.integrations.amazonq import AmazonQIntegration
from importlib import resources
td = tempfile.mkdtemp()
inst = AmazonQIntegration()
result = inst.check(pathlib.Path(td))
print(result['installed'])
"
    Expected Result: False (no files installed yet)
    Failure Indicators: True (check incorrectly reports installed)
    Evidence: .sisyphus/evidence/task-4-amazonq-check-missing.txt
  ```

  **Commit**: YES
  - Message: `feat(integration): AmazonQ integration module`
  - Files: `src/specify_cli/integrations/amazonq.py, src/specify_cli/integrations/__init__.py`

- [ ] 5. Cursor Integration Module

  **What to do**:
  - Create `src/specify_cli/integrations/cursor.py` with `CursorIntegration(SkillsIntegration)` class:
    - `key = "cursor"`, `name = "Cursor"`, `requires_cli = False`
    - `skills_dir = ".cursor/skills"`, `file_extension = "/SKILL.md"`, `context_file = ".cursor/rules/specify-rules.mdc"`
  - Implement `install()`:
    - Create `.cursor/skills/` directory
    - For each of 9 command templates: create subdirectory `.cursor/skills/speckit-<name>/` and copy template as `SKILL.md`
    - Apply `process_template()` substitution
    - Create `.cursor/rules/specify-rules.mdc` from agent-file-template with YAML frontmatter (`description: "Project Development Guidelines"`, `globs: ["**/*"]`, `alwaysApply: true`)
    - Write manifest to `.specify/integrations/cursor.manifest.json` (following spec-kit pattern) with SHA256 hashes
  - Implement `check()`:
    - Verify `.cursor/skills/` directory exists
    - Check all 9 expected `speckit-<name>/SKILL.md` files exist
    - Verify `.cursor/rules/specify-rules.mdc` exists and has valid frontmatter
    - Validate manifest
  - Register in `INTEGRATION_REGISTRY` in `__init__.py`

  **Must NOT do**:
  - Do NOT forget YAML frontmatter on `.mdc` file — it's required for Cursor auto-include
  - Do NOT create files outside `.cursor/`
  - Do NOT use `readchar` for any interactive logic

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 4 — AmazonQ)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 6, 7
  - **Blocked By**: Tasks 2, 3

  **References**:

  **Pattern References**:
  - `src/specify_cli/integrations/base.py` — SkillsIntegration base class
  - `.specify/integrations/opencode.manifest.json` — manifest format reference
  - `.specify/templates/agent-file-template.md` — template for context/rules file content
  - spec-kit's `CursorAgentIntegration` config: `key="cursor-agent"`, `folder=".cursor/"`, `commands_subdir="skills"`, `extension="/SKILL.md"`, `context_file=".cursor/rules/specify-rules.mdc"`

  **Acceptance Criteria**:

  - [ ] `CursorIntegration` class exists and extends `SkillsIntegration`
  - [ ] `install()` creates 9 `speckit-<name>/SKILL.md` directories in target `.cursor/skills/`
  - [ ] `install()` creates `.cursor/rules/specify-rules.mdc` with valid YAML frontmatter
  - [ ] `install()` writes valid manifest with SHA256 hashes
  - [ ] `check()` correctly reports installed/missing files
  - [ ] `INTEGRATION_REGISTRY["cursor"]` maps to `CursorIntegration`

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Cursor install creates all skill directories with SKILL.md
    Tool: Bash
    Preconditions: base.py and templates exist
    Steps:
      1. python -c "
import tempfile, pathlib
from specify_cli.integrations.cursor import CursorIntegration
from importlib import resources
td = tempfile.mkdtemp()
pkg_templates = resources.files('specify_cli') / 'templates'
inst = CursorIntegration()
inst.install(pathlib.Path(td), pkg_templates)
skills = list((pathlib.Path(td) / '.cursor/skills').glob('*/SKILL.md'))
print(len(skills))
"
    Expected Result: 9
    Failure Indicators: Any other number
    Evidence: .sisyphus/evidence/task-5-cursor-install.txt

  Scenario: Cursor rules MDC file has valid frontmatter
    Tool: Bash
    Preconditions: Cursor install completed
    Steps:
      1. python -c "
import tempfile, pathlib
from specify_cli.integrations.cursor import CursorIntegration
from importlib import resources
td = tempfile.mkdtemp()
pkg_templates = resources.files('specify_cli') / 'templates'
inst = CursorIntegration()
inst.install(pathlib.Path(td), pkg_templates)
content = (pathlib.Path(td) / '.cursor/rules/specify-rules.mdc').read_text()
has_frontmatter = content.startswith('---') and 'alwaysApply' in content
print(has_frontmatter)
"
    Expected Result: True
    Failure Indicators: False — missing frontmatter or alwaysApply key
    Evidence: .sisyphus/evidence/task-5-cursor-mdc-frontmatter.txt

  Scenario: Cursor check detects missing files
    Tool: Bash
    Preconditions: No cursor install done
    Steps:
      1. python -c "
import tempfile, pathlib
from specify_cli.integrations.cursor import CursorIntegration
td = tempfile.mkdtemp()
inst = CursorIntegration()
result = inst.check(pathlib.Path(td))
print(result['installed'])
"
    Expected Result: False
    Failure Indicators: True
    Evidence: .sisyphus/evidence/task-5-cursor-check-missing.txt
  ```

  **Commit**: YES
  - Message: `feat(integration): Cursor integration module`
  - Files: `src/specify_cli/integrations/cursor.py, src/specify_cli/integrations/__init__.py`

- [ ] 6. `specify init` Command

  **What to do**:
  - Create `src/specify_cli/commands/init.py` with the `init` command implementation:
  - Interactive wizard using `typer.prompt()` and Rich `Prompt.ask()`:
    - Project directory (default: current, or `--here` for current)
    - AI assistant choice: AmazonQ / Cursor / Both (use numbered choices, not arrow-key picker)
    - Branch numbering: Sequential / Timestamp
    - Script type: Bash only for v1 (skip prompt, default to bash)
    - Git init: Yes/No (default: Yes)
  - CLI flags: `--here`, `--ai <amazonq|cursor|both>`, `--no-git`
  - When `--ai` flag provided, skip wizard for AI selection
  - Init logic:
    1. Detect/create project directory
    2. Check if `.specify/` already exists — if so, prompt: overwrite/merge/abort (never silently overwrite)
    3. Create `.specify/` directory structure (memory/, scripts/bash/, templates/)
    4. Copy bash scripts from bundled assets to `.specify/scripts/bash/`
    5. Copy core templates from bundled assets to `.specify/templates/`
    6. Initialize `.specify/memory/constitution.md` from constitution template
    7. For each selected AI agent, instantiate from `INTEGRATION_REGISTRY` and call `install()`
    8. Write `.specify/init-options.json` with all wizard choices
    9. Write `.specify/integration.json` with primary integration + `installed_integrations` list
    10. Initialize git repo (unless `--no-git`) and make initial commit
    11. Set execute permissions (`chmod +x`) on bash scripts
  - Use `importlib.resources` to access bundled templates and scripts (NOT `__file__`)
  - Use Rich for formatted output (progress, success messages, file tree display)

  **Must NOT do**:
  - Do NOT silently overwrite existing `.specify/`
  - Do NOT use `__file__` for locating bundled assets
  - Do NOT add `readchar` dependency for arrow-key picker
  - Do NOT support PowerShell in v1

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 7 — check command)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 8, 9
  - **Blocked By**: Tasks 1, 2, 4, 5

  **References**:

  **Pattern References**:
  - `.specify/init-options.json` — format: `{"ai": "opencode", "branch_numbering": "sequential", "here": true, "integration": "opencode", "preset": null, "script": "sh", "speckit_version": "0.5.1.dev0"}`
  - `.specify/integration.json` — format: `{"integration": "opencode", "version": "0.5.1.dev0", "scripts": {"update-context": ".specify/integrations/opencode/scripts/update-context.sh"}}`
  - `src/specify_cli/integrations/base.py` — `SkillsIntegration.install()` signature
  - `src/specify_cli/integrations/__init__.py` — `INTEGRATION_REGISTRY` for looking up integrations

  **API/Type References**:
  - `importlib.resources.files()` — for accessing bundled package data
  - `shutil.copy2()` — for copying files preserving metadata
  - `subprocess.run()` — for git init, chmod

  **Acceptance Criteria**:

  - [ ] `specify init --ai amazonq --here` creates `.specify/` with AmazonQ skills
  - [ ] `specify init --ai cursor --here` creates `.specify/` + `.cursor/` structure
  - [ ] `specify init --ai both --here` creates both integrations
  - [ ] Interactive wizard works when no `--ai` flag provided
  - [ ] Existing `.specify/` is detected and user is prompted
  - [ ] `init-options.json` and `integration.json` are valid JSON
  - [ ] Bash scripts have execute permissions after init
  - [ ] Git repo is initialized (unless `--no-git`)

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Init with AmazonQ creates correct structure
    Tool: Bash
    Preconditions: specify-cli installed via pip install -e .
    Steps:
      1. mkdir /tmp/specify-test-aq && cd /tmp/specify-test-aq && git init
      2. specify init --ai amazonq --here
      3. test -d .specify && echo "PASS: .specify exists"
      4. test -d .specify/amazonq/skills && echo "PASS: amazonq skills dir"
      5. ls .specify/amazonq/skills/*.md | wc -l
      6. test -f .specify/init-options.json && echo "PASS: init-options.json"
      7. test -f .specify/integration.json && echo "PASS: integration.json"
    Expected Result: All PASS, 9 skill files
    Failure Indicators: Any test -d fails, wrong file count
    Evidence: .sisyphus/evidence/task-6-init-amazonq.txt

  Scenario: Init with Cursor creates correct structure
    Tool: Bash
    Preconditions: specify-cli installed
    Steps:
      1. mkdir /tmp/specify-test-cursor && cd /tmp/specify-test-cursor && git init
      2. specify init --ai cursor --here
      3. test -d .cursor/skills && echo "PASS: cursor skills"
      4. ls .cursor/skills/*/SKILL.md | wc -l
      5. test -f .cursor/rules/specify-rules.mdc && echo "PASS: rules file"
      6. head -5 .cursor/rules/specify-rules.mdc | grep -c "alwaysApply"
    Expected Result: All PASS, 9 SKILL.md files, 1 alwaysApply match
    Failure Indicators: Any test fails
    Evidence: .sisyphus/evidence/task-6-init-cursor.txt

  Scenario: Init with both integrations
    Tool: Bash
    Preconditions: specify-cli installed
    Steps:
      1. mkdir /tmp/specify-test-both && cd /tmp/specify-test-both && git init
      2. specify init --ai both --here
      3. test -d .specify/amazonq/skills && echo "PASS: amazonq"
      4. test -d .cursor/skills && echo "PASS: cursor"
    Expected Result: Both PASS
    Failure Indicators: Either directory missing
    Evidence: .sisyphus/evidence/task-6-init-both.txt

  Scenario: Init detects existing .specify directory
    Tool: Bash
    Preconditions: .specify/ already exists in target directory
    Steps:
      1. mkdir /tmp/specify-test-existing && cd /tmp/specify-test-existing && mkdir .specify && git init
      2. specify init --ai amazonq --here 2>&1
    Expected Result: Output contains "already exists" or similar warning, does NOT silently overwrite
    Failure Indicators: Silent overwrite or crash
    Evidence: .sisyphus/evidence/task-6-init-existing.txt

  Scenario: Bash scripts are executable after init
    Tool: Bash
    Preconditions: init completed
    Steps:
      1. cd /tmp/specify-test-aq
      2. test -x .specify/scripts/bash/create-new-feature.sh && echo "PASS: executable"
    Expected Result: PASS
    Failure Indicators: File not executable
    Evidence: .sisyphus/evidence/task-6-init-scripts-exec.txt
  ```

  **Commit**: YES
  - Message: `feat(cmd): specify init command with interactive wizard`
  - Files: `src/specify_cli/commands/init.py, src/specify_cli/__init__.py`

- [ ] 7. `specify check` Command

  **What to do**:
  - Create `src/specify_cli/commands/check.py` with the `check` command implementation:
  - Check categories:
    - **Core tools**: Verify `git` and `python3` are available in PATH (use `shutil.which()`)
    - **Specify config**: Verify `.specify/` exists, `init-options.json` and `integration.json` are valid JSON
    - **Templates**: Verify all 6 template files exist in `.specify/templates/`
    - **Scripts**: Verify all 5 bash scripts exist and are executable in `.specify/scripts/bash/`
    - **Constitution**: Verify `.specify/memory/constitution.md` exists and is non-empty
    - **Integration files**: For each integration in `installed_integrations` from `integration.json`, call integration's `check()` method
  - Find `.specify/` by walking up from CWD (same logic as spec-kit's `find_specify_root()`)
  - CLI flags: `--json` (machine-readable output), `-v/--verbose` (show file paths)
  - Exit codes: 0 (all pass), 1 (some fail), 2 (not in specify project)
  - Use Rich for formatted output with ✓/✗ indicators
  - JSON output format: `{"core_tools": {...}, "config": {...}, "templates": {...}, "scripts": {...}, "constitution": {...}, "integrations": {...}, "all_passed": bool}`

  **Must NOT do**:
  - Do NOT crash if `.specify/` doesn't exist — return exit code 2 with clear message
  - Do NOT check for AmazonQ CLI or Cursor CLI — both are IDE-based (no CLI to check)
  - Do NOT require all integrations to be installed — only check installed ones

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 6 — init command)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 8, 9
  - **Blocked By**: Tasks 1, 2, 4, 5

  **References**:

  **Pattern References**:
  - `src/specify_cli/integrations/base.py` — `IntegrationBase.check()` return format
  - `src/specify_cli/integrations/__init__.py` — `INTEGRATION_REGISTRY` for looking up integrations

  **API/Type References**:
  - `shutil.which()` — for checking tool availability
  - `json.loads()` — for validating JSON config files

  **Acceptance Criteria**:

  - [ ] `specify check` reports ✓ for healthy setup
  - [ ] `specify check` reports ✗ for missing files
  - [ ] `specify check --json` outputs valid JSON
  - [ ] Exit code 0 when all pass, 1 when some fail, 2 when no `.specify/` found
  - [ ] Works from subdirectories (walks up to find `.specify/`)

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Check reports pass on healthy setup
    Tool: Bash
    Preconditions: specify init completed successfully
    Steps:
      1. cd /tmp/specify-test-aq
      2. specify check
      3. echo "Exit code: $?"
    Expected Result: Exit code 0, output contains ✓ marks
    Failure Indicators: Exit code 1 or 2, ✗ marks for installed items
    Evidence: .sisyphus/evidence/task-7-check-pass.txt

  Scenario: Check reports failures for missing files
    Tool: Bash
    Preconditions: Directory with incomplete .specify structure
    Steps:
      1. mkdir /tmp/specify-test-partial && cd /tmp/specify-test-partial && mkdir .specify && git init
      2. specify check
      3. echo "Exit code: $?"
    Expected Result: Exit code 1, output contains ✗ marks
    Failure Indicators: Exit code 0 (false positive)
    Evidence: .sisyphus/evidence/task-7-check-fail.txt

  Scenario: Check returns exit code 2 when not in specify project
    Tool: Bash
    Preconditions: Clean directory with no .specify/
    Steps:
      1. mkdir /tmp/specify-test-empty && cd /tmp/specify-test-empty
      2. specify check 2>&1
      3. echo "Exit code: $?"
    Expected Result: Exit code 2, error message about no .specify/ found
    Failure Indicators: Exit code 0 or 1, or crash
    Evidence: .sisyphus/evidence/task-7-check-no-project.txt

  Scenario: Check --json outputs valid JSON
    Tool: Bash
    Preconditions: Healthy specify project
    Steps:
      1. cd /tmp/specify-test-aq
      2. specify check --json > /tmp/check-output.json
      3. python -c "import json; d=json.load(open('/tmp/check-output.json')); print(d['all_passed'])"
    Expected Result: True
    Failure Indicators: JSON parse error, all_passed is False
    Evidence: .sisyphus/evidence/task-7-check-json.txt
  ```

  **Commit**: YES
  - Message: `feat(cmd): specify check command with validation`
  - Files: `src/specify_cli/commands/check.py, src/specify_cli/__init__.py`

- [ ] 8. pytest Test Suite

  **What to do**:
  - Create `tests/test_init.py`:
    - `test_init_creates_specify_dir` — init creates `.specify/` structure
    - `test_init_amazonq_creates_skills` — init with `--ai amazonq` creates 9 skill files
    - `test_init_cursor_creates_skills` — init with `--ai cursor` creates 9 SKILL.md dirs + rules
    - `test_init_both_integrations` — init with `--ai both` creates both
    - `test_init_detects_existing_specify` — init prompts when `.specify/` exists
    - `test_init_options_json_valid` — `init-options.json` is valid JSON with expected keys
    - `test_init_integration_json_valid` — `integration.json` is valid JSON
    - `test_init_scripts_executable` — bash scripts have +x permission
    - `test_init_git_repo_created` — git repo initialized (unless `--no-git`)
  - Create `tests/test_check.py`:
    - `test_check_passes_on_healthy_setup` — returns exit 0
    - `test_check_fails_on_missing_files` — returns exit 1
    - `test_check_returns_2_without_specify` — returns exit 2
    - `test_check_json_output` — `--json` produces valid JSON
    - `test_check_integration_health` — integration check method works
  - Create `tests/conftest.py` with fixtures:
    - `tmp_project_dir` — creates temp dir with git init
    - `initialized_project` — runs init on temp dir and returns path
  - Use `tmp_path` pytest fixture for isolation
  - All tests must clean up temp directories

  **Must NOT do**:
  - Do NOT write tests that depend on the current workspace's `.specify/`
  - Do NOT use `__file__` in test code
  - Do NOT make tests that require manual cleanup

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (sequential after Tasks 6, 7)
  - **Blocks**: Task 9
  - **Blocked By**: Tasks 6, 7

  **References**:

  **Pattern References**:
  - `src/specify_cli/commands/init.py` — init command to test
  - `src/specify_cli/commands/check.py` — check command to test
  - `src/specify_cli/integrations/amazonq.py` — AmazonQ integration to test
  - `src/specify_cli/integrations/cursor.py` — Cursor integration to test

  **Acceptance Criteria**:

  - [ ] `pytest tests/ -v` passes with all tests green
  - [ ] At least 14 test functions (9 for init, 5 for check)
  - [ ] No tests depend on external state

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: All pytest tests pass
    Tool: Bash
    Preconditions: All implementation tasks complete
    Steps:
      1. pytest tests/ -v
    Expected Result: All tests pass, 0 failures
    Failure Indicators: Any test failure
    Evidence: .sisyphus/evidence/task-8-pytest-results.txt

  Scenario: Tests are isolated (no side effects)
    Tool: Bash
    Preconditions: Tests have been run
    Steps:
      1. pytest tests/ -v
      2. pytest tests/ -v  # Run twice
    Expected Result: Both runs produce identical results
    Failure Indicators: Different results between runs
    Evidence: .sisyphus/evidence/task-8-test-isolation.txt
  ```

  **Commit**: YES
  - Message: `test: pytest test suite for init and check`
  - Files: `tests/test_init.py, tests/test_check.py, tests/conftest.py`

- [ ] 9. README + Integration Testing

  **What to do**:
  - Create `README.md` with:
    - Project description and motivation
    - Installation: `pip install specify-cli` (or `pip install -e .` for dev)
    - Usage: `specify init`, `specify check` with examples
    - Supported integrations: AmazonQ, Cursor
    - Development setup instructions
  - Run full end-to-end integration test:
    - Install from clean: `pip install -e .`
    - Init with AmazonQ: verify `.specify/` + skills
    - Init with Cursor: verify `.specify/` + `.cursor/`
    - Init with both: verify both structures
    - Run `specify check` after each init
    - Verify `specify check --json` output
  - Fix any issues found during integration testing

  **Must NOT do**:
  - Do NOT add `uv` to installation instructions
  - Do NOT document features that don't exist yet

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (after Task 8)
  - **Blocks**: F1-F4
  - **Blocked By**: Task 8

  **References**:

  **Pattern References**:
  - `src/specify_cli/__init__.py` — main CLI entry point
  - `pyproject.toml` — installation instructions

  **Acceptance Criteria**:

  - [ ] `README.md` exists with installation and usage instructions
  - [ ] Full end-to-end flow works: install → init → check
  - [ ] No `uv` references in README or docs

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Full end-to-end flow works
    Tool: Bash
    Preconditions: All code complete, pip install -e . successful
    Steps:
      1. pip install -e .
      2. mkdir /tmp/e2e-test && cd /tmp/e2e-test && git init
      3. specify init --ai both --here
      4. specify check
      5. echo "Exit: $?"
    Expected Result: Exit code 0, all checks pass
    Failure Indicators: Any step fails
    Evidence: .sisyphus/evidence/task-9-e2e-flow.txt

  Scenario: README has no uv references
    Tool: Bash
    Preconditions: README.md created
    Steps:
      1. grep -i "\\buv\\b" README.md
    Expected Result: No matches (exit code 1 from grep)
    Failure Indicators: Any match for standalone "uv"
    Evidence: .sisyphus/evidence/task-9-no-uv-readme.txt
  ```

  **Commit**: YES
  - Message: `docs: README and integration testing`
  - Files: `README.md`

---

## Final Verification Wave

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, run command). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in .sisyphus/evidence/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Run `pip install -e . && specify --version`. Run pytest. Review all Python files for: `__file__` usage (FORBIDDEN — must use importlib.resources), `as any`, empty catches, print() instead of Rich, commented-out code, unused imports. Check AI slop: excessive comments, over-abstraction, generic names.
  Output: `Build [PASS/FAIL] | Tests [N pass/N fail] | Files [N clean/N issues] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high`
  Start from clean state. Execute EVERY QA scenario from EVERY task. Test cross-task integration: init with both agents, then check. Test edge cases: existing `.specify/`, missing python, invalid flags. Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff. Verify 1:1 — everything in spec was built, nothing beyond spec was built. Check "Must NOT do" compliance. Detect cross-task contamination. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

- **1**: `feat(scaffold): initial project structure with pyproject.toml` - pyproject.toml, src/specify_cli/__init__.py, src/specify_cli/commands/__init__.py
- **2**: `feat(core): integration base classes` - src/specify_cli/integrations/base.py, src/specify_cli/integrations/__init__.py
- **3**: `feat(assets): bundled templates and bash scripts` - templates/, scripts/
- **4**: `feat(integration): AmazonQ integration module` - src/specify_cli/integrations/amazonq.py
- **5**: `feat(integration): Cursor integration module` - src/specify_cli/integrations/cursor.py
- **6**: `feat(cmd): specify init command with interactive wizard` - src/specify_cli/commands/init.py, src/specify_cli/__init__.py
- **7**: `feat(cmd): specify check command with validation` - src/specify_cli/commands/check.py
- **8**: `test: pytest test suite for init and check` - tests/
- **9**: `docs: README and integration testing` - README.md

---

## Success Criteria

### Verification Commands
```bash
pip install -e . && specify --version                    # Expected: 0.1.0
specify init --ai amazonq --here                         # Expected: creates .specify/ + amazonq skills
specify check                                            # Expected: all checks pass, exit 0
specify check --json                                     # Expected: valid JSON output
pytest tests/ -v                                         # Expected: all tests pass
python -c "from importlib import resources; print(resources.files('specify_cli') / 'templates')"  # Expected: template path
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] All tests pass
- [ ] No `__file__` usage in Python code
- [ ] No `uv` references anywhere
- [ ] `specify init` + `specify check` work end-to-end
