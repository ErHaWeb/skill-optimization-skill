# Skill Quality Baseline

Use this checklist when optimizing generic skill quality rather than topic
content.

## Minimum Baseline For Any Skill

- The target has a clear maintenance context.
  Prefer a local Git repository or an obvious parent repo. If no Git context is
  present, report that as a quality gap instead of initializing one unless the
  user asked for it.
- The target has local hygiene coverage.
  Prefer a local `.gitignore` when editor, cache, dependency, package-manager,
  or generated artifacts can accumulate inside the skill directory. If a parent
  repo already covers the same files and no local exception is needed, that is
  acceptable, but note it explicitly when relevant.
- The target has at least one machine-checkable quality contract.
  Acceptable examples:
  - `evals/evals.json` with realistic prompts and sharp assertions
  - a deterministic verifier or validator script with stable input data
  - a script-plus-fixture contract that is explicitly referenced from the skill
- `SKILL.md` tells the agent when to read or run support files that affect
  behavior.
  This applies to `scripts/`, `references/`, `fixtures/`, `evals/`, `assets/`,
  and `agents/` when they exist.
- If `agents/openai.yaml` exists, keep it aligned when the skill's activation
  surface or default workflow changes materially.
- The target keeps its routine context footprint intentionally small.
  `SKILL.md` should avoid mandatory broad reads, duplicated rules, or verbose
  default output scaffolding unless they materially improve behavior.

## Additional Baseline For Complex Skills

Treat a skill as complex when it generates files, transforms structured data,
ships helper scripts, depends on fixtures, or has several support directories.

Complex skills should usually have:

- realistic evals that defend activation, scope, and workflow boundaries
- an executable verifier or validator when output determinism matters
- stable fixtures or reference files that make the verifier repeatable
- a short README or eval note when future maintainers would otherwise miss the
  contract

Do not add all of these mechanically. Add the smallest combination that makes
the behavior testable and hard to drift.

## IDE Inspection Exceptions

`.idea` is optional and should stay rare.

If it is present:

- commit only shared project files, not personal workspace state
- keep `.idea/.gitignore` aligned so user-local files stay untracked
- prefer scope-based exceptions over global inspection suppression
- document every deliberate false-positive exception in a short project note
- keep the exception narrow to the exact fixture or generated file that needs it

Do not add `.idea` just to satisfy a checklist.

## Hygiene Rules

- Ignore or remove editor noise such as `.DS_Store`, workspace files, caches,
  or dependency directories when they can appear locally.
- Treat agent-generated worktree mirrors such as `/.claude/worktrees/` as local
  artifacts unless the project intentionally versions them.
- Do not treat committed build output or dependency trees as normal unless the
  skill truly requires them.
- Keep fixtures intentionally minimal and deterministic.
- Prefer stable, text-based fixtures over opaque binary inputs when either would
  work.

## Context Footprint Contract

Treat token efficiency as a quality contract, not as optional polish.

- Reduce default read sets, duplicated instructions, and verbose reporting
  requirements when behavior stays intact.
- Prefer on-demand support-file reads over mandatory bulk loading.
- Do not move bloat into new support files unless the moved content is reused
  or clearly too large for `SKILL.md`.
- Never save tokens by removing activation boundaries, determinism, QA
  contracts, or safety-critical guidance.

## When To Edit Versus Report

Edit locally when the fix is small, deterministic, and clearly inside the
target skill. Examples: adding a missing `.gitignore`, linking a verifier from
`SKILL.md`, adding a minimal eval, narrowing an inspection exception, or
removing duplicated instructions and unnecessary read requirements.

Report instead of editing when the missing quality measure would require:

- repo-wide normalization
- bootstrapping infrastructure outside the target skill
- speculative tool choice without a clear local need
- broad process layers with no real behavior gain

## Loop Termination

Stop the optimization loop when another pass would only:

- rewrite wording without changing behavior
- reorder sections for taste only
- add meta-process text without increasing determinism or safety
- create new QA layers that do not close a real gap
- chase extra token savings that would weaken behavior or clarity

At that point, say plainly that no substantial change remains.
