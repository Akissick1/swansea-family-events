"""Build the public website (index.html) from the guide's page source.

Usage:  python3 tools/build_site.py <page.html> [<out index.html>]

<page.html> is the guide exactly as published on Claude (either the source file,
or the full HTML that the Artifact "read" action saves, which starts with a
small <!doctype ...><body> wrapper). The guide itself is not changed: this only
moves the title, icons, fonts and styles into a proper <head> and adds the
details a normal website has (language, description, social sharing preview).
"""
import os, re, sys

SITE = "https://swansea-family-events.netlify.app/"
TITLE = "Swansea Family Events | What's on for kids in Swansea and nearby"
DESC = ("Family and children's events across Swansea, Gower, Neath Port Talbot, "
        "Llanelli and nearby: Halloween, Christmas, half term, shows, workshops and "
        "indoor places for rainy days. Every listing links to the page that confirms its date.")

# Visitor analytics (PostHog, EU cloud, cookieless: no cookies or local storage, so no consent banner).
# Website only: the Claude guide never carries this. Added 29 October 2026.
ANALYTICS = """<script>
!function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
posthog.init("phc_zJ3C4TbprQaw5u4h9QrUJFhmSC84iF3vTMtxHbEtWXEk",{api_host:"https://eu.i.posthog.com",cookieless_mode:"always",person_profiles:"identified_only",capture_pageview:true,capture_pageleave:true,autocapture:false,disable_session_recording:true});
(function(){
  function cap(n,p){ try{ window.posthog && posthog.capture(n,p||{}); }catch(e){} }
  function sheetTitle(){ var h=document.getElementById("sheetTitle"); return h ? h.textContent.trim() : ""; }
  document.addEventListener("click", function(ev){
    var t = ev.target; if(!t || !t.closest) return;
    var evBtn = t.closest("[data-ev]");
    if(evBtn){ var id = evBtn.getAttribute("data-ev"); setTimeout(function(){ cap("event_opened",{event_id:id, event_title:sheetTitle()}); },80); return; }
    var jmp = t.closest("[data-jump]");
    if(jmp){ var jb = jmp.querySelector("b"); cap("section_jumped",{section: jb ? jb.textContent.trim() : jmp.getAttribute("data-jump")}); return; }
    var tab = t.closest("[data-view]");
    if(tab){ cap("tab_viewed",{tab:tab.getAttribute("data-view")}); return; }
    if(t.closest("#seasonJump")){ cap("season_button",{label:t.closest("#seasonJump").textContent.trim()}); return; }
    var a = t.closest("a[href]");
    if(a && a.closest("#sheet") && !a.hasAttribute("data-cal")){
      var h = a.getAttribute("href")||"";
      var kind = /calendar\\.google\\.com|outlook\\.live\\.com/.test(h) ? "calendar_added" : /^mailto:|whatsapp|facebook\\.com\\/sharer/.test(h) ? "event_shared" : "listing_opened";
      cap(kind,{event_title:sheetTitle(), url: kind==="listing_opened" ? h : undefined});
      return;
    }
    if(a && /^mailto:ashleykissick1/.test(a.getAttribute("href")||"")){ cap("post_event_email"); }
  }, true);
  var q, timer;
  document.addEventListener("input", function(ev){
    if(!ev.target || ev.target.type!=="search" && ev.target.id!=="q") return;
    q = ev.target.value.trim(); clearTimeout(timer);
    timer = setTimeout(function(){ if(q.length>=3) cap("search_used",{query:q.slice(0,60)}); },1500);
  }, true);
})();
</script>
"""

# Weather widget (website only, added 30 October 2026). The page keeps its events inside a closed function,
# so the build exposes them as window.SFE_EVENTS for tools/weather.html. If the anchor ever changes,
# the site still builds, just without weather.
EVENTS_ANCHOR = "EVENTS = EVENTS.filter(function(e){ return lastDayOf(e) >= TODAY; });"
def add_weather(page):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weather.html")
    if not os.path.exists(path) or page.count(EVENTS_ANCHOR) != 1:
        print("warning: weather widget skipped (anchor or tools/weather.html missing)")
        return page
    page = page.replace(EVENTS_ANCHOR, EVENTS_ANCHOR + " window.SFE_EVENTS = EVENTS;")
    extras = [path]
    cal = os.path.join(os.path.dirname(path), "calendar.html")   # Save to your calendar, added 30 October 2026
    if os.path.exists(cal): extras.append(cal)
    blocks = "\n".join(open(x, encoding="utf-8").read().strip() for x in extras)
    return page.replace("\n</body>", "\n" + blocks + "\n</body>")

def build(src):
    s = src
    # Drop the hosting wrapper if the input came from an Artifact read.
    head = s[:4000].lower()
    if head.lstrip().startswith("<!doctype") and "<body>" in head:
        s = s[s.lower().index("<body>") + len("<body>"):]
    s = re.sub(r"</body>\s*</html>\s*$", "", s.rstrip())
    marker = '<header class="top gut">'
    if s.count(marker) != 1:
        sys.exit("could not find the page header marker")
    i = s.index(marker)
    head_part, body_part = s[:i], s[i:]
    head_part = re.sub(r"<title>.*?</title>\s*", "", head_part, count=1, flags=re.S)
    meta = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{SITE}">
<meta name="theme-color" content="#F8F6F2">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Swansea Family Events">
<meta property="og:title" content="Swansea Family Events">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{SITE}">
<meta property="og:image" content="{SITE}og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<style>html{{scroll-padding-top:env(safe-area-inset-top,0px)}}body{{margin:0;padding:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
"""
    out = (meta + head_part.strip() + "\n" + ANALYTICS + "</head>\n<body>\n"
           + '<noscript><p style="padding:20px;font-family:sans-serif">This guide needs JavaScript switched on to show the events.</p></noscript>\n'
           + body_part.strip() + "\n</body>\n</html>\n")
    return add_weather(out)

if __name__ == "__main__":
    src = open(sys.argv[1], encoding="utf-8").read()
    dst = sys.argv[2] if len(sys.argv) > 2 else "index.html"
    open(dst, "w", encoding="utf-8").write(build(src))
    print("wrote", dst)
