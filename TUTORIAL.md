# Tutorial: Set Up Your Workspace in 30 Minutes

> **Time:** ~30 minutes | **Result:** A working multi-project workspace | **Prerequisite:** Claude Code CLI installed

This tutorial walks you through creating a workspace, adding two mini-projects, and practicing the workspace management workflow. By the end, you'll have a functional workspace and understand how the two-layer system (workspace + projects) works together.

---

## What You'll Learn

| Step | Concept | Skill Used |
|------|---------|-----------|
| 1 | Workspace setup | `SetupWorkspace.md` |
| 2 | Creating projects | `/newproject` |
| 3 | Multi-project context | `/startnow` |
| 4 | Cross-project docs | `/updatenow` |
| 5 | Research workflow | `/advise` |
| 6 | Workspace vs project skills | Both layers |

---

## Before You Start

1. Install Claude Code: `npm i -g @anthropic-ai/claude-code`
2. Clone this repo:
   ```bash
   git clone https://github.com/gmarmat/claude-workspace-kit.git
   cd claude-workspace-kit
   ```
3. Have a GitHub account ready

---

## Step 1: Create Your Workspace

Launch Claude Code:

```bash
claude
```

Tell Claude:

> Read SetupWorkspace.md and set up my workspace at ~/ai-projects

Claude walks you through:
- Creating the folder structure
- Copying skills and templates
- Personalizing CLAUDE.md
- Verifying everything works

When done, navigate to your new workspace:

```bash
cd ~/ai-projects
claude
```

Run `/startnow` to see your empty workspace. You should see a tree view with no projects yet.

> **What just happened:** You created a workspace with 7 management skills, a CLAUDE.md with your rules, and a docs/ folder ready for cross-project documentation.

---

## Step 2: Create Your First Project

Tell Claude:

```
/newproject todo-app
```

Describe the project when asked:

> A simple task manager. Users create, edit, delete, and complete tasks. Tech stack: Next.js, Tailwind, Supabase.

Claude will clone [claude-project-kit](https://github.com/gmarmat/claude-project-kit) and walk you through the project bootstrap (PRD, arch.md, skills). Follow the prompts — this takes about 10 minutes.

When done, your workspace looks like:

```
ai-projects/
├── CLAUDE.md
├── docs/arch.md
├── .claude/skills/          ← 7 workspace skills
└── todo-app/                ← Your first project
    ├── CLAUDE.md            ← Project-specific rules
    ├── docs/arch.md         ← Project architecture
    └── .claude/skills/      ← 6 project skills
```

> **Key concept: Two-layer skills.** The workspace has `/startnow` that shows all projects. The project has its own `/startnow` that shows just that project's context. When you're inside `todo-app/`, the project skills take precedence.

---

## Step 3: Create a Second Project

Now add a second project to see the workspace pattern:

```
/newproject recipe-tracker
```

> A personal recipe collection. Save recipes with ingredients and instructions. Simple CRUD, no auth. Same stack as todo-app.

Follow the bootstrap again. Now your workspace has two projects:

```
ai-projects/
├── todo-app/
└── recipe-tracker/
```

---

## Step 4: Experience Multi-Project Context

From the workspace root (`~/ai-projects`), run:

```
/startnow
```

Claude now shows you a **tree view** of both projects with their status — branches, last commits, what skills each has. This is the workspace-level context that doesn't exist in single-project kits.

> **Why this matters:** When you switch between projects, you don't lose context. `/startnow` at the workspace level gives you the full picture in seconds.

---

## Step 5: Practice Cross-Project Research

Use `/advise` at the workspace level:

```
/advise Both projects use Supabase. Should they share a Supabase instance or have separate ones? Consider cost, data isolation, and simplicity.
```

Claude researches the question considering **both** projects. The recommendation gets saved to `docs/plans/` at the workspace level — available to all projects.

> **Key difference from project-level /advise:** Workspace-level research considers cross-project implications. Project-level research focuses on one project's constraints.

---

## Step 6: Update Workspace Docs

After setting up both projects, run:

```
/updatenow
```

Claude updates the workspace `docs/arch.md` with:
- Both projects in the project index
- Their tech stacks, git status, and skill counts
- Version history entry

Check `docs/arch.md` — it should be a compact index of your entire workspace.

> **Why this matters:** As you add projects and make changes, `/updatenow` keeps the workspace index current. Future sessions start with accurate context, not stale information.

---

## What You Just Practiced

| Concept | What You Did |
|---------|-------------|
| **Workspace setup** | Created the multi-project folder structure with skills |
| **Project scaffolding** | Used `/newproject` to bootstrap two projects from templates |
| **Two-layer context** | Saw workspace `/startnow` vs project `/startnow` |
| **Cross-project research** | Used workspace-level `/advise` for a decision affecting both projects |
| **Documentation sync** | Used `/updatenow` to keep workspace arch.md current |

---

## Next Steps

1. **Build features** — `cd todo-app && claude` → follow the project kit's [TUTORIAL.md](https://github.com/gmarmat/claude-project-kit/blob/main/TUTORIAL.md) to build actual features
2. **Add more projects** — `/newproject` for anything: code, planning docs, research
3. **Read the guides** in `docs/meta/`:
   - [Cheat Sheet](docs/meta/cheat-sheet.md) — 1-page workspace reference
   - [Communication Guide](docs/meta/communication-guide.md) — give Claude better instructions
   - [Anti-Patterns](docs/meta/anti-patterns.md) — mistakes to avoid
   - [Memory Guide](docs/meta/memory-guide.md) — what to store across sessions
   - [Domain Skill Design](docs/meta/domain-skill-design.md) — create your own custom skills
4. **Try non-code projects** — the workspace pattern works for construction planning, career prep, content creation, and more

---

## The Daily Workflow

```
cd ~/ai-projects
claude
/startnow                    ← See all projects, pick one
cd [project]                 ← Focus on that project
/startnow                    ← Load project context
[build features]             ← Use the build loop
commit                       ← After each sub-task
/updatenow                   ← Update project docs
cd ..                        ← Back to workspace
/updatenow                   ← Update workspace index
```
