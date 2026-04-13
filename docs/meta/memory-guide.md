# Memory Best Practices

Claude Code has an auto-memory system that persists information across conversations. Used well, it makes every session smarter. Used poorly, it creates noise that wastes context tokens.

---

## What to Store in Memory

| Type | What to Store | Example |
|------|-------------|---------|
| **User** | Role, preferences, hardware, knowledge level | "Deep Go expertise, new to React" |
| **Feedback** | Corrections + confirmed approaches | "Don't mock the database in integration tests" |
| **Project** | Active initiatives, deadlines, decisions not in code | "Merge freeze begins 2026-03-05 for mobile release" |
| **Reference** | Pointers to external resources | "Pipeline bugs tracked in Linear project INGEST" |

## What NOT to Store

| Don't Store | Why | Where It Lives Instead |
|------------|-----|----------------------|
| Code patterns and conventions | Derivable from the codebase | Read the code |
| Git history and recent changes | `git log` is authoritative | Run `git log` |
| Debugging solutions | The fix is in the code | Read the commit |
| Anything in CLAUDE.md | Already read every session | CLAUDE.md itself |
| Ephemeral task state | Only useful in current conversation | Tasks tool |
| Architecture details | Changes frequently, arch.md is source of truth | docs/arch.md |

## Memory vs Other Persistence

| Mechanism | Scope | Use When |
|-----------|-------|----------|
| **Memory** | Cross-conversation | Info useful in future sessions |
| **Tasks** | Current conversation | Tracking work in progress |
| **Plans** | Current conversation | Aligning on approach before building |
| **CLAUDE.md** | Every session | Hard rules and constraints |
| **arch.md** | Every session | Architecture state |
| **docs/plans/** | Permanent | Research and decision records |

## Context Loading Strategy

```
Session start → /startnow reads:
  1. CLAUDE.md (rules)
  2. docs/arch.md (architecture)
  3. Memory files (cross-session context)
  4. git log (recent changes)
  5. Config files (dependencies)
```

This gives Claude full context in ~30 seconds instead of manually explaining everything.

## Tips

- **Convert relative dates** — "next Thursday" → "2026-04-17" so the memory stays useful
- **Include why** in feedback memories — "Don't mock DB (reason: prod migration broke despite passing tests)"
- **Save from success too** — don't only save corrections; save confirmed good approaches
- **Prune stale memories** — old project decisions may no longer apply
- **Verify before acting** — a memory that names a file/function may be outdated; check the code first
