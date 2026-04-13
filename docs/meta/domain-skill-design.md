# Domain Skill Design Guide

Beyond the 7 core skills (startnow, updatenow, advise, l3, audit, localcompact, newproject), you can create **domain-specific skills** for any repeatable multi-step workflow. This guide covers advanced patterns extracted from real production skill ecosystems.

---

## When to Create a Domain Skill

| Signal | Example |
|--------|---------|
| You do the same 5+ step workflow regularly | "Parse a JD, match to resume, generate tailored version" |
| The workflow has a specific output format | "Comparison table → recommendation → save to plans/" |
| Multiple people need to do it consistently | "Every new job application follows the same setup" |
| The workflow crosses multiple files | "Read 6 career files, match against JD, produce resume" |

**Don't create a skill for:** one-off tasks, simple file edits, or anything that takes fewer than 3 steps.

---

## Skill Anatomy

```yaml
---
name: skill-name
description: "[ProjectName] What this skill does — one line."
argument-hint: what-the-user-passes (e.g., job-folder-name)
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Skill Title

## Context
[Project-specific domain knowledge, constraints, key files to read]

## Input
[What the user provides — arguments, pasted content, etc.]

## Execution Steps
### Step 1: [Name]
[What to do, what to read, what to produce]

### Step 2: [Name]
[...]

## Rules
[Hard constraints specific to this skill]
```

---

## Advanced Patterns

### 1. Skill Routing

When you have multiple skills, users sometimes invoke the wrong one. Add a routing table to your project's CLAUDE.md:

```markdown
| User wants to... | Right skill | Wrong skill (redirect) |
|---|---|---|
| Log a quick update | `/track add` | `/newjob` (too heavy) |
| Build a full prep guide | `/interview-prep` | `/track` (too light) |
| Research an interviewer | `/profile-intel` | `/interview-prep` (different scope) |
```

**Why:** Prevents users from using a heavy skill for a light task (or vice versa). Claude reads this table and can redirect automatically.

### 2. Two-Tier Model

Not everything needs full treatment. Create a lightweight path and a heavyweight path:

```
Lightweight: /track add → one line in tracker.md (every item)
Heavyweight: /newjob → full folder with 6 files (only serious items)
```

**Why:** Avoids folder/file bloat. Most items never graduate past the lightweight tier. Only escalate when the user signals it's worth the investment.

### 3. Context Model

Define where data lives and how skills find it:

```
Global context (base level):
  - profile.md, experiences.md, skills.md
  - Updated when user shares new info
  - All skills read from here

Per-item context (subfolders):
  - activejobs/{company}/jd.md, resume.md
  - Created by /newjob, populated by /generate-resume
  - Only relevant skills read these
```

**Why:** Skills need to know where to find data without hardcoding paths. A clear context model means skills compose well together.

### 4. Skill Chaining

Design skills that feed into each other:

```
/newjob → creates folder + placeholder files
    ↓
/generate-resume → reads JD + career data → produces resume
    ↓
/profile-intel → reads interviewer LinkedIn → produces intel brief
    ↓
/interview-prep → reads everything above → produces prep guide
```

Each skill produces artifacts the next skill consumes. The user can enter the chain at any point.

**Why:** Skills that compose are more powerful than monolithic skills. Users can skip steps they don't need.

### 5. Side-Effect Updates

Skills should update source-of-truth files when new information surfaces during execution:

```
During /generate-resume, user says "actually the revenue was $2.3M, not $1.5M"
  → Fix the number in resume.md
  → ALSO update experiences.md (the source file)
  → ALSO grep for the old number across all files
  → ALSO update memory if it references the old number
```

**Why:** Data corrections should propagate to the source, not just the current output. Otherwise the next skill run will have the old wrong data.

---

## Skill vs Command

| | Skill | Command |
|---|---|---|
| **Location** | `.claude/skills/name/SKILL.md` | `.claude/commands/name.md` |
| **Has YAML frontmatter** | Yes (name, description, allowed-tools) | No |
| **Tool access control** | Yes — restricts which tools Claude uses | No |
| **Use when** | Core workflow skills that need guardrails | Simple domain-specific shortcuts |

**Rule of thumb:** If the skill touches external services or writes files, use the skill format with `allowed-tools`. If it's just a prompt shortcut, a command is fine.

---

## Non-Code Projects

Skills work for any repeatable workflow, not just code:

| Domain | Example Skills |
|--------|---------------|
| Construction planning | `/quote-compare`, `/permit-status`, `/contractor-brief` |
| Career prep | `/generate-resume`, `/interview-prep`, `/profile-intel` |
| Content creation | `/writestory`, `/pushcontent`, `/translate` |
| Home network | `/device-audit`, `/dns-check`, `/troubleshoot` |

The same patterns (routing, two-tier, context model, chaining) apply regardless of domain.
