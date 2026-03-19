# Skill Optimization

`skill-optimization` is a maintenance skill for improving existing AI skills and
subagents.

It is designed for situations where a skill already exists, but its activation
is too broad, its scope is blurry, its instructions are too long or too vague,
or its vendor-specific details are mixed into otherwise portable guidance.

This repository contains:

- `SKILL.md`: the machine-facing instructions used by the agent
- `agents/openai.yaml`: the UI metadata kept aligned with the skill's real
  trigger surface
- `references/`: compact reusable guidance for generic skill QA
- `references/official-vendor-baseline.md`: the binding Anthropic/OpenAI
  quality baseline for vendor-specific behavior
- `evals/`: small regression scenarios that protect the intended behavior
- `scripts/verify_skill_contract.py`: a deterministic contract check for
  maintainer-facing metadata, fixtures, and reference alignment

## What This Skill Does

The skill helps an agent improve an existing skill with a small number of
high-value edits.

Its main priorities are:

1. make activation more reliable
2. narrow the scope and clarify non-triggers
3. make instructions shorter, more operational, and more reproducible
4. keep portable guidance separate from OpenAI/Codex and Anthropic/Claude Code
   specifics
5. treat official Anthropic/OpenAI docs as binding when vendor-specific rules
   are in play
6. enforce a small, generic QA baseline when it materially helps
7. touch evals only when that closes a real gap

In practice, this means the skill prefers focused repairs over broad rewrites.
If a skill is already good enough, it should say so instead of inventing
changes.
If a recurring optimization heuristic is still too vague to apply safely, the
skill should tighten or report that heuristic first instead of exporting the
ambiguity into the target skill.

## What This Skill Is For

Use it when you want to improve an existing:

- `SKILL.md`
- skill directory
- standalone Claude Code subagent markdown file

Typical problems it is meant to fix:

- the description is too broad and causes false activations
- the skill tries to cover too many adjacent tasks
- the instructions are repetitive, vague, or overly process-heavy
- vendor-neutral rules and vendor-specific notes are mixed together
- local vendor assumptions drift away from official Anthropic or OpenAI docs
- support files exist but are not linked from `SKILL.md`
- `agents/openai.yaml` is stale, missing in an established local skill
  landscape, or treated as optional decoration
- a Claude Code subagent has been normalized away from `.claude/agents/`,
  carries stale frontmatter, or treats `tools` as mandatory boilerplate
- `.gitignore`, evals, verifier scripts, or deterministic fixtures are missing
  or weak
- `.idea` inspection exceptions are absent, too broad, or undocumented
- the evals no longer match the real behavior of the skill

## What This Skill Is Not For

Do not use it for:

- creating a brand-new skill from scratch
- generic repository cleanup unrelated to a skill
- listing, installing, or running skills without changing them
- product or application code that is not really skill behavior

## How It Works

At a high level, the skill:

1. reads the primary skill file first
2. reads Claude Code subagent frontmatter and current scope early when the
   target is a Claude subagent
3. loads the official Anthropic/OpenAI baseline when vendor-specific behavior
   may change
4. reads `agents/openai.yaml` early when activation, defaults, or QA
   maintenance may be involved
5. checks the local QA surface such as `.gitignore`, `README`, evals, support
   files, and committed `.idea` settings when present
6. clusters the highest-value weaknesses
7. improves only the most important 1 to 3 issues in that pass
8. re-reviews the result against the same checklist
9. stops once the remaining ideas are cosmetic rather than behavioral

It intentionally avoids heavy audit rituals, mandatory confirmation loops, and
large repo-wide rewrites unless they are actually necessary. All changes stay
inside the target skill or subagent unless the user explicitly broadens scope.
When a local skill ecosystem already treats `agents/openai.yaml` as standard,
the skill should handle missing or stale metadata as a real maintenance gap,
not a speculative add-on. That alone is not a reason to invent new eval
scenarios if existing coverage already defends the behavior.
For Claude Code subagents, the skill should preserve the current project/user
scope and treat YAML frontmatter as real configuration. It should not force a
`tools` field just because a subagent exists, and it should not flatten Claude
Code-specific fields into generic Markdown prose.
For all vendor-specific behavior, official Anthropic and OpenAI docs outrank
local habit, copied examples, and stale repository folklore.
When this skill's own contract files change, rerun
`python3 scripts/verify_skill_contract.py` so metadata, fixtures, and
maintainer docs cannot drift silently.

## Supported Targets

The skill is written to work well with:

- OpenAI Codex skills
- Anthropic Claude Code subagents
- portable, markdown-based skill setups

It keeps the core guidance portable and separates vendor-specific notes where
that improves practical use.

## Example Prompts

These are the kinds of prompts that should trigger this skill:

```text
Review this skill and make it trigger more reliably.
```

```text
Tighten the scope of this SKILL.md and remove redundant instructions.
```

```text
Clean up this Claude Code subagent so it is narrower and easier to delegate to.
```

```text
Improve this skill, but only if there is a material gain in activation, scope,
or instruction quality.
```

```text
Optimize only the main skill file. Do not touch other files unless they would
become misleading.
```

## Example Non-Goals

These are intentionally out of scope:

```text
Create a new skill for weekly release announcements.
```

```text
List all available skills in this repository.
```

```text
Install this skill and show me how to run it.
```

```text
Clean up the whole repository documentation.
```

## Repository Layout

```text
SKILL.md
agents/
  openai.yaml
references/
  official-vendor-baseline.md
  skill-quality-baseline.md
evals/
  README.md
  evals.json
  files/
scripts/
  verify_skill_contract.py
```

- `SKILL.md` is the actual skill definition
- `agents/openai.yaml` is the maintained UI metadata for discovery-facing
  activation guidance
- `references/official-vendor-baseline.md` defines the authoritative
  Anthropic/OpenAI baseline for vendor-specific behavior
- `references/skill-quality-baseline.md` holds the generic QA checklist used for
  skill hardening
- `evals/README.md` summarizes what the eval scenarios defend
- `evals/evals.json` contains regression scenarios
- `evals/files/` contains small fixtures used by those scenarios
- `scripts/verify_skill_contract.py` verifies that the local maintenance
  contract and its stable fixtures stay aligned

## Design Principles

This skill is opinionated in a few specific ways:

- minimality beats completeness
- clear scope beats broad ambition
- reproducible instructions beat abstract process language
- deterministic QA beats ceremonial QA
- official vendor rules beat repeated local assumptions
- self-critical heuristic hardening beats undocumented operator taste
- a few good edits beat endless meta-optimization
- no-op is a valid outcome when no real improvement is justified

## If You Want to Use or Adapt It

Read [SKILL.md](SKILL.md) for the exact agent instructions.

If you adapt this skill for another environment, keep the core behavior narrow:
improve existing skills, do not turn it into a general audit or governance
framework.
