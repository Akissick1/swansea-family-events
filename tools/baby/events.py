"""Baby and bump events for the family guide, 1 November 2026 batch.
Weekly sessions: every matching weekday from START to END (term ends Fri 18 Dec; listed no further so
Christmas closures are not guessed). Term courses: every week of the stated term."""
import json, datetime as dt
START, END = dt.date(2026,11,2), dt.date(2026,12,18)
WD = {"Mon":0,"Tue":1,"Wed":2,"Thu":3,"Fri":4}
def weekly(days, a=START, b=END, skip=()):
    out=[]; d=a
    while d<=b:
        if d.weekday() in [WD[x] for x in days] and d.isoformat() not in skip: out.append(d.isoformat())
        d+=dt.timedelta(1)
    return out
ADD="2026-11-01"
HAP="https://www.happity.co.uk/swansea/c/rhyme-time"
LW="Times from the Libraries Wales listing. "
HN="Day and time from the library's Happity listing, which says term time only. "
E=[]
def ev(**k):
    k.setdefault("indoor","in"); k.setdefault("cat","baby"); k.setdefault("area","swansea"); k.setdefault("added",ADD)
    E.append(k)
FREE_RHYME="Songs and action rhymes for babies and little ones with their grown-ups. "
lib=[ # id, title, library, areaLabel, days, time, ages, tags, src, note, span
 ("bb-sketty","Rhyme Time at Sketty Library","Sketty Library, Vivian Road, Sketty","Sketty",["Tue","Fri"],"10.30am to 11am","Babies to 5","https://llyfrgelloedd.cymru/event/amser-rhigwm-rhyme-time-96/","Libraries Wales lists Tuesdays; the library's Happity listing adds Fridays at the same time.","Tuesdays and Fridays to 18 December"),
 ("bb-gorseinon","Rhyme Time at Gorseinon Library","Gorseinon Library","Gorseinon",["Thu"],"2.30pm to 3pm","Babies to 5","https://llyfrgelloedd.cymru/event/amser-rhigwm-rhyme-time-714/",LW+"Free, weekly on Thursdays.","Thursdays to 17 December"),
 ("bb-pontarddulais","Rhyme Time at Pontarddulais Library","Pontarddulais Library","Pontarddulais",["Mon"],"2pm to 2.30pm","Babies to 5","https://llyfrgelloedd.cymru/event/amser-rhigwm-rhyme-time-618/",LW+"Free, weekly on Mondays.","Mondays to 14 December"),
 ("bb-fforestfach","Rhymetime at Fforestfach Library","Fforestfach Library, Kings Head Road, Gendros SA5 8DA","Fforestfach",["Wed"],"10.30am to 11am","Babies to 5","https://www.happity.co.uk/schedules/fforestfach-library-swansea-fforestfach-library-fforestfach-library-rhymetime-wednesdays-10-30-11-00","Free. Swansea Libraries also post this one as every Wednesday at 10.30am.","Wednesdays to 16 December"),
 ("bb-townhill","Rhymetime at Townhill Library","Townhill Library, Townhill SA1 6PH","Townhill",["Fri"],"2.15pm to 2.45pm","Babies to 4","https://www.happity.co.uk/schedules/townhill-library-townhill-townhill-library-rhymetime",HN+"Free.","Fridays to 18 December"),
 ("bb-stthomas","Bounce and Rhyme at St Thomas Library","St Thomas Library, Swansea SA1 8EZ","St Thomas",["Mon"],"2pm to 2.30pm","Babies to 4","https://www.happity.co.uk/schedules/st-thomas-library-swansea-st-thomas-library-bounce-and-rhyme",HN+"Free.","Mondays to 14 December"),
 ("bb-brynhyfryd","Baby Rhymetime at Brynhyfryd Library","Brynhyfryd Library, Brynhyfryd SA5 9LH","Brynhyfryd",["Tue"],"10am to 10.30am","Birth to 18 months","https://www.happity.co.uk/schedules/brynhyfryd-library-brynhyfryd-brynhyfryd-library-rhymetime",HN+"Free, and pitched at babies rather than toddlers.","Tuesdays to 15 December"),
 ("bb-penlan","Rhymetime at Penlan Library","Penlan Library, Swansea SA5 7AH","Penlan",["Fri"],"1.30pm to 2pm","Babies to 4","https://www.happity.co.uk/schedules/penlan-library-swansea-penlan-library-rhymetime",HN+"Free.","Fridays to 18 December"),
 ("bb-morriston","Rhymetime at Morriston Library","Morriston Library, Morriston SA6 7AA","Morriston",["Wed"],"10.30am to 11am","Babies to 4","https://www.happity.co.uk/schedules/morriston-library-morriston-morriston-library-rhymetime",HN+"Free.","Wednesdays to 16 December"),
 ("bb-morristonwelsh","Welsh Rhymetime at Morriston Library","Morriston Library, Morriston SA6 7AA","Morriston",["Tue"],"11am to 11.30am","Babies to 4","https://www.happity.co.uk/schedules/morriston-library-morriston-morriston-library-welsh-rhymetime",HN+"Free. Welsh songs and rhymes, no Welsh needed to join in.","Tuesdays to 15 December"),
 ("bb-oystermouth","Rhymetime at Oystermouth Library","Oystermouth Library, Dunns Lane, Mumbles SA3 4AA","Mumbles",["Thu"],"10.30am to 11am","Babies to 4","https://www.happity.co.uk/schedules/oystermouth-library-swansea-oystermouth-library-rhymetime",HN+"Free. An older Netmums listing gives Wednesdays instead, so check with the library before your first visit.","Thursdays to 17 December"),
 ("bb-gowerton","Rhyme Time at Gowerton Library","Gowerton Library, Swansea SA4 3BU","Gowerton",["Fri"],"9.30am to 10am","Babies to 5","https://www.happity.co.uk/schedules/gowerton-library-swansea-gowerton-library-rhyme-time","Day and time from the library's Happity listing, which says it runs all year. Free.","Fridays to 18 December"),
 ("bb-clydach","Baby Rhymetime at Clydach Library","Clydach Library, Swansea SA6 5LN","Clydach",["Wed"],"2pm to 2.30pm","Birth to 18 months","https://www.happity.co.uk/schedules/clydach-library-swansea-clydach-library-rhymetime",HN+"Free, and pitched at babies.","Wednesdays to 16 December"),
 ("bb-pennard","Newborn Rhymetime at Pennard Library","Pennard Library, Pennard SA3 2AD","Pennard",["Wed"],"2.30pm to 3pm","Birth to 4 months","https://www.happity.co.uk/schedules/pennard-library-pennard-pennard-library-rhymetime",HN+"Free, and set aside for the very youngest babies.","Wednesdays to 16 December"),
]
for i,t,v,a,d,tm,ag,src,note,span in lib:
    tags=["baby"] if "months" in ag else ["baby","u5"]
    ev(id=i,t=t,scene="library",areaLabel=a,days=weekly(d),span=span,time=tm,venue=v,cost="Free",ages=ag,ageTags=tags,weekly=True,
       desc=FREE_RHYME+note,src=src)
NPTS="https://www.npt.gov.uk/libraries/learning-and-wellbeing/babies-and-toddlers/"
NPTN="Bookstart song and rhyme, listed by Neath Port Talbot Libraries as term time only. "
for i,t,v,a,d,span,extra,skip in [
 ("bb-nptneath","Song and Rhyme at Neath Library","Neath Library","Neath",["Mon"],"Mondays to 14 December","",()),
 ("bb-nptpt","Song and Rhyme at Port Talbot Library","Port Talbot Library","Port Talbot",["Mon","Wed","Fri"],"Mondays, Wednesdays and Fridays to 18 December","The council's what's on page shows Monday 2 November as cancelled, so that one is left off. ",("2026-11-02",)),
 ("bb-nptpontardawe","Song and Rhyme at Pontardawe Library","Pontardawe Library","Pontardawe",["Tue"],"Tuesdays to 15 December","",()),
 ("bb-nptglynneath","Song and Rhyme at Glynneath Library","Glynneath Library","Glynneath",["Tue"],"Tuesdays to 15 December","",()),
 ("bb-nptbaglan","Song and Rhyme at Baglan and Sandfields","Baglan Library or Sandfields Library","Port Talbot",["Fri"],"Fridays to 18 December","The council lists Baglan and Sandfields together for Fridays, so ask which library before you go. ",()),
]:
    ev(id=i,t=t,scene="library",area="nearby",areaLabel=a,days=weekly(d,skip=skip),span=span,time="10.30am",venue=v,cost="Free",
       ages="Babies and toddlers",ageTags=["baby","u5"],weekly=True,desc=NPTN+extra+"Free.",src=NPTS)
BSE="https://www.babysensory.com/swanseaeast/timetable"; BSW="https://www.babysensory.com/swanseawest/timetable"
BS="Baby Sensory: lights, bubbles, puppets, signing and music, a different theme each week. "
ev(id="bb-bsmayhill",t="Baby Sensory, Mayhill",scene="baby",areaLabel="Mayhill",days=weekly(["Fri"],dt.date(2026,11,6),dt.date(2026,12,11)),
   span="Fridays, 6 November to 11 December",time="11am to 12pm",venue="Mayhill Community Centre, Mayhill Road, Swansea SA1 6TD",
   cost="£52.50 for the term, or a 3 session trial for £26.25",ages="Birth to 13 months",ageTags=["baby"],course=True,
   desc=BS+"Booked as a term, so join from the start.",src=BSE)
ev(id="bb-bspenllergaer",t="Baby Sensory, Penllergaer",scene="baby",areaLabel="Penllergaer",days=weekly(["Fri"],dt.date(2026,11,6),dt.date(2026,12,4)),
   span="Fridays, 6 November to 4 December",time="10am, 11.30am and 1.30pm",venue="RSPCA Llys Nini Animal Centre, Penllergaer",
   cost="Waiting list only",ages="Birth to 13 months, split by age",ageTags=["baby"],course=True,sold=True,
   desc=BS+"All three winter term classes were on a waiting list when checked on 1 November: 7 to 13 months at 10am, birth to 6 months at 11.30am, birth to 13 months at 1.30pm.",src=BSW)
ev(id="bb-bsammanford",t="Baby Sensory, Ammanford",scene="baby",area="nearby",areaLabel="Ammanford",days=weekly(["Thu"],dt.date(2026,11,5),dt.date(2026,12,3)),
   span="Thursdays, 5 November to 3 December",time="10am, 11.30am and 1.30pm",venue="Penybanc Welfare Hall, Penybanc Road, Ammanford SA18 3QS",
   cost="£44.75 for the term, 3 class trial £26.85 at 1.30pm",ages="Birth to 13 months, split by age",ageTags=["baby"],course=True,
   desc=BS+"Birth to 6 months at 10am, 7 to 13 months at 11.30am, birth to 13 months at 1.30pm.",src=BSW)
ev(id="bb-bsrhos",t="Baby Sensory, Rhos near Pontardawe",scene="baby",area="nearby",areaLabel="Rhos, Pontardawe",days=weekly(["Mon"],dt.date(2026,11,2),dt.date(2026,12,7)),
   span="Mondays, 2 November to 7 December",time="12.15pm and 1.30pm",venue="Rhos Community Centre, March Hywel off Plas Road, SA8 3HD",
   cost="£52.50 for the term, or a 3 session trial for £26.25",ages="Birth to 8 months at 12.15pm, birth to 13 months at 1.30pm",ageTags=["baby"],course=True,
   desc=BS+"Booked as a term.",src=BSE)
ev(id="bb-bsporttalbot",t="Baby Sensory, Port Talbot",scene="baby",area="nearby",areaLabel="Port Talbot",days=weekly(["Wed"],dt.date(2026,11,4),dt.date(2026,12,9)),
   span="Wednesdays, 4 November to 9 December",time="12.15pm",venue="St Theodore's Church, Talbot Road, Port Talbot SA13 1LB",
   cost="£52.50 for the term, or a 3 session trial for £26.25",ages="Birth to 8 months",ageTags=["baby"],course=True,
   desc=BS+"The 1.30pm class for birth to 13 months was on a waiting list when checked on 1 November.",src=BSE)
ev(id="bb-bsystrad",t="Baby Sensory, Ystradgynlais",scene="baby",area="nearby",areaLabel="Ystradgynlais",days=weekly(["Tue"],dt.date(2026,11,3),dt.date(2026,12,8)),
   span="Tuesdays, 3 November to 8 December",time="9.15am and 10.30am",venue="Cwm Wanderers AFC, Parc Afon Twrch, 90 to 94 Bethel Road, Ystradgynlais SA9 2PU",
   cost="£52.50 for the term, or a 3 session trial for £26.25",ages="Birth to 13 months",ageTags=["baby"],course=True,
   desc=BS+"Two classes each Tuesday, both booked as a term.",src=BSE)
ev(id="bb-babylovefounders",t="Babylove Newborn Group, Wind Street",scene="baby",areaLabel="City centre",days=weekly(["Thu"],b=dt.date(2026,12,17)),
   span="Thursdays to 17 December",time="1.45pm to 2.45pm",venue="Founders & Co., 24 Wind Street, Swansea SA1 1DY",
   cost="Booked in blocks through Babylove",ages="Birth to 4 months",ageTags=["baby"],course=True,weekly=True,
   desc="A postnatal group for new parents and very young babies, run by Babylove. Happity lists it as running all year, Thursdays 1.45pm to 2.45pm. Pre-booking only.",
   src="https://happity.co.uk/schedules/babylove-groups-swansea-founders-co-swansea-babylove-postnatal")
ev(id="bb-babylovepier",t="Babylove Tinies at Mumbles Pier",scene="baby",areaLabel="Mumbles",days=weekly(["Wed"],b=dt.date(2026,12,16)),
   span="Wednesdays to 16 December",time="12.30pm to 1.10pm",venue="Mumbles Pier, Mumbles Road, Swansea SA3 4EN",
   cost="Pre-booking essential through Babylove",ages="1 to 10 months",ageTags=["baby"],course=True,weekly=True,
   desc="Sensory play, music, baby massage and signing for young babies. Mumbles Pier lists Babylove on Wednesdays and Fridays; the Tinies time comes from Babylove's Happity listing. Call 07903 674253 to book.",
   src="https://www.mumbles-pier.co.uk/whats-on/childrens-events/babylove-at-mumbles-pier")
YP="Yoga Place Abertawe at St John's Church, High Street, Clydach SA6 5LN"
ev(id="bb-ypbaby",t="Mum and Baby Yoga, Clydach",scene="baby",areaLabel="Clydach",days=weekly(["Fri"]),span="Fridays to 18 December",
   time="10.30am to 11.30am",venue="St John's Church, High Street, Clydach SA6 5LN",cost="£6 a session",ages="Birth to 12 months",ageTags=["baby"],weekly=True,
   desc="Gentle yoga for parents with babies, followed by tea and cake. Happity lists it as running all year. Contact Yoga Place Abertawe before your first session.",
   src="https://www.happity.co.uk/schedules/yoga-place-abertawe-swansea-st-johns-church-mum-baby-yoga")
ev(id="bb-ypbump",t="Pregnancy Yoga, Clydach",scene="baby",areaLabel="Clydach",days=weekly(["Wed"]),span="Wednesdays to 16 December",
   time="6pm to 7.15pm",venue="St John's Church, High Street, Clydach SA6 5LN",cost="£8 a session (one line of the listing says £6)",ages="From 12 weeks pregnant to term",ageTags=["baby"],bump=True,weekly=True,
   desc="Pregnancy yoga for mums to be from 12 weeks. Happity lists it as running all year.",
   src="https://www.happity.co.uk/schedules/yoga-place-abertawe-swansea-st-johns-church-pregnancy-yoga")
ev(id="bb-wellbeingyoga",t="Mother and Baby Yoga, Walter Road",scene="baby",areaLabel="Uplands",days=weekly(["Wed"]),span="Wednesdays to 16 December",
   time="11am",venue="The Swansea Wellbeing Centre, Walter Road, Swansea SA1 5PQ",cost="Pay what you can, by donation",ages="Mums with babies",ageTags=["baby"],weekly=True,
   desc="Relax and Recharge: postnatal exercise for mums and bonding activities with babies. Listed weekly on the University Health Centre's events page. Contact Emma on 07825 269256.",
   src="https://www.universityhealthcentreswansea.nhs.wales/events/995-mother-and-baby-yoga")
for e in E:
    assert e["days"], e["id"]
    for k in ["id","t","cat","scene","area","areaLabel","days","time","venue","cost","ages","ageTags","desc","src"]: assert k in e,(e["id"],k)
json.dump(E,open("/home/claude/baby/events.json","w"),ensure_ascii=False,indent=0)
print(len(E),"events,",sum(len(e["days"]) for e in E),"dates")
