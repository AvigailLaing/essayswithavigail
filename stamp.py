#!/usr/bin/env python3
"""Stamp style.css with its own content hash in every page that links it.

GitHub Pages caches style.css hard, so a deploy that only changes CSS can leave
a browser showing the old design until someone hard refreshes. The hash changes
whenever the file does, so the browser is forced to fetch it, and nothing is
refetched when the CSS has not moved. Run this before every commit that touches
style.css.
"""
import hashlib, io, re, glob

h = hashlib.md5(open("style.css", "rb").read()).hexdigest()[:8]
for page in glob.glob("*.html"):
    s = io.open(page, encoding="utf-8").read()
    new, n = re.subn(r'(href=")style\.css(?:\?v=[0-9a-f]+)?(")', rf'\1style.css?v={h}\2', s)
    if n and new != s:
        io.open(page, "w", encoding="utf-8").write(new)
    print(f"{page}: {n} link(s) -> style.css?v={h}")
