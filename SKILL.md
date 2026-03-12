---
name: skill-optimization
description: >
  Improve an existing skill or subagent in place. Use this skill when the user
  wants to review, tighten, simplify, harden, refactor, or modernize a
  SKILL.md, Claude Code subagent, or skill directory, especially to improve
  activation, narrow scope, reproducibility, evals, deterministic QA helpers,
  support-file linkage, `.gitignore` hygiene, or narrowly scoped IDE inspection
  exceptions. Do not use it for creating a brand-new skill, repo-wide
  normalization, or generic cleanup unrelated to the target skill.
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

Run the work as a short optimization loop:
1. Read the baseline files and cluster the real weaknesses.
2. Fix only the 1 to 3 highest-impact gaps in that pass.
3. Re-read the result against the same criteria.
4. Stop when another pass would only produce cosmetic churn.

## Use This Skill When

- The user wants to review, tighten, simplify, refactor, harden, or clean up an
  existing `SKILL.md`, skill directory, or Claude Code subagent.
- The skill triggers unreliably, reads too broadly, mixes vendor rules
  together, or is weighed down by process.
- The skill lacks generic QA structure such as evals, deterministic verifier
  scripts, fixture/reference linkage, `.gitignore`, or justified `.idea`
  inspection exceptions.
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
- Default to the smallest file set that can solve the problem. Start with the
  primary skill file; touch `evals/`, fixtures, or supporting files only when
  they would otherwise become stale or misleading.
- Only edit the requested target skill or subagent. Use neighboring skills or
  sibling directories as read-only reference material unless the user explicitly
  widens scope.
- If the request turns out to be out of scope after the first file read, say so
  briefly and stop instead of stretching the skill to fit.
- Ask follow-up questions only when the target skill is ambiguous or the scope
  would be unsafe to assume.
- Prefer workable defaults over process mechanics.
- Treat no-op as a valid result. Stop when another pass would only improve tone,
  formatting, or wording without changing behavior, determinism, or safety.

## What To Inspect

1. Read the primary skill file first: usually `SKILL.md`, or the target
   markdown file for a standalone subagent.
2. Check the target skill's local QA surface: `.gitignore`, committed `.idea`,
   `README`, `references/`, `evals/`, and support files only as far as they
   affect behavior or determinism.
3. Start `evals/` with `evals/evals.json` when behavior, scope boundaries, QA
   guarantees, or support-file contracts may change.
4. Open only the referenced or obviously relevant support files needed to
   preserve behavior.
5. Use external docs only when vendor behavior or the skills standard materially
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

### 4. Generic Skill QA

- Does the target skill have a clear local maintenance context such as a Git
  repo, or at least an explicit note when that context is missing?
- Is there a local `.gitignore` or equivalent hygiene coverage for editor,
  generated, cache, or package-manager artifacts that can appear in the skill
  directory?
- Is there at least one machine-checkable quality contract such as realistic
  evals, a deterministic verifier, or a validator script with stable fixtures?
- If `scripts/`, `references/`, `fixtures/`, `evals/`, `assets/`, or
  `agents/` exist, does `SKILL.md` say when to read or run them, and does
  `agents/openai.yaml` still match the skill's trigger surface when it exists?
- If `.idea` is committed, are inspection exceptions narrow, scope-based, and
  documented instead of globally suppressing warnings?

Read [`references/skill-quality-baseline.md`](references/skill-quality-baseline.md)
when the request touches QA structure, determinism, support files, or IDE
exceptions.

### 5. Redundancy and Complexity

- Remove duplicated guidance, inflated QA theater, mandatory phase gates, or
  approval loops that do not protect against real risk.
- Cut meta-instructions that mostly exist to manage the skill's own complexity.
- Prefer one good default workflow over multiple modes unless those modes are
  genuinely necessary.

### 6. Portability

- Keep portable skill guidance in the main flow.
- Keep vendor-specific behavior in clearly labeled sections.
- Do not bake one client's file layout or tool semantics into portable
  instructions unless the skill is intentionally vendor-specific.

## Working Method

Run this loop until no substantial change remains:

1. Cluster the real gaps after the first read.
   Pick from activation, boundaries, operational instructions, QA baseline,
   eval coverage, and report/no-op behavior.
2. Choose only the 1 to 3 highest-impact weaknesses for the current pass.
   A change is substantial only if it improves behavior, determinism, scope
   clarity, QA defense, or safe defaults.
3. Make the smallest edit set that closes those weaknesses.
   Prefer `SKILL.md` first. Touch `references/`, `evals/`, fixtures, or docs
   only when they would otherwise stay stale, misleading, or untestable.
4. Re-read the edited files against the same checklist.
   If the next pass would only rephrase, reorder, or add meta commentary, stop.
5. Report the final state compactly.
   Name the material gains, the files changed, remaining risks, and say plainly
   when the loop reached a justified no-op.

## Standard / Portable Guidance

- Keep `name` and `description` concise and aligned with actual usage.
- Treat the description as the activation surface: it should say when to use the
  skill, not just what it contains.
- Keep `SKILL.md` compact enough to load comfortably; move detailed reference
  material out only when it is reused or clearly too large for the main file.
- Use relative file references from the skill root.
- If you add supporting files, reference them directly from `SKILL.md` instead
  of relying on deep reference chains.
- Keep QA rules generic and content-independent. Prefer a small baseline that
  can be reused across many skills over topic-specific governance.
- Require at least one machine-checkable quality contract for the target skill.
  Complex, script-heavy, or high-risk skills often need both evals and an
  executable verifier or validator with stable fixtures.
- Do not invent repo-wide standards while optimizing one skill. Report broader
  repository issues separately instead of silently widening scope.

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
  control, QA baseline behavior, loop termination, or a critical workflow
  expectation.
- Remove or rewrite eval expectations that enforce unnecessary confirmation
  loops, exhaustive audit rituals, or verbose report scaffolding.
- Prefer realistic prompts and sharp assertions over broad process checklists.
- When you introduce or tighten QA behavior, add the smallest scenario that
  proves it. Reuse existing fixtures when possible.

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
- Did I strengthen generic QA expectations without drifting into repo-wide
  governance?
- Did I stop once the remaining ideas became cosmetic rather than behavioral?
- Did I separate portable guidance from vendor-specific notes?
- Would an external reviewer call the result simpler and more usable?

## Output

After the review, give a compact report that includes:
- the main strengths and weaknesses of the previous skill
- the files changed
- the 3 to 5 most important changes and why they mattered, if any
- whether the loop ended because no substantial change remained
- the sources actually used, if any
- any remaining risks or follow-up recommendations
- if no material change was warranted, say that plainly instead of
  manufacturing edits

Do not dump full file contents unless the user asks.

## Constraints

- No cosmetic rewrites without functional gain.
- No repo-wide expansion unless the problem spans multiple files.
- No speculative vendor claims.
- No mandatory confirmation steps unless the user asked for them or the action
  is risky.
- No new complexity unless it clearly improves activation, scope control, or
  execution quality.
- No edits outside the requested target skill or subagent unless the user
  explicitly broadens scope.

## Success Criteria

The skill is improved when:
- it triggers more reliably for the right requests
- it avoids obvious false positives
- its scope and non-goals are easy to read
- its instructions are shorter, more operational, and reproducible
- it applies a generic, deterministic QA baseline when that materially helps
- vendor-specific details are clearly isolated
- evals or other machine-checkable QA contracts, if touched, better reflect the
  skill's real purpose
- it stops once no substantial change remains
