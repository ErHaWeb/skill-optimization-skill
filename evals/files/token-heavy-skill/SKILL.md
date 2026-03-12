---
name: token-heavy-skill
description: >
  Improve writing, workflow, and documentation skills across many use cases.
---

# Token Heavy Skill

## Use This Skill When

- The user wants to improve an existing editorial or reporting skill.

## Defaults

- Always read `SKILL.md`, `README.md`, `references/process-notes.md`,
  `references/examples.md`, and `evals/evals.json` before deciding whether
  they matter.
- Repeat the core operating rules in the final report so later runs can reuse
  the response as documentation.
- Produce a comprehensive multi-section answer even for a one-line fix.

## Workflow

1. Read every support file before identifying the actual issue.
2. Summarize each file separately before proposing changes.
3. Ask whether the user prefers brief, medium, or full optimization unless they
   explicitly requested token reduction.
4. Stop after the audit and ask for approval before changing anything.

## Quality

- Keep activation narrow.
- Keep the scope inside the target skill.
- Keep evals aligned when behavior changes.

## Output

- Include a long per-section recap of unchanged guidance.
