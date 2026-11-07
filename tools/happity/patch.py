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

# 2. Weekly under-5 sessions stay out of the date rows (like the baby sessions) and live in
#    "With a baby", "Little ones", "Weekend clubs and regulars", the calendar, search and filters.
OLD = '    if(!babyFocus) pool = pool.filter(function(e){ return e.cat!=="baby"; });\n'
NEW = ('    function isTot(e){ return e.weekly && e.cat==="clubs" && e.ageTags.length>0 &&\n'
       '      e.ageTags.every(function(a){ return a==="baby"||a==="u5"; }); }\n'
       '    var totFocus = babyFocus || state.age==="u5" || Object.keys(state.cats).every(function(k){ return k==="clubs" ? state.cats[k] : !state.cats[k]; });\n'
       '    if(!babyFocus) pool = pool.filter(function(e){ return e.cat!=="baby"; });\n'
       '    if(!totFocus) pool = pool.filter(function(e){ return !isTot(e); });\n')
rep(OLD, NEW, optional=True)
rep('{t:"Weekend clubs and regulars",s:"Same time most weeks",\n',
    '{t:"Weekend clubs and regulars",s:"Same time most weeks",all:true,\n', optional=True)
rep('{t:"Little ones",s:"Where the organiser says under 5s are welcome",f:',
    '{t:"Little ones",s:"Toddler groups, classes and events for under 5s",all:true,f:', optional=True)

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
