# Claude Workspace Kit

A workspace scaffolding tool for [Claude Code](https://claude.ai/claude-code). Sets up a multi-project `ai-projects/` folder with built-in skills for context management, documentation, research, debugging, and project creation.

Built from patterns extracted across 10+ real projects — web apps, construction planning, career prep, AI content studios, and more. Not theoretical. Every pattern earned its place by surviving real production use.

---

## Philosophy: You Are the Architect

This kit is built on one principle: **you make the decisions, Claude handles the execution.**

This maps directly to what Andrej Karpathy calls [Agentic Engineering](https://addyosmani.com/blog/agentic-engineering/) — the structured successor to "vibe coding":

| Agentic Engineering Principle | How This Kit Implements It |
|-------------------------------|---------------------------|
| **Plan** before prompting | PRD-first workflow, `/advise` before every architecture decision |
| **Direct** with precision | Communication guide + doc references in every instruction |
| **Review** rigorously | Build loop — test locally, review each sub-task |
| **Test** systematically | `/audit` skill — security, cost, performance, quality |
| **Own** the architecture | `/updatenow` keeps docs current, you stay in control |

> **The difference between vibe coding and building real products is a system.** This kit is the workspace layer of that system.

---

## Why a Workspace Kit?

Most Claude Code starter kits handle a single project. But real work involves **multiple projects** running in parallel — each with its own git repo, tech stack, and conventions.

This kit solves the workspace problem:

| Challenge | How This Kit Solves It |
|-----------|----------------------|
| **Context switching** | `/startnow` loads ALL project states in one view |
| **Cross-project patterns** | Workspace CLAUDE.md inherits rules to all projects |
| **Documentation drift** | `/updatenow` syncs workspace index + project docs |
| **New project overhead** | `/newproject` scaffolds from templates in minutes |
| **Token waste** | arch.md stays under 300 lines at both levels |

---

## Two-Kit Architecture

This workspace kit works alongside [claude-project-kit](https://github.com/gmarmat/claude-project-kit):

```
Workspace Kit (this repo)              Project Kit (companion)
├── Sets up ai-projects/ folder        ├── Bootstraps individual projects
├── 7 workspace management skills      ├── 6 project development skills
├── Cross-project context              ├── Single-project focus
├── /newproject clones project kit     ├── StartHere.md guided bootstrap
└── Manages the forest                 └── Manages the trees
```

**Use the workspace kit** when you're managing multiple projects or tasks in one place.
**Use the project kit** when you're building a single standalone app.

---

## What This Creates

```
ai-projects/
├── CLAUDE.md                    ← Workspace rules + project index
├── docs/
│   ├── arch.md                  ← Architecture overview (<300 lines)
│   ├── features/                ← Workspace-level feature docs
│   ├── plans/                   ← Research & decision docs
│   └── meta/                    ← Guides: cheat sheet, anti-patterns, etc.
├── .claude/
│   ├── settings.local.json      ← Tool permissions
│   └── skills/                  ← 7 workspace management skills
│       ├── startnow/            ← Load context at session start
│       ├── updatenow/           ← Update docs after changes
│       ├── advise/              ← Research + recommend
│       ├── ingest/              ← Process knowledge sources
│       ├── l3/                  ← Debug/investigate
│       ├── audit/               ← Health check + staleness detection
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

---

## Tutorial: Set Up Your Workspace

New to this? Follow [TUTORIAL.md](TUTORIAL.md) — a guided 30-minute walkthrough that sets up a workspace with two mini-projects and teaches you the workspace management workflow.

---

## Skills Reference

| Skill | Purpose |
|-------|---------|
| `/startnow` | Load workspace context — tree view + project status |
| `/updatenow` | Update workspace docs after changes |
| `/advise [topic]` | Research a domain, present options with costs/risks |
| `/ingest [source]` | Process articles, research, or docs into structured knowledge with cross-references |
| `/l3 [error]` | Systematic debugging across projects |
| `/audit [focus]` | Security, cost, performance, quality, staleness health check |
| `/localcompact` | Keep arch.md under 300 lines |
| `/newproject [name]` | Scaffold new project from idea or PRD |

---

## Learnings & Guides

Extracted from real project experience. Find them in `docs/meta/`:

| Guide | What It Covers |
|-------|---------------|
| [Cheat Sheet](docs/meta/cheat-sheet.md) | 1-page quick reference for workspaces |
| [Communication Guide](docs/meta/communication-guide.md) | How to give Claude good instructions |
| [Anti-Patterns](docs/meta/anti-patterns.md) | 12 common mistakes and what to do instead |
| [Memory Guide](docs/meta/memory-guide.md) | What to store in auto-memory, what not to |
| [Domain Skill Design](docs/meta/domain-skill-design.md) | Advanced patterns: routing, chaining, two-tier models |
| [Workflow Evolution](docs/meta/workflow-evolution.md) | How your daily routine changes with /ingest and staleness detection |

---

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

---

## Works for Non-Code Projects Too

This workspace pattern works for any multi-project workflow — not just code:

| Project Type | What Skills Help With |
|-------------|----------------------|
| Construction planning | Contractor comparison, permit tracking, budget management |
| Career prep | Resume tailoring, interview prep, company research |
| Content creation | Story writing, content pipelines, multi-language publishing |
| Course development | Class structure, lesson plans, teaching materials |
| Home infrastructure | Device audits, network troubleshooting, documentation |

The same documentation system, build loop, and research workflow apply regardless of domain.

---

## Companion Repo

- **[claude-project-kit](https://github.com/gmarmat/claude-project-kit)** — Public template for bootstrapping individual projects. Used by `/newproject`.

## License

MIT

---

**Created by [gmarmat](https://github.com/gmarmat)**
