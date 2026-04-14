---
description: Convert existing tasks into actionable, dependency-ordered GitHub issues for the feature based on available design artifacts.
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

**Check for extension hooks (before tasks-to-issues conversion)**:
- Check if `.specify/extensions.yml` exists and look for `hooks.before_taskstoissues` entries.

## Outline

1. Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks`.

2. Get the Git remote:
   ```bash
   git config --get remote.origin.url
   ```

   > [!CAUTION]
   > ONLY PROCEED IF THE REMOTE IS A GITHUB URL

3. For each task, use the GitHub MCP server to create an issue.

   > [!CAUTION]
   > UNDER NO CIRCUMSTANCES EVER CREATE ISSUES IN REPOSITORIES THAT DO NOT MATCH THE REMOTE URL

4. **Check for extension hooks**: Check for `hooks.after_taskstoissues`.

## Important Notes

- Tasks are converted to GitHub issues in the repository matching the git remote
- Each issue should represent one task from tasks.md
- Issues should maintain dependency ordering
- Labels can be used to indicate task phase (Setup, Foundational, US1, US2, etc.)