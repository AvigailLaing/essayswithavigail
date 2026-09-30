#!/usr/bin/env python3
"""Compare what the site advertises against what Stan actually charges.

prices.json is the site's single source of truth, but Stan is the source of
truth for money: whatever the store charges at checkout is the real price. A
site price that is HIGHER than Stan undersells her; one that is LOWER is a
price she advertised and has to honour. Either way she wants to know the same
day, which is why this runs on a schedule rather than when someone remembers.

Exit codes: 0 all matched, 1 a mismatch, 2 could not check (network, or a
product whose title moved). Never exits 0 on a product it failed to find.
"""
import json, pathlib, re, sys, urllib.request

STORE = "https://stan.store/avigaillaing"
HERE = pathlib.Path(__file__).parent

# site key -> a distinctive fragment of the Stan product title.
# Fragments, not whole titles, so a wording tweak on Stan doesn't read as an outage.
PRODUCTS = {
    "complete":        "Complete Package",
    "essay30":         "Essay Done in 30 Days",
    "supplementals30": "Supplementals Done in 30 Days",
    "session":         "1:1 Essay Strategy Session",
    "hybrid":          "One Call, Then Written Edits",
    "bothEdit":        "Common App + Supplementals Edited",
    "essayEdit":       "Essay Edits, Back in 48 Hours",
    "suppsEdit":       "Supplemental Edits, Back in 48 Hours",
    "oneEdit":         "One-Time Essay Edit",
    "pack":            "The Full College Essay System",
}


PRICE_RE = re.compile(r'data-slot="(regular-price|sale-price)">\$([0-9,]+)')


def fetch():
    req = urllib.request.Request(STORE, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")


def price_after(html, fragment, window=4000):
    """Stan renders the product title then its price, so anchor on the title we
    are looking for and take the first price block after it. Matching the title
    first (rather than guessing the nearest title before a price) is what makes
    this survive the store's markup changing around it.

    Returns (effective_price, both_prices) or (None, None) if the title is gone.
    """
    i = html.lower().find(fragment.lower())
    if i < 0:
        return None, None
    seen = {}
    for m in PRICE_RE.finditer(html, i, i + window):
        seen.setdefault(m.group(1), "$" + m.group(2))
        if len(seen) == 2:
            break
    if not seen:
        return None, None
    # a buyer pays the sale price when there is one
    return seen.get("sale-price") or seen.get("regular-price"), seen


def main():
    site = json.loads((HERE / "prices.json").read_text())
    try:
        html = fetch()
    except Exception as e:
        print(f"COULD NOT CHECK: {e}")
        return 2
    if len(PRICE_RE.findall(html)) < 5:
        print("COULD NOT CHECK: the store page came back without its prices")
        return 2

    mismatch, missing, ok = [], [], []
    for key, fragment in PRODUCTS.items():
        stan_price, _ = price_after(html, fragment)
        if stan_price is None:
            missing.append((key, fragment))
        elif site.get(key) != stan_price:
            mismatch.append((key, site.get(key), stan_price))
        else:
            ok.append(key)

    if mismatch:
        print("PRICES DO NOT MATCH STAN\n")
        for key, s, t in mismatch:
            direction = "site HIGHER than Stan" if _num(s) > _num(t) else "site LOWER than Stan, she must honour it"
            print(f"  {key:18s} site {s:>6}   stan {t:>6}   {direction}")
        print("\n  If Stan is right: edit prices.json, then run  python3 sync-prices.py")
        print("  If the site is right: change the price in Stan.")
    if missing:
        print("\nCOULD NOT FIND ON STAN (renamed, unlisted, or sold out):")
        for key, frag in missing:
            print(f"  {key:18s} looked for {frag!r}")

    if not mismatch and not missing:
        print(f"All {len(ok)} prices match Stan.")
        return 0
    return 1 if mismatch else 2


def _num(p):
    try:
        return int(re.sub(r"[^0-9]", "", p or "0"))
    except ValueError:
        return 0


if __name__ == "__main__":
    sys.exit(main())
