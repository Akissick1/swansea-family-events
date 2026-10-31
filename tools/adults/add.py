"""Append adult events to events.jsonl. Usage: python3 add.py <<'EOF' [ {...}, ... ] EOF (JSON list on stdin)."""
import json, sys, datetime
ADD = "2026-10-31"
def rng(a, b):
    d0 = datetime.date.fromisoformat(a); d1 = datetime.date.fromisoformat(b); out = []
    while d0 <= d1: out.append(d0.isoformat()); d0 += datetime.timedelta(days=1)
    return out
items = json.load(sys.stdin)
seen = set()
try:
    for l in open("/home/claude/adults/events.jsonl"):
        seen.add(json.loads(l)["id"])
except FileNotFoundError:
    pass
n = 0
with open("/home/claude/adults/events.jsonl", "a") as f:
    for e in items:
        if "range" in e:
            e["days"] = rng(*e.pop("range"))
        e.setdefault("added", ADD); e.setdefault("time", ""); e.setdefault("cost", ""); e.setdefault("ages", "")
        e.setdefault("ageTags", []); e.setdefault("indoor", "in")
        for k in ("id", "t", "cat", "area", "areaLabel", "days", "venue", "desc", "src"):
            assert k in e and e[k], (e.get("id"), k)
        assert e["id"] not in seen, "duplicate " + e["id"]
        seen.add(e["id"]); f.write(json.dumps(e, ensure_ascii=False) + "\n"); n += 1
print("added", n, "total", len(seen))
