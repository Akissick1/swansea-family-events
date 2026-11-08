"""Run ledger for the family refresh: every source that is due gets a line, and the run
cannot call itself finished while any due line is unread, part-read or failed.

Added 8 November 2026 after Ashley asked how to make sure every site is checked on every run.

  python3 tools/family/ledger.py plan [YYYY-MM-DD]
      Lists the sources due today (EVERY, plus MON or THU by weekday, plus MONTHLY on the
      first run of the month) and every source carried over from the last run's retry list.
      Writes tools/family/ledger.tsv with status "todo" for each.
  python3 tools/family/ledger.py mark ID STATUS [PAGE_TOTAL] [READ_COUNT] [NOTE...]
      STATUS is full, limited, partial, failed or blocked. "limited" is only for a known,
      permanent limit of the site (Freedom Leisure timetables show today only) and needs a note. Give the page's own total and how many
      items you captured whenever the page prints a total. full with READ_COUNT < PAGE_TOTAL
      is refused.
  python3 tools/family/ledger.py check PAGE.html [PREVIOUS_PAGE.html]
      Exit code 0 only when every due source is "full" and the page passes its checks.
      Otherwise prints ATTENTION lines, writes tools/family/retry.tsv so the next run starts
      with those sources, and exits 1. Paste its output into last_run.md and lead the phone
      notification with the first ATTENTION line.
"""
import csv, datetime as dt, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCES = os.path.join(HERE, "sources.tsv")
LEDGER = os.path.join(HERE, "ledger.tsv")
RETRY = os.path.join(HERE, "retry.tsv")
HISTORY = os.path.join(HERE, "source_history.tsv")
COLS = ["id", "schedule", "name", "url", "status", "page_total", "read_count", "note"]


def read(path):
    if not os.path.exists(path):
        return []
    return list(csv.DictReader(open(path, encoding="utf-8"), delimiter="\t"))


def write(path, rows, cols):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def first_run_of_month(day):
    """True when no run has been logged yet this calendar month."""
    return not [h for h in read(HISTORY) if h["date"][:7] == day.isoformat()[:7] and h["date"] < day.isoformat()]


def plan(day):
    wd = day.weekday()
    half = {0: "MON", 3: "THU"}.get(wd, "MON" if wd < 3 else "THU")
    monthly = first_run_of_month(day)
    due = []
    for s in read(SOURCES):
        sch = s["schedule"]
        if sch == "EVERY" or sch == half or (sch == "MONTHLY" and monthly):
            due.append(dict(s, status="todo", page_total="", read_count="", note=""))
    ids = {d["id"] for d in due}
    for r in read(RETRY):
        if r["id"] not in ids:
            due.append(dict(r, status="todo", page_total="", read_count="",
                            note="carried over: " + r.get("note", "")))
            ids.add(r["id"])
    # anything not read in full for 14 days is due regardless of its schedule
    last_full = {}
    for h in read(HISTORY):
        if h["status"] == "full":
            last_full[h["id"]] = max(last_full.get(h["id"], ""), h["date"])
    cutoff = (day - dt.timedelta(days=14)).isoformat()
    for s in read(SOURCES):
        if s["id"] not in ids and s["schedule"] != "MONTHLY" and s["id"] in last_full and last_full[s["id"]] < cutoff:
            due.append(dict(s, status="todo", page_total="", read_count="", note="stale: not read in full for 14 days"))
            ids.add(s["id"])
    write(LEDGER, due, COLS)
    print(f"{day} {half} half{' + monthly' if monthly else ''}: {len(due)} sources due")
    for d in due:
        print(f"  {d['id']:>5} [{d['schedule']}] {d['name']}  {d['url']}  {d['note']}")


def mark(sid, status, total="", count="", note=""):
    assert status in ("full", "limited", "partial", "failed", "blocked"), "status must be full, limited, partial, failed or blocked"
    if status == "limited" and not note:
        sys.exit("limited needs a note saying what the page cannot show (for example: today only)")
    rows = read(LEDGER)
    hit = [r for r in rows if r["id"] == sid]
    if not hit:
        sys.exit(f"{sid} is not in today's ledger; run plan first or check the id")
    if status == "full" and total and count and int(count) < int(total):
        sys.exit(f"refused: {sid} read {count} of {total}. That is partial, not full. Keep reading or mark it partial.")
    hit[0].update(status=status, page_total=total, read_count=count, note=note)
    write(LEDGER, rows, COLS)


def page_checks(page, prev):
    out = []
    s = open(page, encoding="utf-8").read()
    ids = re.findall(r'\{"id":\s*"([^"]+)"', s)
    if len(ids) != len(set(ids)):
        dup = sorted({i for i in ids if ids.count(i) > 1})
        out.append(f"duplicate event ids: {', '.join(dup[:8])}")
    if "function isTot(" in s:
        out.append("the old toddler filter is back in the page (Ashley asked for toddler groups in the date rows)")
    bad = re.findall(r'"src":\s*"(?!https?://)([^"]*)"', s)
    if bad:
        out.append(f"{len(bad)} events have no web link in src")
    if prev and os.path.exists(prev):
        p = open(prev, encoding="utf-8").read()
        n0 = len(set(re.findall(r'\{"id":\s*"([^"]+)"', p)))
        n1 = len(set(ids))
        if n0 and n1 < n0 * 0.85:
            out.append(f"event count fell from {n0} to {n1}: check nothing was dropped by mistake")
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
    full = len(rows) - len(bad)
    print(f"Sources: {full} of {len(rows)} due sources read in full or as far as the site allows.")
    for r in limited:
        print(f"Known limit: {r['name']}: {r['note']}")
    for r in bad:
        what = {"todo": "not checked", "partial": "only partly read", "failed": "failed",
                "blocked": "blocked"}[r["status"]]
        extra = f" ({r['read_count']} of {r['page_total']})" if r["page_total"] else ""
        print(f"ATTENTION: {r['name']} {what}{extra}. {r['note']}".strip())
    for p in problems:
        print(f"ATTENTION: {p}")
    if bad:
        print(f"These {len(bad)} sources are first in the queue for the next run (tools/family/retry.tsv).")
    sys.exit(1 if bad or problems else 0)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "plan":
        plan(dt.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else dt.date.today())
    elif cmd == "mark":
        a = sys.argv[2:]
        mark(a[0], a[1], *(a[2:4]), " ".join(a[4:]))
    elif cmd == "check":
        check(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    else:
        print(__doc__)
