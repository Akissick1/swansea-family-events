"""Turn the Happity weekday sweep into family-guide records for every class not already listed.

Usage: python3 build.py sweep_YYYY-MM-DD.tsv page.html  -> writes new_events.json and report.txt
Rules (Ashley, 7 Nov 2026): every class the sweep finds goes on the site unless it is adults only,
has no usable dates, or is already listed from another source. One card per activity per venue.
Weekly dates: next sessions to 23 Dec, term-time classes skip HOLS, nothing 24 Dec to 1 Jan.
"""
import csv, json, re, sys, datetime as dt
from collections import OrderedDict

ADDED = "2026-11-07"
START, END = "2026-11-07", "2026-12-23"
HOLS = [("2026-12-21", "2027-01-01")]
SKIP = ("2026-12-24", "2027-01-01")
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
LONG = {"Mon": "Mondays", "Tue": "Tuesdays", "Wed": "Wednesdays", "Thu": "Thursdays",
        "Fri": "Fridays", "Sat": "Saturdays", "Sun": "Sundays"}
BASE = "https://www.happity.co.uk/schedules/"

# Already on the site from another source (schedule slug prefix or provider+venue key)
COVERED_SLUGS = [
    "sketty-library-swansea-sketty-library-rhymetime", "pontarddulais-library-pontarddulais",
    "story-babies-swansea-the-lighthouse-bar-kitchen-and-lounge-tiny-babies",
    "story-babies-swansea-the-lighthouse-bar-kitchen-and-lounge-bouncing-babies",
    "baby-sensory-swansea-rhos-community-centre", "baby-sensory-port-talbot-st-theodore",
    "baby-sensory-swansea-mayhill", "baby-sensory-ammanford-penybanc",
]
# Left out, with the reason given in the report
EXCLUDE = {
    "st-david-s-church-morriston-swansea-st-david-s-church-morriston-parent-and-toddler-group": "same group as St David's Baby and Toddler Group, merged into that card",
    "st-illtyd-s-swansea-st-illtyd-s-church-hall-play-group": "same session as St Peter's Baby Group at St Illtyd's, merged into that card",
    "annabel-s-school-of-dance-swansea-st-hilary-church-absolute-beginner-adult-ballet": "adults only",
    "little-nest-baby-wellness-bridgend-kenfig-national-nature-reserve-luxury-baby-spa-christmas-special": "one-off event, the listing shows no date",
    "little-nest-baby-wellness-bridgend-kenfig-national-nature-reserve-baby-massage-course": "fixed course, the listing shows no course dates",
    "annabel-s-school-of-dance-swansea-st-hilary-church-ballet-class": "selected dates only, no dates shown",
}
# RKLSwims and others marked "Selected dates": only the next date the listing shows
NEXT_ON = {"RKLSwims": {"Wed": ["2026-11-11"], "Sun": ["2026-11-08"]}}

PLACE = {  # venue -> (areaLabel, area)
    "Ebenezer Baptist Church": ("Swansea city centre", "swansea"), "Townhill Baptist Church": ("Townhill", "swansea"),
    "The Vivian Hall": ("Blackpill", "swansea"), "Sketty Community Church": ("Tycoch", "swansea"),
    "St. David's Church Morriston": ("Morriston", "swansea"), "Capel y Nant": ("Clydach", "swansea"),
    "Village Hotel Swansea": ("SA1 Swansea", "swansea"), "Singleton day nursery": ("Sketty", "swansea"),
    "All Saints church": ("Mumbles", "swansea"), "Kenfig National Nature Reserve": ("Kenfig", "nearby"),
    "Resolven Building Blocks Centre": ("Resolven", "nearby"), "Cornelly Scout Hall": ("North Cornelly", "nearby"),
    "Clase Community Cwtch": ("Clase", "swansea"), "Teilo's Community Cwtch": ("Portmead", "swansea"),
    "SA18 1UN (Ammanford)": ("Ammanford", "nearby"), "St Thomas Library": ("St Thomas", "swansea"),
    "St Theodore's Parish Hall": ("Port Talbot", "nearby"), "Venue.No.1": ("Swansea", "swansea"),
    "Pentrehafod School": ("Hafod", "swansea"), "Mount Elim Evangelical Church": ("Pontardawe", "nearby"),
    "LC Swansea": ("Swansea city centre", "swansea"), "Norton Village Hall": ("Norton, Mumbles", "swansea"),
    "Tircoed Village Hall": ("Tircoed", "swansea"), "Tircoed Forest Village Hall": ("Tircoed", "swansea"),
    "Sgiliau Llanelli": ("Llanelli", "nearby"), "Cornelly Community Centre": ("North Cornelly", "nearby"),
    "Bonymaen Family Cwtch": ("Bonymaen", "swansea"), "Swansea Tennis Centre": ("Sketty Lane", "swansea"),
    "The Lighthouse Bar & Kitchen And Lounge": ("Mumbles", "swansea"), "Llanelli Leisure Centre": ("Llanelli", "nearby"),
    "Siloam Baptist Church Killay": ("Killay", "swansea"), "Clare House School Porthcawl": ("Porthcawl", "nearby"),
    "RKLSwims": ("Llanelli", "nearby"), "The Mission Church": ("Morriston", "swansea"),
    "Pantygwydr Baptist Church": ("Uplands", "swansea"), "East Early Help Hub": ("Penlan", "swansea"),
    "St Theodore's Church, Port Talbot": ("Port Talbot", "nearby"), "Mumbles Pier": ("Mumbles", "swansea"),
    "Llys Nini Animal Centre": ("Penllergaer", "swansea"), "Ty'n Cellar Farm Community Centre": ("Kenfig Hill", "nearby"),
    "Killay Library": ("Killay", "swansea"), "Go Underhill Hwb": ("Mumbles", "swansea"),
    "Treboeth Gospel Hall": ("Treboeth", "swansea"), "Ammanford Pensioners' Hall": ("Ammanford", "nearby"),
    "Ebenezer Evangelical Church (Neath)": ("Neath", "nearby"), "Baglan Community Church": ("Baglan", "nearby"),
    "The Hub Youth & Community Centre": ("Swansea city centre", "swansea"), "Founders & Co. Swansea": ("Wind Street", "swansea"),
    "Community Centre (Gendros)": ("Gendros", "swansea"), "Purple Elephant Cakes Swansea": ("Morriston", "swansea"),
    "Gorseinon Institute": ("Gorseinon", "swansea"), "Parc Llewelyn Community Centre": ("Morriston", "swansea"),
    "Urban Zen Yoga & Movement Studio": ("Swansea city centre", "swansea"), "Townhill Library": ("Townhill", "swansea"),
    "Bulldogs Boxing & Community Activities": ("Port Talbot", "nearby"), "Pontarddulais Comprehensive School": ("Pontarddulais", "swansea"),
    "Cimla Community Centre": ("Cimla, Neath", "nearby"), "DCF Church Swansea": ("Dunvant", "swansea"),
    "St Illtyd's Church Fforestfach": ("Fforestfach", "swansea"), "St.Illtyd's Church Hall": ("Fforestfach", "swansea"),
    "Libanus Evangelical Church": ("Morriston", "swansea"), "Saron Hall": ("Saron, Ammanford", "nearby"),
    "Seven Sisters community hall": ("Seven Sisters", "nearby"), "SA13 1RF (Port Talbot)": ("Port Talbot", "nearby"),
    "Parklands Church Swansea": ("Sketty", "swansea"), "Sketty Park Community Centre": ("Sketty Park", "swansea"),
    "Morriston Library": ("Morriston", "swansea"), "Llansamlet Library": ("Llansamlet", "swansea"),
}

def months(txt):
    """Return (min,max) age in months from Happity's age text, or None."""
    t = txt.split("(")[0].lower()
    if "antenatal" in t or "parents" in t:
        return None
    parts = [p.strip() for p in t.split(" - ")]
    def one(p):
        y = re.search(r"(\d+)\s*year", p); m = re.search(r"(\d+)\s*month", p)
        if y or m:
            return (int(y.group(1)) * 12 if y else 0) + (int(m.group(1)) if m else 0)
        n = re.match(r"(\d+)", p)
        return int(n.group(1)) * (12 if "year" in t else 1) if n else None
    if len(parts) == 2:
        lo, hi = one(parts[0]), one(parts[1])
        if parts[0].isdigit():  # "0 - 4 years"
            lo = int(parts[0]) * (12 if "year" in parts[1] else 1)
        return lo, hi
    lo = one(parts[0])
    if lo is None:
        return None
    return (lo, 18) if lo < 12 else (lo, 144)

def tags(ages, prov, cls):
    if re.search(r"pregnan|antenatal", cls, re.I):
        return ["baby"], True
    r = months(ages)
    if not r:
        return [], False
    lo, hi = r
    if hi <= 18:
        return ["baby"], False
    t = []
    if lo < 12: t.append("baby")
    if lo < 60 and hi > 12: t.append("u5")
    if hi >= 60 and lo < 144: t.append("5-11")
    if hi >= 144 and hi < 999: t.append("12+")
    return t, False

def dates(day, term, start=START, end=END):
    wd = DAYS.index(day)
    d = dt.date.fromisoformat(start)
    out = []
    while d.isoformat() <= end:
        s = d.isoformat()
        if d.weekday() == wd and not (SKIP[0] <= s <= SKIP[1]):
            if not (term.startswith("Term") and any(a <= s <= b for a, b in HOLS)):
                out.append(s)
        d += dt.timedelta(days=1)
    return out

def t12(hm):
    h, m = map(int, hm.split(":"))
    s = f"{h % 12 or 12}" + (f".{m:02d}" if m else "") + ("am" if h < 12 else "pm")
    return s

def slug(s):
    return re.sub(r"[^a-z0-9]+", "", s.lower())[:22]

def main(tsv, page):
    rows = list(csv.DictReader(open(tsv), delimiter="\t"))
    src_page = open(page, encoding="utf-8").read()
    report = {"covered": [], "excluded": [], "added": []}
    groups = OrderedDict()
    for r in rows:
        s = r["schedule"]
        if s in src_page or any(s.startswith(c) for c in COVERED_SLUGS):
            report["covered"].append(f'{r["day"]} {r["time"]} {r["provider"]}: {r["class"]}, {r["venue"]}')
            continue
        if s in EXCLUDE:
            report["excluded"].append(f'{r["day"]} {r["provider"]}: {r["class"]}, {r["venue"]} ({EXCLUDE[s]})')
            continue
        cls = r["class"].replace(" (second listing)", "")
        key = (r["provider"], cls, r["venue"])
        groups.setdefault(key, []).append(r)

    out = []
    for (prov, cls, venue), rs in groups.items():
        r0 = rs[0]
        area_label, area = PLACE[venue]
        ageTags, bump = tags(r0["ages"], prov, cls)
        # slots per day, de-duplicated
        slots = OrderedDict()
        for r in rs:
            a, b = r["time"].split("-")
            slots.setdefault(r["day"], [])
            txt = f"{t12(a)} to {t12(b)}"
            if txt not in slots[r["day"]]:
                slots[r["day"]].append(txt)
        days = []
        sel = NEXT_ON.get(prov)
        for d in slots:
            days += sel[d] if sel else dates(d, r0["term"])
        days = sorted(set(days))
        if not days:
            report["excluded"].append(f"{prov}: {cls}, {venue} (no dates in window)")
            continue
        dlist = [d for d in DAYS if d in slots]
        if len(dlist) == 1:
            time = " and ".join(slots[dlist[0]])
        else:
            time = "; ".join(f"{d} " + " and ".join(slots[d]) for d in dlist)
        pattern = " and ".join(LONG[d] for d in dlist)
        if sel:
            span = "Next dates on Happity"
        elif r0["term"].startswith("Term"):
            span = f"{pattern}, term time"
        elif r0["term"] == "Selected dates":
            span = f"{pattern}, selected dates"
        else:
            span = f"{pattern}, all year"
        generic = cls.lower() in {"toddlers", "toddler group", "parent & toddler group", "play group", "baby group",
                                  "kids club", "busy bees", "tiny tots", "mums and tots", "parent and toddler group"}
        if prov.lower() in cls.lower() or cls == prov:
            title = f"{cls}, {area_label}" if venue.lower() in prov.lower() or prov in venue else f"{cls}, {venue}"
        elif generic or prov.split()[0] in venue:
            title = f"{cls}, {venue}"
        else:
            title = f"{prov}: {cls}, {venue}"
        title = title.replace("Swansea Tennis Centre (Tots to Tops): ", "")
        cost = r0["cost"].replace("From free", "Free")
        if cost.startswith("From "):
            cost = cost + " (Happity price)"
        ages = r0["ages"].replace(" (card says 2 months - 4 months)", "")
        if "Tennis" in prov:
            ages = "2 to 4 years"
        term_note = {"Term time only": "Term time only.", "All year": "Runs all year.",
                     "Selected dates": "Runs on selected dates only."}.get(r0["term"], "")
        who = venue if (prov.split()[0] in venue or venue.split()[0] in prov) else f"{prov} at {venue}"
        desc = (f"{who}, listed on Happity. {term_note} "
                f"Book or check the next session on the Happity listing before going.").replace("  ", " ")
        if sel:
            desc = (f"{prov} at {venue}. Happity lists these on selected dates and shows only the next one, "
                    f"so book through the listing and check later dates there.")
        if cls == "St David's Baby and Toddler Group":
            desc += " Happity also lists a Parent and Toddler Group at the same church and time, marked all year, which looks like the same group."
        if prov == "St Peter's Community Centre":
            desc += " Happity also lists a Play Group at St Illtyd's Church Hall at the same time, which looks like the same session."
            title = "Baby and toddler group, St Illtyd's Church, Fforestfach"
        if prov == "Treboeth Gospel Hall":
            title = "Lighthouse kids club, Treboeth Gospel Hall"
        if prov == "Townhill Library" and cls == "Craft Club":
            ageTags = ["u5", "5-11"]; ages = "All ages"
        if "Tiny Toes Ballet Pontardullais" in cls:
            desc += " Happity lists the session as 9am to 12pm with an age range of 6 to 7 months, which looks like a listing error, so check the class times with Tiny Toes."
        cat = "baby" if (ageTags == ["baby"] or bump) else "clubs"
        scene = "library" if "Library" in venue else ("swim" if re.search(r"swim", cls, re.I) else ("baby" if cat == "baby" else "play"))
        rec = {"id": "hp-" + str(len(out)+1).zfill(3) + "-" + slug(prov)[:12] + slug(cls)[:10], "t": title, "cat": cat, "scene": scene,
               "area": area, "areaLabel": area_label, "days": days, "span": span, "time": time,
               "venue": f"{venue}, {area_label} ({r0['pc']})", "cost": cost, "ages": ages, "ageTags": ageTags,
               "weekly": not bool(sel), "indoor": "in", "desc": desc, "src": BASE + r0["schedule"], "added": ADDED}
        if bump:
            rec["bump"] = True
        out.append(rec)
        report["added"].append(f"{title} [{cat}] {span} {time}")

    ids = [o["id"] for o in out]
    assert len(ids) == len(set(ids)), "duplicate ids"
    json.dump(out, open("new_events.json", "w"), ensure_ascii=False, indent=0)
    with open("report.txt", "w") as f:
        for k in ("added", "covered", "excluded"):
            f.write(f"== {k} ({len(report[k])})\n" + "\n".join(report[k]) + "\n")
    print({k: len(v) for k, v in report.items()}, "records", len(out))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
