---
name: check-types
description: Run static type checking.
context: repository
allowed-tools:
  - Read
  - Bash
argument-hint: "[optional path]"
---

# Type Checking

## Purpose

Run static type checking on the project and report any type errors.

## Steps

1. Read the project.
2. Run the type checker.
3. Collect type errors.
4. Summarize affected files.
5. Suggest fixes.

## Output

Return:

- Files with type errors
- Number of type errors
- Suggested corrections