# Slide archetypes (Deck API)

```python
import sys; sys.path.insert(0, r'<skill>/scripts')
from studio import Deck
d = Deck('medieval_pastoral', assets='assets', brand='Ba · 无界森居', brand_en='MEDIEVAL PASTORAL INTERIOR',
         meta=dict(title=..., author=..., subject=..., keywords=...))
...archetype calls...
d.save('out/deck.pptx')
```
* Paths are relative to `assets` (project photos, crops, 3D renders, board). Theme decor comes from the theme folder.
* Colours in content tuples are semantic theme names (`primary`, `accent`, `line`, …) or hex `'B0623A'`.
* Run dicts (for titles/footers): `dict(text=, size=, color=, bold=, italic=, font='head'|'body'|..., latin=True)`.
* Every archetype accepts `note=` (speaker notes; auto-generated from slide text if omitted) and
  animates itself; the transition comes from the theme by slide kind (cover, contents, section, content, gallery, board, end).
* Canvas 13.333 × 7.5 in. Content slides share the chrome: corner decor, title (26pt), English caption, running
  header (brand), folio. Titles ≤ 8 Chinese chars; English captions short.
* Visual reference for every archetype: `examples/ba_wujie/preview/medieval_pastoral-1..4.jpg` (slide order below).

| # in example | method | use for |
|---|---|---|
| 1 | `cover(title, subtitle, en_line, info, photo, focus, kicker)` | title page; `info=[(label,value)]` ≤3 rows (主讲人/学号/地点) |
| 2 | `contents(parts, photo, focus, heading, heading_en)` | `parts=[(num, cn, en, desc)]` ≤4 |
| 3,13,19,27 | `section(num, part, cn, en, photo, focus, items, poem, mark)` | chapter divider; `items` may contain `\n`; `mark` = vertical spine word |
| 4 | `overview(title, en, stats, facts, paragraph, photos)` | project overview: 3 stat cards, ≤4 fact rows, paragraph, 3 framed photos `(path, focus, label)` |
| – | `text_image(title, en, heading, paragraphs, photo, focus, items)` | generic statement page |
| – | `gallery_grid(title, en, tiles, cols=4)` | grid of framed photos `(path, caption)` ≤ 2 rows |
| 5 | `location_levels(title, en, levels, callout)` | 3 map levels `(img, title, text)`; `callout=dict(meta, pin, text)` points at the pin of level 3 |
| 6 | `poi_map(title, en, map_img, meta, pois, center, neighbors, insight, nudge)` | slab map with numbered pins; `pois=[(icon, pin_key, desc)]` ≤6; `neighbors=[(text, fx, fy)]` fractions of map box; `insight=(title, en, text)` |
| 7 | `chart_page(title, en, line_chart, bar_chart, stats, responses, source)` | native charts: `(title, cats, values[, fmt])`; 4 stat tiles `(icon, value, unit, caption)`; responses `(key, text)` ≤4 |
| 8 | `persona(title, en, people, extra_line, day, mapping)` | 3 persona cards `(icon, name, role, hobby, need)`; day timeline `(time, act, room)` ≤6; mapping `(need, space)` ≤6 |
| 9 | `pillars(title, en, quote, cols)` | concept with 3 pillars `(char, title, en, photo, text)` |
| 10 | `moodboard(title, en, heading_lines, heading_en, text, keywords, tiles)` | style positioning; 8 framed crops `(photo, title, caption)`; keywords ≤6 |
| 11 | `palette(title, en, statement, swatches, ratio, ratio_note, photo, focus)` | colour analysis; swatches `(hex, name, use)` ≤8; ratio `(fraction, hex, label, text_colour)` |
| 12 | `materials(title, en, mats, subs)` | 3 material circles `(texture, application_img, name, rooms, text)` + ≤4 sub materials `(img, name, use)` |
| 14 | `plan_annotated(title, en, plan_img, rooms, dims, points, offset)` | numbered room badges at source-pixel positions; dims `(value, caption)` ≤4; points `'key：text'` ≤3 (one line each) |
| 15 | `plan_legend(title, en, plan_img, legend, note_text)` | coloured plan + legend swatches `(img_or_hex, name, rooms)` ≤5 |
| 16 | `model3d(title, en, img, meta, labels, intro, points)` | 3D render with projected label pills; points `(icon, key, text)` ×3 |
| 17 | `zones(title, en, img, meta, zone_of, zones)` | zoning render; `zone_of={label: zone_idx}`; zones `(cn, en, chip_hex, rooms, desc)` |
| 18 | `flows(title, en, plan_img, flows, entry, summary, offset)` | circulation arrows; flows `(name, colour, dash, [paths], desc)`, path = source-pixel points |
| 20–26 | `room(title, en, photo, points, keyplan, rect, offset, side, details, focus)` | rendering page: big photo + key plan with highlighted rect + ≤4 icon points; `side='left'` mirrors; `details=[crop paths]` (1–2) |
| 28 | `board(title, en, img, points, spec_lines)` | exhibition board image + composition notes |
| 29 | `summary(title, en, quote, quote_en, tiles)` | 4 framed tiles `(icon, key, text, photo)` |
| 30 | `thanks(photo, focus, big, sub, line, footer)` | closing page |

Icons: any name in `themes/<t>/icons/` (`<name>_primary|light|accent.png`); add more with `scripts/assets/icons.py`.
Plan coordinates: measure on `photo_prep.py preview` output (labels are source pixels); if the plan image was
cropped by N px, pass `offset=(N, N)` and keep using the original coordinates.

## Typical outlines

**Interior / architecture design proposal (26–32 slides)** — cover · contents · §1 前期分析 (项目概况, 区位×2,
气候, 人群, 设计理念, 风格定位, 色彩, 材质) · §2 平面 (平面布置, 彩色平面, 3D 鸟瞰, 功能分区, 动线) ·
§3 效果图 (one `room` per render, alternate `side`) · §4 展板 (board, 设计总结) · thanks.

**Course / research report (12–18)** — cover · contents · section · text_image (背景) · chart_page (数据) ·
pillars (方法/观点) · gallery_grid (案例) · moodboard (参考) · section · text_image ×n · summary · thanks.

**Product / brand pitch (12–16)** — cover · pillars (价值主张) · overview (关键数字) · gallery_grid (产品) ·
palette (视觉识别) · materials (工艺/材质) · chart_page (市场) · persona (用户) · summary · thanks.

## Extending

Add a method to `Deck` following the pattern: `s, tl, n = self.new(kind)`; `self.chrome(...)`; place shapes with
`add_text/add_shape/add_pic` (positions in inches), register each with `tl.add(shape, effect, at=ms, dur=ms)`;
`return self.finish(s, tl, note)`. Keep 0.5 in margins, text ≥ 9.5 pt (body 10.5–13), and stagger at 80–200 ms.
