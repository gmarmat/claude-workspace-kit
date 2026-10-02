#!/usr/bin/env python3
"""ctx.py : two-step context for large Claude Code projects (load little every session, search the rest on a miss).

Stdlib only (Python 3.9+). Driven by a `.context-hygiene.json` in the managed folder (see the example config).

  python3 ctx.py check   [--dir D]           sizes, token budget, PRIOR count, pending roll/compact, journal lint
  python3 ctx.py roll    [--dir D] [--apply] threads file: dated sections / rows older than N days -> the "older" file
  python3 ctx.py compact [--dir D] [--apply] state file: keep NEXT block(s) + K PRIOR, move older blocks -> the archive
  python3 ctx.py find    [--dir D] <terms..> [--max N]   step 2: search every tier-2 file, print hit lines only
  python3 ctx.py log     [--dir D] <field> [<field>..] [--at HH:MM] [--from-tz Area/City]
                                             append one journal line, time stamped by the machine

Moves are lossless and verified (every moved line must exist in the destination). Dry run unless --apply.
Exit codes: check -> 1 if anything to fix; roll/compact -> 1 if a verify fails; find/log -> 0.
"""
import datetime, glob, json, os, pathlib, re, sys

try:
    from zoneinfo import ZoneInfo
except ImportError:  # Python < 3.9
    ZoneInfo = None


# ---------------------------------------------------------------- config
def load(argv):
    d = pathlib.Path(".")
    if "--dir" in argv:
        i = argv.index("--dir"); d = pathlib.Path(argv[i + 1]); del argv[i:i + 2]
    d = d.resolve()
    cfgp = d / ".context-hygiene.json"
    if not cfgp.exists():
        sys.exit(f"no .context-hygiene.json in {d} (copy context-hygiene.example.json and edit it)")
    cfg = json.loads(cfgp.read_text(encoding="utf-8"))
    return d, cfg


def tz(cfg):
    name = cfg.get("timezone", "UTC")
    return ZoneInfo(name) if ZoneInfo else datetime.timezone.utc


def today(cfg):
    return datetime.datetime.now(tz(cfg)).date()


def rel(d, p):
    return pathlib.Path(os.path.normpath(d / os.path.expanduser(p)))


# ---------------------------------------------------------------- roll (threads)
DATE_RE = re.compile(r"(20\d\d)-(\d\d)-(\d\d)")
SEP_RE = re.compile(r"^\|[\s:|-]+\|$")


MD_RE = re.compile(r"(?<![\d/.])(\d{1,2})/(\d{1,2})(?:/(\d{2}|\d{4}))?(?![\d/])")


def heading_date(h):
    ds = [datetime.date(int(y), int(m), int(dd)) for y, m, dd in DATE_RE.findall(h)]
    return max(ds) if ds else None


def latest_date(text, year, horizon=None):
    """Latest date anywhere in text: YYYY-MM-DD, or M/D[/YY] (year defaults to `year`). Invalid dates are skipped."""
    ds = []
    for y, m, dd in DATE_RE.findall(text):
        try: ds.append(datetime.date(int(y), int(m), int(dd)))
        except ValueError: pass
    for m, dd, y in MD_RE.findall(text):
        yy = int(y) + 2000 if y and len(y) == 2 else int(y) if y else year
        try: ds.append(datetime.date(yy, int(m), int(dd)))
        except ValueError: pass
    if horizon:   # ignore sentinels (01/01/2200) and far-future data values; near deadlines still count
        ds = [x for x in ds if x <= horizon]
    return max(ds) if ds else None


def roll_plan(cfg, lines):
    t = cfg["threads"]
    cutoff = today(cfg) - datetime.timedelta(days=t.get("days", 14))
    never = [s.lower() for s in t.get("neverMove", [])]
    row_re = re.compile(t.get("rowDatePattern", r"\(carried from (\d{1,2})/(\d{1,2})"))
    year = t.get("rowYear", today(cfg).year)
    level = t.get("sectionLevel", "## ")
    closed = [c.lower() for c in t.get("closedSections", [])]
    horizon = today(cfg) + datetime.timedelta(days=t.get("futureDays", 60))
    dest_of = lambda h: "closed" if any(c in h.lower() for c in closed) else "older"
    kept, moved, i = [], [], 0
    section, header, in_preamble = None, None, True
    while i < len(lines):
        ln = lines[i]
        if ln.startswith(level) and not ln.startswith(level + "#"):
            in_preamble = False
            section, header = ln, None
            protected = any(n in ln.lower() for n in never)
            j = i + 1
            while j < len(lines) and not (lines[j].startswith(level) and not lines[j].startswith(level + "#")):
                j += 1
            if t.get("sectionDate", "heading") == "latest":   # latest date in heading OR body (opt-in)
                d = latest_date("\n".join(lines[i:j]), int(year), horizon)
            else:                                              # heading date only (default)
                d = heading_date(ln)
            if d and d < cutoff and not protected:
                moved.append((dest_of(ln), None, None, lines[i:j])); i = j; continue
        elif ln.startswith("|") and i + 1 < len(lines) and SEP_RE.match(lines[i + 1].strip()):
            header = [ln, lines[i + 1]]; kept += header; i += 2; continue
        elif header and ln.startswith("| ") and section and not any(n in section.lower() for n in never):
            rd, m = None, row_re.search(ln)
            if m:
                try:
                    rd = datetime.date(int(year), int(m.group(1)), int(m.group(2)))
                except ValueError:
                    rd = None
            elif any(x.lower() in section.lower() for x in t.get("rowDateSections", [])):
                # opt-in, named sections only (ledger-style tables): a row is as old as the latest date in it
                rd = latest_date(ln, int(year), horizon)
            if rd and rd < cutoff:
                moved.append((dest_of(section), section, header, [ln])); i += 1; continue
        kept.append(ln); i += 1
    # drop tables left with only a header
    out, j = [], 0
    while j < len(kept):
        if (kept[j].startswith("|") and j + 1 < len(kept) and SEP_RE.match(kept[j + 1].strip())
                and not (j + 2 < len(kept) and kept[j + 2].startswith("| "))):
            j += 2; continue
        out.append(kept[j]); j += 1
    return out, moved, cutoff


def roll_render(moved, cutoff, stamp):
    out, last = [f"\n## Rolled {stamp} (dated before {cutoff})\n"], None
    for _, sec, header, rows in moved:
        if sec is None:
            out.append("\n".join(rows).rstrip() + "\n"); last = None; continue
        key = (sec, tuple(header))
        if key != last:
            out.append(f"\n### from: {sec.lstrip('#').strip()}\n\n" + "\n".join(header)); last = key
        out.append(rows[0])
    return "\n".join(out).rstrip() + "\n"


def older_head(cfg):
    t = cfg["threads"]
    return (f"# Older open threads (not read by default)\n\nItems older than {t.get('days', 14)} days, rolled out of "
            f"`{t['file']}` by `ctx.py roll`. **Still open, not closed.** Search: `python3 ctx.py find <terms>`. "
            f"When one comes back to life, move it back with today's date.\n")


def cmd_roll(d, cfg, argv):
    if "threads" not in cfg:
        print("roll: no 'threads' block in .context-hygiene.json, nothing to do"); return 0
    t = cfg["threads"]
    src, dst = d / t["file"], d / t["older"]
    lines = src.read_text(encoding="utf-8").splitlines()
    kept, moved, cutoff = roll_plan(cfg, lines)
    if "--count" in argv:
        print(len(moved)); return 0
    print(f"roll {t['file']}: cutoff {cutoff} · {len(moved)} block(s)/row(s) to move · {len(lines) - len(kept)} line(s) out")
    for _, s, _, r in moved[:6]:
        print("   ", r[0][:110])
    if len(moved) > 6:
        print(f"    … {len(moved) - 6} more")
    nclosed = sum(1 for m in moved if m[0] == "closed")
    if nclosed:
        print(f"    ({nclosed} from closed sections -> {t.get('closedArchive')})")
    if "--apply" not in argv or not moved:
        return 0
    stamp, dests = today(cfg).isoformat(), []
    for kind, path, head in (("older", dst, older_head(cfg)),
                             ("closed", d / t["closedArchive"] if t.get("closedArchive") else dst,
                              f"# Closed threads archive (not read by default)\n")):
        part = [m for m in moved if m[0] == kind]
        if not part:
            continue
        body = path.read_text(encoding="utf-8") if path.exists() else head
        path.write_text(body.rstrip() + "\n" + roll_render(part, cutoff, stamp), encoding="utf-8")
        dests.append(path)
    src.write_text("\n".join(kept).rstrip() + "\n", encoding="utf-8")
    return verify(lines, kept, *dests)


def verify(before, kept, *dsts):
    """Every line that left the source must exist verbatim in a destination."""
    keep, dest = set(kept), "\n".join(p.read_text(encoding="utf-8") for p in dsts)
    lost = [l for l in before if l.strip() and l not in keep and l not in dest]
    print(f"    applied · verify {'OK' if not lost else 'LOST ' + str(len(lost))}")
    for l in lost[:5]:
        print("      LOST:", l[:100])
    return 1 if lost else 0


# ---------------------------------------------------------------- compact (state)
def compact_plan(cfg, lines):
    s = cfg["state"]
    prefix, marker, k = s.get("blockPrefix", "## "), s.get("priorMarker", "PRIOR"), s.get("keepPriors", 1)
    keep_heads = [x.lower() for x in s.get("keepHeadings", [])]
    starts = [i for i, l in enumerate(lines) if l.startswith(prefix) and not l.startswith(prefix.rstrip() + "#")]
    if not starts:
        return lines, []
    head, blocks = lines[:starts[0]], []
    for a, b in zip(starts, starts[1:] + [len(lines)]):
        blocks.append(lines[a:b])
    keep, move, priors, cut = [], [], 0, False
    for b in blocks:
        h = b[0].lower()
        if any(x in h for x in keep_heads):
            keep.append(b); continue
        if cut:
            move.append(b); continue
        keep.append(b)
        if marker.lower() in h:
            priors += 1
            if priors >= k:
                cut = True
    return head + [l for b in keep for l in b], move


def cmd_compact(d, cfg, argv):
    if "state" not in cfg:
        print("compact: no 'state' block in .context-hygiene.json, nothing to do"); return 0
    s = cfg["state"]
    src, dst = d / s["file"], d / s["archive"]
    lines = src.read_text(encoding="utf-8").splitlines()
    kept, move = compact_plan(cfg, lines)
    if "--count" in argv:
        print(len(move)); return 0
    print(f"compact {s['file']}: {len(move)} block(s) to archive · {sum(len(b) for b in move)} line(s) out")
    for b in move[:6]:
        print("   ", b[0][:110])
    if "--apply" not in argv or not move:
        return 0
    pointer = s.get("pointerHeading", "## Older blocks")
    if not any(l.startswith(pointer) for l in kept):
        kept += ["", pointer, "", f"Archived to `{s['archive']}` (not read by default). Search: `python3 ctx.py find <terms>`."]
    body = dst.read_text(encoding="utf-8") if dst.exists() else f"# {s['file']} archive (not read by default)\n"
    stamp = today(cfg).isoformat()
    add = f"\n## Archived {stamp} from `{s['file']}`\n\n" + "\n".join(l for b in move for l in b)
    dst.write_text(body.rstrip() + "\n" + add.rstrip() + "\n", encoding="utf-8")
    src.write_text("\n".join(kept).rstrip() + "\n", encoding="utf-8")
    return verify(lines, kept, dst)


# ---------------------------------------------------------------- find (step 2)
def cmd_find(d, cfg, argv):
    mx = 25
    if "--max" in argv:
        i = argv.index("--max"); mx = int(argv[i + 1]); del argv[i:i + 2]
    terms = [a.lower() for a in argv if not a.startswith("--")]
    if not terms:
        sys.exit("usage: ctx.py find <term> [more terms] [--max N]")
    files, seen = [], set()
    for rank, pat in enumerate(cfg.get("tier2", [])):
        for f in sorted(glob.glob(str(rel(d, pat)), recursive=True)):
            if f not in seen and os.path.isfile(f):
                seen.add(f); files.append((rank, f))
    hits = []
    for rank, f in files:
        try:
            lines = open(f, encoding="utf-8", errors="replace").read().splitlines()
        except OSError:
            continue
        for n, ln in enumerate(lines, 1):
            low = ln.lower(); k = sum(t in low for t in terms)
            if k:
                hits.append((-(k == len(terms)), -k, rank, os.path.relpath(f, d), n, ln.strip()))
    hits.sort()
    full = sum(1 for h in hits if h[0] == -1)
    print(f"find {' '.join(terms)} · {len(files)} files · {len(hits)} line(s), {full} with all terms · showing {min(mx, len(hits))}")
    for h in hits[:mx]:
        print(f"  {h[3]}:{h[4]}  {h[5][:150]}")
    if not hits:
        print("  nothing in tier 2: try other terms, or ask")
    return 0


# ---------------------------------------------------------------- log (journal)
def cmd_log(d, cfg, argv):
    j = cfg.get("journal")
    if not j:
        sys.exit("no 'journal' block in .context-hygiene.json")
    at, src_tz = None, None
    if "--at" in argv:
        i = argv.index("--at"); at = argv[i + 1]; del argv[i:i + 2]
    if "--from-tz" in argv:
        i = argv.index("--from-tz"); src_tz = argv[i + 1]; del argv[i:i + 2]
    fields = [a for a in argv if a.strip()]
    if not fields or any("\n" in f for f in fields):
        sys.exit("usage: ctx.py log <field> [<field>..] (single-line fields)")
    now = datetime.datetime.now(tz(cfg)); when = now
    if at:
        m = re.fullmatch(r"(\d{1,2}):(\d{2})", at)
        if not m:
            sys.exit("--at must be HH:MM")
        z = ZoneInfo(src_tz) if (src_tz and ZoneInfo) else tz(cfg)
        when = datetime.datetime.now(z).replace(hour=int(m[1]), minute=int(m[2]), second=0, microsecond=0).astimezone(tz(cfg))
        if when > now + datetime.timedelta(minutes=5):
            sys.exit(f"{at} is in the future ({when:%H:%M} vs now {now:%H:%M}): wrong --from-tz?")
    label = cfg.get("timezoneLabel", "")
    line = f"{when:%Y-%m-%d %H:%M}{' ' + label if label else ''} · " + " · ".join(fields)
    p = d / j["file"]
    text = p.read_text(encoding="utf-8") if p.exists() else ""
    with p.open("a", encoding="utf-8") as fh:
        fh.write(("" if not text or text.endswith("\n") else "\n") + line + "\n")
    print(line); return 0


def journal_lint(d, cfg):
    j = cfg.get("journal")
    if not j or not (d / j["file"]).exists():
        return []
    label = cfg.get("timezoneLabel", "")
    pat = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2})" + (re.escape(" " + label) if label else "") + r" · ")
    since = j.get("since", "0000")
    now = datetime.datetime.now(tz(cfg)).replace(tzinfo=None)
    issues, prev = [], None
    for ln in (d / j["file"]).read_text(encoding="utf-8").splitlines():
        ln = re.sub(r"^\s*-\s+", "", ln)
        if not re.match(r"^\d{4}-\d{2}-\d{2}", ln) or ln[:10] < since:
            continue
        m = pat.match(ln)
        if not m:
            issues.append("journal format: " + ln[:80]); continue
        ts = datetime.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M")
        if ts > now + datetime.timedelta(minutes=5):
            issues.append("journal future time: " + ln[:80])
        if prev and ts < prev - datetime.timedelta(minutes=30):
            issues.append("journal out of order: " + ln[:80])
        prev = ts
    return issues


# ---------------------------------------------------------------- check
def cmd_check(d, cfg, argv):
    warns, total = [], 0
    print(f"context check · {d.name}")
    for t in cfg.get("tier1", []):
        p = rel(d, t["file"])
        if not p.exists():
            warns.append(f"{t['file']} missing"); continue
        text = p.read_text(encoding="utf-8")
        n, tok = text.count("\n"), len(text) // 4
        total += tok
        lim = t.get("maxLines")
        bad = lim is not None and n > lim
        print(f"  {'WARN' if bad else 'ok  '} {t['file']:<28} {n:>5} lines{f' (limit {lim})' if lim else ''} · ~{tok:,} tokens")
        if bad:
            warns.append(f"{t['file']}: {n} lines > {lim}")
    budget = cfg.get("tokenBudget")
    if budget:
        print(f"  {'WARN' if total > budget else 'ok  '} tier-1 total ~{total:,} tokens (budget {budget:,})")
        if total > budget:
            warns.append(f"tier-1 ~{total:,} tokens > {budget:,}")
    if "state" in cfg:
        s = cfg["state"]; lines = (d / s["file"]).read_text(encoding="utf-8").splitlines()
        _, move = compact_plan(cfg, lines)
        print(f"  {'WARN' if move else 'ok  '} {s['file']}: {len(move)} block(s) beyond NEXT + {s.get('keepPriors', 1)} PRIOR")
        if move:
            warns.append(f"{s['file']}: run `ctx.py compact --apply`")
    if "threads" in cfg:
        t = cfg["threads"]; lines = (d / t["file"]).read_text(encoding="utf-8").splitlines()
        _, moved, cutoff = roll_plan(cfg, lines)
        print(f"  {'WARN' if moved else 'ok  '} {t['file']}: {len(moved)} item(s) dated before {cutoff}")
        if moved:
            warns.append(f"{t['file']}: run `ctx.py roll --apply`")
    vt = cfg.get("versionTable")
    if vt:
        rows = len(re.findall(r"^\| \d+\.\d+(\.\d+)? \|", rel(d, vt["file"]).read_text(encoding="utf-8"), re.M))
        if rows > vt.get("max", 3):
            warns.append(f"{vt['file']}: {rows} version rows > {vt.get('max', 3)}")
    warns += journal_lint(d, cfg)
    for w in warns:
        print("  WARN " + w)
    print("context: within limits" if not warns else f"context: {len(warns)} to fix")
    return 1 if warns else 0


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] not in ("check", "roll", "compact", "find", "log"):
        sys.exit(__doc__)
    cmd = argv.pop(0)
    d, cfg = load(argv)
    return {"check": cmd_check, "roll": cmd_roll, "compact": cmd_compact, "find": cmd_find, "log": cmd_log}[cmd](d, cfg, argv)


if __name__ == "__main__":
    sys.exit(main())
