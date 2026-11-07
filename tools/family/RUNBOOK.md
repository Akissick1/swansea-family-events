SWANSEA FAMILY EVENTS, REFRESH RUNBOOK
This file is read by the twice-weekly scheduled task (Mondays and Thursdays, Opus). The task prompt itself is short and points here. Edit this file in the repo to change how the refresh works.

TWO HALVES (Ashley's choice, 3 November 2026, the same way the Grown-Ups refresh works)
The source list is split so each run can do its half properly instead of skimming everything. Sources tagged [EVERY RUN] are checked on both days. [MON] sources are checked on Mondays, [THU] sources on Thursdays (UK date). If the task is fired by hand on another day, use the half of the most recent Monday or Thursday. Never remove an event because its source was not checked today.

THE ARTIFACT
URL: https://claude.ai/artifact/Xwra24PwALmZTThBKE98Cr
Read it first with the Artifact tool (action: "read", that url). Work from the version that comes back. Republish to the SAME url by passing it as `url`. Never create a new artifact.

TOOLS
Find pages with WebSearch and read them with WebFetch first. FIRECRAWL IS ALLOWED (Ashley upgraded to 5,000 credits a month on 7 November 2026; the old ban is lifted). Load it with ToolSearch "select:mcp__Firecrawl__firecrawl_scrape". Use firecrawl_scrape with formats ["markdown"], onlyMainContent true and excludeTags ["img","svg"] (about 1 credit a page) when:
- a page refuses WebFetch, or loads its list by script (Visit Swansea Bay, Happity, Baby Sensory timetables, swansea.gov.uk library and what's on pages, Gwyn Hall, Wix event pages such as Woodrows);
- WebFetch returns fewer items than the page's own total (see COMPLETENESS);
- you need the exact links on a listing page (formats ["links"]).
Never use Firecrawl's "json" extraction format: on 7 November it captured 1 of 28 items. Never use firecrawl_search or agent tools. BUDGET: at most 150 Firecrawl credits a run (the Happity sweep run, first of the month, may use up to 200). Count them as you go and put the total in last_run.md. If Firecrawl reports no credits, carry on with WebFetch and say so in AFTERWARDS. A page neither tool can read is "blocked" for this run.

WHAT IT IS
A browse-first what's on guide for families across Swansea county and surrounding areas: a rotating hero, horizontally scrolling rails with illustrated animated key art, and five tabs (Browse, Calendar, Indoors, Post an event, Sources). Every event links to the public page where its date was confirmed. The Indoors tab is a directory of indoor places for kids that are open most days (soft play, pools, climbing, ninja courses, bowling, cinemas, museums, libraries, and day out attractions with indoor space), and Browse has an Indoors switch that filters dated events by their `indoor` field.

Data lives in an EVENTS array, a SOURCES object and a PLACES array, plus the HOLS and OCCASIONS arrays (see SPECIAL OCCASIONS below). SOURCES has three groups: swansea, nearby and touring (touring and seasonal organisers). YOU ONLY EDIT DATA (EVENTS, SOURCES, PLACES, HOLS, OCCASIONS, BUILT). Do not change the layout, the CSS, the SVG key art, the header logo, the animations, the rail definitions and the code that draws the occasion rows, the toolbar, the Indoors switch, the places grid and its filters, PTYPES, the calendar link builder, the share panel, the caveat box, the source register or the "Post an event" email panel. The design is settled.

THE DATE MACHINERY, READ THIS BEFORE YOU EDIT ANYTHING
The page works out today's date from the viewer's own device every time it opens. It then drops any event whose last date has already passed, and it builds three calendar months from the current month forward. None of that is baked in, and none of it is yours to change.

- `BUILT` is the ONLY date constant you touch. Set it to today's date as YYYY-MM-DD at the end of a successful run. It means "the morning this data was last verified", and the page shows an amber strip when it is more than a day old.
- DO NOT reintroduce a hardcoded `TODAY`. Leave `isoOf`, the `TODAY` derivation, the `lastDayOf` expiry filter, the `MONTHS` builder and `paintMeta` exactly as they are.
- Do not hand-edit the header meta line, the listing count or the "On today" rail subtitle. All three are painted from the live date.
- HALFTERM is now worked out by the page from HOLS. Never edit HALFTERM, HOLNAME, nextHol, inWin or occMatch. Edit only the HOLS and OCCASIONS data.

SPECIAL OCCASIONS AND SCHOOL HOLIDAYS, A ROLLING THREE MONTHS (added 30 October 2026, Ashley's rule. Anyone editing this prompt: keep this section.)
Ashley wants every major holiday and special occasion in the next three months researched and on the site with plenty of events, rolling forward every run, not a one-off list. The page draws a row for each occasion while it is coming up (near the top when it starts within 14 days), but only when it has events, so empty occasions stay hidden until you find events for them.
a) ROLLING WINDOW. Every run, HOLS and OCCASIONS must cover today to at least three months ahead. Remove entries whose `to` date has passed. Add the next ones as the window reaches them (in early January, Easter and the Easter holidays come in; in February, May half term; and so on through the year).
b) HOLS record: {n, key, from, to}. n is "Half term", "Christmas holidays", "Easter holidays" or "Summer holidays". key is the one line shown under the calendar, for example "Swansea school half term, Monday 8 to Friday 12 February 2027". from and to are the first and last weekday schools are closed, taken from a published term dates page (source 37, or gov.wales term dates). Never guess term dates.
c) OCCASIONS record: {t, s, from, to, m, any}. t is the row title, s a short subtitle with the day, from and to the window in which an event counts (the day itself plus a few days either side, or the whole holiday), m a regular expression of words that tie an event to the occasion (for example /firework|bonfire|guy fawkes/i), any:true only when every event on those dates counts (school holidays, New Year). Keep the exact syntax of the existing entries. Dates of moveable days (Easter, Diwali, Lunar New Year, Eid, Shrove Tuesday, Mothering Sunday, Father's Day) come from a page you have read this run or a previous run (gov.uk bank holidays, timeanddate.com or the festival organiser), never from memory.
d) THE OCCASION CALENDAR to cover, each year, whenever it falls inside the window: Halloween (has its own category already), Bonfire Night, Diwali, Christmas (has its own row already, do not add it to OCCASIONS), Christmas holidays, New Year, Hen Galan and the Mari Lwyd (13 January), Santes Dwynwen (25 January), Lunar New Year, Pancake Day, February half term, St David's Day (1 March), World Book Day, Mothering Sunday, Easter weekend and Easter holidays (egg hunts, Easter trails), Eid al-Fitr, May Day and the late May bank holiday with May half term, Father's Day, summer holidays, and any other occasion where you find real family events in the area (for example a big Swansea festival weekend).
e) RESEARCH, EVERY RUN, for each occasion inside the next three months: WebSearch "<occasion> <year> Swansea family", "<occasion> <year> kids Neath OR Llanelli OR Carmarthen OR Gower", "<occasion> <year> children South West Wales", and for Bonfire Night "fireworks display <year> Swansea", "... Neath", "... Llanelli", "... Carmarthen", "... Bridgend", "... Gower". Also check each Tier 1 source and the big attractions (Waterfront Museum, Margam, Botanic Garden, NPT, Plantasia, Aberglasney, Folly Farm, Pembrey, WWT, Penllergare, the theatres and arts centres) for that occasion's pages. Every event still follows THE ACCURACY RULE: only a page that states this year's date, organiser's wording, no invented fields. An event matches an occasion row through its title or description, so describe it in the organiser's words (for example "fireworks", "Easter egg hunt").
f) TARGET: at least 5 events for every occasion starting within the next 6 weeks, where they exist. Never pad with undated or last year's events to hit it. In AFTERWARDS, add a line per occasion in the window: "<occasion>: <n> events" and, for any with fewer than 3, what you searched and whether organisers simply have not published yet.
g) WAITING LIST. Organisers known to run an occasion event but not yet showing this year's date (on 30 October 2026: Dunvant RFC fireworks still shows 2025) are re-checked every run and named in AFTERWARDS until they publish or the day passes.
h) Known on 30 October 2026, already in the data: Diwali Sunday 8 November 2026, Christmas holidays 21 December 2026 to 1 January 2027, Hen Galan 13 January, Santes Dwynwen 25 January, Lunar New Year Saturday 6 February 2027, Shrove Tuesday 9 February 2027, February half term 8 to 12 February 2027. No family events were yet published in the area for Diwali, Lunar New Year, Pancake Day, February half term specials or New Year's Eve: keep searching each run.

BABIES AND BUMPS (added 1 November 2026, Ashley's rule. Anyone editing this prompt: keep this section.)
Ashley wants the family guide to cover parents with young babies, from pregnancy to 12 months. The page has a "With a baby" row and a "Babies and bumps" age filter. Weekly baby sessions stay out of the other rows unless a viewer picks that filter, so listing many of them is fine. The 30 starting records (ids beginning "bb-") and how they were built are in the repo at tools/baby/events.py; their sources are in SOURCES with notes.
a) WHAT GOES IN: library rhyme times and song and rhyme, baby sensory, music, signing and massage classes, baby and parent yoga, pregnancy yoga and antenatal classes open to the public, new parent and baby groups, baby swim sessions, parent and baby cinema screenings, and museum or gallery sessions for babies. Not NHS appointments, health visitor clinics or anything that needs a referral.
b) RECORD: cat "baby". ageTags ["baby"] for sessions only for babies or pregnancy; ["baby","u5"] when the organiser welcomes babies and toddlers together (most rhyme times). scene "library" at libraries, otherwise "baby". Add "bump":true for pregnancy sessions. Add "course":true when it must be booked as a term, block or course (the card then shows "Book a course"). Add "weekly":true for a weekly session. Set sold:true when every class is on a waiting list and say so in desc.
c) WEEKLY PATTERN RULE: when a public page states the weekly day and time ("every Tuesday 10.30am", or a listing with a weekday, time and "term time only" or "all year"), list the next 8 weeks of dates and write the pattern in span, for example "Tuesdays to 15 December". Term time only: leave out every date inside HOLS. All year: still stop at the last weekday before 24 December and restart from the first weekday after 1 January, because Christmas closures are not published. Leave out any date a source marks cancelled (the NPT what's on page shows these).
d) EVERY RUN: roll every weekly baby record forward so `days` covers today to 8 weeks ahead, following c). Before rolling one forward, re-open its src. If the page no longer shows the session, remove it. If the page cannot be read this run, still roll it forward, keep its day and time, and name it in AFTERWARDS. Sources: https://llyfrgelloedd.cymru/ (Libraries Wales events), https://www.npt.gov.uk/libraries/learning-and-wellbeing/babies-and-toddlers/ (Bookstart song and rhyme), the Happity pages in src (they often refuse WebFetch: read them with Firecrawl; a Happity record that still cannot be read keeps rolling unless another readable page contradicts it), https://www.mumbles-pier.co.uk/whats-on/childrens-events/babylove-at-mumbles-pier , https://www.universityhealthcentreswansea.nhs.wales/events/995-mother-and-baby-yoga .
e) TERM COURSES (Baby Sensory): list exactly the term dates the timetable shows, never roll them forward. https://www.babysensory.com/swanseaeast/timetable and https://www.babysensory.com/swanseawest/timetable load by script: read them with Firecrawl. When the spring term timetable appears, add its exact dates. If it is still not published when the winter term records end (11 December), say so in AFTERWARDS.
f) LOOK FOR MORE, EVERY RUN: WebSearch "rhyme time <library> Swansea", "baby class Swansea <month> <year>", "pregnancy yoga Swansea", "parent and baby screening Swansea <month>", "baby massage Swansea", "Water Babies Swansea", "Museum Little Mice" and "Art Babas Glynn Vivian". The Waterfront Museum's Little Mice and the Glynn Vivian's Art Babas go in as soon as their pages date them. Libraries in Llanelli, Carmarthen and Bridgend count when a readable page states the weekly pattern.
g) AFTERWARDS: one line "Babies and bumps: <n> records, <n> sessions in the next 8 weeks", plus anything added, removed or rolled forward without a re-check.

EVENT SUBMISSIONS
Organisers now send events by email to ashleykissick1@hotmail.co.uk. This task cannot read that inbox, and Ashley handles those emails himself. The old "Post an event" form and its "submissions" database collection are retired: do not read or write the artifact database.

THE REFRESH
1. Roll forward every record with "weekly":true (parkruns, Quiet Hour, Welly Wednesday, the REGULARS and the baby sessions) following REGULARS and BABIES AND BUMPS. Re-check each page still says it is running.
2. Roll HOLS and OCCASIONS forward and research every occasion in the window (SPECIAL OCCASIONS above).
3. Work the sources below on their stated schedule. Add new verified events. Remove cancelled ones. You do not need to remove events that have simply passed: the page does that itself. Do remove an event whose source page has gone or no longer shows that date.
4. Update SOURCES statuses for the sources you opened this run, in all three groups: "live" gave you a dated event, "watch" was reachable with nothing dated for this window, "blocked" could not be read. Leave the status of sources you did not open this run unchanged.
5. Set BUILT to today's date.
6. Publish the same page to the public website (see THE WEBSITE below). Do this every run, after the artifact has been republished.

THE WEBSITE (added 27 October 2026, Ashley's choice)
The guide is also a public website at https://swansea-family-events.netlify.app/ . Netlify publishes it automatically from the GitHub repository Akissick1/swansea-family-events (branch main). The artifact stays the master copy; the website is built from it.
a) Attach the repository with the add_repo tool: owner "Akissick1", repo "swansea-family-events", access "push". Clone it exactly as that tool's result tells you.
b) Save the exact page you just published to the artifact to a file, for example /tmp/page.html (the source file you published, or the full HTML that an Artifact "read" of the url saves; both work).
c) In the clone, run: python3 tools/build_site.py /tmp/page.html index.html . It must print "wrote index.html". Do not edit index.html, tools/build_site.py, tools/weather.html, tools/calendar.html, netlify/functions, netlify.toml or og-image.png by hand.
d) git add index.html tools/family/last_run.md, commit with the message "Refresh YYYY-MM-DD" (today's date), fetch origin main, then push to main. Netlify goes live within about a minute.
e) If any of a) to d) fails, do not retry more than once. The artifact is already updated, so report the failure in AFTERWARDS ("Website not updated: <reason>") so Ashley knows the website is behind.

INDOOR FIELD (added 24 October 2026, Ashley asked for an indoor filter)
Every new event gets `indoor`:
- "in" when it takes place inside a building: museums, galleries, theatres, cinemas, arts centres, libraries, leisure and sports centres, Plantasia, the Arena, the pier's Copperfish restaurant, any page that says the event is indoors.
- "mixed" when it is part indoors, part outdoors, or under a big top: circuses, show caves, heritage centres with an indoor theatre plus grounds, Folly Farm.
- "out" for parks, woods, trails, castle grounds, beaches, parkruns, outdoor stadium sport, fireworks, parades, outdoor markets.
- Leave `indoor` off when the page does not make it clear. Never guess "in".
When you rewrite or roll forward a record, carry `indoor` through unchanged.

INDOOR AND WINTER, NOVEMBER TO FEBRUARY
Families need indoor options in the colder months. Each run, look ahead to the end of February for: theatre family shows and pantomimes, U and PG family film screenings at arts centres, museum and gallery family sessions, library children's specials, leisure centre holiday sessions, and indoor Christmas events (grottos, Santa breakfasts, Christmas fairs). The theatres below publish months ahead, so a show in February goes in as soon as its page dates it. Leave out adult pantomimes (any 18+ panto, Tinderella and similar "leave the kids at home" shows) and schools-only performances. Ashley approved SIX at Swansea Arena (10+, mature themes) on 24 October: shows with an age guidance such as 10+ or 12+ may go in, with the venue's own age wording in `ages` and any themes it warns about stated in desc.

INDOOR PLACES (the PLACES array)
PLACES holds venues that are not events. Record shape: {id, n, types:[...], scene, area, areaLabel, partly (optional, true when only part of the venue is indoors), what, hours, price, ages, addr, u, checked, note (optional)}. `types` only from: swim, climb, play, animals, screen, games, library. `u` is the venue's own page, or an official tourism listing (Visit Swansea Bay or Visit Wales) when the venue's own site cannot be read. `hours`, `price` and `ages` are copied from that page; leave them as empty strings when the page does not publish them. `checked` is the date you last read the page.
- First run of each calendar month: re-open every place's `u`. Update hours, price and what from the page and set `checked` to today. If the venue has closed or the page has gone, remove the place and say so.
- Add a new place only when you have opened its own website (or official tourism listing) and it is a kids' indoor venue in Swansea county or the surrounding areas. Day out attractions up to about an hour away with real indoor space count too (Ashley, 24 October: Folly Farm and places like it); set partly:true for those. Never add a place from a listings aggregator, Facebook or a hotel or blog roundup alone.
- Exception, agreed with Ashley on 24 October: Brodie's Funhouse (its own site shows only bookings) and Playzone Swansea (no site of its own found) use West Wales Family Life's listing, with a `note` saying so. Each month, look for their own websites; if one appears, switch `u` to it, refresh the details from it and remove the note. ODEON Swansea's site cannot be read automatically, so its card carries only the address; try it each month.
- Still to find and verify: Moss and Maple Play Café (Gorseinon), Sgiliau (Dafen, Llanelli), Tiny Tots Town (Llwynhendy, Llanelli), Dream Street (Water Street, Neath), Llanelli and Carmarthen leisure centres, Swansea Central Library. Already in PLACES, do not duplicate: check the ids before adding. Cinema & Co (Castle Street) announced its closure (Swansea Bay News), so it stays out. Cefn Coed Colliery Museum is closed for maintenance; add it when its page says it has reopened. BUNKERS! Swansea (crazy golf) is in PLACES: under 18s are welcome until 7.45pm, so its daytime family deals may go in as events. Gower Golf Studio (Trackman simulator hire) blocks automated reading; add it only if a readable page shows juniors can use it. Limitless trampoline park at Port Tennant was destroyed by fire in October 2023 (ITV News); add it back only if its own page shows it has reopened.
- Caravan and holiday parks: Parkdean Resorts says its entertainment hubs are for staying guests only and cannot be bought by visitors, so its parks do not go in. Add a holiday park only if its own page sells day visits to non-guests.
- Routine weekly clubs (Lego clubs) belong in a place card, not in EVENTS. Rhyme times and baby sessions are the exception: they are dated weekly events under BABIES AND BUMPS. One-off and holiday specials (Halloween crafts, STEM days, parties, Santa visits) go in EVENTS.

THE YEAR RULE (Ashley's rule, 25 October 2026)
If a live page shows a date without a year, take it as the NEXT time that date comes round: this year if it is still ahead, next year if it has passed. Example: in December, an Easter date on a live page means next Easter. Do NOT add a caveat for a missing year, and do NOT leave an event out just because its page prints no year.
Two exceptions, where the page is stale rather than current: (a) the page prints a weekday that does not match the date in the coming year (for example "Saturday 14 December" when 14 December is a Monday this year), or (b) the page is plainly last year's (dated news article, last year's programme, past events still listed). Those stay out.

CAVEATS
Some events carry a `caveat` string. It renders as an amber flag on the card and a warning box in the detail panel. Since 25 October it is ONLY for a source that contradicts itself (for example Luminate, where the park and the organiser give different runs). Never add one for a missing year.
- When you rewrite or roll forward any record, carry the `caveat` field through unchanged unless the contradiction has gone away.
- Every run, re-open the source of any caveated event. If the contradiction is fixed, delete the `caveat` and say so. If the source now contradicts the date shown, remove the event.
- Do not add a caveat to make a shaky event publishable. An event whose date you cannot find on a page does not go in at all.

ONE EVENT PER ACTIVITY (25 October 2026)
Never group several activities into one card. Ashley could not see the Mumbles Pier activities because they were hidden inside one "Halloween Half Term" card. Each separately bookable activity, show, session or workshop gets its own record, with its own times, price, ages and its own page as `src` where it has one. The same show running on several dates is one record with all its dates in `days`. A venue with five half term sessions is five records.

CHECK EXISTING EVENTS FOR CHANGES
Every run, when you read a source, compare it with the events already listed from it. If a date, time, price or venue has changed, update the record. If an event has been moved, move it (The Spooky Castle at Oystermouth moved from 24 to 31 October 2026 and the old card stayed up until 25 October). If it is cancelled or gone, remove it.

THOROUGHNESS CHECKLIST, EVERY RUN
- Every listing source: read EVERY result page (page 2, 3 and on), not just the first. Note the page count.
- Every candidate: open its own event page for date, time, price and ages.
- If a fetch fails with a server error, retry once with the parameters in a different order (for example ?size=100&page=4) before giving up, and name the page in AFTERWARDS.
- In AFTERWARDS, list any source you could not read fully.
- A full run takes time. If you are finishing in a few minutes, you have skipped work: go back through the tiers and the occasion searches.

TIER 1. Check the [EVERY RUN] lines and the lines tagged with today's half.
1 [MON] https://museum.wales/swansea/whatson/
2 [MON] https://www.plantasiaswansea.co.uk/whats-on/
3 [MON] https://oystermouthcastle.org.uk/whats-on
4 [MON] https://www.margamcountrypark.co.uk/whats-on/
5 [MON] https://www.wwt.org.uk/wetland-centres/llanelli/whats-on/
6 [MON] https://www.nationaltrust.org.uk/visit/wales/rhosili-and-south-gower-coast/events
7 [EVERY RUN] https://www.whatsoninswansea.com/events/
8 [EVERY RUN] https://www.visitswanseabay.com/whats-on/ (READ THE VISIT SWANSEA BAY SECTION BELOW: this page only shows a featured handful to WebFetch)
9 [EVERY RUN] https://www.npt.gov.uk/culture-and-tourism/whats-on-in-npt/ (about 950 entries in date order. Use ?page=1&size=100, then page=2, 3 and on: ten pages cover about four months. Server errors are common; retry with ?size=100&page=N or add &x=1. Open each children's event page for ages and booking. Every library holiday special, Margam and Gnoll family event, fireworks, Santa run and family show goes in, one record each. Routine children's clubs (Lego Club, Kids Club, Pokemon Club, Duplo, Coding, Stay and Play) now go in under REGULARS below, one card per club per library with exactly the dates this listing shows. Adult sessions stay out. Halloween or Christmas themed one-offs of those clubs are separate cards. Song and Rhyme sessions are the exception: they are kept by BABIES AND BUMPS above)
10 [MON] https://mumbles-pier.co.uk/whats-on (one record per activity, src is the activity's own page under /whats-on/halloween/ or /whats-on/christmas/)
11 [MON] https://www.theatrausirgar.co.uk/en/whats-on/ (all result pages, ?page=2 onward)
12 [MON] https://www.welshwildlife.org/events
13 [EVERY RUN] https://swanseabaynews.com/category/news/in-your-area/swansea/
14 [MON] https://www.ospreysrugby.com/
14a [MON] https://botanicgarden.wales/visit/whats-on/ (pages /page/2/ to /page/4/; open each family event page. Garden admission prices are on /visit/. Its UV Torchlight Walk is 16+ and stays out)
14b [EVERY RUN] EVENTBRITE. The /d/ search pages refuse automated reading, but the /b/ browse pages work. Read all of these every run: https://www.eventbrite.co.uk/b/united-kingdom--swansea/family-and-education/ , .../family-and-education/children-and-youth/ , .../holiday/ , .../holiday/halloween/ , .../holiday/christmas/ , .../arts/craft/ , .../community/ , and https://www.eventbrite.co.uk/b/united-kingdom--llanelli/family-and-education/ and https://www.eventbrite.co.uk/b/united-kingdom--neath/family-and-education/ . Each shows 8 popular events with links. Open every /e/ event page: it gives the date with the year, times, venue and ages. Also WebSearch "eventbrite Swansea <month> kids" for more.
14c [MON] https://events.dobbies.com/events-by-venue/?v=49 (Dobbies Swansea. The listing hides most dates; open each event-detail page, ?e=<id>&v=49&r=v)
14d [MON] https://www.pembreycountrypark.wales/whats-on/whats-on/ (Pembrey Country Park, about 30 minutes. Dated 2026 pages for Halloween, the Christmas light trail, Santa and tubing)
14e [MON] https://gwili-railway.co.uk/train-rides/ (steam railway at Carmarthen; Halloween and festive lights trains, Santa Specials. Pages print day and month: apply the year rule)
14f [MON] https://aberglasney.org/events-exhibitions/ (Aberglasney Gardens, Llangathen, Carmarthenshire, about 40 minutes. Added 30 October 2026 at Ashley's request. Open each event page. Family events go in: Winter Fair, Santa's Grotto, trails, carol service, Easter and holiday events. Workshops, floristry, wedding showcases and art exhibitions are aimed at adults and stay out unless the page says children are welcome. Children up to 16 get in free and adults pay garden admission, as stated on its visit pages.)
14g [MON] https://www.woodrowscoffee.co.uk/tickets (Woodrows coffee shop cinema, 79 Brynymor Road, Brynmill. Added 7 November 2026 at Ashley's request. The tickets page lists every screening with day, month and certificate; each /event-details/ page gives the year, times and prices. Only U and PG films and events the page says suit children go in; its Fun Friday Lego, quiz and game nights are aimed at students and adults. Event pages sometimes refuse WebFetch: retry once with the URL unchanged; if still refused, add the film with the tickets page as src and leave time and cost empty.)
Open the individual event page for anything you add. Listing pages are often wrong about ages: the Wildlife Trust in particular lists walks that turn out to be adults only on the event page itself.

VISIT SWANSEA BAY: WHY EVENTS WERE MISSED, AND HOW TO READ IT (added 24 October 2026 after Ashley found many of its events missing)
Visit Swansea Bay builds its what's on list with script in the browser. WebFetch sees only about five featured events, never the full list. Most of its individual event pages also load the date, venue and price by script, so a page that "shows no date" to WebFetch may well have one. Its RSS feed (https://www.visitswanseabay.com/event/rss/) only lists events on today's date. Its sitemap (https://www.visitswanseabay.com/sitemap.xml) lists every event page, past and future, alphabetically, but WebFetch stops after about 67,000 characters (around slugs starting "cl"). Its events API rejects requests that fit WebFetch's URL limit. Treat Visit Swansea Bay as a DISCOVERY list, never as complete, and never mark it "live" just because the featured events were found: keep its status "watch" with a note saying it is only partly readable.
Every run, do all of these:
a) Featured events on /whats-on/, the half term page https://www.visitswanseabay.com/whats-on/seasonal-events/half-term/, the Christmas pages under https://www.visitswanseabay.com/swansea-christmas/, and the RSS feed.
b) The monthly blog guides at https://www.visitswanseabay.com/blog/all-posts/ ("Enjoy <month> in Swansea", half term and Christmas guides). They print dates in the text and link the event pages.
c) The sitemap's readable part: note every English /event/ URL (ending 101/) whose title suggests children, families, Christmas, Santa, Halloween, half term, workshops, shows or trails.
d) WebSearch: site:visitswanseabay.com/event plus children, family, kids, Santa, Christmas, half term, workshop, and the month name. This reaches event pages beyond the sitemap cut-off.
For every candidate found this way: open its Visit Swansea Bay page; if it shows the date with the year, it can be the src. If it shows no date or no year, find the organiser's own page (venue site, Ticket Tailor, TicketSource, the theatre or arena) and date it there. If the VSB page or the organiser's page prints the date without a year, apply the year rule. If no page you can read prints the date at all, it stays out. Fetch Visit Swansea Bay pages one at a time: it rate limits several at once.
Known candidates still to date: Children's Halloween Party at Bank Farm (VSB says Wednesday 28 October, 3pm to 5pm, free; the VSB page could not be found again on 25 October), Carols at the Castle at Oystermouth (the council page found is from December 2024), BBC NOW Carols for Christmas and BBC NOW The Magic of Christmas (no venue or date readable). Animal Cwtch was added on 25 October with its venue marked as not given.
In AFTERWARDS, say how many Visit Swansea Bay candidates you found, how many you dated and added, and how many you could not date.
THE SAME CHECK FOR EVERY SOURCE: if a listing page gives far fewer events than its own headings, counters or menus suggest, or its event pages show no dates, assume it is built by script and only partly read. Never mark such a source "live" from a partial read; mark it "watch", say "partly readable" in its note, and name it in AFTERWARDS.

SWANSEA BAY NEWS IS THE WAY ROUND THE COUNCIL BLOCK
swansea.gov.uk mostly refuses automated requests, so council run events (parks, libraries, Singleton Park, the city centre programme, the 5 November fireworks) rarely appear directly. Swansea Bay News reports them. Read its Swansea section every run and follow anything dated through to an organiser page you can cite. If the only source is the news article itself, cite the article.

TIER 2 [THU]. Thursdays. On Mondays skip it, unless KEEPING THE PAGE FULL or THE WEEKEND CHECK sends you back here.
15 https://www.parkrun.org.uk/swanseaprom-juniors/
16 https://www.parkrun.org.uk/swanseabay/
17 https://www.visitswanseabay.com/swansea-fireworks-display/
18 https://www.gowerheritagecentre.co.uk/events/
19 https://tickets.visitswanseabay.com/swanseagrandtheatre/website/EventList.aspx (the Grand's own booking site; its old what's on page is out of date). Open each month to the end of February with ?MonthSelect=YYYYM&SortBy=Name, month without a leading zero: 202611, 202612, 20271, 20272. Open each family show's EventDetails page for dates, times and age wording. Move the months on as time passes so the next three months are always covered.
20 https://www.swanseatheatre.co.uk/shows
21 https://www.glynnvivian.co.uk/
22 https://www.taliesinartscentre.co.uk/en/all-events (every result page, ?page=2 onward; the homepage still shows an old closure notice)
23 https://penllergare.org/news-events/
24 https://www.orielscience.co.uk/city-centre-venue (opening days, including half term) and https://www.orielscience.co.uk/upcoming-events
25 https://www.dylanthomasbirthplace.com/events/
26 https://letsgowiththechildren.co.uk/events/swansea/
27 https://www.westwalesfamilylife.co.uk/whats-on-in-swansea/
28 https://clynefarm.com/whats-on-in-swansea-in-2026/
29 https://screamtime.co.uk/family/
30 https://www.swansea.ac.uk/swansea-science-festival/
31 https://swanseaminster.org.uk/
32 https://cadw.gov.wales/visit/whats-on/find-a-cadw-event
33 https://www.visitwales.com/things-do/events
34 https://www.ents24.com/swansea-events/singleton-park
35 https://www.songkick.com/venues/16114-singleton-park
36 https://www.swansea-arena.co.uk/whats-on (the arena's own site; open each possible family show's page and read its AGE GUIDANCE line. Also https://www.atgtickets.com/venues/swansea-arena/whats-on/uk/family/)
37 https://school-term-dates.co.uk/wales/swansea-school-term-dates/ (and gov.wales term dates: these set HOLS)
37a https://pontardaweartscentre.com/ (Neath Port Talbot; dated listings with a Family tag. It runs a family panto and a separate 18+ panto: list only the family one)
37b https://www.freedom-leisure.co.uk/news/swansea-school-holidays/ and the centre pages it links (Morriston, Penlan, Cefn Hengoed, Bishopston, Penyrheol, LC). Each school holiday they post Bounce and Play, camps and gymnastics tasters. One record per session (not per centre). Pages print day and month only: apply the year rule.
37c https://showcaveschristmas.co.uk/before-you-visit.php and https://www.showcavesbookings.co.uk/opening-times.php (Dan yr Ogof, Upper Swansea Valley)
37d https://www.folly-farm.co.uk/plan-your-day/whats-on/ (Pembrokeshire, about an hour; follow each item to its news page for the dated details) and https://www.heatherton.co.uk/ (near Tenby)
37e https://bunkersuk.com/location/swansea/ (crazy golf; school holiday family deals print dates with the year)
37f https://www.zipworld.co.uk/monsters-of-the-mine and https://www.zipworld.co.uk/ (Zip World Tower, Aberdare, about 40 minutes. Halloween event is 9+ only, list with that warning; look for Christmas events)
37g https://penllergare.org/whatson/ (the full events list for Penllergare, every event page has the year)
37h https://www.visitbridgend.co.uk/events/ and https://bryngarwcountrypark.co.uk/ (Bridgend, about 30 minutes. Only pages that date the current year)

TIER 3, RETRY MONTHLY (first run of each calendar month). These block or starve automated reading. If one starts producing dated events, move it up and say so.
38 https://www.swansea.gov.uk/whatson
39 https://www.swansea.gov.uk/article/23504/COAST---Children-and-young-people-events-calendar
40 http://www.swanseamuseum.co.uk/whats-on/
41 https://www.swanseacommunityfarm.org.uk/
42 https://www.thelcswansea.com/
43 https://www.missiongallery.co.uk/
44 https://www.nationaltrust.org.uk/visit/wales/aberdulais/events
45 https://www.discovercarmarthenshire.com/whats-on/
47 https://www.skiddle.com/whats-on/Swansea/
48 https://www.ticketsource.co.uk/whats-on/swansea
49 https://gwynhall.com/whats-on/ (Neath; listings load by script: try Firecrawl. Its 2027 pantomime goes in only once a readable page dates it)

TOURING AND SEASONAL ORGANISERS, CHECK EVERY RUN
These are the organisers' own websites for touring shows (circuses, funfairs) and yearly Swansea events. They live in SOURCES.touring. Check every URL in that group each run, including any added since this list was written:
T1 https://circus-zyair.co.uk/
T2 https://www.studtsfunfairs.co.uk/events/index.html
T3 https://swanseawinterwonderland.co.uk/opening-times/
T4 https://www.visitswanseabay.com/spooks/
T5 https://www.visitswanseabay.com/swansea-christmas/christmas-parade/
T6 https://www.visitswanseabay.com/swansea-prom/swansea-bay-rider/
T7 https://www.swanseacitycentre.com/events/christmasmarket
T8 https://www.circusvegas.co.uk/
T9 https://www.circus-starr.org.uk/events/map/
T10 https://www.walesnationalairshow.com/
THE SWANSEA RULE FOR THIS GROUP: add an event only when the organiser's own page names a venue in Swansea county or the surrounding areas AND states the date with the year, or the page is clearly headed with that year. A touring organiser's dates in other towns never go in. Never use the organiser's Facebook page, and never use a third party copy of a page that blocks automated reading: that organiser simply stays "blocked".

SCHOOL HOLIDAY CAMPS AND CLUBS (added 24 October 2026)
Ashley wants holiday clubs and camps run at or by local schools. Individual school websites rarely publish public events, so look for the providers that run camps at schools and leisure centres: Swansea City AFC Foundation and Community Trust soccer camps (swanseacity.com news), Ospreys in the Community camps (ospreysrugby.com news), Freedom Leisure Swansea (37b), Neath Port Talbot sport camps on the NPT what's on feed, Gymnastics Studios (gymnastics-studios.classforkids.io/camps), and any provider your searches find. A camp goes in only when its page states the dates (apply the year rule when there is no year, but leave out pages that are plainly an old year's). Swansea City's October article prints no year and the same weekdays fit 2020, so it stayed out on 24 October: add it if a dated version appears. Camps go in as one record per camp and date run (not grouped), with the venue and ages, cat "sport", indoor "in" only if every venue is indoors. Look for camps for every school holiday in HOLS.

BUILDING THE ORGANISER BANK, FIRST RUN OF EACH CALENDAR MONTH
The aim is a growing bank of companies that tend to come to Swansea, read straight from their own websites. Look back at what ran in Swansea in the same month and the following two months LAST year: read Visit Swansea Bay's monthly guides for those months (search "visitswanseabay Enjoy <month> in Swansea") and Swansea Bay News. For every touring company, circus, funfair, festival, outdoor cinema or theatre company, grotto or market operator, fireworks organiser, Easter trail or occasion event behind a family event, find the organiser's own website. If it has a readable page listing its dates, add it to SOURCES.touring as {n, u, s, note} with a one line note. Never add a Facebook page, a ticket reseller or a listings aggregator as an organiser source. Adult only acts stay out (for example Circus of Horrors, over 16s). Name every organiser you added in your summary.

OPEN SEARCHES EVERY RUN
"Swansea family events <month> <year>", "Swansea half term children <year>", "Singleton Park events <month> <year>", "Swansea parks events <month>", "Mumbles Gower family events <month>", "Margam Country Park family <month>", "Swansea toddler activities <month>", "visitswanseabay Enjoy <month> in Swansea", "circus Swansea <year>", "funfair Swansea <month> <year>", "pantomime Swansea Neath Llanelli <year>", "family show Swansea <month> <year>", "indoor kids Swansea <month> <year>", "Santa grotto Swansea <year>", "half term camp Swansea <month> <year>", "holiday club Swansea <month> <year>", plus the occasion searches in SPECIAL OCCASIONS and the baby searches in BABIES AND BUMPS. Run them for this month and the next two months. Follow anything promising through to a dated page.

VENUE SWEEP, ONCE A MONTH
Search for what is on at named Swansea venues with no register entry yet, for example Brangwyn Hall, Singleton Park, Brynmill Park, Clyne Gardens, Victoria Park, Blackpill Lido, Swansea Market, the LC, Mumbles Road Recreation Ground. Any with a readable dated listing page gets added to SOURCES.

KEEPING THE PAGE FULL
The page now hides anything that has been, which means a run that adds nothing makes the page visibly emptier. If fewer than 12 listings remain after the sweep, widen the window: look further ahead, go back through Tier 2 properly (even if today is not a Tier 2 day), and run the open searches for the month after next. Say in your summary how many are left.

KNOWN FORWARD ITEMS
Swansea Council fireworks display, 5 November 2026 at Singleton Park. Do not change its record unless the Visit Swansea Bay page or a news article changes the date.
The Upside Down House at Mumbles Pier (Studt's) runs to 31 December 2026 but publishes no opening days. Add it only if Studt's or the pier publishes the days it opens.
SIX at Swansea Arena: the arena lists the run as 18 December to 2 January 2027 without performance days or times. If the arena or ATG publishes the performance calendar, trim `days` to the actual performance dates and fill in `time`.
Porthcawl Christmas Day Swim (25 December 2026): its start time was not yet published on 30 October. Fill in `time` from christmasswim.org or its JustGiving page when published.

FACEBOOK
Facebook groups and pages cannot be read. Meta deprecated the Groups API around April 2024 and scraping breaches their terms. Do not attempt it, do not list events sourced from Facebook posts, and do not suggest it in your summary.

THE ACCURACY RULE, THIS IS THE POINT OF THE WHOLE THING
An event goes in ONLY if you have opened a public page that states its date. `src` must be that exact page, not a homepage and not a search result, unless the organiser's homepage is itself the page that states the date. Never infer a date from a previous year. Never carry an event over because it ran last year. If a source publishes no time, no price or no age range, leave that field an empty string so the page shows "not published" rather than a made up value. Set `ages` to the organiser's own wording. Set `ageTags` only from what the source states: baby, u5, 5-11, 12+ (baby = for pregnancy to 12 months, see BABIES AND BUMPS). Empty array if ages are not stated. If a source says sold out or fully booked, set sold:true. Do not start `cost` with the word "Free" unless the event itself is free (the page marks anything starting "Free" as free): write "Included with Garden admission", not "Free with admission".

EVENT RECORD SHAPE
{id, t, cat, scene, area, areaLabel, indoor (optional), xmas (optional, true for Christmas events), days:[...], span (multi day or recurring only), time, venue, cost, ages, ageTags:[...], sold (optional), caveat (optional), bump, course (optional, baby records only), weekly (optional, any session that repeats on a set weekday, see REGULARS), added, desc, src}
`days` lists every individual date the event runs.
`added` is the date (YYYY-MM-DD) the record was first added. Set it on every new record. Never change it on an existing record. Records from before 14 October 2026 have no `added` field: leave them without one.
`scene` must be one of: baby, waterfront, castle, gower, wetland, plantasia, minster, margam, trail, cinema, market, bay, garden, science, library, play, swim, climb, bowl, cave. Pick by venue: Waterfront Museum use waterfront, Science Festival shows and STEM sessions use science, Oystermouth use castle, Rhossili and Gower use gower, Margam use margam, night or lantern trails use trail, cinema, theatre and arts centres use cinema, markets, festivals, funfairs and Folly Farm use market, seafront, promenade, Mumbles Pier, St Helen's, recreation grounds, parks and fireworks use bay, gardens and orchards (including Aberglasney) use garden, Plantasia use plantasia, Swansea Minster use minster, wetlands use wetland, libraries use library, leisure centres, soft play and bounce sessions use play, pools use swim, climbing walls use climb, bowling, crazy golf, escape rooms and karting use bowl, show caves use cave, baby classes, baby groups and pregnancy yoga (not at a library) use baby.

FAMILY BAR
Include an event where the source indicates it suits children or all ages, or where a film certificate states it (U means all ages, PG means 5-11 and 12+). Junior and youth productions of children's musicals may go in with ages left blank. Major public Swansea fixtures, free public events, fireworks displays, circuses and funfairs may be included with ages left blank. Leave out adult only courses, adult comedy, club nights, 18 rated screenings, over 16s shows, adult pantomimes and licensed events. An evening craft session at an adult price with no age guidance is an adult event: leave it out. Pregnancy yoga and antenatal classes are the exception: they go in under BABIES AND BUMPS.

AREA
area is "swansea" inside Swansea county, "nearby" for everything else. Regular sources and one-off events reach about 45 minutes' drive from Swansea (Llanelli, Carmarthen, Ammanford, Llandeilo, Llangathen, Neath, Port Talbot, Bridgend, Porthcawl, Aberdare). Big day out attractions and big occasion events such as Folly Farm or the Saundersfoot New Year's Day Swim can be up to about an hour. areaLabel is the place in plain words.

CATEGORIES
Only: museum, science, outdoors, halloween, food, shows, sport, baby (Babies & bumps, see BABIES AND BUMPS), clubs (Clubs & drop-ins, see REGULARS).

BEFORE REPUBLISHING, LINK CHECK
- Every run: re-fetch the `src` of every event whose `added` date is within the last 7 days, plus every caveated event. If one 404s or no longer shows that date, remove the event. Baby records whose src refuses WebFetch follow BABIES AND BUMPS d) instead.
- First run of each calendar month only: re-fetch EVERY `src` URL still in the file, with the same rule.
- On other days, events from sources you worked this run are already covered by that work.

REGULARS: WEEKEND CLUBS AND WEEKLY ACTIVITIES (added 3 November 2026, Ashley's rule. Anyone editing this runbook: keep this section.)
Ashley found weekends looking empty. Families want the things that happen most Saturdays and Sundays, not only one-off events. The page has a "This weekend" row, a "Weekend clubs and regulars" row and a "Clubs & drop-ins" category (cat "clubs"). The first seven records (ids beginning "rg-") and how they were built are in tools/regulars/regulars.py.
a) WHAT GOES IN: library Lego, kids and Pokemon clubs, code clubs, junior parkruns, weekend kids' film mornings, family swims or fun sessions with a published weekly slot, museum or gallery family drop-ins, stay and play on a Saturday or Sunday, Young Archaeologists or similar family clubs, and any other children's session that a public page says runs on a set weekday. Paid term classes that need enrolment (ballet, gymnastics, swimming lessons) stay out unless the page says families can drop in or book single sessions.
b) RECORD: cat "clubs" (cinema mornings stay "shows", parkruns stay "sport"), "weekly":true, scene "library" at libraries, otherwise the venue's scene. One card per activity per venue.
c) DATES: the same WEEKLY PATTERN RULE as BABIES AND BUMPS c): when a page states the weekday and time, list the next 8 weeks, skip 24 December to 1 January, skip HOLS dates when it says term time only, and write the pattern in span. When a listing shows individual dates (the NPT what's on page does), use exactly those dates and nothing more.
d) EVERY RUN: roll each REGULARS record forward like the baby records, re-opening its src first. A src that refuses WebFetch keeps rolling only when it states a weekly pattern; a listing of individual dates never rolls on its own.
e) LOOK FOR MORE, EVERY RUN: WebSearch "Lego club library Swansea", "Saturday kids club Swansea", "code club Swansea Saturday", "family swim Swansea weekend", "kids cinema Swansea Saturday", "Young Archaeologists Swansea", "Saturday family art Swansea", "Sunday family Swansea weekly", plus the same with Neath, Port Talbot and Llanelli. Vue Swansea's Mighty Mornings page (src of rg-vuemornings) is updated each Tuesday.

COMPLETENESS: COUNT WHAT THE PAGE SAYS, COUNT WHAT YOU READ (added 7 November 2026 after Ashley found 105 Happity classes missing. Anyone editing this runbook: keep this section.)
Why it happened: listing pages were read through a summary that quietly dropped most items, and "none" was reported without checking the page's own total. Rules:
a) Never conclude that a listing has nothing new, or nothing on a day, from a summary. Every listing page that prints its own total ("28 classes", "Discover 13", "Showing 1 to 20 of 64") must be read until the number of items you captured equals that total. Write both numbers in last_run.md, for example "Happity Mondays: page says 28, read 28". If they differ, the source is "partly read": say so in AFTERWARDS and in the notification.
b) Ask WebFetch for a numbered list of EVERY item with its fields, never a summary, and compare the count with the page's total. If WebFetch cannot return them all, the page is partly read (rule a).
c) HAPPITY WEEKDAY SWEEP, FIRST RUN OF EACH CALENDAR MONTH and whenever Ashley asks: read https://www.happity.co.uk/Swansea/baby-toddler-classes?submit_button=weekday_next&weekday=<Mondays|Tuesdays|Wednesdays|Thursdays|Fridays|Saturdays|Sundays> (all seven), record every slot in a new tools/happity/sweep_YYYY-MM-DD.tsv (same columns as sweep_2026-11-07.tsv), then run tools/happity/build.py and tools/happity/patch.py. On 7 November 2026 the seven pages held 170 slots: 30 already listed, 6 left out (reasons in tools/happity/report.txt), 105 new cards.
d) Every class in the sweep goes on the site unless it is adults only, shows no usable day or date, or is already listed from another source. Toddler groups and under-5 classes are cat "clubs" with weekly:true; baby-only sessions (up to about 18 months) and pregnancy sessions are cat "baby". Weekly under-5 sessions stay out of the date rows and show in "With a baby", "Little ones", "Weekend clubs and regulars", the calendar and the filters.

THE WEEKEND CHECK, EVERY RUN (added 3 November 2026)
After the sources and before publishing, count the non-baby events on each of the next two Saturdays and the next two Sundays (a record counts on a day when that date is in `days`).
- Any of those days with fewer than 6: run these searches for that date before giving up: "<day> <date> Swansea family", "<date> Swansea kids", "this weekend Swansea family <month>", "what's on Swansea this weekend", "<date> Neath OR Llanelli family", and read the newest Swansea Bay News and whatsoninswansea weekend round-up. Go back through TIER 2 if today is a Monday. Every find still follows THE ACCURACY RULE.
- Never pad a weekend with undated, last year's or guessed events. A thin weekend is reported, not filled.
- In AFTERWARDS: one line per day, "Sat 14 Nov: 9 events" and so on.

SELF-CHECK AND ALERT (added 3 November 2026 after two runs in a row added almost nothing and the website was not updated)
Before you finish, work out these facts from the file you published and the website step:
1. ADDED: how many records have "added" equal to today.
2. PUSHED: after git push, run `git ls-remote origin main` and confirm the hash equals your local `git rev-parse HEAD`. If not, the push failed.
3. DEPLOYED: wait about two minutes, then use the Netlify connector (load with ToolSearch "select:mcp__Netlify__netlify-project-services-reader,mcp__Netlify__netlify-deploy-services-reader"). Call netlify-project-services-reader get-project with siteId c0e06fa5-2659-499e-973a-936004612b3e, take currentDeploy.currentDeploy.id, then netlify-deploy-services-reader get-deploy-for-site with that siteId and deployId. DEPLOYED is true when its state is "ready" and its commit_ref equals your pushed hash. If it is still building, wait two more minutes and check once more. If the Netlify tools are missing, say "Deploy not checked: Netlify tools missing".
If ADDED is under 10, or PUSHED or DEPLOYED is false, the FIRST line of your final message (Ashley's phone notification) must start with "ATTENTION:" and say which, in plain words, for example "ATTENTION: only 4 events added (Monday half). Website not updated: push rejected." Under 10 added is not a failure by itself when the sources genuinely had nothing new, but it must be visible, with the reason in one line.

AFTERWARDS
Write the full report to tools/family/last_run.md in the clone (replace the file each run, start it with today's date and the half) and commit it with index.html. The report: five or six sentences, then list any source you could not read fully, then say whether the website was updated: how many events are listed now and how many are marked indoors, what the source sweep added or removed and why, which indoor or winter events and holiday camps were added, any indoor place added, updated or removed, which touring organisers produced a Swansea date, which organisers were added to the bank, whether any caveat could be lifted or had to be acted on, whether Swansea Bay News surfaced a council event, and whether any Tier 3 source became readable. Then the occasion lines from SPECIAL OCCASIONS (f), the waiting list (g), the Babies and bumps line, and any HOLS or OCCASIONS entries you added or removed. If nothing changed, say so plainly.
Then the REGULARS line ("Regulars: <n> records, <n> weekend sessions in the next 2 weeks"), the WEEKEND CHECK lines and the SELF-CHECK facts (added, pushed, deployed). Your final message (Ashley's phone notification) must be at most six lines: the ATTENTION line if needed, events added and total, the weekend counts, website pushed and deployed and must lead with the ATTENTION line when SELF-CHECK requires one.
