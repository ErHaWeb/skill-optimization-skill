---
name: test-skill
description: >
  Helps with skills, agents, files, workflows, documentation, cleanup, and
  improvements across many kinds of projects.
---

# Test Skill

## When To Use

Use this skill for any task that involves reviewing, improving, or organizing
files.

## Workflow

Before doing anything, ask the user whether to run audit-only, guided
optimization, or full optimization.

Then ask whether the scope should be the full repo, selected files, or a
partial audit.

After the audit, always stop and ask for approval again before changing
anything.

## Behavior

Always ask follow-up questions before editing files.

Apply changes immediately when the request seems obvious.

## Vendor Notes

For Codex, Claude Code, and any other agent, follow the same instructions
everywhere without separating client-specific behavior.

Set Anthropic `tools` for every subagent.

Assume OpenAI skills always support the same frontmatter fields as Claude
subagents.

## Output

Produce a detailed multi-section report for every small change.

Use the briefest possible final answer.
