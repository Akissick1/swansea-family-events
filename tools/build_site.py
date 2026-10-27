"""Build the public website (index.html) from the guide's page source.

Usage:  python3 tools/build_site.py <page.html> [<out index.html>]

<page.html> is the guide exactly as published on Claude (either the source file,
or the full HTML that the Artifact "read" action saves, which starts with a
small <!doctype ...><body> wrapper). The guide itself is not changed: this only
moves the title, icons, fonts and styles into a proper <head> and adds the
details a normal website has (language, description, social sharing preview).
"""
import re, sys

SITE = "https://swansea-family-events.netlify.app/"
TITLE = "Swansea Family Events | What's on for kids in Swansea and nearby"
DESC = ("Family and children's events across Swansea, Gower, Neath Port Talbot, "
        "Llanelli and nearby: Halloween, Christmas, half term, shows, workshops and "
        "indoor places for rainy days. Every listing links to the page that confirms its date.")

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
    out = (meta + head_part.strip() + "\n</head>\n<body>\n"
           + '<noscript><p style="padding:20px;font-family:sans-serif">This guide needs JavaScript switched on to show the events.</p></noscript>\n'
           + body_part.strip() + "\n</body>\n</html>\n")
    return out

if __name__ == "__main__":
    src = open(sys.argv[1], encoding="utf-8").read()
    dst = sys.argv[2] if len(sys.argv) > 2 else "index.html"
    open(dst, "w", encoding="utf-8").write(build(src))
    print("wrote", dst)
