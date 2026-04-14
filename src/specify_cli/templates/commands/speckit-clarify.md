---
description: Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec.
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

**Check for extension hooks (before clarification)**:
- Check if `.specify/extensions.yml` exists and look for `hooks.before_clarify` entries.

## Outline

Goal: Detect and reduce ambiguity in the active feature specification.

1. Run `.specify/scripts/bash/check-prerequisites.sh --json --paths-only`.

2. Load the current spec file and perform structured ambiguity scan.

3. Generate prioritized queue of candidate clarification questions (max 5).

4. Sequential questioning loop (interactive):
   - Present ONE question at a time
   - Use multiple-choice or short-answer format
   - Record answers in working memory

5. Integration after each accepted answer:
   - Maintain spec in memory
   - Create `## Clarifications` section if needed
   - Apply clarifications to appropriate sections

6. Validation after each write.

7. Write updated spec back to FEATURE_SPEC.

8. Report completion with coverage summary.

9. **Check for extension hooks**: Check for `hooks.after_clarify`.

## Behavior Rules

- If no meaningful ambiguities found, respond that no critical ambiguities detected.
- Never exceed 5 total questions.
- Respect user early termination signals.