# Claude Workspace Kit

A workspace scaffolding tool for [Claude Code](https://claude.ai/claude-code). Sets up a multi-project `ai-projects/` folder with built-in skills for context management, documentation, research, debugging, and project creation.

## What This Creates

```
ai-projects/
├── CLAUDE.md                    ← Workspace rules + project index
├── docs/
│   ├── arch.md                  ← Architecture overview (<300 lines)
│   ├── features/                ← Workspace-level feature docs
│   └── plans/                   ← Research & decision docs
├── .claude/
│   ├── settings.local.json      ← Tool permissions
│   └── skills/                  ← 7 workspace management skills
│       ├── startnow/            ← Load context at session start
│       ├── updatenow/           ← Update docs after changes
│       ├── advise/              ← Research + recommend
│       ├── l3/                  ← Debug/investigate
│       ├── audit/               ← Health check
│       ├── localcompact/        ← Keep docs lean
│       └── newproject/          ← Create new projects
└── [your-projects]/             ← Each with own git repo + skills
```

## Quick Start

### Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed
- Git and Node.js installed

### Setup

```bash
git clone https://github.com/gmarmat/claude-workspace-kit.git
cd claude-workspace-kit
claude
```

Then tell Claude:

> Read SetupWorkspace.md and set up my workspace.

Claude will walk you through:
1. Where to create the workspace
2. Folder structure and skills
3. Optional user subfolders (for shared machines)
4. MCP server configuration

### After Setup

```bash
cd ~/ai-projects    # or wherever you chose
claude
```

**Start every session with:** `/startnow`

**Create your first project:** `/newproject my-app`

This clones [claude-project-kit](https://github.com/gmarmat/claude-project-kit) and walks you through a full project bootstrap (PRD, architecture, skills).

## Skills Reference

| Skill | Purpose |
|-------|---------|
| `/startnow` | Load workspace context — tree view + project status |
| `/updatenow` | Update workspace docs after changes |
| `/advise [topic]` | Research a domain, present options with costs/risks |
| `/l3 [error]` | Systematic debugging across projects |
| `/audit [focus]` | Security, cost, performance, quality health check |
| `/localcompact` | Keep arch.md under 300 lines |
| `/newproject [name]` | Scaffold new project from idea or PRD |

## How It Works

**Workspace** manages multiple projects — context loading, cross-project patterns, documentation.

**Projects** (created via `/newproject`) are independent — own git repo, own skills, own conventions. Project skills can override workspace skills.

```
Workspace Skills (this kit)          Project Skills (project kit)
├── /startnow (multi-project view)   ├── /startnow (single project)
├── /updatenow (workspace docs)      ├── /updatenow (project docs)
├── /advise (cross-project)          ├── /advise (project-specific)
├── /l3 (workspace-aware)            ├── /l3 (project-focused)
├── /audit                           └── (+ domain commands)
├── /localcompact
└── /newproject
```

## Companion Repo

- **[claude-project-kit](https://github.com/gmarmat/claude-project-kit)** — Public template for bootstrapping individual projects. Used by `/newproject`.

## License

MIT
