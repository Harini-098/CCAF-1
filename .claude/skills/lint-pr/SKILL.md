---
name: lint-pr
description: Run lint checks before creating a pull request.
context: repository
allowed-tools:
  - Read
  - Bash
argument-hint: "[optional path]"
---

# Lint PR

## Purpose

Check the project for linting issues before creating a pull request.

## Steps

1. Read the project files.
2. Run the project's lint command.
3. Collect lint errors and warnings.
4. Summarize the issues.
5. Suggest fixes.

## Output

Return:

- Total lint errors
- Total warnings
- Files affected
- Suggestions for fixing issues