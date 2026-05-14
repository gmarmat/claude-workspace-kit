---
name: startnow
description: "[Workspace] Load multi-project workspace context — scans all project states (including new upstream commits since your last session), reads workspace arch.md and rules."
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

1. Note the current working directory (workspace root: `personal/`).
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
5. **If the project is a git repo with a remote**, check upstream activity:
   - Run `git fetch --quiet` to update remote refs (silent on failure: offline, no auth, no remote configured — all skipped silently)
   - Run `git log --oneline HEAD..@{u}` to count commits on the upstream branch not yet in local `HEAD`
   - Capture distinct authors via `git log --pretty=format:'%an' HEAD..@{u} | sort -u | head -3`
   - If any commit touched `docs/arch.md`, `CLAUDE.md`, or `.claude/skills/`, note this — those projects need their context re-read before working on them

This per-project upstream check is what makes the workspace summary actionable: when you sit down to a workspace with many projects, you immediately see which ones changed since you last looked.

### Step 4: Read Key Config Files

For any project the user is likely to work on:
1. `package.json` — dependencies, scripts, project name
2. `tsconfig.json` or equivalent — language config
3. `.env.example` — note which vars exist (NEVER read values)

### Step 5: Summarize Context

Present a concise summary with TWO parts:

**Part 1 — Tree view** showing the workspace layout at a glance. Include all project folders, key subfolders (content staging, skills, docs), and 1-line descriptions. Example:

```
ai-projects/
├── CLAUDE.md                    ← Workspace rules + project index
├── profile/                     ← GitHub profile README
├── home-renovation/             ← Planning docs (non-code project)
├── project-a/                   ← Example web app (Next.js + Supabase)
│   ├── docs/                    ←   Architecture + feature docs
│   └── .claude/skills/          ←   Project-specific skills
├── project-b/                   ← Example mobile app
│   └── docs/                    ←   Project docs
└── kit/                         ← Claude Code bootstrap kit (read-only)
```

Build this tree dynamically from what you find on disk — don't hardcode it. Show projects with a 1-line description pulled from CLAUDE.md's project table. For projects with subfolders of interest (content dirs, skills, docs), expand one level deeper.

**Part 2 — Status table** for git-tracked projects. The `New Upstream` column shows commits on origin not yet pulled locally — that's where you should look first when returning to a workspace:

```
| Folder | Branch | Last Commit | New Upstream | Has Skills |
|--------|--------|-------------|--------------|------------|
| project-a | main | feat: new feature (2h ago) | 0 | 8 skills |
| project-b | main | fix: auth redirect (3d ago) | 3 by @teammate ⚠ docs | 4 skills |
| project-c | feat/x | wip: experiment (1w ago) | no remote | 2 skills |
```

The `⚠ docs` flag on a row means upstream commits touched architecture docs, CLAUDE.md, or skills — your local mental model of that project may be stale. Re-read its arch.md before starting work there.

Then:
```
Available skills: /advise, /startnow, /updatenow, /l3, /audit, /localcompact
                  + project-specific skills when working inside a subfolder

What are we working on today?
```

### If the User Picks a Specific Project

When the user says they want to work on a specific project (e.g., "let's work on my-app"):

1. **Read that project's CLAUDE.md** to load its rules and constraints
2. **Read that project's docs/arch.md** to load its architecture context
3. **Note which project-specific skills are available** in that project's `.claude/skills/`
4. **Use that project's conventions** for the rest of the session — its skill prefixes, its patterns, its rules
5. **Tell the user** what project-specific skills they have access to

This ensures that even when launched from the workspace root, Claude works within the correct project context. The workspace-level `[Workspace]` skills remain available as fallbacks, but project-specific `[ProjectName]` skills take priority for that session.

## Important Notes

- This is a **read-only** skill — do NOT modify any files
- Do NOT read `.env` values — only note which env vars are configured
- Keep the summary concise — the user wants to start working, not read a report
- If a project has no architecture doc, note it and suggest creating one
- The per-project upstream check (Step 3 sub-step 5) is read-only against each project's remote. `git fetch` only updates local refs, never modifies remote. If the network is down or any project's remote is unreachable, skip that project's upstream check silently without erroring out
- Workspaces with many projects: per-project `git fetch` runs sequentially. With 10-20 projects this typically completes in under 30 seconds. If a workspace becomes too large for this to feel snappy, consider adding a `--no-fetch` argument to skip the upstream check on demand
