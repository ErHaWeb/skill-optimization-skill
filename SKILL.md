---
name: skill-optimization
description: >
  Performs a comprehensive, system-wide optimization of an existing skill directory —
  analyzing, refactoring, and harmonizing SKILL.md, all referenced files, modules,
  configuration, and documentation into a coherent, production-grade system.
  Use this skill whenever the user wants to optimize, audit, clean up, refactor,
  harmonize, or improve any skill or skill directory, even if they just say
  "review my skill", "clean this up", or "make this better".
---

# Skill Optimization & Harmonization Skill

---

## 1. Purpose

This skill performs a comprehensive, system-wide optimization of an existing skill directory.

It analyzes, validates, refactors, and harmonizes all files in the skill directory — SKILL.md, referenced files, modules, utilities, configuration, documentation, templates, and auxiliary resources — into a production-grade, logically consistent, and fully synchronized system. It operates directly on the filesystem and applies improvements in place.

---

## 2. Execution Context

- Executed from within a skill directory.
- Read/write access to the target directory is preferred. If write access is restricted, run in **Audit only** mode and explicitly report blocked write operations.
- If an operation requires elevated permissions, request user confirmation before proceeding.
- The skill may modify any file within the directory.
- The skill must maintain or improve functional correctness.
- The skill must treat the directory as a cohesive system, not as isolated artifacts.

### 2.1 Directory Conventions

- `SKILL.md` is the primary entry point.
- `evals/` (including fixtures and `evals/evals.json`) is treated as utility/support content for validation purposes.

---

## 3. Operational Principles

The optimization process must adhere to:

- Deterministic logic over interpretive flexibility
- Minimal redundancy
- High signal-to-noise ratio
- Cross-file consistency
- Explicit fallback behavior
- Structural coherence
- Professional engineering rigor
- Zero orphaned logic
- Zero contradictory instruction sets

No superficial edits.
All changes must serve structural, logical, or performance improvements.

---

## 4. Optimization Dimensions

### 4.1 Execution Efficiency

- Remove redundant logic and repeated guidance.
- Eliminate circular references.
- Optimize instruction ordering.
- Reduce token-heavy ambiguity.
- Consolidate overlapping rules.
- Remove dead or unreachable code.

### 4.2 Logical Consistency

- Detect contradictions between documentation and implementation.
- Resolve ambiguous instruction hierarchies.
- Define explicit fallback behavior.
- Clarify decision trees.
- Ensure responsibilities are unambiguous.

### 4.3 Cross-Source Harmonization

- Ensure terminology consistency across all files.
- Align configuration with implementation logic.
- Update documentation to reflect actual behavior.
- Remove outdated references.
- Synchronize naming conventions.
- Ensure all referenced files exist and are accurate.

### 4.4 Redundancy Elimination

- Merge duplicated logic.
- Consolidate repeated conceptual sections.
- Remove legacy comments that contradict current logic.
- Collapse structurally identical patterns.

### 4.5 Quality Assurance & Robustness

- Introduce validation logic where useful.
- Strengthen error handling.
- Add guardrails for ambiguous user input.
- Improve deterministic behavior.
- Ensure reproducibility.
- Ensure consistent output constraints where applicable.

### 4.6 Content Hardening

If conceptual or domain gaps are detected:

- Integrate missing best practices.
- Modernize outdated patterns.
- Improve domain precision.
- Strengthen technical rigor.
- Ensure alignment with modern LLM orchestration standards.

---

## 5. Interaction & Scope

Before execution, clarify two things with the user:

### 5.1 Execution Mode

Ask the user which mode to use:

| Mode | Description |
|------|-------------|
| **Audit only** | Discover and report issues — no files are modified |
| **Full optimization** | Apply all improvements in place after user confirmation |

In **Full optimization** mode: after Phase 2, present the planned changes and require explicit confirmation before applying Phase 3.

### 5.2 Scope

Ask whether optimization should target:

| Scope | Description |
|-------|-------------|
| **Full directory** | All files in the skill directory |
| **Specific files** | User specifies which files to include |
| **SKILL.md only** | Only the main skill file |

Default to **Full directory** if the user does not specify.

---

## 6. Execution Phases

### Phase 1 — System Discovery

No modifications in this phase.

**Step 1: File inventory**

List all files in the target scope recursively. For each file record:
- Path (relative to skill root)
- Type (`.md`, `.json`, `.yaml`, `.py`, `.sh`, other)
- Size in lines

**Step 2: Reference extraction**

For each file, extract outbound references only from these explicit contexts — do not scan raw text broadly:
- Markdown links: `[text](path)` — extract the path
- Code imports: lines whose first non-whitespace token is `import`, `require`, `include`, `extends`, or `source` — extract the path argument (handles indented lines)
- Explicit path strings in JSON/YAML values: only string values that contain `/` or end with a known extension, and do not start with `http://` or `https://`

The known extension allowlist starts with `.md`, `.json`, `.yaml`, `.yml`, `.py`, `.sh`, `.toml`, `.ts`, `.js`. Extend it automatically by scanning the actual file extensions present in the scope directory — any extension found in the inventory is added to the allowlist for this run.
- Section cross-references: patterns like `see Section X`, `read references/X.md`, `→ agents/X.md`
- Fenced code blocks: only if the string contains `/` or matches a known extension present in the skill directory

Do not extract: version numbers, inline code examples, log fragments, or plain English sentences containing dots.

Before building the reference map, normalize all extracted paths:
- Strip leading `./`
- Resolve `..` segments
- Remove URL fragments (`#section`) for filesystem existence checks; retain the fragment separately if heading validation is needed

Build a reference map: `file → [list of normalized referenced paths]`

**Step 3: Reference validation**

For every extracted reference, check whether the target file exists in the skill directory. Classify each as:
- ✅ Resolved — target exists
- ❌ Broken — target does not exist
- ⚠️ External — URL or absolute path outside the skill directory

**Step 4: Reverse check**

Identify files that exist in the directory but are not referenced by any other file. These are orphan candidates.

**Step 5: Baseline metrics**

Record before any changes:
- Total files
- Total broken references (count)
- Total orphan candidates (count)
- Total duplicate section headings across files (count)
- Total files with contradictory instructions (count, identified by keyword scan for negation pairs: e.g., "always"/"never", "must"/"must not" on the same subject)

These metrics anchor the Before/After comparison in the Output Report.

---

### Phase 2 — Structural Audit (Two-Pass)

Audit is split into two passes. **Do not begin Pass B until Pass A is fully documented.**

---

#### Pass A — Quick Consistency Checks

Focus: issues that are fast to identify and low-risk to assess.

Pass A is audit-only. Collect findings and proposed fixes, but do not modify files during Phase 2.

Work through every file in scope and check:

**Reference integrity**
- [ ] All references from Phase 1 Step 3 are resolved (no ❌ broken references remain)
- [ ] No orphan files exist without a clear purpose (cross-check Phase 1 Step 4)
- [ ] All section cross-references (e.g., "see Section 4.2") point to sections that exist

**Naming consistency**
- [ ] The same concept is referred to by the same term across all files
  - Identify synonym clusters (e.g., "executor" vs "runner", "task" vs "job") and pick one canonical term per concept
- [ ] File names match how they are referenced (case-sensitive)

**Obvious duplication**
- [ ] No section heading appears more than once within the same file
- [ ] No paragraph-level block of text is copy-pasted verbatim across files

**Stop criteria for Pass A:**
- Do NOT rename files during Pass A — only flag for Pass B
- Do NOT delete files during Pass A — only flag as orphan candidates
- Do NOT restructure sections during Pass A — only flag for Pass B

Document all Pass A findings as a numbered issue list with severity (HIGH / MEDIUM / LOW) and proposed fix.

---

#### Pass B — Deep Refactor Planning

Focus: structural and semantic issues requiring larger changes.

Only proceed to Pass B after Pass A findings are documented.

Work through each file in scope:

**Redundancy & Efficiency**
- [ ] Does this file duplicate logic present in another file at a conceptual (not just textual) level?
- [ ] Are there instructions that are unreachable given the defined execution flow?
- [ ] Are there instructions whose scope or trigger condition is undefined?

**Logical Consistency**
- [ ] Do any instructions contradict each other within this file?
- [ ] Do any instructions contradict those in other files?
- [ ] Are all decision branches explicitly defined, including fallbacks for unexpected input?
- [ ] Are there implicit assumptions that should be made explicit?

**Cross-File Harmonization**
- [ ] After Pass A term normalization: is terminology now fully consistent?
- [ ] Is the documentation aligned with the actual implementation behavior?
- [ ] Are configuration values consistent with the logic that consumes them?

**Quality & Robustness**
- [ ] Are edge cases and ambiguous inputs handled?
- [ ] Is error behavior defined?
- [ ] Are output formats and constraints explicitly specified?

Compile Pass B findings into the same numbered issue list, appended after Pass A findings.

**Prioritization heuristic for Phase 3:**
1. Broken references (always first — nothing else is reliable until these are fixed)
2. Contradictions (HIGH severity)
3. Redundancy spanning multiple files (HIGH severity)
4. Intra-file redundancy (MEDIUM)
5. Missing fallbacks and edge cases (MEDIUM)
6. Formatting and naming normalization (LOW)

In **Audit only** mode: present the full issue list and stop here.

In **Full optimization** mode: present planned changes and await explicit user confirmation before Phase 3. Do not modify files before that confirmation.

---

### Phase 3 — Global Refactoring

Apply improvements in the order defined by the prioritization heuristic from Phase 2.

**Hard stop criteria — never proceed without these conditions met:**
- Before renaming any file: confirm all references to that file have been updated in the same operation
- Before deleting any file: confirm it is not referenced by any other file (cross-check Phase 1 reference map)
- Before restructuring a section: confirm no other file references it by heading name or anchor

**Drift protection — applies for the entire duration of Phase 3:**

Phase 3 must not introduce issues that were absent from the baseline. Specifically:
- No new file may be created without being immediately referenced by at least one existing file or listed as an entry point in SKILL.md.
- No new term may be introduced without being added to the canonical term list established in Pass A. Maintain this list in the Output Report under a dedicated "Canonical Terms" subsection; optionally also add a "Terminology" section to SKILL.md if the skill is large enough to benefit from it.
- No new cross-file reference may be created that is not verified as resolvable before the change is applied.

These rules make the system self-stabilizing: each change must leave the reference map and canonical term list in a consistent state, not defer consistency to a later pass.

**Per-change requirements:**
- Preserve the semantic intent of instructions unless a change is explicitly justified.
- If the intent of an instruction is ambiguous, resolve it to the most deterministic interpretation and document the reasoning in the report.
- If a change alters observable behavior (not just wording), flag it as a behavioral change in the report.
- After each file modification, update the reference map if paths or headings changed.

**Execution order within Phase 3:**
1. Fix all broken references (Pass A, highest priority)
2. Normalize terminology across all files (Pass A)
3. Resolve contradictions (Pass B, HIGH severity first)
4. Merge redundant logic (Pass B)
5. Add missing fallbacks and edge case handling (Pass B)
6. Apply formatting and naming normalization (Pass B, LOW severity)

All modifications must preserve systemic coherence.

---

### Phase 4 — QA Gates

After refactoring, run each gate in order. All gates must pass before the report is issued. If a gate fails, fix the issue and re-run from that gate.

---

**Gate 1 — Reference integrity (mandatory)**

Re-run the reference extraction and validation from Phase 1 Steps 2–3. Pass condition: zero broken references (❌ count = 0).

**Gate 2 — Orphan check (mandatory)**

Re-run Phase 1 Step 4. Pass condition: every file in the skill directory satisfies at least one of:
- (a) referenced by at least one other file in the directory
- (b) explicitly listed as a standalone entry point in SKILL.md
- (c) explicitly marked as a utility or support file in documentation (including declared support folders such as `evals/`)

Do not create artificial references just to satisfy this gate. If a file is genuinely unused, flag it for removal rather than manufacturing a reference.

**Gate 3 — Contradiction scan (mandatory)**

For each file, scan for negation pairs on the same subject within the same paragraph block (text separated by blank lines): "always"/"never", "must"/"must not", "required"/"optional", "do"/"do not". Only flag a pair if both terms apply to the same subject within the same paragraph. Pass condition: zero unresolved contradiction pairs.

**Gate 4 — Terminology consistency (mandatory)**

For each canonical term defined during Pass A normalization, verify it is used exclusively across all files. Synonyms that were replaced must no longer appear. Pass condition: zero residual synonym occurrences.

**Gate 5 — Before/After metrics (mandatory)**

Compare current metrics against the Phase 1 baseline:

| Metric | Before | After | Δ |
|--------|--------|-------|---|
| Total files | | | |
| Broken references | | | |
| Orphan candidates | | | |
| Duplicate section headings | | | |
| Files with contradictions | | | |

Pass condition: no problem metric has worsened (Broken references, Orphan candidates, Duplicate section headings, Files with contradictions all have Δ ≤ 0). `Total files` is informational and may increase or decrease.

---

**Gate 6 — Structural completeness (mandatory for SKILL.md)**

Verify SKILL.md contains: a Purpose section, an Execution Context or equivalent scope definition, at least one defined output format or report schema, explicit constraints (what the skill must not do), and success criteria. Pass condition: all five elements present.

**Gate 7 — Optional checks (run if applicable)**

If the skill includes executable scripts: check for syntax errors and verify entry points exist. If the skill includes JSON/YAML config files: verify valid syntax and that all keys referenced in SKILL.md exist in the config. If any issue is found, fix and re-run affected mandatory gates before proceeding.

---

## 7. Output Report

After execution, provide a structured report in this format:

```
# Optimization Report — [Skill Name]
Date: [YYYY-MM-DD]
Mode: [Audit only | Full optimization]
Scope: [Full directory | Specific files | SKILL.md only]

## 1. System Overview
[Brief description of the skill, its structure, and total files analyzed.]

## 2. Before/After Metrics
| Metric                      | Before | After | Δ  |
|-----------------------------|--------|-------|----|
| Total files                 |        |       |    |
| Broken references           |        |       |    |
| Orphan candidates           |        |       |    |
| Duplicate section headings  |        |       |    |
| Files with contradictions   |        |       |    |

## 3. Structural Issues Identified
[Numbered list of all issues found in Phase 2, with severity: HIGH / MEDIUM / LOW]

1. [HIGH] Contradiction between X and Y: ...
2. [MEDIUM] Redundant logic in file Z: ...

## 4. Canonical Terms
[Canonical term list established in Pass A. Use `source -> canonical` mapping. If no normalization was required, state "No term normalization required".]

## 5. Optimizations Applied
[Only in Full optimization mode. Numbered list of changes made, grouped by pass.]

Pass A:
1. Fixed broken reference to agents/executor.md in SKILL.md.
2. Normalized term "runner" → "executor" across 3 files.

Pass B:
3. Merged sections A and B in SKILL.md to eliminate redundancy.

## 6. QA Gate Results
[One line per gate: ✅ PASS or ❌ FAIL with details if failed.]

Gate 1 — Reference integrity: ✅ PASS (0 broken references)
Gate 2 — Orphan check: ✅ PASS
Gate 3 — Contradiction scan: ✅ PASS
Gate 4 — Terminology consistency: ✅ PASS
Gate 5 — Before/After metrics: ✅ PASS (all metrics improved or unchanged)
Gate 6 — Structural completeness: ✅ PASS
Gate 7 — Optional checks: n/a

## 7. Behavioral Changes
[Any change that alters how the skill behaves, not just how it reads. Mark clearly.]

## 8. Remaining Recommendations
[Issues not addressed in this run, with justification.]
```

Do not output full file contents unless explicitly requested.
Per-change context: include patch snippets only for behavioral changes, never for cosmetic edits.

---

## 8. Constraints

- Do not introduce speculative features.
- Do not change behavior without justification.
- Do not remove behavior without verifying impact.
- Do not perform cosmetic edits without structural benefit.
- Do not leave partially updated references.
- Do not proceed to Phase 3 without explicit user confirmation in Full optimization mode.

---

## 9. Success Criteria

The skill is considered optimized when:

- Documentation and implementation are fully synchronized.
- No redundancy remains.
- Instruction hierarchy is unambiguous.
- All dependencies are consistent.
- Naming conventions are standardized.
- Execution logic is deterministic.
- No orphaned or contradictory logic exists.
- The skill can be understood as a cohesive production system.

---

If executed correctly, this skill transforms any existing skill directory into a structurally coherent, efficient, and professionally engineered system ready for long-term maintenance and scaling.
