---
description: Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation.
handoffs: []
scripts:
  - command: ".specify/scripts/bash/check-prerequisites.sh"
    description: "Check prerequisites (require-tasks mode)"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before analysis)**:
- Check if `.specify/extensions.yml` exists and look for `hooks.before_analyze` entries.

## Goal

Identify inconsistencies, duplications, ambiguities, and underspecified items across the three core artifacts (`spec.md`, `plan.md`, `tasks.md`).

## Operating Constraints

**STRICTLY READ-ONLY**: Do **not** modify any files.

**Constitution Authority**: The project constitution is non-negotiable.

## Execution Steps

### 1. Initialize Analysis Context

Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks`.

Derive absolute paths: SPEC, PLAN, TASKS.

### 2. Load Artifacts

From spec.md: Overview, Functional Requirements, Success Criteria, User Stories, Edge Cases.

From plan.md: Architecture/stack choices, Data Model references, Phases.

From tasks.md: Task IDs, Descriptions, Phase grouping, Parallel markers.

From constitution: Load for principle validation.

### 3. Build Semantic Models

- Requirements inventory
- User story/action inventory
- Task coverage mapping
- Constitution rule set

### 4. Detection Passes

- A. Duplication Detection
- B. Ambiguity Detection
- C. Underspecification
- D. Constitution Alignment
- E. Coverage Gaps
- F. Inconsistency

### 5. Severity Assignment

- **CRITICAL**: Violates constitution MUST, missing core spec artifact
- **HIGH**: Duplicate/conflicting requirement, untestable acceptance criterion
- **MEDIUM**: Terminology drift, missing non-functional task coverage
- **LOW**: Style/wording improvements

### 6. Produce Compact Analysis Report

Output Markdown report with findings table, coverage summary, and metrics.

### 7. Provide Next Actions

### 8. Offer Remediation

Ask user if they'd like concrete remediation edits.

### 9. Check for extension hooks

Check for `hooks.after_analyze`.