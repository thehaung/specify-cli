---
description: Generate a custom checklist for the current feature based on user requirements.
handoffs: []
scripts:
  - command: ".specify/scripts/bash/check-prerequisites.sh"
    description: "Check prerequisites and get feature paths"
---

## Checklist Purpose: "Unit Tests for English"

**CRITICAL CONCEPT**: Checklists are **UNIT TESTS FOR REQUIREMENTS WRITING** - they validate the quality, clarity, and completeness of requirements in a given domain.

**NOT for verification/testing**:
- ❌ NOT "Verify the button clicks correctly"
- ❌ NOT "Test error handling works"

**FOR requirements quality validation**:
- ✅ "Are visual hierarchy requirements defined for all card types?"
- ✅ "Is 'prominent display' quantified with specific sizing/positioning?"

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before checklist generation)**:
- Check if `.specify/extensions.yml` exists and look for `hooks.before_checklist` entries.

## Execution Steps

1. **Setup**: Run `.specify/scripts/bash/check-prerequisites.sh --json`.

2. **Clarify intent**: Derive up to THREE initial contextual clarifying questions.

3. **Understand user request**: Combine `$ARGUMENTS` + clarifying answers.

4. **Load feature context**: Read from FEATURE_DIR:
   - spec.md, plan.md (if exists), tasks.md (if exists)

5. **Generate checklist**:
   - Create `FEATURE_DIR/checklists/` directory
   - Generate unique filename (e.g., `ux.md`, `security.md`)
   - Never delete existing content - append new items

6. **Structure Reference**: Use `.specify/templates/checklist-template.md`.

7. **Report**: Output path, item count, and summary.

8. **Check for extension hooks**: Check for `hooks.after_checklist`.

## Item Structure

Each item should follow this pattern:
- Question format asking about requirement quality
- Focus on what's WRITTEN (or not written) in the spec/plan
- Include quality dimension in brackets [Completeness/Clarity/Consistency/etc.]

**PROHIBITED**:
- ❌ Any item starting with "Verify", "Test", "Confirm", "Check"
- ❌ References to code execution or system behavior