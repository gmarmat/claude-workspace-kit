# Workflow Evolution: How Your Daily Routine Changes

This guide covers how the workspace workflow evolves as you add knowledge management (/ingest) and staleness detection to your existing build loop.

---

## The Old Workflow (Still Valid)

```
/startnow → pick feature → /advise (if needed) → build → test → commit → /updatenow
```

This is still the core. Nothing changes about how you build. What changes is what happens **around** the build loop — how you feed knowledge in and keep knowledge fresh.

---

## The Evolved Workflow

```
┌─────────────────────────────────────────────────────┐
│  SESSION START                                       │
│  /startnow → see all projects + status               │
│  /audit staleness → quick health check (monthly)     │
└──────────────────────┬──────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
    ┌────▼────┐   ┌────▼────┐  ┌────▼────┐
    │ INGEST  │   │  BUILD  │  │ RESEARCH│
    │ new     │   │ the     │  │ before  │
    │ source  │   │ feature │  │ deciding│
    └────┬────┘   └────┬────┘  └────┬────┘
         │             │             │
         │        test + commit      │
         │             │             │
         └─────────────┼─────────────┘
                       │
              ┌────────▼────────┐
              │  /updatenow     │
              │  keeps it all   │
              │  in sync        │
              └─────────────────┘
```

Three modes, one session. You flow between them naturally.

---

## Mode 1: Build (unchanged)

The core loop. Same as before.

```
/startnow → pick feature → /advise → build → test → commit → /updatenow
```

**When:** Most sessions. This is where products get built.

---

## Mode 2: Ingest (new)

Processing external knowledge into your workspace's structured docs.

```
/ingest [URL or paste article]
```

**When to ingest:**

| Trigger | Example |
|---------|---------|
| Before `/advise` | "I read an article about auth patterns — let me ingest it first so /advise has it" |
| After reading something useful | "This Stripe engineering blog post is relevant to our payment flow" |
| Competitor research | "Let me ingest what I found about competitor X" |
| Technology evaluation | "Karpathy posted about LLM Wikis — /ingest the gist" |
| After a conference/webinar | "Key takeaways from the talk on agentic engineering" |
| Learning a new tool | "Supabase just released Edge Functions v2 — /ingest the docs" |

**What you get:** A structured summary in `docs/plans/`, cross-references to existing docs, and an entry in `docs/sources.md` that future sessions can find.

**The compound effect:** After 20 ingests, your workspace has a searchable knowledge base. When you run `/advise`, it can reference prior research instead of starting from scratch. When a new team member joins, they can read your sources.md to understand your decision history.

---

## Mode 3: Maintenance (enhanced)

Keeping docs, memory, and knowledge fresh.

```
/audit staleness        ← find what's outdated
/localcompact           ← keep arch.md lean
/updatenow              ← sync docs after changes
```

**When to run staleness checks:**

| Frequency | What to Check |
|-----------|--------------|
| **Every session** | `/updatenow` (already doing this) |
| **Weekly** | Skim `docs/sources.md` — anything feel outdated? |
| **Monthly** | `/audit staleness` — full automated check |
| **After a pivot** | `/audit staleness` + manual review of PRD and arch.md |

---

## What to Care About Going Forward

### 1. Knowledge compounds — but only if you ingest

The workspace is only as smart as the knowledge you put into it. The gap between "I read that somewhere" and "it's in docs/plans/" is the gap between forgetting and leveraging.

**Rule of thumb:** If you spent more than 10 minutes reading something relevant, `/ingest` it. It takes 2 minutes and pays dividends for months.

### 2. Staleness is the silent killer

Outdated docs are worse than no docs — they actively mislead. The staleness audit catches:
- Feature docs that fell behind the code
- Memory files storing decisions that were reversed
- Research that was true 3 months ago but isn't now
- arch.md entries for files that got deleted

**Rule of thumb:** If `/audit staleness` finds more than 5 items, stop building and clean up first. One session of maintenance prevents weeks of confusion.

### 3. Sources.md is your institutional memory

Over time, `docs/sources.md` becomes a bibliography of every decision. When someone asks "why did you choose Supabase over Firebase?" you can point to the dated research with sources.

**Rule of thumb:** If a decision was informed by external research, there should be an ingest page backing it up.

### 4. Cross-references are the real value

A summary alone is just a note. The connections between sources and your existing docs are what make the system compound. When `/ingest` shows that a new article contradicts a decision you made 2 months ago, that's where the value lives.

---

## What to Stop Doing

| Old Habit | Why It's Wasteful | New Habit |
|-----------|------------------|-----------|
| Bookmarking articles "to read later" | They pile up, never get processed | `/ingest` immediately or don't save it |
| Remembering context in your head | Gone next session, gone next week | `/ingest` or save to memory |
| Re-researching the same topic | No record of prior research | Check `docs/sources.md` first |
| Trusting old docs without checking | Docs drift from reality | Run `/audit staleness` monthly |
| Massive /updatenow at end of week | Context is stale by then | `/updatenow` after every feature, not every week |

---

## What to Adapt

| Old Pattern | Evolution | Why |
|------------|-----------|-----|
| `/advise` cold start | `/ingest` relevant sources first, then `/advise` | Advise is better when it has prior research to build on |
| Memory files as brain dump | Memory for corrections/preferences only, `/ingest` for knowledge | Memory is for things that change how Claude behaves; knowledge goes in docs |
| arch.md as the only index | arch.md for architecture, `sources.md` for knowledge | Two indexes, two purposes — both under 300 lines |
| Annual doc cleanup | Monthly `/audit staleness` | Small frequent checks prevent big painful cleanups |

---

## The Complete Skill Map

| Skill | Mode | When | Frequency |
|-------|------|------|-----------|
| `/startnow` | Start | Every session | Every session |
| `/ingest` | Ingest | When you read something relevant | As needed (aim for 2-3/week) |
| `/advise` | Research | Before architecture decisions | As needed |
| `/l3` | Build | When something breaks | As needed |
| `/audit` | Maintenance | Health check | Monthly (staleness), per-deploy (security) |
| `/audit staleness` | Maintenance | Find outdated docs/memory | Monthly |
| `/localcompact` | Maintenance | arch.md over 300 lines | As needed |
| `/updatenow` | Sync | After any changes | Every session, after every feature |
| `/newproject` | Create | Starting something new | As needed |

---

## TL;DR

1. **Build the same way.** The build loop doesn't change.
2. **Ingest what you read.** If it took 10+ minutes to read, it's worth 2 minutes to ingest.
3. **Check staleness monthly.** One `/audit staleness` prevents weeks of confusion.
4. **Trust the compound effect.** 20 ingested sources + cross-references = a workspace that actually remembers what you learned.
5. **Clean as you go.** `/updatenow` every session, staleness audit monthly, localcompact when needed.
