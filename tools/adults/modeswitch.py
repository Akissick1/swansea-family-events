"""Add the Family | Grown-ups switch under the header of a guide page (idempotent).

Usage: python3 modeswitch.py <page.html> family|adults
"""
import sys, re
P, MODE = sys.argv[1], sys.argv[2]
s = open(P, encoding="utf-8").read()
SITE = "https://swansea-family-events.netlify.app/"
CSS = """
/* ---------- Family | Grown-ups switch ---------- */
.modebar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding-block:10px;background:var(--surface);border-bottom:1px solid var(--line)}
.modesw{display:inline-flex;background:var(--surface-2);border:1px solid var(--line);border-radius:999px;padding:4px;gap:2px}
.modesw a{display:inline-flex;align-items:center;gap:7px;padding:8px 18px;border-radius:999px;font-weight:700;font-size:14px;text-decoration:none;color:var(--ink-2);line-height:1.2}
.modesw a:hover{color:var(--ink);background:var(--surface)}
.modesw a[aria-current="page"]{background:var(--accent);color:#fff;box-shadow:0 2px 8px rgba(0,0,0,.14)}
.modesw a i{width:8px;height:8px;border-radius:50%;background:currentColor;opacity:.7}
.modehint{color:var(--ink-3);font-size:13px}
@media (max-width:520px){.modehint{display:none}.modesw{width:100%}.modesw a{flex:1;justify-content:center}}
"""
fam_cur = ' aria-current="page"' if MODE == "family" else ""
ad_cur = ' aria-current="page"' if MODE == "adults" else ""
hint = "Theatre, gigs, comedy, sport and nights out for grown-ups" if MODE == "family" else "Kids' events, half term and rainy-day places"
NAV = ('<nav class="modebar gut" id="modebar" aria-label="Choose a guide"><div class="modesw">'
       '<a href="' + SITE + '"' + fam_cur + '><i></i>Family</a>'
       '<a href="' + SITE + 'adults/"' + ad_cur + '><i></i>Grown-ups</a></div>'
       '<span class="modehint">' + ("Switch to Grown-ups: " if MODE == "family" else "Switch to Family: ") + hint + '</span></nav>\n')
s = re.sub(r'\n/\* ---------- Family \| Grown-ups switch ---------- \*/\n.*?@media \(max-width:520px\)\{\.modehint[^\n]*\n', "\n", s, flags=re.S)
s = re.sub(r'<nav class="modebar gut" id="modebar".*?</nav>\n', "", s, flags=re.S)
assert s.count("</style>") >= 1 and s.count("</header>") == 1
i = s.index("</style>"); s = s[:i] + CSS.lstrip("\n") + s[i:]
s = s.replace("</header>\n", "</header>\n" + NAV, 1)
open(P, "w", encoding="utf-8").write(s)
print("switch added:", MODE)
