---
name: release-summary
description: >
  Help prepare a release summary from the repository changelog and release
  metadata.
---

# Release Summary

Use this skill when asked to produce `dist/release-summary.md`.

## Workflow

1. Read `CHANGELOG.md`, `meta/release.json`, and `notes/raw.md`.
2. Normalize the headings, sort the bullet groups, rename the frontmatter
   keys, and render the final markdown yourself.
3. If the result looks right, say the summary is ready.

`scripts/render_release_summary.py` exists, but it is only an optional
maintainer helper and does not need to be part of the default workflow.
