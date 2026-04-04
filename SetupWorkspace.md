# Workspace Setup — Initialize Your AI Projects Workspace

You are a workspace initialization agent. When a user points Claude Code at this repo and asks you to set it up, follow these phases sequentially. Each phase must complete before the next begins.

## Prerequisites

- Claude Code CLI installed (`npm i -g @anthropic-ai/claude-code`)
- Git installed
- Node.js installed (for Claude Code and project tooling)

---

## Phase 1: Gather Info

Ask the user:

1. **Where should the workspace live?** (default: `~/ai-projects/`)
2. **Your name?** (used in CLAUDE.md personalization)
3. **Do you want user subfolders?** (e.g., separate folders for different people sharing the machine — like `gaurav/`, `tara/`)
4. **Any MCP servers to configure?** (Supabase, Railway, Vercel — can add later)

Don't over-ask. If the user says "just set it up" — use defaults and let them customize later.

---

## Phase 2: Create Workspace Structure

Using the templates in this repo, create:

```
[workspace-path]/
├── CLAUDE.md                           ← From templates/CLAUDE.md.template
├── docs/
│   ├── arch.md                         ← From templates/arch.md.template
│   ├── features/                       ← Empty, ready for workspace-level feature docs
│   └── plans/
│       └── new-project-checklist.md    ← From docs/plans/new-project-checklist.md
├── .claude/
│   ├── settings.local.json             ← From templates/settings.local.json.template
│   └── skills/
│       ├── startnow/SKILL.md           ← From skills/startnow/SKILL.md
│       ├── updatenow/SKILL.md          ← From skills/updatenow/SKILL.md
│       ├── advise/SKILL.md             ← From skills/advise/SKILL.md
│       ├── l3/SKILL.md                 ← From skills/l3/SKILL.md
│       ├── audit/SKILL.md              ← From skills/audit/SKILL.md
│       ├── localcompact/SKILL.md       ← From skills/localcompact/SKILL.md
│       └── newproject/SKILL.md         ← From skills/newproject/SKILL.md
└── [user-subfolders]/                  ← If requested (e.g., gaurav/, tara/)
```

### Customization During Copy

When copying templates, replace these placeholders:

| Placeholder | Replace With |
|-------------|-------------|
| `{{WORKSPACE_NAME}}` | User's chosen workspace name (default: "AI Projects Workspace") |
| `{{WORKSPACE_PATH}}` | Absolute path to workspace (default: `~/ai-projects/`) |
| `{{USER_NAME}}` | User's name |
| `{{DATE}}` | Today's date (YYYY-MM-DD) |
| `{{KIT_REPO_URL}}` | `https://github.com/gmarmat/claude-project-kit` |

---

## Phase 3: Personalize CLAUDE.md

1. Fill in the workspace name and purpose
2. If user subfolders were created, add them to the Projects table
3. Keep all workflow rules, documentation rules, and skills convention as-is — these are battle-tested defaults
4. Ask if the user wants to customize communication style (default is concise + tables)

---

## Phase 4: Verify Setup

1. List the created files and confirm with the user
2. Show the available skills:
   ```
   /startnow      — Load workspace context at session start
   /updatenow     — Update docs after changes
   /advise        — Research + recommend before decisions
   /l3            — Debug/investigate issues
   /audit         — Project health check
   /localcompact  — Keep arch.md under 300 lines
   /newproject    — Scaffold a new project (uses claude-project-kit)
   ```
3. Tell the user:
   ```
   Workspace ready! Next steps:
     1. cd [workspace-path]
     2. claude
     3. Run /startnow to see your workspace
     4. Run /newproject [name] to create your first project

   Your first project will be bootstrapped using the claude-project-kit templates.
   Claude will walk you through the full setup (PRD, architecture, skills).
   ```

---

## Phase 5: Optional — Configure MCP Servers

If the user wants MCP servers:
1. **Supabase:** `npx -y @anthropic-ai/claude-code mcp add supabase -- npx -y @anthropic-ai/supabase-mcp`
2. **Railway:** `claude mcp add railway -- npx -y @anthropic-ai/railway-mcp`

These are added to the user's global Claude config, not the workspace.

---

## Important Rules

- **This repo is a setup tool, not the workspace itself.** The workspace is created at the user's chosen path.
- **Don't initialize git in the workspace.** Each project inside manages its own git repo.
- **Don't modify this repo** during setup — only read from it.
- **Skills are copied as-is** — they're already generic. No customization needed at workspace level.
- **The project kit is separate.** `/newproject` will clone `claude-project-kit` from GitHub when the user creates their first project.
