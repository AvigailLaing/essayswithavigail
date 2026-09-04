#!/usr/bin/env python3
"""Push prices.json into index.html.

Prices live in exactly one place. Edit prices.json, run this, commit.
Every price on the page is wrapped in <span data-price="key">, so this only
ever rewrites those spans and cannot touch surrounding copy.
"""
import io, json, re, sys

prices = json.load(open("prices.json"))
html = io.open("index.html", encoding="utf-8").read()

changed = []
def sub(m):
    key, old = m.group(1), m.group(2)
    new = prices.get(key)
    if new is None:
        sys.exit(f"prices.json has no key '{key}'")
    if new != old:
        changed.append(f"  {key}: {old} -> {new}")
    return f'<span data-price="{key}">{new}</span>'

out = re.sub(r'<span data-price="([a-zA-Z0-9]+)">([^<]*)</span>', sub, html)
n = len(re.findall(r'<span data-price=', out))
if n == 0:
    sys.exit("no data-price spans found; nothing to sync")
io.open("index.html", "w", encoding="utf-8").write(out)
print(f"{n} price slots synced")
print("\n".join(changed) if changed else "  (all already current)")
