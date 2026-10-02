---
name: context-hygiene
description: "[Workspace] Two-step context for large, long-running projects: load only recent state every session, search everything older on a miss. Use when session-state / active-threads / journal files grow past a few hundred lines, when /startnow feels slow or loads stale history, when the user says 'trim context', 'archive old threads', 'too much loading', or to set this up in a new project. Also run its checks at every /updatenow wrap once set up."
argument-hint: [setup | check | roll | compact | find <terms>]
disable-model-invocation: false
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Context hygiene: load little, search on a miss

Big projects pay for their history every session: rolling session-state blocks, threads nobody closed, a journal
that only grows. This skill keeps **tier 1** (read every session) small and makes **tier 2** (everything older) one
search away, so nothing is lost and nothing is loaded by default.

| Tier | What | When |
|---|---|---|
| **1. Loaded** | CLAUDE.md · session-state (NEXT + 1 PRIOR) · active-threads (last N days) · memory index | Every session |
| **2. Searched** | older threads · session-state archive · closed threads · docs · memory files · anything in `tier2` | Only when tier 1 has no answer: `ctx.py find <terms>`, read the hit lines only |

**Rule for the agent:** if tier 1 has no answer, run `find` **before** saying "unknown" or asking the user.
**Never load an archive whole.**

## Files
- `ctx.py` (stdlib Python 3.9+): `check · roll · compact · find · log`. Dry run unless `--apply`; every move is verified
  lossless (each moved line must exist in its destination).
- `context-hygiene.example.json`: copy to `<managed folder>/.context-hygiene.json` and edit.

## Setup (`/context-hygiene setup`)
1. Pick the managed folder (where session-state / active-threads live). `ctx.py` ships in this skill's folder: run it
   in place (`python3 <skill folder>/ctx.py …`) or copy it to e.g. `tools/context/`. Copy the example config to
   `<folder>/.context-hygiene.json`.
2. Fill `tier1` with the files read every session and realistic `maxLines`; set `tokenBudget` (start at ~40k).
3. Turn on only what the project has: `state` (rolling NEXT/PRIOR blocks), `threads` (dated sections or rows),
   `journal` (one line per event), `versionTable`. List the older material in `tier2`.
4. Dry run: `python3 ctx.py check --dir <folder>`, then `roll` and `compact` without `--apply`. **Read what would move.**
   Adjust `neverMove` / `rowDateSections` until nothing still live is listed.
5. `--apply`, then `check` must say `within limits`.
6. Add the two-step rule to the project's CLAUDE.md and the wrap step below to `/updatenow`.

## At every wrap (`/updatenow`)
```
python3 ctx.py roll --dir <folder> --apply
python3 ctx.py compact --dir <folder> --apply
python3 ctx.py check --dir <folder>        # fix every WARN before committing
```

## How things are dated (threads)
| Option | Effect |
|---|---|
| default | a `## ` section is as old as the date in its **heading** (YYYY-MM-DD) |
| `"sectionDate": "latest"` | as old as the **latest date anywhere in it**, so a section updated recently or carrying a near deadline stays; undated stale sections roll too |
| `"futureDays": 60` | dates further out than this are ignored (sentinels like 01/01/2200, data values) |
| `rowDatePattern` | rows carrying a marker such as `(carried from 9/25)` roll one by one |
| `"rowDateSections"` | ledger-style tables (Awaiting, Closed) roll **row by row** by their latest date; never use it on sections whose rows are open questions |
| `neverMove` | headings that never roll (standing reminders, meetings, promised dates). Pin anything else by adding words from its heading |
| `closedSections` + `closedArchive` | rows from closed sections go to the closed archive, not the "older open" file |

## Strongest case against (say it before setting up)
- Small projects do not need this; turn it on when tier 1 passes ~300 lines or ~30k tokens.
- Dates are a proxy for "live". A live item with only old dates rolls out: it is still found by `find`, and pinning it
  via `neverMove` keeps it in tier 1. Always read the dry run the first time.

## Output banner
```
context-hygiene · <folder>: tier 1 ~N tokens (was M)
  rolled: X items to older, Y to closed archive · compacted: Z blocks
  check: within limits
```
