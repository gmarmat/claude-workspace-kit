# Claude Workspace Kit

A workspace scaffolding tool for Claude Code. Sets up multi-project `ai-projects/` folders with built-in skills, templates, and cross-project context management.

## About This Repo

This is a **scaffolding kit** — it ships templates and skills that get copied into a user's workspace during setup. The kit itself is the source, not a workspace.

| What Ships | Purpose |
|------------|---------|
| `SetupWorkspace.md` | Guided workspace setup (entry point) |
| `TUTORIAL.md` | Guided walkthrough |
| `templates/CLAUDE.md.template` | Workspace rules template |
| `templates/arch.md.template` | Workspace architecture template |
| `templates/settings.local.json.template` | Permissions template |
| `skills/` | 8 workspace-level skills |
| `docs/meta/` | Guides (cheat sheet, anti-patterns, memory, domain skills) |
| `docs/plans/` | New project checklist |

## Part of the Kit Ecosystem

| Kit | Purpose |
|-----|---------|
| claude-project-kit | Bootstrap **new** projects |
| **claude-workspace-kit** (this repo) | Manage **multi-project** workspaces |
| claude-project-rehab | Assess + upgrade **existing** projects, guide **new** ideas |
| claude-pm-kit | **PM Twin** — digital peer product manager |

## Rules for Contributing

- Skills use `[Workspace]` prefix in descriptions
- Templates have `<!-- CUSTOMIZE -->` markers — intentional, don't remove
- `docs/meta/` guides ship with the kit but are reference material
- `/newproject` skill depends on `claude-project-kit` being available (locally or via GitHub)
- No personal data in any file
