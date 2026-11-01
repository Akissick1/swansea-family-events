"""Phone back button closes the open panel instead of leaving the page (idempotent)."""
import sys
for P in sys.argv[1:]:
    s = open(P, encoding="utf-8").read()
    if "sheetHist" in s: print(P, "already done"); continue
    n = s.count('scrim.classList.add("open");')
    assert n >= 1, P
    s = s.replace('scrim.classList.add("open");',
                  'scrim.classList.add("open"); sheetPush();')
    old = "  function closeSheet(){\n    dayCtx = null;"
    assert s.count(old) == 1, P
    s = s.replace(old, """  /* Back button: opening a panel adds one history step, so Back closes the panel, not the page. */
  var sheetHist = false;
  function sheetPush(){ if(sheetHist) return; try{ history.pushState({sfeSheet:1}, ""); sheetHist = true; }catch(err){} }
  window.addEventListener("popstate", function(){ if(sheetHist){ sheetHist = false; closeSheet(true); } });
  function closeSheet(fromBack){
    if(sheetHist && fromBack !== true){ sheetHist = false; try{ history.back(); }catch(err){} }
    dayCtx = null;""")
    open(P, "w", encoding="utf-8").write(s)
    print(P, "patched,", n, "openers")
