"""Add babies and bumps to the family guide page (idempotent: refuses to run twice)."""
import sys, json
P, EV = sys.argv[1], sys.argv[2]
s = open(P, encoding="utf-8").read()
assert 'baby:{label:' not in s, "already patched"
def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (old[:60], s.count(old))
    s = s.replace(old, new)
# 1 colour + flag styles
rep("--halloween-a:#77397F;", "--halloween-a:#77397F; --baby-a:#A8467A;")
rep(".flag.warn{background:#F3C969;color:#3A2A02;border-color:transparent}",
    ".flag.warn{background:#F3C969;color:#3A2A02;border-color:transparent}\n.flag.baby{background:#F7D3E4;color:#5A1638;border-color:transparent}\n.flag.course{background:#FFFFFF;color:#5A1638;border-color:transparent}")
# 2 category
rep('sport:{label:"Sport",short:"Sport"}', 'sport:{label:"Sport",short:"Sport"},\n    baby:{label:"Babies & bumps",short:"Babies"}')
# 3 age filter
rep('<option value="any">Any age</option>\n        <option value="u5">Under 5s</option>',
    '<option value="any">Any age</option>\n        <option value="baby">Babies and bumps</option>\n        <option value="u5">Under 5s</option>')
# 4 card flags
rep("""    if(e.ageTags.indexOf("u5")!==-1) f += '<span class="flag">Under 5s</span>';""",
    """    if(e.ageTags.indexOf("baby")!==-1) f += '<span class="flag baby">'+(e.bump?'Bump':'Babies')+'</span>';
    if(e.course) f += '<span class="flag course">Book a course</span>';
    else if(e.ageTags.indexOf("u5")!==-1 && e.ageTags.indexOf("baby")===-1) f += '<span class="flag">Under 5s</span>';""")
# 5 sheet tags
rep("""        (e.sold?'<span class="tag sold">Sold out</span>':'')+'</div>'+""",
    """        (e.course?'<span class="tag strong">Book a course</span>':'')+(e.weekly?'<span class="tag">Weekly</span>':'')+
        (e.sold?'<span class="tag sold">'+(e.course?'Waiting list':'Sold out')+'</span>':'')+'</div>'+""")
rep("""    if(e.sold) f += '<span class="flag sold">Sold out</span>';""",
    """    if(e.sold) f += '<span class="flag sold">'+(e.course?'Waiting list':'Sold out')+'</span>';""")
# 6 rails: weekly baby sessions live in their own row unless the viewer is looking for them
rep("""    document.getElementById("qres").hidden = true; lastResultCount = null;
    var week = plus(7);""",
    """    document.getElementById("qres").hidden = true; lastResultCount = null;
    /* Weekly baby sessions would crowd every row, so they sit in "With a baby" unless the
       Babies age filter or the Babies & bumps type alone is picked. */
    var allPool = pool;
    var babyFocus = state.age==="baby" || Object.keys(state.cats).every(function(k){ return k==="baby" ? state.cats[k] : !state.cats[k]; });
    if(!babyFocus) pool = pool.filter(function(e){ return e.cat!=="baby"; });
    var week = plus(7);""")
rep("""      {t:"Rainy day? These are indoors",s:"Where the venue is a building",""",
    """      {t:"With a baby",s:"Rhyme times, classes and bump yoga",all:true,
       f:function(e){return e.ageTags.indexOf("baby")!==-1;}},
      {t:"Rainy day? These are indoors",s:"Where the venue is a building",""")
rep("      var items = pool.filter(r.f);", "      var items = (r.all ? allPool : pool).filter(r.f);")
# hero never leads with a weekly baby session
rep("""    var out = [], seen = {};
    function add(e,kick){""", """    var out = [], seen = {};
    pool = pool.filter(function(e){ return e.cat!=="baby"; });
    function add(e,kick){""")
# 7 artwork: a cot mobile
SCENE = r'''    baby:function(u){
      var s=sky(u,"#241C42","#5A4382","#D99AAE")+stars()+'<circle class="a-glow" cx="300" cy="120" r="64" fill="#FFE3B8" opacity=".16"/>';
      s+='<path d="M200 40v74" stroke="#F6E7CF" stroke-width="3"/><circle cx="200" cy="40" r="6" fill="#F6E7CF"/>'+
        '<path d="M86 150Q200 96 314 150" fill="none" stroke="#F6E7CF" stroke-width="5" stroke-linecap="round"/>';
      [[104,262],[162,318],[238,300],[298,250]].forEach(function(p){ s+='<path d="M'+p[0]+' '+(148-(p[0]>150&&p[0]<250?24:0))+'V'+(p[1]-26)+'" stroke="#F6E7CF" stroke-width="1.6" opacity=".8"/>'; });
      s+='<path d="M118 262a24 24 0 1 1-20-34a19 19 0 1 0 20 34z" fill="#FFD98E"/>'+
        '<path d="M162 296l7 15 16 2-12 11 3 16-14-8-14 8 3-16-12-11 16-2z" fill="#F7C6DA"/>'+
        '<path d="M214 300a16 16 0 0 1 22-15a20 20 0 0 1 36 6a14 14 0 0 1 0 28h-56a14 14 0 0 1-2-19z" fill="#E8F1FF"/>'+
        '<path d="M298 262c-14-10-24-18-24-30a12 12 0 0 1 24-4a12 12 0 0 1 24 4c0 12-10 20-24 30z" fill="#FF9DB8"/>';
      s+='<rect y="430" width="400" height="170" fill="#3B2A5C"/>'+
        '<path d="M0 452c60-22 120-22 200 0s140 22 200 0v148H0z" fill="#F4C7D6"/>'+
        '<path d="M0 500c70-18 130-18 200 0s130 18 200 0v100H0z" fill="#E7A9C0" opacity=".9"/>';
      for(var x=40;x<=360;x+=40) s+='<rect x="'+(x-4)+'" y="400" width="8" height="70" rx="4" fill="#F6E7CF" opacity=".85"/>';
      return s+'<rect x="24" y="392" width="352" height="12" rx="6" fill="#F6E7CF"/>';},

'''
rep("    play:function(u){", SCENE + "    play:function(u){")
# 8 data
ev = json.load(open(EV, encoding="utf-8"))
ids = [e["id"] for e in ev]
for i in ids: assert '"id":"%s"' % i not in s and '"id": "%s"' % i not in s, i
rows = ",\n".join("    " + json.dumps(e, ensure_ascii=False, separators=(",", ":")) for e in ev)
rep("  var EVENTS = [\n", "  var EVENTS = [\n" + rows + ",\n")
# 9 sources
SW = [
 ("Libraries Wales events","https://llyfrgelloedd.cymru/","live","National library events listing. Swansea rhyme times with weekly pattern: Sketty Tuesdays, Gorseinon Thursdays, Pontarddulais Mondays."),
 ("Happity, Swansea rhyme times","https://www.happity.co.uk/swansea/c/rhyme-time","live","Each Swansea library's rhymetime day, time, age range and term time or all year. Plain fetches are refused, read through Firecrawl."),
 ("Swansea Council library events","https://www.swansea.gov.uk/libraryevents","blocked","Links to a page per library and a Spydus catalogue of events, both refuse automated reads. Libraries Wales and Happity carry the same sessions."),
 ("Baby Sensory Swansea East","https://www.babysensory.com/swanseaeast/timetable","live","Term dates, times, ages and prices for Mayhill, Port Talbot, Rhos and Ystradgynlais. Timetable loads by script, read through Firecrawl."),
 ("Baby Sensory Swansea West","https://www.babysensory.com/swanseawest/timetable","live","Term dates for Penllergaer (Llys Nini) and Ammanford. Franchise is advertising for a new owner, so watch for changes."),
 ("Babylove groups","https://www.happity.co.uk/babylove-groups/swansea","live","Baby groups at Founders & Co, Mumbles Pier, LC Swansea and All Saints Mumbles. Venue pages and the provider page disagree on some slots, so only the two consistent ones are listed."),
 ("Mumbles Pier children's events","https://www.mumbles-pier.co.uk/whats-on/childrens-events/babylove-at-mumbles-pier","live","Babylove on Wednesdays and Fridays, pre-booking essential."),
 ("Yoga Place Abertawe","https://www.happity.co.uk/schedules/yoga-place-abertawe-swansea-st-johns-church-mum-baby-yoga","live","Mum and baby yoga Fridays, pregnancy yoga Wednesdays, St John's Church Clydach, all year."),
 ("Swansea Wellbeing Centre","https://www.universityhealthcentreswansea.nhs.wales/events/995-mother-and-baby-yoga","live","Mother and baby yoga, Wednesdays 11am, by donation."),
 ("Water Babies Swansea","https://www.waterbabies.co.uk/baby-swimming/wales-south-west/the-village-hotel-swansea/","watch","Baby swimming at the Village Hotel. Class times only appear after a postcode and due date search, so nothing dated to list."),
 ("Glynn Vivian Art Babas","https://www.glynnvivian.co.uk/art-babas/","watch","Sensory art sessions from 6 months. No dates listed on 1 November."),
 ("National Waterfront Museum, Little Mice","https://museum.wales/swansea/whatson/","watch","Under 5s Museum Little Mice sessions. Last dated one was December 2025, none listed for this winter yet."),
 ("Cinema & Co baby screenings","https://ticket247.co.uk/Event/baby-friendly-screening-at-cinema-co.-swansea-405025","watch","Has run baby friendly screenings before, none on sale on 1 November."),
 ("ODEON Swansea Newbies","https://www.odeon.co.uk/special-screenings/odeon-newbies/","blocked","Parent and baby screenings for under 2s. ODEON's site refuses automated reads, so no dates confirmed."),
]
NB = [
 ("Neath Port Talbot Libraries, babies and toddlers","https://www.npt.gov.uk/libraries/learning-and-wellbeing/babies-and-toddlers/","live","Bookstart song and rhyme days and times for Neath, Port Talbot, Pontardawe, Glynneath, Baglan and Sandfields, term time only. Cancellations show on the council's what's on page."),
]
def src_rows(lst): return "".join('\n      {n:%s,u:%s,s:%s,note:%s},' % tuple(json.dumps(x, ensure_ascii=False) for x in r) for r in lst)
rep("  var SOURCES = {\n    swansea:[", "  var SOURCES = {\n    swansea:[" + src_rows(SW))
i = s.index("var SOURCES"); j = s.index("\n    nearby:[", i)
s = s[:j] + "\n    nearby:[" + src_rows(NB) + s[j + len("\n    nearby:["):]
open(P, "w", encoding="utf-8").write(s)
print("patched:", len(ev), "events,", len(SW) + len(NB), "sources")
