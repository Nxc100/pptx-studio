# Animation & transitions

## How it is encoded (engine.Timeline / build_timing)
One auto-start click group (`<p:cond delay="indefinite"/><p:cond evt="onBegin">` → plays when the slide appears,
exactly like the reference template). Items are grouped by absolute start time `at` (ms); each group is a `p:par`
with `delay=at`. Shapes with text get `<p:bldP grpId="0"/>`, shapes without text `animBg="1"`; pictures, charts,
connectors need no bldP. `check_deck.py` verifies targets/ids.

## Effect catalog (`tl.add(shape, effect, at=, dur=, **kw)`)
| effect | preset | look | typical use |
|---|---|---|---|
| `fade` | 10 | opacity | decor, paragraphs, labels |
| `wipe` dir=left/right/up/down | 22 | reveal from edge | titles, captions, lines, bars, charts |
| `rise` dy=0.05–0.1 (neg = from above) | 42 | fade + float up | cards, photos, hanging branches (dy<0) |
| `slide` dx=0.03–0.05 | 42 | fade + drift from right | list rows, names |
| `zoom` scale=0 / 0.85–0.94 | 53 | grow (+fade) | hero photos (0.9), badges/pins (0), stat cards (0.85) |
| `circle` | 6/32 | circular iris | round material swatches |
| `split` / `splitv` | 16 | barn doors | ornamental dividers |
| `letters` pct=9000–18000 | 0 + iterate lt | char-by-char fade + drift | cover/section/thanks titles, summary quote |

## Choreography recipes (ms)
* **Content slide chrome**: sprig fade 0/700 · title wipe 150/550 · caption wipe 450/550 · header fade 350/600 ·
  bottom sprig rise 500/900. Content starts ≈ 600–900.
* **Cover**: hero photo zoom(0.9) 0/1300 · frames fade 500,700 · kicker wipe 300 · title letters 500 ·
  subtitle fade 1350 · English wipe 1600 · divider split 1850 · pill wipe 2050 · info rows slide 2300+180n ·
  seal zoom 1500 · branch rise(dy -0.06) 900 · garland rise 1200. Total ≈ 2.9 s.
* **Section**: photo zoom(0.92) 0/1300 · big number fade 200/1200 · "The Part" rise 300 · title letters 600 ·
  English wipe 1300 · pill 1550 · divider 1750 · items fade 1950 · poem 2250 · leaves rise 1200+250n.
* **Grids/lists**: stagger 120–200 ms per item, inner elements +100…+400 ms after their container.
* **Diagrams**: base image first, then overlays by meaning (pins 160 ms apart; flows 700 ms per flow; zones 450 ms).
Keep the whole build ≤ 3.5 s: presenters click on before longer builds finish.

## Transitions by slide kind (theme `transitions`)
cover/end: `p15:curtains` 2.4 s (or `p15:drape`) · section: `p15:pageCurlDouble` 1.7 s (book) / `p14:reveal` ·
content: `fade` 0.7–0.9 s · rendering pages: `p14:gallery` dir l 1.6 s / `p14:pan` · board: `p15:prestige`.
Avoid mixing more than 4 kinds; never use vortex/shred/flash on content.

## Compatibility notes
PowerPoint 2013+ plays everything; older versions and some WPS builds use the `p:fade` fallback automatically.
LibreOffice ignores animation in PDF export (good for QA: you see the end state). If the user only has WPS,
mention that p14/p15 transitions depend on the WPS version. Reference decks: `analyze_deck.py` prints every
timeline as `entr:wipe[22/8] withEffect step@500 +0ms dur=['500'] -> 'shape name'`.
