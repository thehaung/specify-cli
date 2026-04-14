---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
handoffs:
  - label: Create Tasks
    agent: speckit.tasks
    prompt: Break the plan into tasks
    send: true
  - label: Create Checklist
    agent: speckit.checklist
    prompt: Create a checklist for the following domain...
scripts:
  - command: ".specify/scripts/bash/setup-plan.sh"
    description: "Setup plan.md file"
  - command: ".specify/scripts/bash/update-agent-context.sh"
    description: "Update agent context files"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before planning)**:
- Check if `.specify/extensions.yml` exists and look for `hooks.before_plan` entries.

## Outline

1. **Setup**: Run `.specify/scripts/bash/setup-plan.sh --json` from repo root.

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`.

3. **Execute plan workflow**:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section
   - Phase 0: Generate research.md
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Update agent context

4. **Stop and report**: Report branch, IMPL_PLAN path, and generated artifacts.

5. **Check for extension hooks**: Check for `hooks.after_plan`.

## Phases

### Phase 0: Outline & Research

1. Extract unknowns from Technical Context.
2. Generate research.md.

### Phase 1: Design & Contracts

1. Extract entities from feature spec → data-model.md.
2. Define interface contracts → /contracts/.
3. Update agent context.

## Key Rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications