"""Back button retraces every step in the guide: tabs, panels (event, day, place), moving between
panels, and search. Replaces the simpler panel-only version. Idempotent."""
import sys
OLD_BLOCK = """  /* Back button: opening a panel adds one history step, so Back closes the panel, not the page. */
  var sheetHist = false;
  function sheetPush(){ if(sheetHist) return; try{ history.pushState({sfeSheet:1}, ""); sheetHist = true; }catch(err){} }
  window.addEventListener("popstate", function(){ if(sheetHist){ sheetHist = false; closeSheet(true); } });
  function closeSheet(fromBack){
    if(sheetHist && fromBack !== true){ sheetHist = false; try{ history.back(); }catch(err){} }
    dayCtx = null;"""
NEW_BLOCK = """  /* Back button: every step (tab, panel, search) adds one history entry, and Back undoes the
     steps one at a time, in order. Only when none are left does Back leave the guide. */
  var NAV = [], navBusy = false, navSkip = 0, curPanel = null;
  function navPush(kind, undo, extra){
    if(navBusy) return;
    try{ history.pushState({sfe:NAV.length+1}, ""); }catch(err){ return; }
    var s = {k:kind, u:undo}; if(extra) s.prev = extra; NAV.push(s);
  }
  window.addEventListener("popstate", function(ev){
    if(navSkip > 0){ navSkip--; return; }
    var target = (ev.state && ev.state.sfe) || 0, popped = null;
    while(NAV.length > target){ popped = NAV.pop(); }
    if(!popped) return;
    navBusy = true; var did = true;
    try{ did = popped.u() !== false; }finally{ navBusy = false; }
    if(!did && NAV.length) history.back(); /* that step was already undone another way: go one further */
  });
  function samePanel(a,b){ return !!a && !!b && a.t===b.t && a.id===b.id && a.d===b.d; }
  function panelStep(p){
    var prev = curPanel; curPanel = p;
    if(navBusy || samePanel(prev,p)) return;
    if(prev && prev.t==="day" && p.t==="day") return; /* next or previous day inside the day panel */
    var top = NAV[NAV.length-1];
    if(top && top.k==="panel" && samePanel(top.prev, p)){ NAV.pop(); navSkip++; history.back(); return; }
    navPush("panel", function(){ if(!curPanel) return false; restorePanel(prev); }, prev || {t:"none"});
  }
  function restorePanel(p){
    if(!p){ shutSheet(); return; }
    if(p.t==="ev"){ dayCtx = p.day || null; openSheet(p.id); }
    else if(p.t==="day") openDay(p.d);
    else if(p.t==="pl") openPlace(p.id);
  }
  function closeSheet(){
    if(!navBusy){
      var n = 0; for(var i=NAV.length-1; i>=0 && NAV[i].k==="panel"; i--) n++;
      if(n && curPanel){ history.go(-n); return; }
    }
    shutSheet();
  }
  function shutSheet(){
    curPanel = null;
    dayCtx = null;"""
for P in sys.argv[1:]:
    s = open(P, encoding="utf-8").read()
    if "function panelStep" in s: print(P, "already done"); continue
    assert s.count(OLD_BLOCK) == 1, (P, "old block")
    s = s.replace(OLD_BLOCK, NEW_BLOCK)
    # the three panel openers
    i = s.index("function openSheet(id){"); j = s.index('scrim.classList.add("open"); sheetPush();', i)
    s = s[:j] + 'scrim.classList.add("open"); panelStep({t:"ev",id:id,day:dayCtx});' + s[j+len('scrim.classList.add("open"); sheetPush();'):]
    i = s.index("function openDay(d){"); j = s.index('scrim.classList.add("open"); sheetPush();', i)
    s = s[:j] + 'scrim.classList.add("open"); panelStep({t:"day",d:d});' + s[j+len('scrim.classList.add("open"); sheetPush();'):]
    i = s.index("function openPlace(id){"); j = s.index('scrim.classList.add("open"); sheetPush();', i)
    s = s[:j] + 'scrim.classList.add("open"); panelStep({t:"pl",id:id});' + s[j+len('scrim.classList.add("open"); sheetPush();'):]
    assert "sheetPush" not in s and "sheetHist" not in s, P
    # tabs
    old = """    if(tab){
      state.view = tab.getAttribute("data-view");"""
    assert s.count(old) == 1, (P, "tab")
    s = s.replace(old, """    if(tab){
      var fromView = state.view;
      state.view = tab.getAttribute("data-view");
      if(fromView !== state.view) navPush("view", function(){
        if(state.view === fromView) return false;
        var t = document.querySelector('.tab[data-view="'+fromView+'"]'); if(t) t.click();
      });""")
    # search: the first letter typed is a step; Back clears the search
    old = """    qTimer = setTimeout(function(){ state.q = qEl.value.trim().toLowerCase(); renderAll(); }, 160);"""
    assert s.count(old) == 1, (P, "search")
    s = s.replace(old, """    qTimer = setTimeout(function(){
      var was = state.q; state.q = qEl.value.trim().toLowerCase();
      if(!was && state.q) navPush("search", function(){ if(!state.q) return false; qEl.value = ""; state.q = ""; renderAll(); });
      renderAll();
    }, 160);""")
    open(P, "w", encoding="utf-8").write(s)
    print(P, "patched")
