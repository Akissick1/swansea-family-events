"""Make sideways scrolling and the view tabs obvious (Ashley, 9 Nov 2026: people did not know
they could slide the rows or tap the tabs).

Usage: python3 tools/swipe/patch_swipe.py page.html   (family or Grown-Ups page; safe to run twice)

Adds to every scrolling row: a "Swipe for more" chip in the row heading, a round next button and a
fade on the right edge (phones), a back button once scrolled, a progress bar under the row, and
always-visible arrows on computers. The first row gives a small sideways nudge on every visit, and
a "Swipe sideways" coach bubble shows until the visitor has swiped a row once.
On phones the view tabs become a full-width bar of icon buttons, so every tab is visible.
"""
import re, sys

MARK = "SWIPE-HINTS v1"
page = sys.argv[1]
s = open(page, encoding="utf-8").read()
if MARK in s:
    print("already patched"); sys.exit(0)

CSS = """
/* ---------- """ + MARK + """: make sideways scrolling and the tabs obvious ---------- */
.tab .ti{display:none;width:20px;height:20px;flex:none}
@media (max-width:620px){
  .top .segmented{display:grid;grid-auto-flow:column;grid-auto-columns:1fr;width:100%;border-radius:14px;padding:4px;gap:3px}
  .top .tab{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;padding:7px 2px 6px;
    border-radius:10px;font-size:11.5px;line-height:1.15;white-space:normal;text-align:center;min-height:52px}
  .top .tab .ti{display:block}
  .top .tab[aria-selected="true"]{color:var(--accent)}
  .top.stuck .tab{min-height:44px;padding-block:5px 4px}
  .top.stuck .tab .ti{width:17px;height:17px}
}
.swipechip{margin-left:auto;display:none;align-items:center;gap:6px;border:1px solid var(--accent);background:var(--accent-soft);
  color:var(--accent);font:inherit;font-size:12.5px;font-weight:700;border-radius:999px;padding:4px 11px;cursor:pointer;white-space:nowrap;align-self:center}
.swipechip i{font-style:normal;font-size:16px;line-height:1;display:inline-block;animation:jnudge 1.4s ease-in-out infinite}
.rail-wrap.sw-can .swipechip{display:inline-flex}
.rail-wrap.sw-can.sw-end .swipechip{opacity:.55}
.rail-wrap.sw-end .swipechip i{animation:none}
.rail-head .swipechip span{color:inherit;font-size:inherit;font-weight:inherit;white-space:nowrap}
.swipechip .sw-m{display:none}
@media (hover:hover) and (pointer:fine){.swipechip .sw-t{display:none}.swipechip .sw-m{display:inline}}
.swfade{position:absolute;right:0;width:56px;pointer-events:none;z-index:25;display:none;
  background:linear-gradient(90deg,rgba(255,255,255,0),var(--ground) 82%)}
.today-band .swfade{background:linear-gradient(90deg,rgba(255,255,255,0),var(--accent-soft) 82%)}
.swnext,.swprev{position:absolute;z-index:31;width:42px;height:42px;border-radius:50%;border:1px solid var(--line-2);
  background:var(--surface);color:var(--ink);font-size:24px;line-height:1;cursor:pointer;display:none;place-items:center;
  box-shadow:0 4px 14px rgba(25,22,18,.25);padding:0 0 3px}
.swnext{right:6px}.swprev{left:6px}
.rail-wrap.sw-can:not(.sw-end) .swfade{display:block}
.rail-wrap.sw-can:not(.sw-end) .swnext{display:grid;animation:swpulse 2.2s ease-in-out 3}
.rail-wrap.sw-can:not(.sw-start) .swprev{display:grid}
@keyframes swpulse{0%,100%{transform:scale(1)}50%{transform:scale(1.12)}}
.swbar{height:4px;border-radius:2px;background:var(--surface-3);margin:6px 0 4px;overflow:hidden;display:none;position:relative;z-index:2}
.swbar i{display:block;height:100%;width:30%;border-radius:2px;background:var(--accent);transition:margin-left .12s linear}
.rail-wrap.sw-can .swbar{display:block}
.today-band .swbar{margin-bottom:12px}
@media (hover:hover) and (min-width:760px){
  .swnext,.swprev,.swfade{display:none!important}
  .rail-wrap.sw-can:not(.sw-start) .arrow.l,.rail-wrap.sw-can:not(.sw-end) .arrow.r{display:flex}
}
.swcoach{position:absolute;z-index:40;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:10px;
  background:rgba(25,22,18,.9);color:#fff;border-radius:999px;padding:10px 16px 10px 12px;font-size:14px;font-weight:700;
  box-shadow:0 10px 30px rgba(25,22,18,.35);white-space:nowrap;cursor:pointer;border:0;font-family:inherit;
  animation:swcoachin .35s ease both}
.swcoach .sw-m{display:none}
@media (hover:hover) and (pointer:fine){.swcoach .sw-t{display:none}.swcoach .sw-m{display:inline}}
.swcoach svg{width:30px;height:30px;flex:none;animation:swhand 1.6s ease-in-out infinite}
.swcoach.out{opacity:0;transition:opacity .3s;pointer-events:none}
@keyframes swhand{0%,100%{transform:translateX(8px)}50%{transform:translateX(-8px)}}
@keyframes swcoachin{from{opacity:0;transform:translate(-50%,8px)}to{opacity:1;transform:translate(-50%,0)}}
@media (prefers-reduced-motion:reduce){.swipechip i,.swcoach svg,.rail-wrap .swnext{animation:none!important}}
"""

JS = r"""
/* """ + MARK + """: hints that rows slide sideways, added to every scrolling row */
(function(){
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function getKey(k){ try { return localStorage.getItem(k); } catch(e){ return null; } }
  function setKey(k,v){ try { localStorage.setItem(k,v); } catch(e){} }
  var coachDone = getKey("swipeCoachDone") === "1", coachEl = null, peeked = false;
  function finishCoach(){
    if(!coachDone){ coachDone = true; setKey("swipeCoachDone","1"); }
    if(coachEl){ var c = coachEl; coachEl = null; c.classList.add("out"); setTimeout(function(){ if(c.parentNode) c.parentNode.removeChild(c); }, 350); }
  }
  function step(tr, dir){ tr.scrollBy({left: dir * tr.clientWidth * 0.82, behavior: "smooth"}); }
  function setup(wrap){
    var tr = wrap.querySelector(".track");
    if(!tr || wrap.getAttribute("data-sw") === "1") return;
    wrap.setAttribute("data-sw","1");
    var head = wrap.querySelector(".rail-head");
    if(head){
      var chip = document.createElement("button");
      chip.type = "button"; chip.className = "swipechip";
      chip.setAttribute("aria-label","Scroll this row for more");
      chip.innerHTML = '<span class="sw-t">Swipe for more</span><span class="sw-m">Scroll for more</span> <i aria-hidden="true">&#8250;</i>';
      chip.addEventListener("click", function(){ step(tr, 1); });
      head.appendChild(chip);
    }
    var fade = document.createElement("span"); fade.className = "swfade"; fade.setAttribute("aria-hidden","true");
    var nx = document.createElement("button"); nx.type = "button"; nx.className = "swnext"; nx.setAttribute("aria-label","See more in this row"); nx.innerHTML = "&#8250;";
    var pv = document.createElement("button"); pv.type = "button"; pv.className = "swprev"; pv.setAttribute("aria-label","Back along this row"); pv.innerHTML = "&#8249;";
    nx.addEventListener("click", function(){ step(tr, 1); });
    pv.addEventListener("click", function(){ step(tr, -1); });
    wrap.appendChild(fade); wrap.appendChild(nx); wrap.appendChild(pv);
    var bar = document.createElement("div"); bar.className = "swbar"; bar.setAttribute("aria-hidden","true"); bar.innerHTML = "<i></i>";
    tr.parentNode.insertBefore(bar, tr.nextSibling);
    function place(){
      var c = tr.querySelector(".art") || tr.firstElementChild; if(!c) return;
      var wr = wrap.getBoundingClientRect(), cr = c.getBoundingClientRect();
      if(!cr.height) return;
      var top = cr.top - wr.top;
      fade.style.top = top + "px"; fade.style.height = cr.height + "px";
      nx.style.top = pv.style.top = (top + cr.height/2 - 21) + "px";
    }
    function upd(){
      var max = tr.scrollWidth - tr.clientWidth, can = max > 8;
      wrap.classList.toggle("sw-can", can);
      wrap.classList.toggle("sw-start", tr.scrollLeft <= 4);
      wrap.classList.toggle("sw-end", !can || tr.scrollLeft >= max - 4);
      var vis = tr.scrollWidth ? tr.clientWidth / tr.scrollWidth : 1, w = Math.max(10, vis*100);
      bar.firstChild.style.width = w + "%";
      bar.firstChild.style.marginLeft = (max > 0 ? (tr.scrollLeft/max) * (100 - w) : 0) + "%";
    }
    var userTouched = false;
    ["touchstart","pointerdown","wheel"].forEach(function(t){ tr.addEventListener(t, function(){ userTouched = true; }, {passive:true}); });
    tr.addEventListener("scroll", function(){ upd(); if(userTouched && tr.scrollLeft > 30) finishCoach(); }, {passive:true});
    if(window.ResizeObserver){ new ResizeObserver(function(){ place(); upd(); }).observe(wrap); }
    window.addEventListener("resize", function(){ place(); upd(); });
    place(); upd();
    wrap._swPlace = place; wrap._swUpd = upd;
  }
  function firstRail(){
    var all = document.querySelectorAll("#rails .rail-wrap.sw-can");
    for(var i=0;i<all.length;i++){ if(all[i].getBoundingClientRect().height) return all[i]; }
    return null;
  }
  var watching = null;
  function coachAndPeek(){
    var wrap = firstRail(); if(!wrap || watching === wrap) return;
    watching = wrap;
    var tr = wrap.querySelector(".track");
    function showCoach(){
      if(coachDone || coachEl) return;
      coachEl = document.createElement("button");
      coachEl.type = "button"; coachEl.className = "swcoach";
      coachEl.innerHTML = '<svg viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 17V7.5a2 2 0 0 1 4 0V15"/><path d="M16 14.5v-2a2 2 0 0 1 4 0V16"/><path d="M20 15a2 2 0 0 1 4 0v4.5c0 4.5-3 8-7.5 8h-1c-3 0-4.6-1.4-6.3-3.6l-3-4a2 2 0 0 1 3.1-2.5L12 20"/><path d="M3 6h6M3 6l2.5-2.5M3 6l2.5 2.5M29 6h-6M29 6l-2.5-2.5M29 6l-2.5 2.5"/></svg>'+
        '<span class="sw-t">Swipe sideways to see more</span><span class="sw-m">Scroll sideways or use the arrows</span>';
      coachEl.addEventListener("click", function(){ step(tr, 1); finishCoach(); });
      var c = tr.querySelector(".art") || tr.firstElementChild;
      var wr = wrap.getBoundingClientRect(), cr = c ? c.getBoundingClientRect() : wr;
      coachEl.style.top = Math.max(0, (cr.top - wr.top) + cr.height*0.55) + "px";
      wrap.appendChild(coachEl);
      var mine = coachEl;
      setTimeout(function(){ if(coachEl === mine){ coachEl = null; mine.classList.add("out"); setTimeout(function(){ if(mine.parentNode) mine.parentNode.removeChild(mine); }, 350); } }, 8000);
    }
    function go(){
      showCoach();
      if(peeked || reduce) return;
      peeked = true;
      setTimeout(function(){
        tr.scrollBy({left: 110, behavior: "smooth"});
        setTimeout(function(){ tr.scrollBy({left: -110, behavior: "smooth"}); }, 750);
      }, 600);
    }
    if("IntersectionObserver" in window){
      var io = new IntersectionObserver(function(en){
        if(!en[0].isIntersecting) return; io.disconnect(); go();
      }, {threshold: 0.6});
      io.observe(tr);
    } else setTimeout(go, 1200);
  }
  var queued = false;
  function scan(){
    queued = false;
    document.querySelectorAll(".rail-wrap").forEach(setup);
    document.querySelectorAll(".rail-wrap[data-sw]").forEach(function(w){ if(w._swPlace){ w._swPlace(); w._swUpd(); } });
    coachAndPeek();
  }
  function queue(){ if(!queued){ queued = true; requestAnimationFrame(scan); } }
  new MutationObserver(queue).observe(document.body, {childList: true, subtree: true});
  if(document.fonts && document.fonts.ready) document.fonts.ready.then(queue);
  queue();
})();
"""

ICONS = {
  "browse": '<path d="M4 6h16M4 12h16M4 18h16" opacity=".35"/><rect x="3" y="4" width="7" height="16" rx="1.5"/><rect x="14" y="4" width="7" height="16" rx="1.5"/>',
  "cal": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
  "places": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>',
  "post": '<circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/>',
  "src": '<path d="M8 6h13M8 12h13M8 18h13"/><circle cx="4" cy="6" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="18" r="1"/>',
}

# 1. CSS: before the first </style>
i = s.index("</style>")
s = s[:i] + CSS + s[i:]

# 2. Tab icons
def add_icon(m):
    view = m.group(2)
    if view not in ICONS:
        return m.group(0)
    svg = ('<svg class="ti" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
           'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONS[view] + '</svg>')
    return m.group(1) + svg + '<span>' + m.group(3) + '</span></button>'
s, n = re.subn(r'(<button class="tab" role="tab" aria-selected="(?:true|false)" data-view="(\w+)">)([^<]+)</button>', add_icon, s)
if n < 4:
    sys.exit(f"only found {n} tabs")
s = s.replace(MARK, MARK)  # no-op, keeps the marker in place

# 3. JS: before the last </script>
j = s.rindex("</script>")
s = s[:j] + JS + s[j:]
open(page, "w", encoding="utf-8").write(s)
print(f"patched: {n} tabs")
