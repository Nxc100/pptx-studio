---
name: pptx-studio
description: Build or rebuild presentation-grade, fully animated .pptx decks (design proposals, interior / architecture / landscape / product / course reports, 汇报/答辩/方案PPT) in any visual style from a theme + a short content spec, including reference-deck analysis, 3D maps for 区位分析 (three.js), 3D floor plans, exhibition boards (展板), slide transitions and auto-play entrance animations, plus a LibreOffice render + QA loop. Use this whenever the user wants a beautiful PPT/PPTX, asks to 改造/美化/重做/升级 a deck, to imitate or surpass a reference deck's look, animation or transitions, to add missing analysis pages (区位/气候/人群/色彩/材质/动线), or names a style for slides (欧式/中世纪田园/侘寂/新中式/北欧/法式/轻奢/工业风…), even if they never mention this skill.
---

# pptx-studio

A proven pipeline (first used for "Ba · 无界森居", a 30-slide 欧洲中世纪田园风 interior proposal, see
`references/case-ba-wujie.md`) packaged so the next deck costs a fraction of the tokens:
**content becomes a ~250-line spec; layout, animation, transitions and theme are code.**

```
scripts/studio/        Deck class: 22 animated slide archetypes + engine (OOXML, animations, transitions, theme)
scripts/analyze_deck.py  reference/draft deck -> report.md (layouts, fonts, colours, timelines) + contact sheets
scripts/render_deck.py   pptx -> pdf -> slide JPGs + 3x3 grids (cheap visual QA)
scripts/check_deck.py    structural QA (anim targets, transitions, notes, LibreOffice clipping traps, fonts)
scripts/assets/        paper.py · recolor.py · derive_theme.py · icons.py · render_svg.py (botanical.js/ornament.js) · photo_prep.py
scripts/three/         render3d.py + map3d.html (GeoJSON 3D maps, pins, POIs) · prep_plan.py + plan3d.html (3D plan from 彩平图)
scripts/board/         render_html.py (HTML board/poster -> print-res image) ; templates/board_a1.html
themes/                medieval_pastoral(.json + decor/icons), wabi_sabi (derived)  — add yours
examples/ba_wujie/     spec.py (full 30-slide spec), three/*.json configs, preview/*.jpg (what each archetype looks like)
```
Environment: python-pptx, Pillow, numpy, opencv, PyMuPDF, playwright(chromium), LibreOffice. Run scripts with
`PYTHONIOENCODING=utf-8` on Windows. Specs import with `sys.path.insert(0, '<skill>/scripts'); from studio import Deck`.

## Workflow (follow in order; each step names the cheap tool)

1. **Inventory the inputs** – `photo_prep.py sheet <素材dir> sheet.jpg` (one image shows every material),
   `photo_prep.py convert` to RGB/JPEG with ASCII names, `photo_prep.py preview` for crop coordinates.
2. **Analyze reference + the user's draft** – `analyze_deck.py ref.pptx out/ref --brief` and the same for the draft;
   read `report.md` + `grid-*.jpg` (not raw XML). Write a 10-line design brief: palette, fonts, motif (frame shape,
   corner decor, ornaments), slide types (cover/contents/section/content/end), animation vocabulary & timing,
   transitions (check layouts too — templates often define transitions on *unused* layouts), and what the draft lacks
   (missing analysis pages, text that contradicts the materials, leftover template pages). See `references/reference-analysis.md`.
3. **Theme** – reuse `themes/*.json`, or derive one in one command (`derive_theme.py`, recolours decor + icons +
   paper), or pick a recipe from `references/design-system.md`. New motif shapes (bamboo, ginkgo, art-deco…)
   → `render_svg.py` / a fork agent with the prompt in `references/assets.md`.
4. **Assets in parallel** (fork agents; prompts in `references/assets.md`): photo crops (3:4 for arch frames),
   3D location maps + POIs (`three/render3d.py` with map configs; GeoJSON from geo.datav.aliyun.com for China
   adcodes), 3D plan / zoning (`prep_plan.py` → `render3d.py --same-trim`), board (`templates/board_a1.html`).
5. **Spec** – copy `examples/ba_wujie/spec.py`, keep the structure, replace content. Archetype API + typical outlines:
   `references/archetypes.md`; look at `examples/ba_wujie/preview/*.jpg` to choose layouts without rendering.
   Pass real `note=` speaker notes for key slides (others get auto notes).
6. **Build + QA loop** – `python spec.py out/deck.pptx` → `check_deck.py out/deck.pptx --fonts` →
   `render_deck.py out/deck.pptx out/r` → read grids, then single slides with problems → fix spec → repeat.
   Before delivery give one fresh-eyes QA subagent all slide JPGs (prompt in `references/qa.md`); fix what it finds.
   Optional: `pptx` skill's `validate.py --original <draft>` (its core.xml "dc.xsd" error is a network artefact).
7. **Deliver** – back up the original (`<name>_原稿备份.pptx`), write the new deck under the original file name,
   also export the PDF (fonts-proof) and the board image. Tell the user: fonts used (install/embed on other PCs),
   that animations were structurally verified but not play-tested in PowerPoint/WPS, and which content is
   assumed/approximate (personas, climate normals, POI positions).

## Quality bar (why the result looks designed, not generated)

- **One motif, repeated**: theme frame geometry (arch / rrect / plaque / oval…) on photos, cards, swatches; the same
  corner decor, bullet ornament, divider and folio on every content slide; big faint chapter number on sections.
- **Palette discipline**: paper background (texture, never pure white) 60%, primary 30%, accent ≤10%; text in
  ink/ink_soft, never black. Swatches on colour slides are sampled from the actual renders (`photo_prep palette`).
- **Every slide has a visual**; long text is split into icon points, cards, or stat callouts.
- **Choreographed auto-play**: decor fades → title wipes → hero image zooms/rises → content in reading order,
  80–200 ms staggers, whole build 2–3.5 s; cover/section titles animate letter by letter. Transitions by slide kind
  (cover/end = curtains/drape, sections = page curl/reveal, renders = gallery, content = fade), always with fade fallback.
- **Content fidelity**: fix text that contradicts the materials, add the analysis pages a proposal needs
  (区位·气候·人群·理念·风格·色彩·材质·平面·分区·动线·效果图·展板·总结), label approximations.

## Pitfalls already solved in code (don't re-debug) — details in `references/qa.md`

two `<p:bg>` in the default master (paper ignored) · letter-spacing + transparency clipped by LibreOffice ·
rotated text frames leaving the slide clipped (use `vert=True`) · `#ppt_y+-0.05` formulas · `from engine import *`
skips `_private` names · source plans with clipped dimension text (crop + `offset`) · crops past the image edge
(black bars) · python-pptx default 4:3 layouts (removed on save) · Chinese text on Windows consoles (`PYTHONIOENCODING`).

## Token savers

Grids before singles (9 slides per image at 50 dpi) · `analyze_deck.py --brief` instead of XML dumps · `preview`
gallery instead of test renders · fork agents for assets with fixed file names/sizes · one QA subagent pass ·
rebuild only after batching several fixes · never paste whole reports back to the user.
