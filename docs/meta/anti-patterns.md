# Anti-Patterns: What NOT to Do

Common mistakes when using Claude Code for real projects. Each one extracted from 10+ projects.

---

| # | Anti-Pattern | Why It's Bad | Do This Instead |
|---|-------------|-------------|-----------------|
| 1 | **No PRD, just start coding** | Claude makes wrong assumptions about scope | Write a PRD first, even a rough one |
| 2 | **One giant prompt** | Claude loses focus, misses requirements | Break into sub-tasks, one feature at a time |
| 3 | **No CLAUDE.md** | Claude reinvents conventions every session | Set rules once, enforce always |
| 4 | **Bloated arch.md (500+ lines)** | Wastes context tokens, Claude skims instead of reads | Run `/localcompact`, link to feature docs |
| 5 | **Vague instructions** | "Make it look better" → random changes | Reference specific docs, patterns, design tokens |
| 6 | **Skipping /updatenow** | Docs drift from reality, next session starts confused | Always update docs after changes |
| 7 | **Letting Claude decide architecture** | It optimizes for "works now" not "scales later" | Use `/advise` for all architecture decisions |
| 8 | **No boundaries table in PRD** | Claude does things you'd never want | ALWAYS / ASK FIRST / NEVER table in every PRD |
| 9 | **Mocking everything in tests** | Tests pass but production breaks | Hit real database in integration tests |
| 10 | **One massive commit** | Impossible to rollback specific changes | Commit after each sub-task |
| 11 | **Git at workspace level** | Conflicts with project repos, messy history | Each project manages its own git repo |
| 12 | **Modifying the kit folder** | Breaks the template source for new projects | Kit is read-only reference — copy from it, don't edit it |

## The Root Cause

Most anti-patterns come from treating Claude as a magic box instead of a junior developer who needs structure. The fix: **better context, clearer boundaries, smaller tasks.**
