"""Build the Swansea Grown-Ups page from the family page source plus adults/events.jsonl.

Usage: python3 build_adults.py <family_source.html> <events.jsonl> <out.html> [BUILT yyyy-mm-dd]
The family page is the template: same engine, adult data, adult rails, no kids-only parts.
"""
import json, sys, re, os

SRC, EVJ, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
BUILT = sys.argv[4] if len(sys.argv) > 4 else "2026-10-31"
HERE = os.path.dirname(os.path.abspath(__file__))
s = open(SRC, encoding="utf-8").read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit("expected %d of %r, found %d" % (count, old[:90], n))
    s = s.replace(old, new)

def rep_re(pat, new, flags=re.S):
    global s
    s2, n = re.subn(pat, lambda m: new, s, count=1, flags=flags)
    if n != 1:
        sys.exit("regex miss: %r" % pat[:90])
    s = s2

# ---------- data ----------
SCENE = {"comedy": "mic", "music": "gig", "theatre": "stage", "film": "cinema", "sport": "stadium",
         "talks": "talk", "nights": "nightout", "classes": "paint", "social": "paint", "food": "dine", "mystery": "mystery"}
KEEP = ["id", "t", "cat", "scene", "area", "areaLabel", "indoor", "days", "span", "time", "venue", "cost",
        "ages", "ageTags", "sold", "caveat", "added", "desc", "src", "xmas"]
events = []
for line in open(EVJ, encoding="utf-8"):
    e = json.loads(line)
    if e["cat"] == "social":
        e["cat"] = "classes"
    e["scene"] = SCENE[e["cat"]]
    e["indoor"] = "out" if e["cat"] == "sport" and "Arena" not in e["venue"] else "in"
    e["ageTags"] = []
    e["days"] = sorted(set(e["days"]))
    events.append({k: e[k] for k in KEEP if k in e and e[k] not in ("", None) or k in ("days", "ageTags", "desc", "src")})
events.sort(key=lambda e: (e["days"][0], e["t"]))
ev_js = "  var EVENTS = [\n" + ",\n".join("    " + json.dumps(e, ensure_ascii=False) for e in events) + "\n  ];\n"

SOURCES = {
  "swansea": [
    {"n": "Swansea Building Society Arena", "u": "https://www.swansea-arena.co.uk/whats-on", "s": "live", "note": "Every show and its date on one page, through to 2028. Show pages add ages and prices for some shows."},
    {"n": "Swansea Grand Theatre", "u": "https://www.swanseagrand.co.uk/WhatsOn", "s": "live", "note": "Cards link to the theatre's own show pages, which open on phones. A few shows are only on its box office site, whose pages can open blank on phones; those cards say so."},
    {"n": "Taliesin Arts Centre", "u": "https://www.taliesinartscentre.co.uk/en/all-events", "s": "live", "note": "Theatre, comedy, gigs, talks, film and event cinema at Swansea University, Singleton."},
    {"n": "Swansea City AFC fixtures", "u": "https://www.swanseacity.com/news/swansea-citys-2026-27-championship-fixtures-confirmed", "s": "live", "note": "Home games only. Kick-off times come from the club's TV selection announcements; others are not set yet."},
    {"n": "Ospreys fixtures", "u": "https://www.ospreysrugby.com/news/2627-bkt-urc-fixtures-annouced-st-helens", "s": "live", "note": "Home games at St Helen's with kick-off times. The club says fixtures may change."},
    {"n": "Eventbrite, Swansea", "u": "https://www.eventbrite.co.uk/d/united-kingdom--swansea/sip-and-paint/", "s": "live", "note": "Paint and sip nights, workshops, gigs and club nights. Only events with a stated date are used."},
    {"n": "Cinema & Co., Swansea", "u": "https://ticket247.co.uk/Page/CinemaCo", "s": "watch", "note": "Independent cafe cinema. Checked 31 October: nothing dated after mid September is listed yet."},
  ],
  "nearby": [
    {"n": "Pontardawe Arts Centre", "u": "https://pontardaweartscentre.com/", "s": "live", "note": "Gigs, comedy, talks, event cinema, film club and classes, with times."},
    {"n": "Theatrau Sir Gar (Lyric, Ffwrnes, Miners')", "u": "https://www.theatrausirgar.co.uk/en/whats-on/", "s": "live", "note": "Listing gives day and month with no year; dates are read as their next occurrence. Most listings don't name which of the three theatres."},
    {"n": "Scarlets fixtures", "u": "https://www.scarlets.wales/article/full-bkt-urc-fixture-list-for-2026-27-season/", "s": "live", "note": "Home games at Parc y Scarlets with kick-off times."},
  ],
  "touring": [
    {"n": "Utilita Arena Cardiff", "u": "https://www.utilitaarenacardiff.co.uk/whats-on", "s": "live", "note": "Loads by script. November listings read on 31 October; later months still to add."},
    {"n": "The Glee Club Cardiff", "u": "https://www.glee.co.uk/cardiff/", "s": "live", "note": "Comedy club in Cardiff Bay. Times shown are doors."},
    {"n": "Wales Millennium Centre", "u": "https://www.wmc.org.uk/en/whats-on", "s": "watch", "note": "Its calendar failed to load on 31 October, so only featured shows are listed."},
    {"n": "New Theatre Cardiff", "u": "https://www.newtheatrecardiff.co.uk/whats-on/", "s": "blocked", "note": "The site blocks automatic reading."},
    {"n": "Cardiff City FC fixtures", "u": "https://www.cardiffcityfc.co.uk/news/202627-sky-bet-championship-fixtures", "s": "live", "note": "Home games. Kick-off times not set yet."},
    {"n": "Cardiff Rugby fixtures", "u": "https://www.cardiffrugby.wales/news/2026-27-urc-fixture-list-confirmed-in-landmark-150th-season/", "s": "live", "note": "Home games at Cardiff Arms Park with kick-off times."},
    {"n": "Wales rugby internationals", "u": "https://www.rugbyworld.com/news/wales-rugby-fixtures-171083", "s": "live", "note": "Principality Stadium home games with kick-off times."},
  ],
}
G2K = {"swansea": "swansea", "nearby": "nearby", "cardiff": "touring"}
for line in open(os.path.join(HERE, "sources.jsonl"), encoding="utf-8"):
    x = json.loads(line)
    SOURCES[G2K[x["g"]]].append({"n": x["n"], "u": x["u"], "s": x["s"], "note": x["note"]})
for k in SOURCES:
    SOURCES[k].sort(key=lambda x: ({"live": 0, "watch": 1, "blocked": 2}[x["s"]], x["n"].lower()))
allsrc = [dict(x, group=k) for k in ("swansea", "nearby", "touring") for x in SOURCES[k]]
for i, x in enumerate(allsrc):
    x["half"] = "Tuesday" if i % 2 == 0 else "Friday"
json.dump(allsrc, open(os.path.join(HERE, "sources_split.json"), "w"), ensure_ascii=False, indent=1)
print("sources:", len(allsrc), "live:", sum(1 for x in allsrc if x["s"] == "live"))
src_js = "  var SOURCES = " + json.dumps(SOURCES, ensure_ascii=False, indent=2).replace("\n", "\n  ") + ";\n"

# swap the data blocks (EVENTS ... SOURCES ... PLACES)
i0 = s.index("  var EVENTS = [\n"); i1 = s.index("  var SOURCES = {")
s = s[:i0] + ev_js + "\n" + s[i1:]
i0 = s.index("  var SOURCES = {"); i1 = s.index("  /* Indoor places:")
s = s[:i0] + src_js + "\n" + s[i1:]
i0 = s.index("  var PLACES = ["); i1 = s.index("  var MN=[")
s = s[:i0] + "  var PLACES = [];\n\n" + s[i1:]

rep_re(r'  var CATS = \{.*?\n  \};\n',
  '  var CATS = {\n'
  '    comedy:{label:"Comedy",short:"Comedy"}, music:{label:"Live music",short:"Music"},\n'
  '    theatre:{label:"Theatre & musicals",short:"Theatre"}, sport:{label:"Sport",short:"Sport"},\n'
  '    film:{label:"Film & screenings",short:"Film"}, talks:{label:"Talks & evenings with",short:"Talk"},\n'
  '    nights:{label:"Nights out",short:"Night out"}, classes:{label:"Classes & activities",short:"Activity"},\n'
  '    food:{label:"Food & drink",short:"Food"}, mystery:{label:"Murder mysteries",short:"Murder mystery"},\n'
  '    christmas:{label:"Christmas",short:"Christmas"}\n'
  '  };\n')
rep_re(r'  var WF = .*?\n  var MG = [^\n]*\n', '')

rep('  var BUILT = "2026-10-30";', '  var BUILT = "%s";' % BUILT) if '  var BUILT = "2026-10-30";' in s else rep_re(r'  var BUILT = "\d{4}-\d{2}-\d{2}";', '  var BUILT = "%s";' % BUILT)
rep_re(r'  var HOLS = \[.*?\n  \];\n', '  var HOLS = [];\n')
rep_re(r'  var OCCASIONS = \[.*?\n  \];\n',
  '  var OCCASIONS = [\n'
  '    {t:"Bonfire Night", s:"Fireworks nights", from:"2026-10-31", to:"2026-11-08", m:/firework|bonfire/i},\n'
  '    {t:"Autumn internationals", s:"Wales at the Principality Stadium", from:"2026-11-01", to:"2026-11-21", m:/^Wales v /},\n'
  '    {t:"Christmas party season", s:"Festive nights out, gigs and comedy", from:"2026-11-20", to:"2026-12-24", m:/christmas|xmas|festive|dolig|carol|jingle|messiah|nutcracker/i},\n'
  '    {t:"Between Christmas and New Year", s:"Something to get you out of the house", from:"2026-12-26", to:"2026-12-30", any:true},\n'
  '    {t:"New Year\'s Eve", s:"Thursday 31 December", from:"2026-12-31", to:"2026-12-31", any:true},\n'
  '    {t:"Santes Dwynwen and Valentine\'s", s:"Date night ideas", from:"2027-01-18", to:"2027-02-14", m:/dwynwen|valentine|burlesque|love|candlelight/i},\n'
  '    {t:"Six Nations", s:"Wales at home", from:"2027-02-01", to:"2027-03-21", m:/^Wales v /}\n'
  '  ];\n')

# scenes
rep('  var SC = {\n', '  var SC = {\n' + open(os.path.join(HERE, "scenes.js"), encoding="utf-8").read())

# ---------- look ----------
rep_re(r'  --museum-a:[^\n]*\n  --halloween-a:[^\n]*\n',
  '  --comedy-a:#C2405A; --music-a:#6A3FC4; --theatre-a:#A9542A; --sport-a:#2F6DB5;\n'
  '  --film-a:#3A3F8F; --talks-a:#0E7C77; --nights-a:#B5307A; --classes-a:#4C7A2E; --food-a:#B5651D; --mystery-a:#7A1F2B; --christmas-a:#1C6D46;\n')
rep('  --accent:#C2451A; --accent-bright:#FF6A3D; --accent-soft:#FCEDE6;',
    '  --accent:#4338A8; --accent-bright:#6C5CE7; --accent-soft:#EEEBFB;')
rep('  --ground:#F8F6F2;', '  --ground:#F6F5F9;')
# grown-ups keeps one look all year apart from the festive skin
rep('    if(m===10) return "halloween";\n', '')
rep('    if(m===9 || m===11) return "autumn";\n', '')
rep('{halloween:"Halloween season",festive:"Festive season",autumn:"Autumn in Swansea",\n                 "default":"What\'s on in Swansea"}',
    '{halloween:"What\'s on for grown-ups",festive:"Party season",autumn:"What\'s on for grown-ups",\n                 "default":"What\'s on for grown-ups"}')

# ---------- head + header ----------
rep('<title>Swansea Family Events</title>', '<title>Swansea Grown-Ups</title>')
rep('<span class="mark">Swansea Family</span><span class="sub">Events</span>', '<span class="mark">Swansea</span><span class="sub">Grown-Ups</span>')
rep('    <button class="tab" role="tab" aria-selected="false" data-view="places">Indoors</button>\n', '')
rep('<span class="tagline" id="seasonLabel">Autumn in Swansea</span>', '<span class="tagline" id="seasonLabel">What\'s on for grown-ups</span>')
rep('<input id="q" type="search" placeholder="Search events, venues or places" aria-label="Search events">',
    '<input id="q" type="search" placeholder="Search acts, venues or teams" aria-label="Search events">')
rep('        <option value="nearby">Nearby only</option>\n',
    '        <option value="nearby">Nearby (Neath, Llanelli, Carmarthenshire)</option>\n        <option value="cardiff">Cardiff</option>\n')
rep('    <label class="field sel"><span class="sr">Ages</span>', '    <label class="field sel" style="display:none"><span class="sr">Ages</span>')
rep('<button class="switch" id="indoorOnly" role="switch" aria-checked="false">', '<button class="switch" id="indoorOnly" role="switch" aria-checked="false" style="display:none">')

# post an event
rep('Running something for families in Swansea or nearby?', 'Running a gig, comedy night, class or night out in Swansea, nearby or Cardiff?')
rep('subject=Event%20for%20Swansea%20Family%20Events', 'subject=Event%20for%20Swansea%20Grown-Ups')
rep('          <li>Suitable ages, in your own words</li>\n', '          <li>Any age limit, like 18+</li>\n')

# sources + footer
rep('block("Swansea county",SOURCES.swansea)+block("Surrounding areas",SOURCES.nearby)+\n      (SOURCES.touring ? block("Touring and seasonal organisers",SOURCES.touring) : "")',
    'block("Swansea",SOURCES.swansea)+block("Within 45 minutes",SOURCES.nearby)+\n      (SOURCES.touring ? block("Cardiff",SOURCES.touring) : "")')
rep('<div><h4>Ages</h4><p>Shown in the organiser\'s own words. Where a source says nothing, this says nothing.</p></div>',
    '<div><h4>Age limits</h4><p>Shown in the organiser\'s own words, like 14+ or 18+. Where a source says nothing, this says nothing.</p></div>')
rep_re(r'<footer class="gut">.*?</footer>',
  '<footer class="gut">\n  <p>Swansea, everywhere within about 45 minutes, and Cardiff. Sport is home fixtures only.</p>\n'
  '  <p>An event disappears from this page by itself the day after its last date. The twice-weekly check adds new events and re-tests every source link already listed.</p>\n</footer>')
rep('<p class="calhint">Tap any day to see everything on it.</p>', '<p class="calhint">Tap any day to see everything on it.</p>')

# ---------- cards + sheet ----------
rep("    if(e.caveat) f += '<span class=\"flag warn\">Check year</span>';", "    if(e.caveat) f += '<span class=\"flag warn\">Check details</span>';")
rep("    if(e.ageTags.indexOf(\"u5\")!==-1) f += '<span class=\"flag\">Under 5s</span>';\n    if(!e.ageTags.length) f += '<span class=\"flag\">Ages n/a</span>';\n",
    "    if(/18\\+|over 18/i.test(e.ages||\"\")) f += '<span class=\"flag\">18+</span>';\n")
rep("(e.ages?'<span class=\"tag\">'+esc(e.ages)+'</span>':'<span class=\"tag unknown\">Ages not stated</span>')",
    "(e.ages?'<span class=\"tag\">'+esc(e.ages)+'</span>':'')")
rep("(e.ages?'<span class=\"tag\">'+esc(e.ages)+'</span>':'<span class=\"tag unknown\">Age suitability not stated</span>')+\n        (e.indoor===\"in\"?'<span class=\"tag in\">Indoors</span>':e.indoor===\"mixed\"?'<span class=\"tag in\">Part indoors</span>':'')+",
    "(e.ages?'<span class=\"tag\">'+esc(e.ages)+'</span>':'')+")
rep("'<p class=\"noresults\">Nothing found. Try a town or venue (Mumbles, Margam, Plantasia), or a word like Santa, panto, swim or craft.'",
    "'<p class=\"noresults\">Nothing found. Try a venue or town (Arena, Grand, Glee, Cardiff), a team, or a word like comedy, tribute or wreath.'")

# ---------- rails ----------
rep_re(r'    var defs = \[\n      \{t:"On today".*?\n    \];\n',
  '    var tp = TODAY.split("-").map(Number), dow = new Date(tp[0],tp[1]-1,tp[2]).getDay();\n'
  '    var wkA = (dow===6||dow===0) ? TODAY : plus(5-dow), wkB = dow===0 ? TODAY : plus(7-(dow===6?6:dow));\n'
  '    var ahead = plus(56);\n'
  '    var defs = [\n'
  '      {t:"On today",s:pretty(TODAY),win:[TODAY,TODAY],f:function(e){return e.days.indexOf(TODAY)!==-1;}},\n'
  '      {t:"This weekend",s:"Friday to Sunday",win:[wkA,wkB],f:function(e){return e.days.some(function(d){return d>=wkA&&d<=wkB;});}},\n'
  '      {t:"In the next seven days",s:"",win:[TODAY,week],f:function(e){return e.days.some(function(d){return d>=TODAY&&d<=week;});}},\n'
  '      {t:"Murder mysteries",s:"Dinners, plays and whodunnits in the next three months",win:[TODAY,plus(92)],f:function(e){return e.cat==="mystery" && e.days.some(function(d){return d>=TODAY&&d<=plus(92);});}},\n'
  '      {xmasSlot:true},\n'
  '      {t:"Comedy",s:"Stand-up and comedy clubs",f:function(e){return e.cat==="comedy";}},\n'
  '      {t:"Live music",s:"Gigs, tributes and concerts",f:function(e){return e.cat==="music";}},\n'
  '      {t:"Theatre & musicals",s:"",f:function(e){return e.cat==="theatre";}},\n'
  '      {t:"Sport",s:"Home fixtures, rugby and football",f:function(e){return e.cat==="sport";}},\n'
  '      {t:"Nights out",s:"Club nights, bingo, cabaret and quizzes",f:function(e){return e.cat==="nights";}},\n'
  '      {t:"Food & drink",s:"Brunches, supper clubs, tastings and markets",f:function(e){return e.cat==="food";}},\n'
  '      {t:"Classes & activities",s:"Paint and sip, wreaths, pottery, salsa and more",f:function(e){return e.cat==="classes";}},\n'
  '      {t:"Mumbles",s:"Bars, cafes and restaurants on the front and Newton Road",f:function(e){return /mumbles|west cross|langland|newton/i.test(e.areaLabel+" "+e.venue);}},\n'
  '      {t:"Regular nights",s:"Weekly and monthly: quizzes, open mics, jams and clubs",f:function(e){return /every|weekly|sundays|saturdays|first sunday|first tuesday/i.test((e.span||"")+" "+e.desc);}},\n'
  '      {t:"Film & screenings",s:"Film clubs, event cinema and live broadcasts",f:function(e){return e.cat==="film";}},\n'
  '      {t:"Talks & evenings with",s:"",f:function(e){return e.cat==="talks";}},\n'
  '      {occLater:true},\n'
  '      {t:"Cardiff",s:"About an hour by car or train",f:function(e){return e.area==="cardiff";}},\n'
  '      {t:"Worth the drive",s:"Neath, Pontardawe, Llanelli and Carmarthenshire",f:function(e){return e.area==="nearby";}},\n'
  '      {t:"Free, or pay what you can",s:"",f:isFree},\n'
  '      {t:"Book ahead",s:"Big names already on sale for later",f:function(e){return nextDay(e) > ahead;}},\n'
  '      {t:"Everything coming up",s:"In date order",f:function(){return true;}}\n'
  '    ];\n')
rep("    if(e.indoor===\"in\") f += '<span class=\"flag in\">Indoors</span>';\n    else if(e.indoor===\"mixed\") f += '<span class=\"flag in\">Part indoors</span>';\n", "")
rep('    var xmasRail = {t:"Christmas",s:"Santa, pantos, light trails and markets",f:isXmas};',
    '    var xmasRail = {t:"Christmas",s:"Festive gigs, comedy, parties and carols",f:isXmas};')
rep('    if(mo===11 || mo===12){ defs.splice(slot,1); defs.splice(2,0,xmasRail); } else defs[slot] = xmasRail;',
    '    if(mo===11 || mo===12){ defs.splice(slot,1); defs.splice(4,0,xmasRail); } else defs.splice(slot,1);')
rep('    defs.splice.apply(defs, [2,0].concat(soon));', '    defs.splice.apply(defs, [4,0].concat(soon));')

# ---------- long rows: show the first 16 cards, the rest on request (page was ~13s to draw 2,300 cards) ----------
rep('          items.map(function(e,n){ return r.rank ? rankedCard(e,n,r.win) : card(e,r.win); }).join("")+',
    '          items.slice(0,CAP).map(function(e,n){ return r.rank ? rankedCard(e,n,r.win) : card(e,r.win); }).join("")+\n'
    '          (items.length>CAP ? (MORE[i]={items:items.slice(CAP),win:r.win}, \'<button type="button" class="card morecard" data-more="\'+i+\'"><b>See all \'+items.length+\'</b><span>\'+(items.length-CAP)+\' more in this row</span><i aria-hidden="true">&#8250;</i></button>\') : "")+')
rep('  function renderRails(){\n', '  var CAP = 16, MORE = {};\n  function renderRails(){\n    MORE = {};\n')
rep('  document.addEventListener("click", function(ev){\n',
    '  document.addEventListener("click", function(ev){\n'
    '    var mo = ev.target.closest && ev.target.closest("[data-more]");\n'
    '    if(mo){ var m = MORE[mo.getAttribute("data-more")]; if(m){ mo.insertAdjacentHTML("afterend", m.items.map(function(e){ return card(e,m.win); }).join("")); mo.remove(); } return; }\n')
rep('/* ---------- card ---------- */\n',
    '/* ---------- card ---------- */\n'
    '.track .morecard{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;text-align:center;border:2px dashed var(--accent);background:var(--accent-soft);color:var(--accent);border-radius:12px;font:inherit;cursor:pointer;aspect-ratio:2/3;align-self:flex-start;padding:14px}\n'
    '.track .morecard b{font-size:18px}.track .morecard span{color:var(--ink-2);font-size:13px}.track .morecard i{font-style:normal;font-size:28px;line-height:1}\n')

open(OUT, "w", encoding="utf-8").write(s)
print("ok", len(events), "events", len(s), "bytes")
