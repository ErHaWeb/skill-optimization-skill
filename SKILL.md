---
name: skill-optimization
description: >
  Improve an existing skill or subagent in place. Use when the user wants to
  tighten activation or scope, reduce context footprint, simplify
  instructions, harden reproducibility, or align evals, deterministic helpers,
  agent metadata, support-file linkage, `.gitignore`, scoped IDE inspection
  exceptions, or official Anthropic/OpenAI guidance. Do not use it for
  new-skill creation, repo-wide normalization, or generic cleanup outside the
  target skill.
---

# Skill Optimization

## Purpose

Improve an existing skill with the smallest high-value change set.

When priorities conflict, use this order:
1. Improve discovery and activation.
2. Narrow the scope and make non-triggers explicit.
3. Make instructions shorter, more operational, and more reproducible.
4. Keep portable guidance standard-first, but treat official Anthropic and
   OpenAI documentation as binding for vendor-specific behavior.
5. Isolate vendor-specific notes cleanly.
6. Touch evals only when that closes a real behavioral gap.

Treat the current skill as input, not authority.

If you notice that this optimization skill relies on a fuzzy recurring pattern
that is not clearly defined here, do not push that ambiguity into the target
skill. Tighten the pattern here first when this skill itself is in scope;
otherwise report the ambiguity briefly and keep the target-skill edit limited
to clearly justified improvements.

Run the work as a short loop:
1. Read the baseline files and cluster the real weaknesses.
2. Fix only the 1 to 3 highest-impact gaps in that pass.
3. Re-read the result against the same criteria.
4. Stop when another pass would only produce cosmetic churn.

## Use This Skill When

- The user wants to review, tighten, simplify, refactor, harden, or clean up an
  existing `SKILL.md`, skill directory, or Claude Code subagent.
- The skill triggers unreliably, reads too broadly, mixes vendor rules, or
  carries too much process.
- The skill wastes tokens through duplicated guidance, mandatory broad reads,
  or verbose default output requirements.
- The skill lacks generic QA structure such as evals, deterministic verifier
  scripts, fixture/reference linkage, `.gitignore`, or justified `.idea`
  inspection exceptions.
- The user says things like `review my skill`, `make this skill better`,
  `tighten this agent`, or `clean up this skill`.

## Do Not Use This Skill When

- The task is to create a new skill from scratch.
- The task is generic repo cleanup or documentation work outside a skill or
  subagent.
- The user only wants to list, install, or run a skill without changing it.
- The real work is product code or app behavior rather than skill behavior.

## Defaults

- Work directly in the repository when writes are allowed.
- Only edit the requested target skill or subagent. Use neighboring skills or
  sibling directories as read-only reference material unless the user explicitly
  widens scope.
- Start with the primary skill file. Touch `references/`, `evals/`, fixtures,
  or docs only when they would otherwise stay stale, misleading, or untestable.
- Do not force audit-only modes, multi-phase approvals, or pre-edit
  confirmation unless the user asked for them or the action is risky.
- If the request turns out to be out of scope after the first file read, say so
  briefly and stop instead of stretching the skill to fit.
- Ask follow-up questions only when the target or scope is still unsafe after
  the first read.
- Prefer workable defaults over process mechanics.
- Prefer the smallest context footprint that preserves behavior, QA, and
  safety.
- When the target depends on OpenAI/Codex or Anthropic/Claude behavior,
  official vendor documentation is the binding quality standard. Local examples
  and neighboring skills are reference material, not authority.
- If `agents/openai.yaml` exists, treat it as a maintained activation and UI
  contract, not as decorative metadata.
- If the target is a Claude Code subagent, treat its YAML frontmatter and
  current scope as maintained configuration. Do not add `tools`, strip valid
  Claude fields, or move between `.claude/agents/` and `~/.claude/agents/`
  unless the intended behavior change actually requires it.
- Treat no-op as a valid result. Stop when another pass would only improve tone,
  formatting, or wording without changing behavior, determinism, or safety.

## What To Inspect

1. Read the primary skill file first: usually `SKILL.md`, or the target
   markdown file for a standalone subagent.
2. If the target is a Claude Code subagent, read its YAML frontmatter and note
   whether it lives in `.claude/agents/` or `~/.claude/agents/` before editing.
3. Read `agents/openai.yaml` early when it exists and activation surface,
   default workflow, or local QA maintenance may be in scope.
4. Check the target skill's local QA surface as relevant: `.gitignore`,
   committed `.idea`, `README`, `references/`, `evals/`, and support files.
5. Start `evals/` with `evals/evals.json` when behavior, scope boundaries, QA
   guarantees, or support-file contracts may change.
6. Read [`references/official-vendor-baseline.md`](references/official-vendor-baseline.md)
   when vendor-specific instructions, metadata, frontmatter, prompt structure,
   or delegation behavior may change.
7. Run `python3 scripts/verify_skill_contract.py` when the target owns that
   verifier and your edits touch QA contracts, metadata, fixture linkage, or
   vendor-baseline references.
8. Open only the support files needed to preserve behavior or validate a real
   contract.
9. Use external docs only when vendor behavior or the skills standard materially
   affects the edit.
10. If your intended change depends on an internal optimization pattern that is
   still underspecified in this skill, clarify or narrow that pattern here
   first instead of silently exporting it into the target skill.

## High-Value Checks

### 1. Discovery and Activation

- Is the frontmatter `description` specific enough to trigger on the right
  requests?
- Does it describe user intent instead of the skill's internal process?
- Does it include clear boundaries or non-triggers so it does not fire on
  generic work?
- When the target uses OpenAI/Codex or Claude Code semantics, do activation and
  metadata follow the applicable official vendor docs instead of local folklore?
- If the target is a Claude Code subagent, does its YAML `description`
  describe when Claude should delegate to it?

### 2. Scope and Boundaries

- Is there a clear `use when` boundary?
- Is the scope narrower than `optimize everything` or `handle any repo`?
- Are nearby but out-of-scope tasks ruled out explicitly when needed?
- Does the optimization stay on the target skill instead of drifting repo-wide?

### 3. Operational Instructions

- Are the instructions actionable in the current environment?
- Are defaults clear enough to avoid unnecessary follow-up questions?
- Are outputs, fallbacks, and stop criteria short and reproducible?
- Is the routine context footprint as small as possible without hiding required
  behavior?
- Has process weight been reduced instead of moved around?

### 4. Generic Skill QA

- Does the target skill have a clear local maintenance context such as a Git
  repo, or at least an explicit note when it is missing?
- Is there a local `.gitignore` or equivalent hygiene coverage for editor,
  generated, cache, or package-manager artifacts that can appear in the skill
  directory?
- Is there at least one machine-checkable quality contract such as realistic
  evals, a deterministic verifier, or a validator script with stable fixtures?
- If `scripts/`, `references/`, `fixtures/`, `evals/`, `assets/`, or
  `agents/` exist, does `SKILL.md` say when to read or run them, and does
  `agents/openai.yaml` still match the trigger surface when present?
- When `agents/openai.yaml` exists, do `SKILL.md`, `README.md`, or an existing
  verifier treat it as a maintained file when that would otherwise drift?
- If official Anthropic or OpenAI docs define the relevant behavior, does the
  target follow those rules before local precedent or adjacent examples?
- If the target is a Claude Code subagent, do its supported frontmatter fields
  still match actual behavior and stay distinct from Codex/OpenAI metadata
  rather than being normalized into it?
- If `.idea` is committed, are inspection exceptions narrow, scope-based, and
  documented instead of globally suppressing warnings?

Read [`references/skill-quality-baseline.md`](references/skill-quality-baseline.md)
when the request touches QA structure, determinism, support files, IDE
exceptions, or agent metadata drift.

Read [`references/official-vendor-baseline.md`](references/official-vendor-baseline.md)
when the request touches OpenAI/Codex or Anthropic/Claude rules, metadata,
frontmatter, prompting structure, or delegation behavior.

### 5. Redundancy and Complexity

- Remove duplicated guidance, inflated QA theater, mandatory phase gates, or
  approval loops that do not protect against real risk.
- Remove mandatory broad-read instructions or verbose report scaffolding that
  increase token cost without improving execution quality.
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
   Pick from activation, boundaries, context footprint, operational
   instructions, QA baseline, eval coverage, and report/no-op behavior.
2. Choose only the 1 to 3 highest-impact weaknesses for the current pass.
   A change is substantial only if it improves behavior, determinism, scope
   clarity, QA defense, safe defaults, or context efficiency.
   If the intended fix depends on a vague optimization pattern from this skill,
   harden that pattern here before applying it elsewhere.
3. Make the smallest edit set that closes those weaknesses.
   Prefer `SKILL.md` first. Touch `references/`, `evals/`, fixtures, or docs
   only when they would otherwise stay stale, misleading, or untestable.
4. Re-read the edited files against the same checklist.
   Stop if the next pass would only rephrase, reorder, or add meta commentary.
5. Report the final state compactly.
   Name the material gains, the files changed, remaining risks, and say plainly
   when the loop reached a justified no-op.

## Standard / Portable Guidance

- Keep `name` and `description` concise and aligned with actual usage.
- Treat the description as the activation surface: say when to use the skill,
  not just what it contains.
- Keep `SKILL.md` compact enough to load comfortably; move detailed reference
  material out only when it is reused or clearly too large for the main file.
- Treat context footprint as a hard quality contract. Reduce duplicated rules,
  mandatory reads, and verbose default outputs unless they materially improve
  activation, scope, QA, or safety.
- Use relative file references from the skill root.
- If you add supporting files, reference them directly from `SKILL.md` instead
  of relying on deep reference chains.
- If official Anthropic or OpenAI docs define a vendor-specific rule, treat
  that rule as binding for the target. Do not preserve a conflicting local
  pattern just because nearby skills already copied it.
- When comparable mature local skills already ship `agents/openai.yaml`, treat
  that file as an established local maintenance surface, not a speculative
  extra. Add or align it only when the target's real trigger surface supports
  it.
- For Claude Code subagents, preserve the current scope unless relocation is an
  explicit part of the requested fix.
- Keep QA rules generic and content-independent. Prefer a small baseline that
  can be reused across many skills over topic-specific governance.
- Require at least one machine-checkable quality contract for the target skill.
  Complex, script-heavy, or high-risk skills often need both evals and an
  executable verifier or validator with stable fixtures.
- If the target already has a verifier or contract script, prefer extending it
  to catch `agents/openai.yaml` drift before inventing additional QA layers.
- When a target-local verifier exists, keep `SKILL.md` or maintainer-facing
  docs aligned with when to run it and rerun it after contract edits that
  affect metadata, vendor-baseline references, or stable fixtures.
- Do not invent repo-wide standards while optimizing one skill. Report broader
  repository issues separately instead of silently widening scope.

## Vendor / Sources

- Optimize frontmatter because Codex discovers skills from lightweight
  metadata first.
- Official OpenAI and Anthropic documentation is the authoritative quality
  baseline for vendor-specific skill and subagent behavior handled by this
  skill.
- Use local examples only after checking the applicable official docs.
  If local practice conflicts with official docs, align the target to the
  official rule or report the divergence plainly when a local exception must be
  preserved.
- Keep Codex-, Claude-, or other client-specific fields only when they
  materially help, and keep them isolated from portable guidance.
- If optimizing a Claude Code subagent, preserve its native file format and
  location conventions instead of rewriting it into another tool's layout.
- For Claude Code subagents, treat Markdown plus YAML frontmatter as native
  configuration. Preserve supported fields such as `tools`,
  `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`,
  `mcpServers`, `hooks`, `memory`, `background`, and `isolation` when they
  are part of the current contract.
- Do not assume OpenAI skill metadata and Claude Code subagent frontmatter
  share the same field surface. In Claude Code, `name` and `description` are
  required, `tools` is optional, and omitted `tools` inherits the parent tool
  set.
- For OpenAI/Codex skills, follow the official Codex skills and prompting docs
  for structure, activation metadata, progressive disclosure, and eval-backed
  prompt iteration.
- For Anthropic Agent Skills, follow the official Agent Skills overview and
  best-practices docs for required frontmatter, concise `SKILL.md` bodies,
  description wording, and iterative evaluation.
- Use external docs only when they change the edit: official OpenAI docs first
  for OpenAI/Codex behavior, official Anthropic docs first for Claude behavior,
  then Agent Skills as portability context, then Cursor as a final portability
  check.
- If official sources stay silent or inconclusive, make the smallest reasonable
  decision, note the gap briefly, and do not invent unsupported vendor rules.
- Treat recurring optimization heuristics as part of this skill's contract, not
  as hidden operator taste. If a heuristic matters repeatedly and is still too
  vague to apply safely, clarify it here before using it to reshape another
  skill.

## Evals

- Inspect existing evals only far enough to see whether they defend the real
  purpose of the skill.
- Update evals when there is a clear gap around activation boundaries, scope
  control, context footprint, QA baseline behavior, loop termination, or a
  critical workflow expectation.
- Add or update the smallest scenario needed when the target previously relied
  on vendor assumptions that conflict with official Anthropic or OpenAI docs.
- Do not add evals mechanically for `agents/openai.yaml`, `README.md`, or
  verifier-maintenance edits. Add or update them only when the metadata gap
  exposes a real behavior contract that existing scenarios do not already
  defend.
- Remove or rewrite eval expectations that enforce unnecessary confirmation
  loops, exhaustive audit rituals, or verbose report scaffolding.
- Prefer realistic prompts and sharp assertions over broad process checklists.
- When you introduce or tighten QA behavior, add the smallest scenario that
  proves it. Reuse existing fixtures when possible.

## Finish Check

Before finishing, confirm:
- activation is more reliable
- scope is narrower and clearer
- context footprint is lower or explicitly already minimal
- instructions are simpler and more reproducible
- generic QA is stronger without repo-wide drift
- vendor-specific behavior follows applicable official Anthropic/OpenAI
  guidance or is explicitly documented as an intentional exception
- remaining ideas are cosmetic rather than behavioral

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
- No token-saving edits that hide required behavior or weaken QA or safety.
- No new complexity unless it clearly improves activation, scope control, or
  execution quality.
- No edits outside the requested target skill or subagent unless the user
  explicitly broadens scope.
- No exporting of vague internal optimization patterns into a target skill.
  Tighten those patterns here first or report the gap instead of degrading the
  target.
