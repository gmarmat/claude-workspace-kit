# New Project Checklist

Copy-paste-ready checklist for scaffolding a new project in this workspace.

## Folder Structure

```
project-name/
  CLAUDE.md                       # Project rules, constraints, tech stack
  docs/
    arch.md                       # Architecture index (<300 lines)
    features/                     # Feature deep-dives (linked from arch.md)
    plans/                        # Research, decisions, migration scripts
  .claude/
    skills/
      startnow/SKILL.md          # Context loader (customized per project)
      updatenow/SKILL.md         # Doc updater (customized per project)
      advise/SKILL.md            # Research agent (customized per project)
    commands/
      [domain-specific].md       # Project-specific commands only
    settings.local.json           # Tool permissions for this project
```

## Steps

### 1. Create folder structure

```bash
mkdir -p project-name/{docs/{features,plans},.claude/{skills/{startnow,updatenow,advise},commands}}
```

### 2. Create CLAUDE.md

Include:
- [ ] Project name and purpose
- [ ] Tech stack
- [ ] Key constraints
- [ ] Communication style (or inherit workspace defaults)
- [ ] Workflow rules (or inherit workspace defaults)
- [ ] Skills table listing available `/commands`

### 3. Create core skills

Copy from kit templates (clone claude-project-kit if needed), then customize:

- [ ] `startnow/SKILL.md` — Update to load this project's specific context files
- [ ] `updatenow/SKILL.md` — Update to maintain this project's specific docs
- [ ] `advise/SKILL.md` — Update description with project-specific domain context

Each skill needs YAML frontmatter:
```yaml
---
name: [skill-name]
description: [scope-specific one-liner]
argument-hint: [optional]
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash[, WebSearch, WebFetch, Write, Edit — as needed]
---
```

### 4. Create settings.local.json

```json
{
  "permissions": {
    "allow": [],
    "deny": []
  }
}
```

### 5. Seed docs/arch.md

- [ ] Create initial arch.md with project header, stack, and empty section scaffolding
- [ ] Keep under 300 lines — link to feature docs for details

### 6. Verify

- [ ] `cd project-name && claude` — launch Claude in the project
- [ ] Type `/` — verify startnow, updatenow, advise appear with correct descriptions
- [ ] Run `/startnow` — verify it loads the right context
- [ ] Run `/updatenow` — verify it can update docs

### 7. Update workspace

- [ ] Run `/updatenow` from workspace root to update the project index in CLAUDE.md and docs/arch.md

## Skill Format Rules

| Format | Use When |
|--------|----------|
| **Skill** (`skills/name/SKILL.md`) | Core workflow skills needing `allowed-tools` |
| **Command** (`commands/name.md`) | Project-specific domain commands |

The 4 core skills (startnow, updatenow, advise, l3) are always **skill** format.
