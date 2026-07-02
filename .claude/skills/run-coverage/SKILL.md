---
name: run-coverage
description: Run test coverage and summarize uncovered code.
allowed-tools:
  - Read
  - Bash
argument-hint: "/run-coverage"
---

# Run Coverage Skill

## Purpose

Run the project's test coverage and identify files or functions that are not adequately tested.

## Steps

1. Read the project structure.
2. Run the project's coverage command.
3. Identify files with low coverage.
4. Summarize uncovered code.
5. Recommend additional tests.

## Output

Return:

- Coverage percentage
- Files with low coverage
- Missing test scenarios
- Suggestions for improving coverage