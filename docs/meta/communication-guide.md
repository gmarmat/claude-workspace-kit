# Communication Guide: How to Talk to Claude Code

The quality of Claude's output is directly proportional to the quality of your instructions.

---

## The Mental Model

```
You (Human)                          Claude (AI)
─────────────                        ──────────
Vision & Goals          ──────>      Understands context via docs
Architecture Decisions  ──────>      Executes within constraints
Review & Course-Correct ──────>      Generates code, docs, plans
Domain Expertise        ──────>      Handles boilerplate + research
Quality Bar             ──────>      Follows your patterns consistently
```

**You are the architect. Claude is the builder.**

---

## Instruction Patterns

| Task Type | Pattern | Example |
|-----------|---------|---------|
| **Features** | "Build [X] per [doc]. Follow [pattern] from arch.md." | "Build auth per docs/features/auth.md. Use Supabase magic links." |
| **Debugging** | "/l3 [exact error message with context]" | "/l3 TypeError: Cannot read 'name' of undefined at /api/profile line 45" |
| **Research** | "/advise X vs Y for [use case]. Consider [constraints]." | "/advise Redis vs Supabase realtime. Budget $25/mo." |
| **Refactoring** | "Refactor [thing] to follow pattern #N. Don't change behavior." | "Refactor API routes to follow Key Pattern #3 in arch.md." |

## Bad vs Good

| Bad | Good |
|-----|------|
| "Add a login page" | "Build login per docs/features/auth.md, use Supabase Auth magic links" |
| "Fix the bug" | "/l3 TypeError at api/generate line 45 — happens after clearing form" |
| "Should we use Redis?" | "/advise Redis vs Supabase realtime for caching. Budget $25/mo, 2 users" |
| "Make it better" | "Apply card pattern from design-system.md to the job list" |

## The Progression

| Level | How You Work | Quality |
|-------|-------------|---------|
| 1. Vibe coding | "Build me an app" → accept whatever | Low — demos only |
| 2. Directed coding | Feature-by-feature with some references | Medium — functional |
| 3. Structured system | PRD → arch.md → skills → doc references in every instruction | High — production-grade |

This kit is designed to get you to Level 3.
