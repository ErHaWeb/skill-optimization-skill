---
name: skill-optimization
description: >
  Improve an existing skill or subagent in place. Use this skill when the user
  wants to review, tighten, simplify, harden, refactor, or modernize a
  SKILL.md, Claude Code subagent, or skill directory, especially to improve
  activation, narrow scope, remove redundant or contradictory instructions, or
  separate portable guidance from vendor-specific details. Do not use it for
  creating a brand-new skill or for generic repo cleanup unrelated to a skill.
---

# Skill Optimization

## Purpose

Improve an existing skill with the smallest set of high-value changes.

When priorities conflict, use this order:
1. Improve discovery and activation.
2. Narrow the scope and make non-triggers explicit.
3. Make instructions shorter, more operational, and more reproducible.
4. Keep the skill standard-first and isolate vendor-specific notes cleanly.
5. Touch evals only when that closes a real behavioral gap.

In practice, the highest-value optimizations usually come from clearer
activation, tighter scope, shorter and more reproducible instructions, less
meta or audit overhead, and a few well-chosen edits instead of broad rewrites.

Treat the current skill as editable input, not as authority over what good
looks like.

## Use This Skill When

- The user wants to review, tighten, simplify, refactor, harden, or clean up an
  existing `SKILL.md`, skill directory, or Claude Code subagent.
- The skill triggers unreliably, reads too broadly, mixes vendor rules
  together, or is weighed down by process.
- The user says things like `review my skill`, `make this skill better`,
  `tighten this agent`, or `clean up this skill`.

## Do Not Use This Skill When

- The task is to create a new skill from scratch.
- The task is generic repo cleanup or documentation work that is not centered on
  a skill or subagent.
- The user only wants to list, install, or run a skill without changing it.
- The real work is product code or application behavior rather than skill
  behavior.

## Defaults

- Work directly in the repository when writes are allowed.
- Do not force an audit-only mode, multi-phase approval flow, or pre-edit
  confirmation unless the user asked for it or the action is risky.
- Default to the smallest file set that can solve the problem. Start with
  `SKILL.md`; touch `evals/`, fixtures, or supporting files only when they
  would otherwise become stale or misleading.
- If the request turns out to be out of scope after the first file read, say so
  briefly and stop instead of stretching the skill to fit.
- Ask follow-up questions only when the target skill is ambiguous or the scope
  would be unsafe to assume.
- Prefer workable defaults over process mechanics.

## What To Inspect

1. Read `SKILL.md` first.
2. Read `evals/` only when you may need to change skill behavior, scope
   boundaries, or related support files; start with `evals/evals.json`.
3. Open only the referenced or obviously relevant support files needed to
   preserve behavior.
4. Use external docs only when vendor behavior or the skills standard materially
   affects the edit.

## High-Value Checks

### 1. Discovery and Activation

- Is the frontmatter `description` specific enough to trigger on the right
  requests?
- Does it describe user intent instead of the skill's internal process?
- Does it include clear boundaries or non-triggers so it does not fire on
  generic work?

### 2. Scope and Boundaries

- Is there a clear `use when` boundary?
- Is the scope narrower than `optimize everything` or `handle any repo`?
- Are nearby but out-of-scope tasks ruled out explicitly when needed?

### 3. Operational Instructions

- Are the instructions actionable in the current environment?
- Are defaults clear enough to avoid unnecessary follow-up questions?
- Are outputs, fallbacks, and stop criteria short and reproducible?

### 4. Redundancy and Complexity

- Remove duplicated guidance, inflated QA theater, mandatory phase gates, or
  approval loops that do not protect against real risk.
- Cut meta-instructions that mostly exist to manage the skill's own complexity.
- Prefer one good default workflow over multiple modes unless those modes are
  genuinely necessary.

### 5. Portability

- Keep portable skill guidance in the main flow.
- Keep vendor-specific behavior in clearly labeled sections.
- Do not bake one client's file layout or tool semantics into portable
  instructions unless the skill is intentionally vendor-specific.

## Working Method

1. Identify the 1 to 3 highest-impact weaknesses.
2. Make the smallest edits that materially improve them.
3. Update supporting files only when needed to keep the skill coherent.
4. Re-read the edited files and check that the new scope, triggers, and
   defaults are consistent.
5. Stop once the important weaknesses are addressed. Do not keep iterating for
   cosmetic gains.

## Standard / Portable Guidance

- Keep `name` and `description` concise and aligned with actual usage.
- Treat the description as the activation surface: it should say when to use the
  skill, not just what it contains.
- Keep `SKILL.md` compact enough to load comfortably; move detailed reference
  material out only when it is reused or clearly too large for the main file.
- Use relative file references from the skill root.
- If you add supporting files, reference them directly from `SKILL.md` instead
  of relying on deep reference chains.

## OpenAI / Codex Notes

- Optimize for strong frontmatter because Codex discovers skills from lightweight
  metadata before reading the full file.
- Keep Codex-specific invocation syntax, tool assumptions, automation notes, or
  `AGENTS.md` conventions in a dedicated subsection instead of mixing them into
  portable instructions.
- Do not add Codex-only behavior unless it gives a clear practical benefit in
  this skill.

## Anthropic / Claude Code Notes

- Claude Code subagents use markdown files with YAML frontmatter; the
  `description` is used to decide delegation, so make it specific and
  action-oriented.
- Keep Claude-specific fields such as `tools` or `model` only when they
  materially improve the subagent. Do not add them by default.
- If optimizing a Claude-specific agent file, preserve its project or user-level
  location conventions instead of rewriting it into another client's layout.

## Evals

- Inspect existing evals only far enough to see whether they defend the real
  purpose of the skill.
- Update evals when there is a clear gap around activation boundaries, scope
  control, or a critical workflow expectation.
- Remove or rewrite eval expectations that enforce unnecessary confirmation
  loops, exhaustive audit rituals, or verbose report scaffolding.
- Prefer realistic prompts and sharp assertions over broad process checklists.

## Source Policy

Use external sources only when they change the edit:
1. Official OpenAI documentation or official OpenAI skill materials for Codex
   behavior
2. Official Anthropic documentation for Claude Code or subagents
3. Agent Skills as the portable format reference
4. Cursor docs only as a portability check when needed

Do not use third-party blogs as normative sources.
If a source is missing or inconclusive, make the smallest reasonable decision
and note that briefly in the final report.

## Self-Review

Before finishing, check:
- Did activation get more reliable?
- Did the scope get narrower and clearer?
- Did I replace process weight with workable defaults?
- Did I separate portable guidance from vendor-specific notes?
- Would an external reviewer call the result simpler and more usable?

## Output

After editing, give a compact report that includes:
- the main strengths and weaknesses of the previous skill
- the files changed
- the 3 to 5 most important changes and why they mattered
- the sources actually used, if any
- any remaining risks or follow-up recommendations

Do not dump full file contents unless the user asks.

## Constraints

- No cosmetic rewrites without functional gain.
- No repo-wide expansion unless the problem spans multiple files.
- No speculative vendor claims.
- No mandatory confirmation steps unless the user asked for them or the action
  is risky.
- No new complexity unless it clearly improves activation, scope control, or
  execution quality.

## Success Criteria

The skill is improved when:
- it triggers more reliably for the right requests
- it avoids obvious false positives
- its scope and non-goals are easy to read
- its instructions are shorter, more operational, and reproducible
- vendor-specific details are clearly isolated
- evals, if touched, better reflect the skill's real purpose
