# Official Vendor Baseline

Use this reference when optimizing a skill or subagent whose behavior depends
on OpenAI/Codex or Anthropic/Claude semantics.

This file defines the binding authority order for vendor-specific behavior:

1. Official OpenAI or Anthropic documentation for the target surface
2. The target skill's actual local contract
3. Neighboring local examples only as secondary reference material

If local convention conflicts with the applicable official docs, treat that as
drift to fix or report. Do not preserve the local pattern just because it is
repeated.

## OpenAI / Codex

Use official Codex docs as the authority for OpenAI-specific skill behavior.

Binding rules to preserve:

- Codex uses progressive disclosure when loading skills, so concise metadata and
  clear `description` scope matter for activation.
- Codex skills live in a skill directory with `SKILL.md` as the main
  instruction file.
- `agents/openai.yaml` is optional Codex metadata, not a universal
  requirement. Add or align it only when the target environment or local skill
  landscape makes it a real maintenance surface.
- Keep descriptions specific about when to use the skill, and make boundaries
  explicit so the skill does not over-trigger.
- Codex skill creation is instruction-first by default. Prefer instructions over
  scripts unless deterministic behavior or external tooling is genuinely needed.
- Write imperative steps with explicit inputs and outputs.
- Test prompts against the skill description to confirm the right trigger
  behavior.
- For prompt or instruction changes that materially affect behavior, keep or add
  eval coverage rather than relying on prompt wording alone.

Prompting and evaluation guidance to apply when relevant:

- Keep durable role or behavior guidance in the top-level instruction surface
  rather than scattering it across optional examples.
- Prefer clear structure, explicit success criteria, and small realistic
  examples over long abstract process prose.
- Treat model or prompt iteration as eval-backed work. Stable prompt behavior
  needs a repeatable test surface.

## Anthropic / Claude

Use official Anthropic Agent Skills, Claude Code, and Anthropic prompting docs
as the authority for Claude-specific skill or subagent behavior.

Binding rules to preserve:

- Anthropic Agent Skills package instructions, metadata, and optional resources
  that Claude uses automatically when relevant.
- Anthropic Agent Skills use progressive disclosure: metadata loads first,
  `SKILL.md` loads when triggered, and referenced files or scripts load only as
  needed.
- Anthropic Skills require a `SKILL.md` file with YAML frontmatter.
- In Anthropic Skills, `name` and `description` are required, `description`
  should say what the Skill does and when to use it, and Anthropic's best
  practices treat that metadata as critical for discovery.
- Anthropic recommends writing Skill descriptions in third person because the
  description is injected into the system prompt.
- Anthropic best practices emphasize concise `SKILL.md` bodies, assuming Claude
  already knows general background, and matching the degree of freedom to the
  task's fragility.
- Anthropic best practices also keep progressive disclosure explicit: prefer
  `SKILL.md` as an overview, keep reference files one level deep, and split out
  detail when the main file grows too large.
- Claude Code subagents are Markdown files with YAML frontmatter.
- Scope matters: project subagents live in `.claude/agents/`, user subagents in
  `~/.claude/agents/`.
- In Claude Code subagents, `name` and `description` are required.
- `tools` is optional and inherits the parent tool set when omitted.
- Preserve supported Claude frontmatter fields when they are part of the
  current contract instead of flattening them into generic prose.

Prompting guidance to apply when relevant:

- Make instructions explicit and specific.
- Use clear structure when the prompt mixes instructions, examples, and data.
- Use examples only when they materially sharpen the intended behavior.
- Prefer evaluation and real-use iteration over speculative process buildup.

## Cross-Vendor Guardrails

- Do not assume OpenAI skill metadata and Claude subagent frontmatter share the
  same field surface.
- Do not copy a vendor-specific rule from one ecosystem into another without an
  official source.
- Keep portable guidance in the main flow and isolate vendor-specific rules.
- If official docs are silent, make the smallest reasonable decision and note
  the gap briefly instead of inventing a hard rule.

## Official Sources

OpenAI:

- Codex skills: https://developers.openai.com/codex/skills
- Codex subagents: https://developers.openai.com/codex/subagents
- Prompt engineering: https://developers.openai.com/api/docs/guides/prompt-engineering

Anthropic:

- Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Claude Code subagents: https://code.claude.com/docs/en/sub-agents
- Claude Code settings and scopes: https://code.claude.com/docs/en/settings
- Prompt engineering overview: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- System prompts: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts
- Use XML tags: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
- Multishot prompting: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting
