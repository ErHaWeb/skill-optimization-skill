#!/usr/bin/env python3
"""Verify the local maintenance contract of the skill-optimization skill."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ".gitignore",
    "README.md",
    "SKILL.md",
    "agents/openai.yaml",
    "evals/README.md",
    "evals/evals.json",
    "evals/files/claude-subagent/.claude/agents/release-notes-subagent.md",
    "references/official-vendor-baseline.md",
    "references/skill-quality-baseline.md",
    "scripts/verify_skill_contract.py",
]

FORBIDDEN_FILES = [
    "evals/files/claude-subagent/release-notes-subagent.md",
]

REQUIRED_GITIGNORE_ENTRIES = {
    ".DS_Store",
    ".idea",
    "__pycache__/",
}

SKILL_SUPPORT_PATHS = [
    "agents/openai.yaml",
    "references/skill-quality-baseline.md",
    "references/official-vendor-baseline.md",
    "evals/evals.json",
    "scripts/verify_skill_contract.py",
]

README_SUPPORT_PATHS = [
    "agents/openai.yaml",
    "references/skill-quality-baseline.md",
    "references/official-vendor-baseline.md",
    "evals/README.md",
    "evals/evals.json",
    "scripts/verify_skill_contract.py",
]

EXPECTED_EVAL_IDS = set(range(1, 19))

OFFICIAL_URLS = [
    "https://developers.openai.com/codex/skills",
    "https://developers.openai.com/codex/subagents",
    "https://developers.openai.com/api/docs/guides/prompt-engineering",
    "https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview",
    "https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices",
    "https://code.claude.com/docs/en/sub-agents",
    "https://code.claude.com/docs/en/settings",
    "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview",
]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def verify_files_exist(errors: list[str]) -> None:
    for relative_path in REQUIRED_FILES:
        require((ROOT / relative_path).is_file(), f"Missing required file: {relative_path}", errors)

    for relative_path in FORBIDDEN_FILES:
        require(not (ROOT / relative_path).exists(), f"Unexpected stale file present: {relative_path}", errors)


def verify_local_artifacts(errors: list[str]) -> None:
    ds_store_paths = [
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob(".DS_Store")
        if ".git" not in path.parts
    ]
    require(not ds_store_paths, f"Unexpected .DS_Store artifacts present: {', '.join(ds_store_paths)}", errors)


def verify_gitignore(errors: list[str]) -> None:
    entries = set(read_text(".gitignore").splitlines())
    for entry in REQUIRED_GITIGNORE_ENTRIES:
        require(entry in entries, f".gitignore must include: {entry}", errors)


def verify_references(errors: list[str]) -> None:
    skill_text = read_text("SKILL.md")
    readme_text = read_text("README.md")

    for support_path in SKILL_SUPPORT_PATHS:
        require(support_path in skill_text, f"SKILL.md does not mention support path: {support_path}", errors)

    for support_path in README_SUPPORT_PATHS:
        require(readme_text.count(support_path) >= 1, f"README.md does not mention support path: {support_path}", errors)

    require(
        "python3 scripts/verify_skill_contract.py" in skill_text,
        "SKILL.md must tell maintainers when to run the verifier",
        errors,
    )
    require(
        "python3 scripts/verify_skill_contract.py" in readme_text,
        "README.md must tell maintainers to rerun the verifier after contract changes",
        errors,
    )


def verify_vendor_baseline(errors: list[str]) -> None:
    text = read_text("references/official-vendor-baseline.md")

    require(
        "1. Official OpenAI or Anthropic documentation for the target surface" in text,
        "Vendor baseline must define the official-docs-first authority order",
        errors,
    )
    require(
        "`agents/openai.yaml` is optional Codex metadata" in text,
        "Vendor baseline must keep Codex agent metadata optional",
        errors,
    )
    require(
        "`tools` is optional" in text,
        "Vendor baseline must preserve the optional Claude Code tools rule",
        errors,
    )

    for url in OFFICIAL_URLS:
        require(url in text, f"Vendor baseline is missing official source URL: {url}", errors)


def verify_evals(errors: list[str]) -> None:
    payload = json.loads(read_text("evals/evals.json"))
    require(payload.get("skill_name") == "skill-optimization", "Unexpected eval skill_name", errors)

    evals = payload.get("evals")
    require(isinstance(evals, list), "evals/evals.json must contain an 'evals' list", errors)
    if not isinstance(evals, list):
        return

    actual_ids = {item.get("id") for item in evals if isinstance(item, dict)}
    require(EXPECTED_EVAL_IDS.issubset(actual_ids), "Expected eval ids 1 through 18", errors)

    indexed = {item.get("id"): item for item in evals if isinstance(item, dict)}

    claude_eval = indexed.get(8, {})
    require(
        ".claude/agents/release-notes-subagent.md" in claude_eval.get("prompt", ""),
        "Eval 8 must point at the Claude project-scope fixture path",
        errors,
    )
    require(
        "Treats the Claude Code tools field as optional rather than mandatory boilerplate"
        in claude_eval.get("assertions", []),
        "Eval 8 must defend the optional Claude tools contract",
        errors,
    )

    metadata_eval = indexed.get(15, {})
    require(
        "agents/openai.yaml" in metadata_eval.get("prompt", ""),
        "Eval 15 must cover agent metadata drift",
        errors,
    )
    require(
        "Does not add new eval scenarios when metadata alignment is the only uncovered gap"
        in metadata_eval.get("assertions", []),
        "Eval 15 must defend metadata-only hardening without eval churn",
        errors,
    )

    vendor_eval = indexed.get(18, {})
    require(
        "official OpenAI and Anthropic documentation" in vendor_eval.get("prompt", ""),
        "Eval 18 must cover official vendor documentation as authority",
        errors,
    )
    require(
        "Treats official Anthropic and OpenAI documentation as the authority for vendor-specific behavior when the edit depends on those semantics"
        in vendor_eval.get("assertions", []),
        "Eval 18 must defend the official vendor baseline",
        errors,
    )


def verify_agent_metadata(errors: list[str]) -> None:
    text = read_text("agents/openai.yaml")

    require('display_name: "Skill Optimization"' in text, "Agent metadata display name drifted", errors)
    require("Use $skill-optimization" in text, "Agent metadata must reference $skill-optimization", errors)
    require("agents/openai.yaml" in text, "Agent metadata must mention agent metadata alignment", errors)
    require("Claude Code subagent" in text, "Agent metadata must mention Claude Code subagent hardening", errors)
    require(
        "Anthropic/OpenAI docs as binding for vendor-specific behavior" in text,
        "Agent metadata must mention the official vendor baseline",
        errors,
    )


def verify_claude_fixture(errors: list[str]) -> None:
    text = read_text("evals/files/claude-subagent/.claude/agents/release-notes-subagent.md")

    require(text.startswith("---\n"), "Claude fixture must start with YAML frontmatter", errors)
    require("name: release-notes-subagent" in text, "Claude fixture name drifted", errors)
    require("description: >" in text, "Claude fixture must keep multiline description frontmatter", errors)
    require("model: haiku" in text, "Claude fixture model field drifted", errors)
    require("maxTurns: 3" in text, "Claude fixture maxTurns field drifted", errors)
    require("# Release Notes Subagent" in text, "Claude fixture heading drifted", errors)
    require("tools:" not in text, "Claude fixture should omit tools to defend the optional-tools rule", errors)


def main() -> int:
    errors: list[str] = []

    verify_files_exist(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    verify_local_artifacts(errors)
    verify_gitignore(errors)
    verify_references(errors)
    verify_vendor_baseline(errors)
    verify_evals(errors)
    verify_agent_metadata(errors)
    verify_claude_fixture(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Skill contract OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
