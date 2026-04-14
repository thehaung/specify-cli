---
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
handoffs: []
scripts:
  - command: ".specify/scripts/bash/check-prerequisites.sh"
    description: "Get feature paths (--paths-only mode)"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before constitution update)**:
- Check if `.specify/extensions.yml` exists and look for `hooks.before_constitution` entries.

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`.

1. Load the existing constitution.
2. Collect/derive values for placeholders.
3. Draft updated constitution content.
4. Consistency propagation checklist:
   - Update plan-template.md if needed
   - Update spec-template.md if needed
   - Update tasks-template.md if needed
   - Update command files
5. Produce Sync Impact Report.
6. Validation before final output.
7. Write completed constitution.
8. Output final summary.

9. **Check for extension hooks**: Check for `hooks.after_constitution`.

## Formatting & Style Requirements

- Use Markdown headings exactly as in the template.
- Wrap long rationale lines (<100 chars).
- Keep single blank line between sections.
- Avoid trailing whitespace.

## Version Bump Rules

- **MAJOR**: Backward incompatible governance/principle removals.
- **MINOR**: New principle/section added or materially expanded.
- **PATCH**: Clarifications, wording, typo fixes.