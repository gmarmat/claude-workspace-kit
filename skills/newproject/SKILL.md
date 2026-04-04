---
name: newproject
description: "[Workspace] Scaffold a new project folder with CLAUDE.md, docs, skills, and architecture from an idea or PRD."
argument-hint: [project name or "update existing-project"]
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion
---

# NewProject — Project Scaffolding Agent

You help the user go from idea -> working project folder with all the standard scaffolding in place.

## Two Modes

| Invocation | What Happens |
|------------|-------------|
| `/newproject myapp` | **Create mode** — scaffold a brand new project from scratch |
| `/newproject update myapp` | **Update mode** — refine an existing project's scaffolding (after PRD, after pivots, etc.) |

---

## Template Source

**Project templates come from the public [claude-project-kit](https://github.com/gmarmat/claude-project-kit) repo.**

### How to Get Templates

1. Check if the kit repo exists locally (look for a `kit/` folder in the workspace or `/tmp/claude-project-kit/`)
2. If not found, clone it: `git clone https://github.com/gmarmat/claude-project-kit.git /tmp/claude-project-kit`
3. Read templates from the cloned repo

### Template Mapping

| Skill/File | Kit Template Path | Adapt How |
|------------|------------------|-----------|
| startnow | `.claude/skills/startnow/SKILL.md` | Fill in all `<!-- CUSTOMIZE -->` markers. Change description to reference this project. Update config files and summary fields. |
| updatenow | `.claude/skills/updatenow/SKILL.md` | Change description to reference this project. Keep the full arch.md structure guide. Add project-specific doc targets if needed. |
| advise | `.claude/skills/advise/SKILL.md` | Fill in the `<!-- CUSTOMIZE -->` Context section with project domain, constraints, key docs. |
| l3 | `.claude/skills/l3/SKILL.md` | Fill in the `<!-- CUSTOMIZE -->` marker. Replace the placeholder investigation areas table with this project's actual file paths. |
| PRD | `docs/PRD.md.template` | Copy to `docs/PRD.md`. Fill in what you can from user's description. |
| arch.md | `docs/arch.md.template` | Copy to `docs/arch.md`. Fill in Quick Reference from PRD. Seed empty sections. |

**CRITICAL: Read each kit template in full before creating the project version.** The kit templates contain important details (source tracking in advise, arch.md structure guide in updatenow, investigation areas in l3) that must be preserved. Don't write skills from memory — always read the template first, then customize.

---

## Create Mode

### Step 1: Gather the Idea

If the user hasn't already explained, ask:
1. **What are you building?** (1-2 sentences)
2. **Who is it for?** (yourself, public, specific audience)
3. **Any tech preferences?** (or should I recommend?)

Don't over-ask. If the user gave a clear description, skip straight to Step 2.

### Step 2: Propose the Setup

Present a compact summary for approval:

```
## Project: [name]

**Purpose:** [1 sentence]
**Stack:** [proposed tech stack]
**Deploy:** [proposed hosting]

Folders & files I'll create:
  [name]/
    CLAUDE.md              — project rules, stack, constraints
    docs/
      arch.md              — architecture index (seeded)
      PRD.md               — product requirements (seeded)
      features/            — (empty, ready for feature docs)
      plans/               — (empty, ready for research)
    .claude/
      skills/
        startnow/SKILL.md  — context loader for this project
        updatenow/SKILL.md — doc updater for this project
        advise/SKILL.md    — research agent for this domain
      settings.local.json  — tool permissions

Shall I proceed?
```

Wait for user confirmation before creating files.

### Step 3: Get Kit Templates

1. Clone or locate the claude-project-kit repo
2. Read all skill templates and doc templates listed in the Template Mapping table above
3. Never write skills from scratch — always start from kit templates

### Step 4: Create Everything

#### 4a. Folder Structure

```bash
mkdir -p [name]/docs/{features,plans} [name]/.claude/skills/{startnow,updatenow,advise}
```

#### 4b. docs/PRD.md

Copy `kit/docs/PRD.md.template` to `[name]/docs/PRD.md`. Pre-fill what you can from the user's description:
- LLM Quick Start (product definition, target users, key constraint)
- Executive Summary (value proposition)
- Problem Statement (if the user described pain points)
- Leave everything else as template placeholders — the user will iterate on this

#### 4c. CLAUDE.md

Write a project CLAUDE.md with:
- Project name and purpose (from user's description)
- Tech stack table (| Component | Technology | Notes |)
- Key constraints (if known from user's description)
- Skills table (| Skill | Purpose |) listing startnow, updatenow, advise
- Workflow rules — start with these defaults, add project-specific ones:
  - Read arch.md before planning/building any feature
  - Run `/updatenow` after completing any feature
  - Use `/advise` before major architecture decisions
  - Commit frequently after each sub-task

#### 4d. docs/arch.md

Seed a minimal arch.md following the structure from the kit updatenow template:

```markdown
# [Project Name] — Architecture
**Version:** 0.1 | **Updated:** YYYY-MM-DD

<!-- LLM: Read this file first. Token-optimized project index. -->

## Quick Reference

### What Is This?
[1-paragraph summary from user's description]

### Tech Stack
| Component | Technology | Notes |
|-----------|-----------|-------|
| [filled from user's description or proposed stack] |

### Project Structure
[Will be filled as code is written]

### Environment Variables
[Will be filled as env vars are added]

## Domain Concepts
[Will be filled as domain is understood]

## Data Model
[Will be filled as schema is designed]

## API Routes
[Will be filled as routes are built]

## Key Patterns
[Will be filled as patterns emerge]

## Feature Index
| Feature | Doc | Status |
|---------|-----|--------|
| [none yet] | | |

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 0.1 | YYYY-MM-DD | **Initial scaffold.** Project created. |
```

Keep it under 60 lines — it'll grow as the project develops.

#### 4e. Skills (from kit templates)

For each skill, read the kit template, then create a customized version:

**startnow/SKILL.md** — Based on kit template:
- YAML `description`: Must start with `[ProjectName]` prefix
- Keep the full protocol from kit
- Customize to list this project's specific key docs and config files

**updatenow/SKILL.md** — Based on kit template:
- YAML `description`: Must start with `[ProjectName]` prefix
- Keep the full arch.md structure guide
- Keep the feature doc template structure and version rules
- Add any project-specific doc targets

**advise/SKILL.md** — Based on kit template:
- YAML `description`: Must start with `[ProjectName]` prefix
- Keep the full 7-phase protocol
- Add a Context section with project-specific constraints and domain knowledge

#### 4f. settings.local.json

```json
{
  "permissions": {
    "allow": [],
    "deny": []
  }
}
```

### Step 5: Update Workspace

- Add the new project to the workspace `CLAUDE.md` Projects table
- Don't initialize git — the user decides when

### Step 6: Report

```
## Project Scaffolded: [name]

Files created:
  - CLAUDE.md
  - docs/arch.md (v0.1)
  - docs/PRD.md (seeded from template)
  - .claude/skills/startnow/SKILL.md (from kit template)
  - .claude/skills/updatenow/SKILL.md (from kit template)
  - .claude/skills/advise/SKILL.md (from kit template)
  - .claude/settings.local.json

Next steps:
  1. cd [name] && claude
  2. Run /startnow to verify context loading
  3. Start building, or run /advise to research your approach first
```

---

## Update Mode

When invoked as `/newproject update [name]`:

### Step 1: Read Current State

1. Read `[name]/CLAUDE.md`
2. Read `[name]/docs/arch.md`
3. Read all skills in `[name]/.claude/skills/`
4. If the user mentions a PRD, read it
5. Ask: "What changed? New PRD, pivot, tech stack change, or just refinement?"

### Step 2: Identify What Needs Updating

Compare what exists against what the user describes. Present a diff plan:

```
## Proposed Updates to [name]

| File | Change |
|------|--------|
| CLAUDE.md | Update stack from [old] -> [new], add [constraint] |
| docs/arch.md | Add data model section, update stack reference |
| startnow/SKILL.md | Add step to read [new config file] |
| advise/SKILL.md | Update domain context with [new details] |
```

Wait for approval.

### Step 3: Apply Changes

Use Edit for surgical updates — don't rewrite files from scratch unless the changes are fundamental.

### Step 4: Report

Show what changed, what's still TODO, and suggest next steps.

---

## Important Rules

- **Always read kit templates first** — never write skills from memory or from scratch
- **Always wait for user approval** before creating/modifying files
- **Don't over-engineer the scaffold** — keep it minimal, the user will grow it
- **Don't create feature docs** yet — those come later when features are being built
- **Don't initialize git** — the user decides when and how
- **Customize every skill** — no generic descriptions. Every skill should reference this specific project's domain, stack, and concerns.
- **Workspace CLAUDE.md must stay updated** — add the new project to the Projects table
- **Preserve kit template depth** — the kit templates have detailed protocols. Keep that depth in project skills — just customize the specifics.
