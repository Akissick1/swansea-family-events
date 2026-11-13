"""Run ledger for the Grown-Ups refresh (Tuesdays and Fridays). Same idea as tools/family/ledger.py:
every source that is due gets a line, and the run cannot call itself finished while any due line is
unread, part-read, failed or blocked. Anything not read in full goes first on the next run.

Added 13 November 2026 after Ashley asked for the family retry checklist on the Grown-Ups refresh too.

  python3 tools/adults/ledger.py plan [YYYY-MM-DD]
      Lists the sources due today from tools/adults/sources_split.json: today's half (Tuesday or
      Friday; on any other day the most recent of the two), the three every-run sources (Mumbles.life,
      Swansea Arena, Swansea Scoop), every source carried over from the last run's retry list, and any
      source not read in full for 14 days. Carried-over sources are listed first.
      Writes tools/adults/ledger.tsv with status "todo" for each.
  python3 tools/adults/ledger.py mark ID STATUS [PAGE_TOTAL] [READ_COUNT] [NOTE...]
      STATUS is full, limited, partial, failed or blocked. "limited" is only for a known, permanent
      limit of the site and needs a note. Give the page's own total and how many items you captured
      whenever the page prints a total. full with READ_COUNT < PAGE_TOTAL is refused.
      ID is the id printed by plan (the source name in lower case with hyphens).
  python3 tools/adults/ledger.py check PAGE.html [PREVIOUS_PAGE.html]
      Exit code 0 only when every due source is "full" or "limited" and the page passes its checks.
      Otherwise prints ATTENTION lines, writes tools/adults/retry.tsv so the next run starts with those
      sources, and exits 1. Lead the phone notification with the first ATTENTION line.

Reading rule: read only what a visitor's browser sees. Never call hidden data feeds or internal APIs,
and never try to get round a site's security checks. A site that blocks automated reading is marked
"blocked" with a note and retried next run.
"""
import csv, datetime as dt, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCES = os.path.join(HERE, "sources_split.json")
LEDGER = os.path.join(HERE, "ledger.tsv")
RETRY = os.path.join(HERE, "retry.tsv")
HISTORY = os.path.join(HERE, "source_history.tsv")
COLS = ["id", "half", "name", "url", "status", "page_total", "read_count", "note"]
EVERY_RUN = re.compile(r"mumbles\.life|swansea-arena\.co\.uk|swanseascoop\.com")
MUST_HAVE = ['id="modebar"', "This weekend", "Book ahead", "Murder mysteries", "Food & drink",
             "Classes & activities", "Mumbles", "Regular nights", "SWIPE-HINTS v1"]


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def read(path):
    if not os.path.exists(path):
        return []
    return list(csv.DictReader(open(path, encoding="utf-8"), delimiter="\t"))


def write(path, rows, cols):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def sources():
    out = []
    for s in json.load(open(SOURCES, encoding="utf-8")):
        half = "EVERY" if EVERY_RUN.search(s["u"]) else s.get("half", "")
        out.append({"id": slug(s["n"]), "half": half, "name": s["n"], "url": s["u"], "site_status": s.get("s", "")})
    return out


def todays_half(day):
    # Tuesday covers Tue, Wed, Thu; Friday covers Fri to Mon
    return "Tuesday" if day.weekday() in (1, 2, 3) else "Friday"


def plan(day):
    half = todays_half(day)
    src = sources()
    by_id = {s["id"]: s for s in src}
    due, ids = [], set()
    for r in read(RETRY):  # carried over first
        s = by_id.get(r["id"])
        if not s or r["id"] in ids:
            continue
        due.append(dict(s, status="todo", page_total="", read_count="", note="carried over: " + r.get("note", "")))
        ids.add(r["id"])
    for s in src:
        if s["id"] not in ids and s["half"] in ("EVERY", half):
            due.append(dict(s, status="todo", page_total="", read_count="", note=""))
            ids.add(s["id"])
    last_full = {}
    for h in read(HISTORY):
        if h["status"] in ("full", "limited"):
            last_full[h["id"]] = max(last_full.get(h["id"], ""), h["date"])
    cutoff = (day - dt.timedelta(days=14)).isoformat()
    for s in src:
        if s["id"] not in ids and s["id"] in last_full and last_full[s["id"]] < cutoff:
            due.append(dict(s, status="todo", page_total="", read_count="", note="stale: not read in full for 14 days"))
            ids.add(s["id"])
    write(LEDGER, due, COLS)
    print(f"{day} {half} half: {len(due)} sources due")
    for d in due:
        print(f"  {d['id']} [{d['half']}] {d['name']}  {d['url']}  {d['note']}")


def mark(sid, status, total="", count="", note=""):
    if status not in ("full", "limited", "partial", "failed", "blocked"):
        sys.exit("status must be full, limited, partial, failed or blocked")
    if status == "limited" and not note:
        sys.exit("limited needs a note saying what the page cannot show")
    rows = read(LEDGER)
    hit = [r for r in rows if r["id"] == sid]
    if not hit:
        sys.exit(f"{sid} is not in today's ledger; run plan first or check the id")
    if status == "full" and total and count and int(count) < int(total):
        sys.exit(f"refused: {sid} read {count} of {total}. That is partial, not full. Keep reading or mark it partial.")
    hit[0].update(status=status, page_total=total, read_count=count, note=note)
    write(LEDGER, rows, COLS)


def events(s):
    i = s.find("var EVENTS = [")
    if i < 0:
        return None
    block = s[i:]
    block = block[:block.index("\n  ];")]
    return [json.loads(l.strip().rstrip(",")) for l in block.splitlines()[1:] if l.strip().startswith("{")]


def norm(x, k=None):
    x = re.sub(r"[^a-z0-9]", "", (x or "").lower())
    return x[:k] if k else x


def page_checks(page, prev):
    out = []
    s = open(page, encoding="utf-8").read()
    try:
        ev = events(s)
    except Exception as e:
        return [f"the EVENTS block does not parse ({e})"]
    if ev is None:
        return ["no EVENTS block found in the page"]
    ids = [e["id"] for e in ev]
    if len(ids) != len(set(ids)):
        dup = sorted({i for i in ids if ids.count(i) > 1})
        out.append(f"duplicate event ids: {', '.join(dup[:8])}")
    seen, pairs = {}, set()
    for e in ev:
        for day in e.get("days", []):
            k = (norm(e.get("t")), norm(e.get("venue"), 10), day)
            if k in seen and seen[k] != e["id"]:
                pairs.add(tuple(sorted((seen[k], e["id"]))))
                break
            seen[k] = e["id"]
    if pairs:
        out.append(f"{len(pairs)} event{'s' if len(pairs) > 1 else ''} listed twice (same title, venue and day): " +
                   "; ".join(f"{a} and {b}" for a, b in sorted(pairs)[:6]) + ". Keep the older one.")
    missing = [m for m in MUST_HAVE if m not in s]
    if missing:
        out.append("the page is missing: " + ", ".join(missing))
    bad = [e["id"] for e in ev if not str(e.get("src", "")).startswith("http")]
    if bad:
        out.append(f"{len(bad)} events have no web link in src: {', '.join(bad[:6])}")
    if prev and os.path.exists(prev):
        try:
            n0 = len(events(open(prev, encoding="utf-8").read()) or [])
        except Exception:
            n0 = 0
        if n0 and len(ev) < n0 * 0.85:
            out.append(f"event count fell from {n0} to {len(ev)}: check nothing was dropped by mistake")
    return out


def check(page, prev=None):
    rows = read(LEDGER)
    if not rows:
        sys.exit("no ledger: run plan at the start of the run")
    bad = [r for r in rows if r["status"] not in ("full", "limited")]
    limited = [r for r in rows if r["status"] == "limited"]
    problems = page_checks(page, prev)
    today = dt.date.today().isoformat()
    hist = read(HISTORY)
    for r in rows:
        hist.append({"date": today, "id": r["id"], "status": r["status"],
                     "page_total": r["page_total"], "read_count": r["read_count"]})
    write(HISTORY, hist[-3000:], ["date", "id", "status", "page_total", "read_count"])
    write(RETRY, bad, COLS)
    print(f"Sources: {len(rows) - len(bad)} of {len(rows)} due sources read in full or as far as the site allows.")
    for r in limited:
        print(f"Known limit: {r['name']}: {r['note']}")
    if bad:
        names = ", ".join(r["name"] for r in bad[:4]) + (f" and {len(bad) - 4} more" if len(bad) > 4 else "")
        print(f"ATTENTION: {len(bad)} of {len(rows)} sources not read in full: {names}. They go first next run.")
    for r in bad:
        what = {"todo": "not checked", "partial": "only partly read", "failed": "failed", "blocked": "blocked"}[r["status"]]
        extra = f" ({r['read_count']} of {r['page_total']})" if r["page_total"] else ""
        print(f"  - {r['name']} {what}{extra}. {r['note']}".rstrip())
    for p in problems:
        print(f"ATTENTION: {p}")
    sys.exit(1 if bad or problems else 0)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "plan":
        plan(dt.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else dt.date.today())
    elif cmd == "mark":
        a = sys.argv[2:]
        if len(a) < 2:
            sys.exit("usage: mark ID STATUS [PAGE_TOTAL] [READ_COUNT] [NOTE...]")
        mark(a[0], a[1], *(a[2:4]), " ".join(a[4:]))
    elif cmd == "check":
        check(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    else:
        print(__doc__)
