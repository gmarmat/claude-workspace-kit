---
name: humanize
description: >
  [Workspace] Use whenever {{USER_NAME}} asks you to draft, write, edit, or
  help with anything another person will read: emails, texts, contractor
  messages, agent replies, HOA letters, family notes, job application material,
  vendor follow-ups, doctor / school messages, GitHub issue / PR bodies for
  open-source contributions, etc. Also use when text needs to sound less like
  AI, more punchy, or more like {{USER_NAME}}'s actual voice. Adapted from
  lguz/humanize-writing-skill (MIT).
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Bash
---

# Humanize : Make Drafts Sound Like {{USER_NAME}}, Not Like a Model

Your job: take any draft you produce for {{USER_NAME}} that another human will
read, and run it through a 3-pass cleanup so it reads like a real person wrote
it, not a language model. Substance comes from {{USER_NAME}}. The voice has to
match.

## When to auto-apply

Auto-apply (no permission needed) whenever {{USER_NAME}} asks you to:
- Draft / write / help with an email or message reply
- Draft a text / iMessage / WhatsApp / Teams / Slack message
- Polish or edit text they wrote that they want to send
- Make something "punchier", "shorter", "more professional", "less AI"
- Write a contractor / vendor / agent reply for any project in the workspace
- Write a note for family, a doctor, a school, an HOA, a city office
- Write a cover letter, application response, or recruiter reply
- Draft a GitHub issue body, PR description, or PR review comment for any
  open-source project {{USER_NAME}} is contributing to — see "OSS
  contributions" section below

Apply it before showing the draft.

## When NOT to apply

- Internal `.md` notes, trackers, CONTEXT files, run logs, plans (these stay
  terse and technical, not humanized prose)
- Code, configs, commit messages, PR titles
- Structured data (CSV, JSON, YAML)
- Ticket titles or contract clauses where exact wording matters (issue / PR
  **bodies** are still in scope — humanize those)
- When {{USER_NAME}} explicitly says "raw" or "verbatim" or "don't reword"

## Default voice

Default to **warm-professional** (see `references/voices.md`) with these
universal overrides on top:

1. **No em-dashes.** Use colons or commas. Em-dash overuse is one of the
   strongest AI tells.
2. **Lead with the substance, not the setup.** Skip "Hope you're doing well"
   and throat-clearing. Open with the point.
3. **Short paragraphs.** 1-3 sentences. Long blocks signal a model.
4. **Direct asks.** "Confirming X." "Requesting Y by Z." Not "I would
   appreciate if you could possibly..."
5. **Light bullet usage.** Bullets only for lists of distinct items (asks,
   clarifications, line items). Not for prose chopped into bullets.
6. **No corporate puffery.** Never "leverage", "synergy", "best-in-class",
   "stakeholder alignment", "drive value".
7. **Sign-off**: `{{SIGN_OFF}}` for standard messages. For casual notes
   (family, neighbors, friendly contractors) just the first name works. Never
   "Best wishes" or "Warm regards" unless requested.

If {{USER_NAME}} asks for a different voice ("punchy", "casual", "sharp"),
pull from `references/voices.md`. If they give writing samples, use `mirror`
voice.

<!-- CUSTOMIZE: Add personal voice rules here. Examples:
  - Specific words to avoid beyond the corporate-puffery list
  - Phrases or sign-offs unique to you
  - Industry-specific vocabulary preferences
-->

## The 3-pass process

### Pass 1 : kill the AI vocabulary

Read `references/ai-patterns-dictionary.md`. For every Tier 1 word in the
draft, replace with the human alternative or restructure the sentence so it
isn't needed. Tier 2 words: max one per piece, only where genuinely natural.
Tier 3 transitions: no more than 2 in the entire piece.

Common offenders for drafts: `delve`, `leverage`, `landscape`, `pivotal`,
`testament`, `crucial`, `holistic`, `comprehensive`, `seamless`,
`cutting-edge`, `game-changer`, `Furthermore`, `Moreover`, `Additionally`,
`Consequently`, `Notably`, `Indeed`.

### Pass 2 : break the AI structures

Scan for and break these patterns. They are stronger AI tells than vocabulary.

- **Parallel negation** ("Not X, but Y") : just say what's true. Drop the
  contrast.
- **Tricolons** (groups of three : "X, Y, and Z") : pick the one or two that
  matter.
- **Em dashes** : zero. Use colons or commas. Hard rule.
- **Rhetorical question + answer** ("What does this mean? It means...") : just
  state the point.
- **Mirror structures** (two consecutive sentences with identical shape) :
  break the symmetry.
- **Dramatic reveals** ("Here's the thing:", "The result?") : drop the setup.
- **Inflation of importance** ("pivotal moment", "testament to") : remove
  these sentences entirely.
- **Neat bow on every paragraph** : let at least one paragraph just stop.

### Pass 3 : add human texture

- Mix sentence lengths. Some short, some medium, occasional longer. Do not
  write three same-length sentences in a row.
- Specific over generic: "the 4/12 site walk" not "our recent visit",
  "the $8K contract" not "the project budget".
- Show position: "Yes, please proceed" beats "We are inclined to proceed
  pending certain considerations".
- Light hedging only when honest: "likely", "looks like" are fine. Avoid
  "it could be argued", "some might say".
- Trust the reader. Don't editorialize about importance.
- It is OK to start a sentence with "And" or "But" once or twice.

## Quality checklist (run before returning the draft)

- [ ] Zero em-dashes
- [ ] Zero Tier 1 banned words
- [ ] Tier 2 words : max 1 each
- [ ] Tier 3 transitions : max 2 in the whole piece
- [ ] No parallel negation
- [ ] No tricolons
- [ ] No rhetorical question + answer combos
- [ ] No mirror structures in consecutive sentences
- [ ] No dramatic reveals or theatrical setups
- [ ] No inflation of importance
- [ ] Sentence length varies
- [ ] Asks are direct
- [ ] No "Hope you're doing well" type throat-clearing
- [ ] Sign-off matches the relationship (formal vs casual)
- [ ] Reads like a real person wrote it in 4 minutes between meetings

## Output protocol

**Every draft : write to an HTML file with per-section copy buttons, then open
it.** {{USER_NAME}} copies from the browser into Outlook / Gmail / Messages /
Slack / wherever. Plain chat output does not work because formatting gets lost
on copy.

### File location

Resolve the output folder in this order:
1. If working inside a subproject folder (any direct child of the workspace
   root, e.g. `<subproject>/`) → write to `<subproject>/drafts/`.
2. Otherwise → write to `drafts/` at the workspace root.

Create the `drafts/` folder if it doesn't exist.

Naming convention: `YYYYMMDD-<topic>-<recipient>.html`
Examples:
- `<subproject>/drafts/20260514-payment-schedule-contractor.html`
- `drafts/20260514-recruiter-reply-meta.html`

### HTML format with copy buttons

Use this template. Fill in `{topic}` (page title) and the sections (one per
discrete unit {{USER_NAME}} will paste somewhere : Subject, Body, Bullet asks,
follow-up text, etc.). Keep section labels short and descriptive.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Draft : {topic}</title>
<style>
  body { font-family: Calibri, Arial, sans-serif; font-size: 15px; line-height: 1.5; max-width: 760px; margin: 24px auto; padding: 0 20px; color: #1a1a1a; background: #fafafa; }
  h1 { font-size: 18px; margin: 0 0 16px; color: #444; font-weight: 600; }
  .toolbar { position: sticky; top: 0; background: #fafafa; padding: 8px 0; margin-bottom: 16px; border-bottom: 1px solid #e5e5e5; z-index: 10; }
  .copy-all { background: #2563eb; color: white; border: none; padding: 8px 14px; border-radius: 5px; cursor: pointer; font: inherit; font-weight: 600; }
  .copy-all:hover { background: #1d4ed8; }
  .copy-all.copied { background: #16a34a; }
  section.block { background: white; border: 1px solid #e5e5e5; border-radius: 6px; margin: 0 0 14px; overflow: hidden; }
  section.block > header { display: flex; align-items: center; justify-content: space-between; background: #f4f4f5; padding: 8px 12px; border-bottom: 1px solid #e5e5e5; }
  section.block > header h3 { margin: 0; font-size: 12px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; }
  section.block .copy { background: #fff; border: 1px solid #d1d5db; padding: 4px 10px; border-radius: 4px; cursor: pointer; font: inherit; font-size: 13px; color: #374151; }
  section.block .copy:hover { background: #f9fafb; }
  section.block .copy.copied { background: #16a34a; color: white; border-color: #16a34a; }
  section.block .content { padding: 14px 16px; }
  section.block .content p { margin: 0 0 10px; }
  section.block .content p:last-child { margin-bottom: 0; }
  section.block .content ul, section.block .content ol { margin: 0 0 10px; padding-left: 22px; }
  section.block .content li { margin: 0 0 4px; }
  section.block .content pre { font: inherit; white-space: pre-wrap; margin: 0; }
</style>
</head>
<body>
<h1>{topic}</h1>
<div class="toolbar"><button class="copy-all">Copy all</button></div>

<section class="block">
  <header><h3>Subject</h3><button class="copy">Copy</button></header>
  <div class="content"><p>{subject text}</p></div>
</section>

<section class="block">
  <header><h3>Body</h3><button class="copy">Copy</button></header>
  <div class="content">
    <p>{paragraph 1}</p>
    <p>{paragraph 2}</p>
  </div>
</section>

<script>
  function flash(btn, label) {
    const original = btn.textContent;
    btn.textContent = label;
    btn.classList.add('copied');
    setTimeout(() => { btn.textContent = original; btn.classList.remove('copied'); }, 1500);
  }
  document.querySelectorAll('section.block .copy').forEach(btn => {
    btn.addEventListener('click', () => {
      const text = btn.closest('section.block').querySelector('.content').innerText.trim();
      navigator.clipboard.writeText(text).then(() => flash(btn, 'Copied'));
    });
  });
  document.querySelector('.copy-all').addEventListener('click', (e) => {
    const text = [...document.querySelectorAll('section.block')].map(b => {
      const label = b.querySelector('header h3').textContent;
      const body = b.querySelector('.content').innerText.trim();
      return label + ':\n' + body;
    }).join('\n\n');
    navigator.clipboard.writeText(text).then(() => flash(e.currentTarget, 'Copied'));
  });
</script>
</body>
</html>
```

### Section guidance

- **Email**: Subject + Body (and optional Bullet asks if there's a numbered
  list of asks the recipient should answer)
- **Text / iMessage / WhatsApp**: just one Body section
- **Teams / Slack**: Body, plus a separate section for any pinned link or ask
- **Letter / formal note**: Subject (for the email cover) + Letter body
- **Cover letter / application**: Hiring-manager email + Letter body as
  separate sections
- **Multi-message thread**: one section per message {{USER_NAME}} will send

When in doubt, err on more sections. Each independently copyable unit = one
section.

### Open the file

After writing, run: `open "<full path>"` so it pops in the default browser.
(macOS — on Linux use `xdg-open`, on Windows use `start`.)

### Confirm with the "Humanized" sentinel

After you've written the file and run `open`, end your reply with a single
confirmation line so {{USER_NAME}} knows the skill ran and the content is
safe to send:

```
Humanized · <relative path from workspace root>
```

Examples:
```
Humanized · <subproject>/drafts/20260514-vendor-followup.html
Humanized · drafts/20260514-recruiter-reply.html
```

If you decided to skip the skill (per the "When NOT to apply" list), do not
output the sentinel. Don't fake it.

Offer once, briefly, to shorten / sharpen / change voice if {{USER_NAME}}
wants a different cut. No need to explain the changes you made unless they
ask.

## OSS contributions (GitHub issues / PRs)

Maintainers of popular repos spot LLM-generated content fast and close those
issues / PRs without engaging. The 3-pass cleanup catches most of it. These
are the OSS-specific tells to also strip:

| LLM tell | What humans actually write |
|---|---|
| "Thank you for this **amazing / incredible / fantastic** project" opener | No opener. Open with the issue. |
| "I hope this helps!" / "Let me know if you need any more info!" closer | Just stop. Or one short offer: "Happy to test on more setups." |
| Religiously filling every issue-template section even when N/A | Skip non-applicable sections, or write `N/A` once. Don't pad. |
| "Steps to reproduce: 1. Open app 2. Click button 3. Observe…" when it isn't actually a repro issue | Prose. Reserve numbered repros for actual bugs. |
| Over-disclosure of system info no one asked for | One line: model / OS / app version. Only what's relevant. |
| Apologetic hedging ("I'm not sure if this is the right place but…") | State the thing. Maintainer will redirect if wrong place. |
| Numbered "Summary / Context / Expected / Actual" headers on a 3-line issue | Just write the 3 lines. Use headers only when the issue actually needs structure. |
| "I'd be happy to contribute a PR for this if the maintainers think it's a good idea!" | Either open the PR or don't. Don't ask for permission to ask. |
| Excessive markdown: code blocks for single words, bold every other phrase, bullets for two-item lists | Use markdown where it earns its place. Plain prose is fine. |

### Format for OSS drafts

GitHub renders markdown in issue / PR bodies, but the HTML draft template
strips paragraph tags on copy. To make markdown survive the copy-paste,
wrap the body section content in `<pre>` so newlines and ``` fences are
preserved exactly:

```html
<section class="block">
  <header><h3>Issue body (markdown)</h3><button class="copy">Copy</button></header>
  <div class="content"><pre>{{markdown source goes here, preserving newlines}}</pre></div>
</section>
```

The `<pre>` styling rule is already in the template `<style>` block.

Sections to produce for an OSS draft:
- **Title** (one section, exact text to paste into the issue / PR title field — not humanized prose, just the title string)
- **Body (markdown)** (one section, the rendered issue / PR body)
- **Labels / area** (optional — suggested labels to apply if the repo uses them)

### What to protect for OSS specifically

- Exact code blocks, error messages, stack traces, version strings — never reword
- Reproducer commands — paste verbatim
- VCP / DDC codes, register values, technical identifiers — never paraphrase

## What to protect

- Facts. Dates. Names. Addresses. Account numbers. Contract amounts. Permit
  numbers. Never paraphrase these into looser language.
- Asks. If the draft requests confirmation by 5/15, the rewrite still requests
  confirmation by 5/15.
- Tone calibration. Vendor escalations stay measured. Family notes stay warm.
  Recruiter replies stay professional but human.

## Provenance

3-pass framework, banned-word list, structural patterns, and voices reference
adapted from https://github.com/lguz/humanize-writing-skill (MIT licensed,
attribution preserved). Workspace-kit additions : default voice rules,
no-em-dash hard rule, output protocol with per-section copy buttons,
"Humanized" confirmation sentinel.
