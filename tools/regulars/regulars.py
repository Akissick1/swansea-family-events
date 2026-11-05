"""Add weekend regulars, a Clubs category and a 'This weekend' rail to the family page.

Usage: python3 regulars.py <page.html>   (edits in place, refuses to run twice)
Only dates a public page states are used. Weekly cards skip 24 Dec to 1 Jan.
"""
import json, sys, datetime as dt

ADDED = "2026-11-03"
SKIP = ("2026-12-24", "2027-01-01")

def sats(start, end):
    d = dt.date.fromisoformat(start)
    out = []
    while d.isoformat() <= end:
        s = d.isoformat()
        if not (SKIP[0] <= s <= SKIP[1]):
            out.append(s)
        d += dt.timedelta(days=7)
    return out

def weekends(start_sat, end):
    out = []
    for s in sats(start_sat, end):
        out.append(s)
        sun = (dt.date.fromisoformat(s) + dt.timedelta(days=1)).isoformat()
        if sun <= end and not (SKIP[0] <= sun <= SKIP[1]):
            out.append(sun)
    return out

NPT = "https://www.npt.gov.uk/culture-and-tourism/whats-on-in-npt/event-details/?id="

EV = [
  {"id":"rg-llansamletlego","t":"Lego Club at Llansamlet Library","cat":"clubs","scene":"library",
   "area":"swansea","areaLabel":"Llansamlet","days":sats("2026-11-07","2026-12-19"),
   "span":"Saturdays, all year","time":"10am to 11am",
   "venue":"Llansamlet Library, 242 Peniel Green Road, Swansea SA7 9BD","cost":"Ask the library",
   "ages":"2 and over","ageTags":["u5","5-11"],"weekly":True,"indoor":"in",
   "desc":"Weekly Lego building session. Happity lists it as every Saturday, all year, with no booking system, so ring the library before a first visit.",
   "src":"https://www.happity.co.uk/schedules/llansamlet-library-swansea-llansamlet-library-lego-club"},
  {"id":"rg-sandfieldskids","t":"Saturday Kids Club, Sandfields Library","cat":"clubs","scene":"library",
   "area":"nearby","areaLabel":"Sandfields","days":["2026-11-07","2026-11-14","2026-11-21","2026-11-28"],
   "span":"Saturdays","time":"From 10am",
   "venue":"Sandfields Library, Morrison Road, Sandfields, Port Talbot SA12 6TG","cost":"Free",
   "ages":"Children","ageTags":["5-11"],"weekly":True,"indoor":"in",
   "desc":"Board games, colouring, puzzles, Lego and footballs to borrow. Neath Port Talbot lists it every Saturday in November. Call 01639 883616 to book or ask.",
   "src":NPT+"55984"},
  {"id":"rg-baglanlego","t":"Saturday Lego and Colouring Club, Baglan Library","cat":"clubs","scene":"library",
   "area":"nearby","areaLabel":"Baglan","days":["2026-11-07","2026-11-14","2026-11-21","2026-11-28"],
   "span":"Saturdays","time":"From 10am",
   "venue":"Baglan Library, Laurel Avenue, Baglan, Port Talbot SA12 8PA","cost":"Free",
   "ages":"Children","ageTags":["5-11"],"weekly":True,"indoor":"in",
   "desc":"Lego building and colouring. Neath Port Talbot lists it every Saturday in November. Questions to 01639 813477.",
   "src":NPT+"59560"},
  {"id":"rg-ptlego","t":"Lego Club, Port Talbot Library","cat":"clubs","scene":"library",
   "area":"nearby","areaLabel":"Port Talbot","days":["2026-11-07","2026-11-14","2026-11-21","2026-11-28"],
   "span":"Saturdays","time":"2.30pm",
   "venue":"Port Talbot Library, Aberafan Shopping Centre, Port Talbot SA13 1PB","cost":"Free",
   "ages":"Children","ageTags":["5-11"],"weekly":True,"indoor":"in",
   "desc":"Saturday afternoon Lego building. Neath Port Talbot lists it every Saturday in November. Questions to 01639 763490.",
   "src":NPT+"53698"},
  {"id":"rg-ptpokemon","t":"Pokemon Club, Port Talbot Library","cat":"clubs","scene":"library",
   "area":"nearby","areaLabel":"Port Talbot","days":["2026-11-14","2026-11-28"],
   "span":"Alternate Saturdays","time":"10.30am",
   "venue":"Port Talbot Library, Aberafan Shopping Centre, Port Talbot SA13 1PB","cost":"Free",
   "ages":"6 and over","ageTags":["5-11","12+"],"indoor":"in",
   "desc":"Bring cards to trade and battle, plus a character hunt and Lego. To reserve a place, email l.hayes@npt.gov.uk.",
   "src":NPT+"53985"},
  {"id":"rg-glynneathlego","t":"Lego Club, Glynneath Library","cat":"clubs","scene":"library",
   "area":"nearby","areaLabel":"Glynneath","days":["2026-11-07"],
   "time":"11am",
   "venue":"Glynneath Library, Park Avenue, Glynneath SA11 5DW","cost":"Free",
   "ages":"","ageTags":[],"indoor":"in",
   "desc":"Lego building session. Only this date is listed so far. Questions to 01639 720776.",
   "src":NPT+"56962"},
  {"id":"rg-vuemornings","t":"Mighty Mornings kids' films, Vue Swansea","cat":"shows","scene":"cinema",
   "area":"swansea","areaLabel":"Swansea","days":weekends("2026-11-07","2026-12-20"),
   "span":"Every weekend","time":"Morning showings from about 10am",
   "venue":"Vue Swansea, Salubrious Place, Swansea","cost":"Cheap tickets; Vue charged £2.49 online in 2025",
   "ages":"Family films","ageTags":["u5","5-11"],"weekly":True,"indoor":"in",
   "desc":"Vue's low-price weekend morning screenings of family films. The film changes each week and listings go up on Tuesdays, so check the Vue Swansea page for this weekend's title and time.",
   "src":"https://www.myvue.com/cinema/swansea/whats-on"},
]

CAT_OLD = 'baby:{label:"Babies & bumps",short:"Babies"}\n  };'
CAT_NEW = 'baby:{label:"Babies & bumps",short:"Babies"},\n    clubs:{label:"Clubs & drop-ins",short:"Clubs"}\n  };'
TOK_OLD = '--sport-a:#3A5C99;'
TOK_NEW = '--sport-a:#3A5C99; --clubs-a:#0F6A8C;'
RAIL_OLD = '      {t:"With a baby",s:"Rhyme times, classes and bump yoga",all:true,'
RAIL_NEW = ('      {t:"This weekend",s:pretty(wkS)+" and "+pretty(wkE),win:[wkS,wkE],\n'
            '       f:function(e){return e.days.some(function(d){return d>=wkS&&d<=wkE;});}},\n'
            '      {t:"Weekend clubs and regulars",s:"Same time most weeks",\n'
            '       f:function(e){return e.weekly && e.days.some(function(d){var p=d.split("-").map(Number),w=new Date(p[0],p[1]-1,p[2]).getDay();return w===0||w===6;});}},\n'
            + RAIL_OLD)
WK_OLD = '    var week = plus(7);\n'
WK_NEW = ('    var week = plus(7);\n'
          '    var dw = (function(){var p=TODAY.split("-").map(Number);return new Date(p[0],p[1]-1,p[2]).getDay();})();\n'
          '    var wkS = plus(dw===0 ? -1 : 6-dw), wkE = plus(dw===0 ? 0 : 7-dw);\n')
EV_ANCHOR = '  var EVENTS = [\n'

def main(path):
    s = open(path, encoding="utf-8").read()
    if '"rg-llansamletlego"' in s or 'clubs:{label' in s:
        sys.exit("already patched")
    for old in (CAT_OLD, TOK_OLD, RAIL_OLD, WK_OLD, EV_ANCHOR):
        if s.count(old) != 1:
            sys.exit("anchor not found once: " + old[:50])
    s = s.replace(CAT_OLD, CAT_NEW).replace(TOK_OLD, TOK_NEW)
    s = s.replace(RAIL_OLD, RAIL_NEW).replace(WK_OLD, WK_NEW)
    lines = ""
    for e in EV:
        e["added"] = ADDED
        lines += "    " + json.dumps(e, ensure_ascii=False) + ",\n"
    s = s.replace(EV_ANCHOR, EV_ANCHOR + lines)
    # existing weekly events that predate the flag
    for i in ("parkrun", "parkrunjr", "quiet", "bgwelly"):
        a = '{id:"%s",' % i
        if s.count(a) == 1:
            s = s.replace(a, a + 'weekly:true,')
    open(path, "w", encoding="utf-8").write(s)
    print("added", len(EV), "events")

if __name__ == "__main__":
    main(sys.argv[1])
