---
description: Execute the implementation plan by processing and executing all tasks defined in tasks.md
handoffs: []
scripts:
  - command: ".specify/scripts/bash/check-prerequisites.sh"
    description: "Check prerequisites for implementation"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before implementation)**:
- Check if `.specify/extensions.yml` exists and look for `hooks.before_implement` entries.

## Outline

1. Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks`.

2. **Check checklists status** (if FEATURE_DIR/checklists/ exists):
   - Count total, completed, and incomplete items per checklist
   - If any checklist is incomplete, ask user if they want to proceed

3. Load implementation context:
   - **REQUIRED**: tasks.md, plan.md
   - **IF EXISTS**: data-model.md, contracts/, research.md, quickstart.md

4. **Project Setup Verification**: Create/verify ignore files.

5. Parse tasks.md structure and extract phases, dependencies, and task details.

6. Execute implementation following the task plan phase-by-phase.

7. Progress tracking: Mark completed tasks as [X].

8. Completion validation: Verify all tasks complete.

9. **Check for extension hooks**: Check for `hooks.after_implement`.

## Key Rules

- Setup first
- Tests before code (if TDD approach)
- Respect dependencies
- Validation checkpoints per phase