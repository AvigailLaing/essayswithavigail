# Essays with Avigail — design system

The visual system used on essayswithavigail.com. Hand this to anything that needs to match.

---

## The idea in one line

Black ink on white paper, a single gold accent, and hairline rules instead of cards. Nothing floats,
nothing glows, and the only decoration is the typography. The proof on the page is screenshots of
real emails, so the interface around them stays quiet enough that they read as documents rather than
as marketing.

---

## Tokens

Drop these in as-is.

```css
:root {
  /* ground */
  --paper:      #ffffff;   /* default page background */
  --paper-2:    #faf9f5;   /* warm off-white, alternating bands and inset panels */
  --band:       #101010;   /* inverted sections */

  /* ink — four steps, never more */
  --ink:        #101010;   /* headings, primary text */
  --ink-2:      #3f3f3c;   /* body copy */
  --ink-3:      #6e6e68;   /* secondary and captions */
  --ink-4:      #9b9b93;   /* labels, metadata, muted */

  /* accent */
  --gold:       #cfae70;   /* BACKGROUNDS ONLY, always with #101010 text on top */
  --gold-deep:  #8a6d1f;   /* gold as TEXT on white — contrast-safe, 4.9:1 */
  --gold-line:  #e0cfa6;   /* faint gold rules */

  /* rules */
  --hair:       #e6e5df;              /* 1px borders on light ground */
  --hair-dark:  rgba(255,255,255,0.16); /* 1px borders on dark ground */

  --font-display: 'Libre Caslon Text', Georgia, 'Times New Roman', serif;
  --font-body:    'Inter', system-ui, -apple-system, sans-serif;

  --page:    1120px;  /* max content width */
  --measure: 62ch;    /* max width for running text */
}
```

**The one colour rule that matters:** `--gold` and `--gold-deep` are not interchangeable. `#cfae70`
on white is roughly 2:1 and fails contrast, so it is only ever a background with dark text on it.
When gold has to *be* the text, use `#8a6d1f`. Getting this backwards is the single easiest way to
make a page look off-brand and fail accessibility at the same time.

The neutrals are warm on purpose. `--paper-2` is `#faf9f5` rather than a grey, and the ink steps
drift very slightly warm (`#3f3f3c`, not `#3f3f3f`) so they sit with the gold instead of fighting it.

---

## Type

Two families, loaded from Google Fonts:

```html
<link href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

**Libre Caslon Text** carries every headline, big number and pull quote, almost always at **700**.
This is the whole personality of the brand. It reads academic without reading stuffy, and the bold
weight is deliberate — the 400 weight looked too delicate at display sizes.

**Inter** does everything else: body copy, labels, buttons, navigation.

### The pairing rule

The hybrid is the point: **serif for the thing being said, uppercase sans for the thing labelling it.**

| Role | Family | Size | Weight | Treatment |
|---|---|---|---|---|
| Page H1 | Caslon | `clamp(36px, 5.4vw, 62px)` | 700 | `letter-spacing: -0.02em`, `text-wrap: balance` |
| Hero H1 | Caslon | `clamp(40px, 6.4vw, 76px)` | 700 | `letter-spacing: -0.022em` |
| Section H2 | Caslon | `clamp(27px, 3.6vw, 41px)` | 700 | `letter-spacing: -0.012em` |
| Big number | Caslon | `clamp(30px, 3.6vw, 42px)` | 700 | `font-variant-numeric: tabular-nums` |
| Eyebrow / section label | Inter | 10.5px | 600 | `letter-spacing: 0.3em`, uppercase, `--gold-deep` |
| Block label | Inter | 10.5px | 600 | `letter-spacing: 0.26em`, uppercase, `--ink`, 1px bottom border in `--ink` |
| Metadata label | Inter | 10px | 600 | `letter-spacing: 0.24em`, uppercase, `--ink-4` |
| Body | Inter | 15–16.5px | 400 | `line-height: 1.8`, colour `--ink-2`, capped at `--measure` |
| Button | Inter | 11px | 600 | `letter-spacing: 0.2em`, uppercase |

Emphasis inside a serif headline is **italic at weight 400**, never bold and never a colour change:

```css
h2 em { font-style: italic; font-weight: 400; }
```

On dark bands the italic goes gold. On light ground it stays black.

Every headline gets `text-wrap: balance`. Every stretch of running text gets `max-width: var(--measure)`.
Anything with digits in a column gets `font-variant-numeric: tabular-nums`.

---

## Layout

- **Container:** `max-width: 1120px; margin: 0 auto; padding: 0 40px` (22px on mobile).
- **Section rhythm:** `padding: 104px 0` desktop, `68px 0` mobile.
- **Band alternation:** white → warm off-white → white, with exactly one or two black sections for
  contrast. Never two dark bands adjacent.
- **Breakpoints:** only two, `980px` and `768px`. Three-column grids go to two, then one.

### Hairlines, not cards

This is the strongest rule in the system. Structure comes from 1px rules and grid gaps, **not** from
rounded corners, drop shadows or filled cards.

```css
/* grid whose gap IS the border */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  background: var(--hair);   /* shows through the gaps */
}
.grid > * { background: var(--paper); padding: 30px; }
```

`border-radius` is **0** everywhere. The only shadows in the whole system are on the acceptance-letter
images, where they exist to make paper look like paper.

### Stat rows

Repeated in three places, always the same shape: a flex row with `border-top` and `border-bottom` in
`--hair`, each cell separated by `border-left`, serif number over an uppercase tracked label. Collapses
to a stacked column at 768px with `border-top` replacing `border-left`.

### Proportional bars

For comparing amounts, bars beat a table. Track is `--paper-2` with a `--hair` border, fill is
`--gold`, and the single largest item gets a taller track with an `--ink` fill so it reads as the
headline number.

---

## Components

**Buttons.** Solid `--gold` with `--ink` text, 11px uppercase at `0.2em` tracking, `18px 38px` padding,
square corners. Hover inverts to `--ink` background with `--paper` text plus `translateY(-2px)`.
Secondary is transparent with a `--hair` border.

**Accordions.** Native `<details>` / `<summary>`, no JavaScript. Marker hidden via
`summary::-webkit-details-marker { display: none }`, replaced with a CSS plus sign built from two
pseudo-element bars; the vertical bar rotates 90° and fades on `[open]`.

**Masonry galleries.** CSS `columns: 3` with `break-inside: avoid` on children. Right for
mixed-aspect screenshots, and it degrades to `columns: 1` cleanly.

**Sticky buy panel.** `position: sticky; top: 96px`, `--paper-2` background, `--hair` border. Goes
`position: static` on mobile.

**Citation card.** Left border 3px `--gold` turning `--ink` on hover, meta line in `--gold-deep`,
serif headline. Used for press mentions.

---

## Motion

Almost none, and it is all the same: `IntersectionObserver` adds a `.visible` class that transitions
`opacity 0 → 1` and `translateY(20px) → 0` over `0.7s ease`. Hovers are `0.2s`. There is one 62s
linear marquee.

Everything sits behind:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
}
```

---

## Writing rules that go with the design

These matter as much as the CSS, because the type treatment assumes copy written this way.

- **No em dashes.** Anywhere. They are a tell and she rejects them on sight. Use a comma, a full
  stop, or restructure.
- **Always contractions.** "isn't", "you'll", "it's".
- **No stacked fragments.** Explain, then land it, in real sentences.
- Labels name the thing plainly. No cleverness in uppercase.
- Numbers are specific and never rounded up for effect.

---

## Adapting this to a dashboard

The system was built for a long scrolling sales page, so a few things need a decision rather than a
copy-paste:

- **Density.** `104px` section padding is far too airy for a dashboard. Keep the tokens and the type
  scale, cut the vertical rhythm to roughly a third.
- **Semantic colour.** There is no success/warning/error in this palette, because the site never
  needed one. Add those separately and keep them clearly distinct from `--gold`, which should stay
  reserved for brand and primary action.
- **Dark mode.** The site is deliberately single-theme. If the dashboard needs dark, invert
  `--paper`/`--ink`, keep `--gold` as the accent, and swap `--hair` for `--hair-dark`.
- **What to keep no matter what:** Caslon 700 headlines, uppercase tracked sans labels, hairline
  borders instead of cards, square corners, and the two-tier gold rule.
