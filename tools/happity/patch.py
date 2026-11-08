"""Insert new_events.json into the family page and keep weekly under-5 sessions in their own rows.

Usage: python3 patch.py page.html new_events.json   (refuses to add an id twice)
"""
import json, sys

page, data = sys.argv[1], sys.argv[2]
s = open(page, encoding="utf-8").read()
E = json.load(open(data))

def rep(a, b, optional=False):
    global s
    if s.count(a) != 1:
        if optional and b in s:
            return
        sys.exit("anchor not found once: " + a[:70])
    s = s.replace(a, b)

# 1. Category label now covers classes too
rep('clubs:{label:"Clubs & drop-ins",short:"Clubs"}', 'clubs:{label:"Clubs & classes",short:"Clubs"}', optional=True)

# 2. (7 Nov 2026) Toddler groups now show in the date rows, so there is no filter to add.
#    Make sure nobody re-adds it by accident.
if "function isTot(" in s:
    sys.exit("page still has the old isTot filter: Ashley asked for toddler groups in the date rows")
rep('{t:"Weekend clubs and regulars",s:"Same time most weeks",\n',
    '{t:"Weekend clubs and regulars",s:"Same time most weeks",all:true,\n', optional=True)

# 3. Events
anchor = '  var EVENTS = [\n'
lines = ""
added = 0
for e in E:
    if '"id": "%s"' % e["id"] in s or '"id":"%s"' % e["id"] in s:
        continue
    lines += "    " + json.dumps(e, ensure_ascii=False, separators=(",", ":")) + ",\n"
    added += 1
rep(anchor, anchor + lines)
open(page, "w", encoding="utf-8").write(s)
print("added", added)
