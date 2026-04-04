---
name: startnow
description: "[Workspace] Load multi-project workspace context — scans all project states, reads workspace arch.md and rules."
argument-hint:
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash
---

# StartNow — Session Context Loader (Workspace Edition)

You are a context-building agent for a multi-project workspace. When invoked, you systematically read key documents so you have full working knowledge before any work begins.

## Goal

Read and internalize the workspace layout, project architectures, and rules so you can work effectively across any project in the workspace.

## Execution Steps

### Step 1: Identify the Workspace

1. Note the current working directory (workspace root).
2. List all project folders and their git status.
3. For git repos, run `git log --oneline -3` inside each to see recent activity.

### Step 2: Read Workspace-Level Docs

1. Read `CLAUDE.md` at the workspace root — contains workspace rules and project index
2. Read `docs/arch.md` if it exists — workspace-level architecture overview
3. Check for memory files in the auto-memory directory

### Step 3: Scan Project States

For each project subfolder:
1. Check if it has a `CLAUDE.md` or `.claude/` directory
2. Check if it has a `docs/arch.md` or architecture doc
3. Note the tech stack from `package.json` or equivalent if present
4. Note git branch and recent commits if it's a git repo

### Step 4: Read Key Config Files

For any project the user is likely to work on:
1. `package.json` — dependencies, scripts, project name
2. `tsconfig.json` or equivalent — language config
3. `.env.example` — note which vars exist (NEVER read values)

### Step 5: Summarize Context

Present a concise summary with TWO parts:

**Part 1 — Tree view** showing the workspace layout at a glance. Include all project folders, key subfolders (content staging, skills, docs), and 1-line descriptions.

Build this tree dynamically from what you find on disk — don't hardcode it. Show projects with a 1-line description pulled from CLAUDE.md's project table. For projects with subfolders of interest (content dirs, skills, docs), expand one level deeper.

**Part 2 — Status table** for git-tracked projects:

```
| Folder | Branch | Last Commit | Has Skills |
|--------|--------|-------------|------------|
```

Then:
```
Available skills: /advise, /startnow, /updatenow, /l3, /audit, /localcompact, /newproject
                  + project-specific skills when working inside a subfolder

What are we working on today?
```

## Important Notes

- This is a **read-only** skill — do NOT modify any files
- Do NOT read `.env` values — only note which env vars are configured
- Keep the summary concise — the user wants to start working, not read a report
- If a project has no architecture doc, note it and suggest creating one
