#!/usr/bin/env python3
"""Inventory a local skill surface with deterministic structural checks."""

from __future__ import annotations

import json
from pathlib import Path
import sys


SUPPORT_DIRECTORIES = {
    "scripts": "scripts",
    "references": "references",
    "fixtures": "fixtures",
    "evals": "evals",
    "assets": "assets",
    "agents": "agents",
    "idea": ".idea",
}

SUPPORT_MENTION_PATTERNS = {
    "scripts": ("scripts/",),
    "references": ("references/",),
    "fixtures": ("fixtures/",),
    "evals": ("evals/",),
    "assets": ("assets/",),
    "agents": ("agents/", "agents/openai.yaml"),
    "agents_openai_yaml": ("agents/openai.yaml",),
}

DETERMINISTIC_WORKFLOW_TERMS = (
    "normalize",
    "normalization",
    "render",
    "validation",
    "validate",
    "export",
    "package",
    "packaging",
    "assemble",
    "assembly",
    "rename",
    "transform",
    "generate",
    "generation",
    "report assembly",
)

QA_SCRIPT_PREFIXES = ("verify", "validate", "check")
QA_SCRIPT_KEYWORDS = ("test", "lint")


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def resolve_target(target_arg: str) -> Path:
    return Path(target_arg).expanduser().resolve()


def determine_inspection_root(target: Path) -> Path:
    if target.is_dir():
        return target

    if (
        target.parent.name == "agents"
        and target.parent.parent.name == ".claude"
        and target.parent.parent.parent.exists()
    ):
        return target.parent.parent.parent

    return target.parent


def determine_target_kind(target: Path, inspection_root: Path) -> str:
    if target.is_file():
        if target.suffix == ".md" and target.parent.name == "agents" and target.parent.parent.name == ".claude":
            return "claude_subagent"
        return "file"

    if (inspection_root / "SKILL.md").is_file():
        return "skill_directory"

    return "directory"


def find_git_root(start: Path) -> Path | None:
    current = start if start.is_dir() else start.parent
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def read_primary_text(target: Path, inspection_root: Path) -> tuple[str, str | None]:
    if target.is_file():
        return target.read_text(encoding="utf-8"), target.name

    skill_file = inspection_root / "SKILL.md"
    if skill_file.is_file():
        return skill_file.read_text(encoding="utf-8"), "SKILL.md"

    return "", None


def collect_relative_paths(root: Path, pattern: str, want_dirs: bool | None = None) -> list[str]:
    matches: list[str] = []
    for path in root.rglob(pattern):
        if ".git" in path.parts:
            continue
        if want_dirs is True and not path.is_dir():
            continue
        if want_dirs is False and not path.is_file():
            continue
        matches.append(path.relative_to(root).as_posix())
    return sorted(matches)


def collect_script_paths(scripts_dir: Path, inspection_root: Path) -> list[str]:
    if not scripts_dir.is_dir():
        return []

    return sorted(
        path.relative_to(inspection_root).as_posix()
        for path in scripts_dir.rglob("*")
        if path.is_file()
    )


def collect_machine_checkable_contracts(inspection_root: Path, script_paths: list[str]) -> list[str]:
    contracts: list[str] = []

    if (inspection_root / "evals" / "evals.json").is_file():
        contracts.append("evals/evals.json")

    for relative_path in script_paths:
        name = Path(relative_path).name.lower()
        stem = Path(relative_path).stem.lower()
        if stem.startswith(QA_SCRIPT_PREFIXES) or any(keyword in name for keyword in QA_SCRIPT_KEYWORDS):
            contracts.append(relative_path)

    return sorted(dict.fromkeys(contracts))


def collect_support_mentions(primary_text: str) -> dict[str, bool]:
    lowered = primary_text.lower()
    mentions: dict[str, bool] = {}
    for key, patterns in SUPPORT_MENTION_PATTERNS.items():
        mentions[key] = any(pattern.lower() in lowered for pattern in patterns)
    return mentions


def collect_deterministic_terms(primary_text: str) -> list[str]:
    lowered = primary_text.lower()
    return [term for term in DETERMINISTIC_WORKFLOW_TERMS if term in lowered]


def collect_quality_gaps(
    inspection_root: Path,
    top_level_files: dict[str, bool],
    support_directories: dict[str, bool],
    support_mentions: dict[str, bool],
    machine_checkable_contracts: list[str],
    script_paths: list[str],
    script_paths_mentioned: list[str],
    deterministic_terms: list[str],
    ds_store_paths: list[str],
    node_modules_paths: list[str],
    claude_worktrees_paths: list[str],
    git_root: Path | None,
) -> list[str]:
    gaps: list[str] = []

    if not git_root:
        gaps.append("No Git context detected")

    if not top_level_files["gitignore"]:
        gaps.append("No local .gitignore detected")

    if not machine_checkable_contracts:
        gaps.append("No obvious machine-checkable QA contract detected")

    for key, present in support_directories.items():
        if key == "idea" or not present:
            continue
        if not support_mentions.get(key, False):
            gaps.append(f"{SUPPORT_DIRECTORIES[key]}/ exists but primary instructions do not mention when to use it")

    if top_level_files["agents_openai_yaml"] and not support_mentions.get("agents_openai_yaml", False):
        gaps.append("agents/openai.yaml exists but primary instructions do not mention it")

    if deterministic_terms and script_paths and not script_paths_mentioned:
        gaps.append("Deterministic workflow terms appear in primary instructions, but no script path is referenced")

    if ds_store_paths:
        gaps.append(".DS_Store artifacts present")

    if node_modules_paths:
        gaps.append("node_modules/ directories present")

    if claude_worktrees_paths:
        gaps.append(".claude/worktrees/ directories present")

    return gaps


def inspect(target: Path) -> dict[str, object]:
    inspection_root = determine_inspection_root(target)
    target_kind = determine_target_kind(target, inspection_root)
    git_root = find_git_root(inspection_root)
    primary_text, primary_source = read_primary_text(target, inspection_root)
    scripts_dir = inspection_root / "scripts"

    top_level_files = {
        "skill_md": (inspection_root / "SKILL.md").is_file(),
        "readme_md": (inspection_root / "README.md").is_file(),
        "gitignore": (inspection_root / ".gitignore").is_file(),
        "agents_openai_yaml": (inspection_root / "agents" / "openai.yaml").is_file(),
        "evals_json": (inspection_root / "evals" / "evals.json").is_file(),
    }

    support_directories = {
        key: (inspection_root / relative_path).is_dir()
        for key, relative_path in SUPPORT_DIRECTORIES.items()
    }

    support_mentions = collect_support_mentions(primary_text)
    script_paths = collect_script_paths(scripts_dir, inspection_root)
    script_paths_mentioned = [
        relative_path for relative_path in script_paths if relative_path.lower() in primary_text.lower()
    ]
    machine_checkable_contracts = collect_machine_checkable_contracts(inspection_root, script_paths)
    deterministic_terms = collect_deterministic_terms(primary_text)
    ds_store_paths = collect_relative_paths(inspection_root, ".DS_Store", want_dirs=False)
    node_modules_paths = collect_relative_paths(inspection_root, "node_modules", want_dirs=True)
    claude_worktrees_paths = collect_relative_paths(inspection_root, "worktrees", want_dirs=True)
    claude_worktrees_paths = [
        path for path in claude_worktrees_paths if path.endswith(".claude/worktrees") or "/.claude/worktrees/" in f"/{path}/"
    ]

    quality_gaps = collect_quality_gaps(
        inspection_root=inspection_root,
        top_level_files=top_level_files,
        support_directories=support_directories,
        support_mentions=support_mentions,
        machine_checkable_contracts=machine_checkable_contracts,
        script_paths=script_paths,
        script_paths_mentioned=script_paths_mentioned,
        deterministic_terms=deterministic_terms,
        ds_store_paths=ds_store_paths,
        node_modules_paths=node_modules_paths,
        claude_worktrees_paths=claude_worktrees_paths,
        git_root=git_root,
    )

    return {
        "target_path": str(target),
        "inspection_root": str(inspection_root),
        "target_kind": target_kind,
        "primary_instruction_source": primary_source,
        "git_context": {
            "present": git_root is not None,
            "root": str(git_root) if git_root else None,
        },
        "top_level_files": top_level_files,
        "support_directories": support_directories,
        "support_path_mentions": support_mentions,
        "machine_checkable_contracts": machine_checkable_contracts,
        "script_paths": script_paths,
        "script_paths_mentioned": script_paths_mentioned,
        "deterministic_workflow_terms": deterministic_terms,
        "local_artifacts": {
            "ds_store_paths": ds_store_paths,
            "node_modules_paths": node_modules_paths,
            "claude_worktrees_paths": claude_worktrees_paths,
        },
        "quality_gaps": quality_gaps,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        return fail("Usage: inspect_skill_surface.py <target-path>")

    target = resolve_target(argv[1])
    if not target.exists():
        return fail(f"Target does not exist: {target}")

    payload = inspect(target)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
