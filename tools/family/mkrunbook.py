import re,sys
p=open(sys.argv[1]).read()
def rep(old,new,count=1):
    global p
    n=p.count(old)
    if n!=count: sys.exit(f"anchor x{n}: {old[:70]!r}")
    p=p.replace(old,new)

rep("Refresh Ashley's Swansea Family Events artifact.\n",
"""SWANSEA FAMILY EVENTS, REFRESH RUNBOOK
This file is read by the twice-weekly scheduled task (Mondays and Thursdays, Opus). The task prompt itself is short and points here. Edit this file in the repo to change how the refresh works.

TWO HALVES (Ashley's choice, 3 November 2026, the same way the Grown-Ups refresh works)
The source list is split so each run can do its half properly instead of skimming everything. Sources tagged [EVERY RUN] are checked on both days. [MON] sources are checked on Mondays, [THU] sources on Thursdays (UK date). If the task is fired by hand on another day, use the half of the most recent Monday or Thursday. Never remove an event because its source was not checked today.
""")

# Tier 1 tagging
tags={"1":"MON","2":"MON","3":"MON","4":"MON","5":"MON","6":"MON","7":"EVERY RUN","8":"EVERY RUN","9":"EVERY RUN",
 "10":"MON","11":"MON","12":"MON","13":"EVERY RUN","14":"MON","14a":"MON","14b":"EVERY RUN","14c":"MON","14d":"MON","14e":"MON","14f":"MON"}
rep("TIER 1, CHECK EVERY RUN\n","TIER 1. Check the [EVERY RUN] lines and the lines tagged with today's half.\n")
s=p.index("TIER 1. Check"); e=p.index("Open the individual event page for anything you add.")
block=p[s:e]
lines=block.split("\n")
for i,l in enumerate(lines):
    m=re.match(r"^(\d+[a-f]?) ",l)
    if m and m.group(1) in tags:
        lines[i]=f"{m.group(1)} [{tags[m.group(1)]}] "+l[len(m.group(0)):]
        tags.pop(m.group(1))
if tags: sys.exit("untagged "+str(tags))
p=p[:s]+"\n".join(lines)+p[e:]

rep("TIER 2, MONDAYS AND THURSDAYS ONLY (UK date). Skip this tier on every other day.\n",
    "TIER 2 [THU]. Thursdays. On Mondays skip it, unless KEEPING THE PAGE FULL or THE WEEKEND CHECK sends you back here.\n")

# NPT clubs now go in as regulars
rep("Routine weekly clubs (Lego Club, Duplo, Coding, Stay and Play) and adult sessions do not, but Halloween or Christmas themed one-offs of those clubs do.",
    "Routine children's clubs (Lego Club, Kids Club, Pokemon Club, Duplo, Coding, Stay and Play) now go in under REGULARS below, one card per club per library with exactly the dates this listing shows. Adult sessions stay out. Halloween or Christmas themed one-offs of those clubs are separate cards.")

rep("Only: museum, science, outdoors, halloween, food, shows, sport, baby (Babies & bumps, see BABIES AND BUMPS).",
    "Only: museum, science, outdoors, halloween, food, shows, sport, baby (Babies & bumps, see BABIES AND BUMPS), clubs (Clubs & drop-ins, see REGULARS).")
rep("bump, course, weekly (optional, baby records only)","bump, course (optional, baby records only), weekly (optional, any session that repeats on a set weekday, see REGULARS)")

rep("1. Roll forward the weekly recurring events: Swansea Prom junior parkrun every Sunday, Swansea Bay parkrun every Saturday, Quiet Hour at the Museum every Monday. Regenerate their `days` arrays so they cover today through the end of the next calendar month, and re-check each page still says it is running.",
    "1. Roll forward every record with \"weekly\":true (parkruns, Quiet Hour, Welly Wednesday, the REGULARS and the baby sessions) following REGULARS and BABIES AND BUMPS. Re-check each page still says it is running.")

# Link check: drop the Monday full sweep, make it monthly
rep("- Mondays only (UK date): re-fetch EVERY `src` URL still in the file, with the same rule.",
    "- First run of each calendar month only: re-fetch EVERY `src` URL still in the file, with the same rule.")

# New sections before AFTERWARDS
new = """REGULARS: WEEKEND CLUBS AND WEEKLY ACTIVITIES (added 3 November 2026, Ashley's rule. Anyone editing this runbook: keep this section.)
Ashley found weekends looking empty. Families want the things that happen most Saturdays and Sundays, not only one-off events. The page has a "This weekend" row, a "Weekend clubs and regulars" row and a "Clubs & drop-ins" category (cat "clubs"). The first seven records (ids beginning "rg-") and how they were built are in tools/regulars/regulars.py.
a) WHAT GOES IN: library Lego, kids and Pokemon clubs, code clubs, junior parkruns, weekend kids' film mornings, family swims or fun sessions with a published weekly slot, museum or gallery family drop-ins, stay and play on a Saturday or Sunday, Young Archaeologists or similar family clubs, and any other children's session that a public page says runs on a set weekday. Paid term classes that need enrolment (ballet, gymnastics, swimming lessons) stay out unless the page says families can drop in or book single sessions.
b) RECORD: cat "clubs" (cinema mornings stay "shows", parkruns stay "sport"), "weekly":true, scene "library" at libraries, otherwise the venue's scene. One card per activity per venue.
c) DATES: the same WEEKLY PATTERN RULE as BABIES AND BUMPS c): when a page states the weekday and time, list the next 8 weeks, skip 24 December to 1 January, skip HOLS dates when it says term time only, and write the pattern in span. When a listing shows individual dates (the NPT what's on page does), use exactly those dates and nothing more.
d) EVERY RUN: roll each REGULARS record forward like the baby records, re-opening its src first. A src that refuses WebFetch keeps rolling only when it states a weekly pattern; a listing of individual dates never rolls on its own.
e) LOOK FOR MORE, EVERY RUN: WebSearch "Lego club library Swansea", "Saturday kids club Swansea", "code club Swansea Saturday", "family swim Swansea weekend", "kids cinema Swansea Saturday", "Young Archaeologists Swansea", "Saturday family art Swansea", "Sunday family Swansea weekly", plus the same with Neath, Port Talbot and Llanelli. Vue Swansea's Mighty Mornings page (src of rg-vuemornings) is updated each Tuesday.

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

"""
rep("AFTERWARDS\n", new+"AFTERWARDS\n")
p=p.rstrip()+"\nThen the REGULARS line (\"Regulars: <n> records, <n> weekend sessions in the next 2 weeks\"), the WEEKEND CHECK lines and the SELF-CHECK facts (added, pushed, deployed). Your final message must be at most six lines and must lead with the ATTENTION line when SELF-CHECK requires one.\n"
open('/home/claude/swansea-family-events/tools/family/RUNBOOK.md','w').write(p)
print(len(p))
