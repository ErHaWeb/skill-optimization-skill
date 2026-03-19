# Skill Optimization Eval Scenarios

These evals defend the core behavior of `skill-optimization`.

They cover:

- activation and scope boundaries
- context-footprint reduction without behavioral drift
- smallest-useful edit behavior
- target-only change discipline
- generic QA baseline checks
- vendor-specific alignment to official Anthropic/OpenAI rules
- loop termination when only cosmetic changes remain
- self-critical hardening of vague recurring optimization heuristics
- agent metadata drift and local tool-artifact hygiene
- script-first replacement of deterministic prompt-only workflows when a local
  helper can own the mechanics
- deterministic inventory of local QA/support-file gaps before deeper manual
  review

Use the smallest set of scenarios that matches the behavior you changed.

When QA guidance changes, prefer scenarios that exercise:

- missing `.gitignore` or local hygiene coverage
- missing or weak machine-checkable QA contracts
- token-heavy `SKILL.md` files with mandatory broad reads or verbose defaults
- support files that are present but not linked from `SKILL.md`
- vendor guidance that conflicts with official Anthropic/OpenAI docs
- overly broad `.idea` inspection suppression
- stale `agents/openai.yaml` metadata after trigger-surface changes
- Claude Code subagent scope or frontmatter drift
- unignored local worktree mirrors such as `/.claude/worktrees/`
- repeatable normalization, rendering, validation, or report assembly that a
  target-local script should own instead of the model
- local skill directories where deterministic surface audit should replace ad
  hoc structural scanning
- missing Git context
- justified no-op after a re-review pass

Do not add a fresh scenario mechanically when the fix is only metadata or
maintainer-doc alignment and an existing scenario already covers that
behavior.
