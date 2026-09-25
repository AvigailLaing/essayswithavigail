#!/usr/bin/env python3
"""Push prices.json into every page that shows a price.

Prices live in exactly one place. Edit prices.json, run this, commit.
Every price on a page is wrapped in <span data-price="key">, so this only
ever rewrites those spans and cannot touch surrounding copy.

It walks every *.html in the folder rather than a hardcoded list: results.html
carried a stale $549 for weeks because the old version only ever opened
index.html, and a page that is not swept is a page that silently drifts.
"""
import io, json, pathlib, re, sys

prices = json.load(open("prices.json"))
pages = sorted(p for p in pathlib.Path(".").glob("*.html"))

changed, total, touched = [], 0, 0
for page in pages:
    html = io.open(page, encoding="utf-8").read()
    if 'data-price=' not in html:
        continue

    def sub(m):
        key, old = m.group(1), m.group(2)
        new = prices.get(key)
        if new is None:
            sys.exit(f"{page}: prices.json has no key '{key}'")
        if new != old:
            changed.append(f"  {page.name}  {key}: {old} -> {new}")
        return f'<span data-price="{key}">{new}</span>'

    out = re.sub(r'<span data-price="([a-zA-Z0-9]+)">([^<]*)</span>', sub, html)
    n = len(re.findall(r'<span data-price=', out))
    total += n
    touched += 1
    if out != html:
        io.open(page, "w", encoding="utf-8").write(out)

if total == 0:
    sys.exit("no data-price spans found on any page; nothing to sync")
print(f"{total} price slots synced across {touched} page(s)")
print("\n".join(changed) if changed else "  (all already current)")

# a price outside a data-price span is the failure mode this system exists to
# prevent, so fail loudly rather than reporting success
stray = []
for page in pages:
    html = io.open(page, encoding="utf-8").read()
    for m in re.finditer(r'\$\d[\d,]*', html):
        a, b = max(0, m.start() - 90), m.end() + 30
        window = html[a:b]
        if 'data-price=' in window:
            continue
        stray.append(f"  {page.name}:{html[:m.start()].count(chr(10))+1}  {m.group(0)}  ...{window[60:150].strip()[:70]}")
if stray:
    print("\nprices NOT under the sync (check these by hand):")
    print("\n".join(stray))
