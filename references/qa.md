# QA: loop, checklist, known traps

## Loop (cheap → expensive)
1. `check_deck.py deck.pptx --fonts` — must say `result: OK`; fonts must be installed or QA renders lie.
2. `render_deck.py deck.pptx out/r` → read `grid-*.jpg` (9 slides each). Open single `s-NN.jpg` only for suspects.
3. Fix several issues per rebuild (spec edits), re-render only changed pages: `--pages 6,14`.
4. Final: one fresh-eyes subagent over all `s-NN.jpg` (prompt below). Fix, re-render those pages.
5. Optional schema check: pptx skill `validate.py deck.pptx --original <user draft>` (a `dc.xsd` import error on
   docProps/core.xml is a network artefact of the validator, also present on untouched files).

## Fresh-eyes QA subagent prompt
"Visual QA of a rendered N-slide deck: images <dir>/s-01.jpg … (13.33×7.5 in at 110 dpi ≈ 1467×825 px). View every
image. Report only user-visible defects: text overflowing/cut off or touching a card edge, single orphaned characters
on a line, overlaps (text over images, decor over text, badges over badges, frames colliding with folio/page
numbers), elements < 0.3 in from each other or slide edges, uneven gaps, low contrast, placeholder or garbled text,
anything inconsistent with the rest of the deck. Format: 'slide NN: problem at location'. List clean slides on one
line. < 400 words. Do not modify files."

## Checklist (what the subagent found last time — check these first)
- corner decor drawn over the first title characters → keep title x ≥ 1.45 in, sprig ≤ 2.1 in wide
- vertical/rotated watermark words clipped or low-contrast over photos → `vert=True` text on the margin, no alpha
- captions of adjacent columns running together → leave ≥ 0.3 in between text boxes
- pin badges overlapping each other/pin stems → place badges ON pin heads, `nudge` near-duplicates apart
- last line of a dark card touching the card bottom → shorten text or enlarge card
- orphaned last character (e.g. "域。") → shorten wording; Chinese wraps per character
- uneven gaps between 1-line and 2-line list rows → compute y per row (chart_page does) or keep rows one line
- folio colliding with big photo frames → photo bottom ≤ 6.85 in
- plan images with clipped dimension text → crop the edge, pass `offset`
- inset image that doesn't show what the caption says (plan crop in a "material application" circle) → use a render/3D crop

## Known traps (fixed in engine; remember when writing custom code)
| symptom | cause | fix |
|---|---|---|
| paper texture not shown, slides white | default master already has `<p:bg>`; two bg elements | `set_master_background` removes old bg |
| text cut in the middle in LibreOffice/PDF | `spc` letter-spacing + `alpha` on the same run | drop alpha (engine warns) |
| rotated text clipped | unrotated frame extends past the slide | `vert=True` box inside the slide |
| PowerPoint "repair" / animation ignored | formula `#ppt_y+-0.05`; duplicate cTn ids; missing targets | `_off()`; `check_deck.py` |
| `NameError _set_fonts` | `from x import *` skips `_names` | import explicitly |
| black bar on a crop | crop box beyond image | `photo_prep crops` clamps |
| odd placeholders when user adds a slide | python-pptx 4:3 default layouts | `drop_unused_layouts` on save |
| garbled Chinese in console | Windows code page | `PYTHONIOENCODING=utf-8` |
| fonts differ on another PC | Noto Serif SC not installed there | tell user: install or 嵌入字体 on save; ship PDF |
| p14/p15 transitions missing in old viewers | unsupported | fade fallback is automatic |

## Delivery checklist
backup original · same file name for the new deck · PDF export · board JPG (A1@150 dpi) · `check_deck` OK ·
QA subagent clean · notes present · summary to the user: what changed, assumptions (personas, approximate data,
POI positions), fonts, animations not play-tested in PowerPoint/WPS.
