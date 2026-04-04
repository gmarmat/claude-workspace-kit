---
name: updatenow
description: "[Workspace] Update workspace-level CLAUDE.md and docs/arch.md with recent changes across projects."
argument-hint: [optional note, e.g. "added new project folder"]
disable-model-invocation: false
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# UpdateNow — Workspace & Architecture Doc Updater

You maintain the workspace's living documentation. When invoked, you review the current session's changes and update all applicable docs to stay current.

## What You Update

### 1. Workspace-Level `CLAUDE.md`

**Purpose:** Project index and workspace rules. Update the Projects table when projects are added, removed, or their status changes significantly.

### 2. `docs/arch.md` — Workspace Architecture Index

**Purpose:** LLM-optimized overview of all projects and cross-cutting concerns. Keep lean (<300 lines).

**Version rules:**
- Version numbers: major.minor (e.g. 1.3). Bump minor for most changes, major for reorganizations
- Date format: YYYY-MM-DD

**What to update based on change type:**

| Change Type | Sections to Update |
|------------|-------------------|
| New project added | Project Index, Version History |
| Project reorganized/moved | Project Structure, Version History |
| Cross-project pattern identified | Key Patterns, Version History |
| New shared tooling/config | Tech Stack, Version History |
| Project completed/archived | Project Index status, Version History |

### 3. Project-Level `docs/arch.md` and `docs/features/*.md`

If changes were made within a specific project that has its own docs:
- Update that project's arch.md and feature docs following the same patterns
- Bump version, update date, add version history entry

### 4. Workspace-Kit Drift Check

After updating workspace docs, check if any **structural changes** were made that should be reflected back in the workspace-kit source repo:

| What Changed | Action |
|-------------|--------|
| New skill added to workspace `.claude/skills/` | Flag: "New skill — consider adding to workspace-kit" |
| CLAUDE.md rules section changed (not project table) | Flag: "Workspace rules updated — review workspace-kit template" |
| docs/plans/new-project-checklist.md changed | Flag: "Checklist updated — sync to workspace-kit" |
| New workflow pattern established | Flag: "New pattern — consider adding to workspace-kit defaults" |

**Don't auto-sync.** Just report drift at the end of the update so the user can decide.

## Execution Steps

### Step 1: Gather Context

1. Check what changed this session — look at recent activity across project folders
2. Read the current workspace CLAUDE.md to see the project table
3. If the user provided a specific note, use that as the primary change description

### Step 2: Update Workspace Docs

1. Update CLAUDE.md project table if projects were added/changed
2. Update docs/arch.md if it exists — surgical edits only
3. Bump version and date

### Step 3: Update Project-Level Docs (if applicable)

1. Identify which project was changed
2. Read and update that project's docs following its own conventions
3. If the project has no docs yet, suggest creating them

### Step 4: Check Workspace-Kit Drift

1. Compare current workspace skills against the workspace-kit repo (if it exists locally)
2. Flag any structural changes (new skills, rule changes, template updates)
3. Report drift findings

### Step 5: Report

```
Updated:
  - CLAUDE.md: [what changed]
  - docs/arch.md vX.Y → vX.Z: [what changed]
  - [project]/docs/arch.md: [what changed]

Workspace-kit drift:
  - [any flagged changes, or "No drift detected"]
```

## Important Notes

- NEVER delete existing content unless it's factually wrong or superseded
- NEVER change document structure or section ordering
- NEVER add emojis to documents
- When in doubt about whether a change warrants a doc update, skip it
- Keep workspace-level docs lean — details belong in project-level docs
