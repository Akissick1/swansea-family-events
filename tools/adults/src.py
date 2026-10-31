"""Append sources: python3 src.py <<'EOF' [ {n,u,s,note,g} ] EOF   g = swansea|nearby|cardiff"""
import json,sys
items=json.load(sys.stdin); seen=set()
try:
    for l in open("sources.jsonl"): seen.add(json.loads(l)["u"])
except FileNotFoundError: pass
with open("sources.jsonl","a") as f:
    for s in items:
        assert s["g"] in ("swansea","nearby","cardiff") and s["s"] in ("live","watch","blocked")
        if s["u"] in seen: continue
        seen.add(s["u"]); f.write(json.dumps(s,ensure_ascii=False)+"\n")
print("sources",len(seen))
