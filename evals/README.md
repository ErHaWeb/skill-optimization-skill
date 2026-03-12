# Skill Optimization Eval Scenarios

These evals defend the core behavior of `skill-optimization`.

They cover:

- activation and scope boundaries
- smallest-useful edit behavior
- target-only change discipline
- generic QA baseline checks
- loop termination when only cosmetic changes remain
- agent metadata drift and local tool-artifact hygiene

Use the smallest set of scenarios that matches the behavior you changed.

When QA guidance changes, prefer scenarios that exercise:

- missing `.gitignore` or local hygiene coverage
- missing or weak machine-checkable QA contracts
- support files that are present but not linked from `SKILL.md`
- overly broad `.idea` inspection suppression
- stale `agents/openai.yaml` metadata after trigger-surface changes
- unignored local worktree mirrors such as `/.claude/worktrees/`
- missing Git context
- justified no-op after a re-review pass
