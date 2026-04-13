# Claude Code Cheat Sheet (Workspace Edition)

One-page quick reference for multi-project workspaces.

---

## Session Workflow (Every Time)

```
/startnow           → Load workspace context (all projects)
[work on a project] → One feature at a time
commit              → After each sub-task (in the project's git repo)
/updatenow          → Update workspace + project docs
```

## Workspace Skills

| Skill | When | What It Does |
|-------|------|-------------|
| `/startnow` | Start of session | Tree view of all projects + status table |
| `/updatenow` | After any change | Updates workspace arch.md + project index |
| `/advise [topic]` | Before decisions | Cross-project research + recommendation |
| `/l3 [error]` | When broken | Debug across project boundaries |
| `/audit [area]` | Periodically | Health check across all projects |
| `/localcompact` | Docs too long | Trim arch.md back under 300 lines |
| `/newproject [name]` | New project | Scaffold from claude-project-kit templates |

## Document Hierarchy (Two Layers)

```
Workspace level:
  CLAUDE.md           = Workspace rules (inherited by all projects)
  docs/arch.md        = Cross-project index (<300 lines)

Project level (each subfolder):
  CLAUDE.md           = Project rules (can override workspace)
  docs/arch.md        = Project architecture (<300 lines)
  docs/PRD.md         = Project requirements
  docs/features/*.md  = Feature deep-dives
  docs/plans/*.md     = Research & decisions
```

## The Build Loop

```
/startnow → Pick project → /advise (if needed) → Build → Test → Commit → /updatenow → Repeat
```

## Golden Rules

1. **No git at workspace level** — each project manages its own repo
2. **Workspace CLAUDE.md inherits down** — common rules apply everywhere
3. **Project CLAUDE.md can override** — each project has its own conventions
4. **Kit folder is read-only** — templates for bootstrapping, never modified
5. **One feature at a time** — even across projects
6. **Commit in the project repo** — not at workspace level
7. **/updatenow updates both levels** — workspace index + project docs
