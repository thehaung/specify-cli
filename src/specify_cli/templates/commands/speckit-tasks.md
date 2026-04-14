---
description: Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.
handoffs: []
scripts:
  - command: ".specify/scripts/bash/check-prerequisites.sh"
    description: "Check prerequisites and get feature paths"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before tasks generation)**:
- Check if `.specify/extensions.yml` exists and look for `hooks.before_tasks` entries.

## Outline

1. **Setup**: Run `.specify/scripts/bash/check-prerequisites.sh --json` from repo root.

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md, spec.md
   - **Optional**: data-model.md, contracts/, research.md, quickstart.md

3. **Execute task generation workflow**:
   - Extract tech stack and user stories
   - Map entities and contracts to user stories
   - Generate tasks organized by user story
   - Create dependency graph

4. **Generate tasks.md**: Use `.specify/templates/tasks-template.md` as structure.

5. **Report**: Output path, task counts, and parallel opportunities.

6. **Check for extension hooks**: Check for `hooks.after_tasks`.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story.

- **Phase 1**: Setup (project initialization)
- **Phase 2**: Foundational (blocking prerequisites)
- **Phase 3+**: User Stories in priority order
- **Final Phase**: Polish & Cross-Cutting Concerns

Every task MUST follow the format: `- [ ] [TaskID] [P?] [Story?] Description with file path`