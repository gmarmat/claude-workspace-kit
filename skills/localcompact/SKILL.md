---
name: localcompact
description: "[Workspace] Compact any project's arch.md back under 300 lines. Dry-run by default, pass 'apply' to execute."
argument-hint: [apply]
disable-model-invocation: false
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# LocalCompact — arch.md Compaction Agent

You maintain the size budget of `docs/arch.md`. When invoked, you analyze the file for bloat and either report what you'd change (dry-run) or execute the compaction (apply mode).

**Core principle:** Never delete content — only move it (to feature docs or archive).

## Context

This is a multi-project workspace. When compacting:
- Identify which project's arch.md to compact (workspace root or a specific project)
- If not specified, default to the current working directory's `docs/arch.md`

## Modes

| Invocation | Behavior |
|------------|----------|
| `/localcompact` | Dry-run — analyze + report, no changes |
| `/localcompact apply` | Execute compaction, then report before/after |

---

## Section Line Budgets

| Section | Budget |
|---------|--------|
| Header + LLM Instructions | 10 |
| Quick Reference (all sub-sections) | 70 |
| Domain Concepts | 30 |
| Data Model | 30 |
| API Routes | 40 |
| Key Patterns | 25 |
| Feature Index | 20 |
| Version History | 25 |
| Custom/unknown sections | 25 each |
| Whitespace/separators | ~20 |

**Total budget: ~300 lines.** If arch.md is already under 250 lines, report "no compaction needed" and stop.

---

## Bloat Patterns to Detect

| Pattern | Detection | Action |
|---------|-----------|--------|
| Prose paragraphs | 3+ consecutive non-table, non-heading, non-list lines | Rewrite as table row or 1-liner |
| Inline implementation details | Multi-line explanations of how something works | Extract to `docs/features/*.md`, replace with link |
| Duplicate content | Content that also exists in a feature doc | Remove from arch.md, keep link in Feature Index |
| Stale entries | Referenced files/routes that don't exist on disk | Remove, note in report |
| Version History overflow | More than 15 entries | Archive older entries to `docs/version-history-archive.md` |
| Long table cells | Cell content > 80 chars | Shorten to key phrase |

---

## Execution Steps

### Step 1: Read + Measure

1. Read `docs/arch.md` in full
2. Count total lines
3. If total lines < 250, report "no compaction needed" and **stop**
4. Identify each section by `##` headings
5. Count lines per section

### Step 2: Identify Bloat

For each section:
1. Compare actual lines vs budget
2. Scan for each bloat pattern listed above
3. For stale entries: use Glob/Grep to verify referenced files/routes exist on disk
4. Record findings

### Step 3: Plan Compaction

For each over-budget section, plan specific actions:
- Which lines to rewrite as tables
- Which content to extract to feature docs (identify target file)
- Which stale entries to remove
- Which Version History entries to archive (keep most recent 15)

### Step 4: Report Analysis

**Always show this table, regardless of mode:**

```
## arch.md Analysis

Total lines: [N] (budget: 300)

| Section | Lines | Budget | Over | Action |
|---------|-------|--------|------|--------|
| Header | [n] | 10 | [+n or ok] | [action or "ok"] |
| ... | ... | ... | ... | ... |

Bloat detected:
  - [list specific bloat findings]

Planned actions:
  - [list what would change]
```

If dry-run mode, stop here with: "Run `/localcompact apply` to execute these changes."

### Step 5: Execute Compaction (apply mode only)

1. **Extract content** to feature docs, replace with 1-line summary + link
2. **Rewrite prose** to table rows or 1-liners
3. **Remove stale entries**
4. **Archive Version History** if > 15 entries
5. **Shorten long cells** > 80 chars
6. **Bump version** + update date in header
7. **Add Version History entry**

### Step 6: Final Report (apply mode only)

```
## Compaction Complete

| Metric | Before | After |
|--------|--------|-------|
| Total lines | [N] | [M] |
| Sections over budget | [N] | [M] |

Changes made:
  - [list of changes]

Content moved to:
  - [list of destination files]
```

---

## Important Rules

- **NEVER delete content without moving it** — extracted content goes to feature docs or archive
- **NEVER reorganize sections** — preserve the existing section order exactly
- **NEVER touch the 15 most recent Version History entries**
- **NEVER change section headings**
- **Preserve all links**
- **Use Edit tool for surgical changes** — don't rewrite the entire file
- Unknown/custom sections get a 25-line default budget
