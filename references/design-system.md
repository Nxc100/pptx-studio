# Design system: theme schema + style recipes

## Theme JSON (`themes/<name>.json`, decor in `themes/<asset_dir>/`)

```json
{
  "name": "Medieval Pastoral", "description": "…", "asset_dir": "medieval_pastoral",
  "colors": {"paper","ink","ink_soft","primary","primary_dk","primary_lt","accent","accent2","extra",
             "line","line_lt","card","muted","deep"},          // 6-digit hex, no '#'
  "fonts": {"head": "Noto Serif SC", "body": "Microsoft YaHei", "latin": "Palatino Linotype"},
  "frame": "arch",                     // arch | rrect | pill | plaque | oval | snip | octagon | rect
  "deco": {"paper","corner_tl","branch_tr","sprig_br","garland","ornament","bullet","node","divider","seal",
           "watermark","floaters":[…]},  // file names in asset_dir; any may be omitted (skipped silently)
  "icons": {"dir": "icons", "primary": "primary", "light": "light", "accent": "accent"},
  "text": {"pill": "INTERIOR  DESIGN", "part_word": "The Part", "folio": "— {n:02d} —"},
  "transitions": {"cover": [kind, ms, {attrs}], "contents", "section", "content", "gallery", "board", "end"}
}
```
Role of each colour: `paper` slide/board background · `ink` main text · `ink_soft` body text · `primary` badges, pills,
dark cards · `primary_dk` titles · `primary_lt` chart bars · `accent` numbers, highlights, pins · `accent2` deep accent
(entry marker, 3rd pillar) · `extra` 3rd persona / soft accent · `line` thin frames, ornaments, captions · `line_lt`
grid lines, light text on dark cards · `card` card fill (70% alpha) · `muted` giant chapter numbers · `deep` dark label.

Decor roles: `corner_tl` small sprig top-left of every content slide (≈2.1 in wide, mostly off-canvas) ·
`branch_tr` large spray hanging into cover/section/thanks top-right · `sprig_br` upright bunch bottom-right/left ·
`garland` horizontal vine near the cover photo base · `ornament` big faint outline motif (quatrefoil/cloud/fan) ·
`bullet` small solid motif for list bullets · `node` solid motif for contents nodes / response bullets ·
`divider` ornamental rule · `seal` stamp near titles (wax seal / 印章 / monogram) · `watermark` faint line drawing ·
`floaters` 2–3 small falling leaves/petals on section slides.

Fonts: Chinese headings need a serif with weights (Noto Serif SC / 思源宋体 is free; check with
`check_deck.py --fonts`). Body: Microsoft YaHei (always on Windows). Latin display: Palatino Linotype / Georgia /
Cambria. LibreOffice renders exactly when the fonts are installed — otherwise QA previews lie.

Transition kinds: `fade` · `p14:<vortex|switch|flip|ripple|honeycomb|prism|doors|window|ferris|gallery|conveyor|pan|glitter|warp|flythrough|flash|shred|reveal|wheelReverse>`
(attrs like `{"dir":"l"}`) · `p15:<curtains|drape|wind|prestige|fracture|crush|peelOff|pageCurlDouble|pageCurlSingle|airplane|origami>`.
All get a `p:fade` fallback for old PowerPoint/WPS.

## Style recipes (palette = paper / ink / primary / primary_dk / accent / line; frame; motifs; transitions)

| style | palette | frame | decor motifs (derive or draw) | transitions |
|---|---|---|---|---|
| 欧洲中世纪田园 Medieval pastoral *(shipped)* | F4EDE0 / 3B2E25 / 5E6B3D / 4A5530 / B0623A / B08D57 | arch | olive branch, lavender, rose vine, quatrefoil, fleur-de-lis, wax seal | curtains · page curl · gallery |
| 侘寂 Wabi-sabi *(shipped, derived)* | EEE9E1 / 2F2B27 / 7A7266 / 3F3A34 / A0715A / 9C8F7E | rrect | dry branch, pampas, ensō circle, clay stamp | drape · reveal · pan |
| 新中式 New Chinese | F3EFE6 / 2B2622 / 3E5C55 (黛青) / 263B36 / A23B2C (朱砂) / B39B6B | plaque or oval | 竹/梅/海棠框 (cloud prst), 回纹 divider, 印章 seal, 祥云 watermark | fade · reveal · wind |
| 北欧极简 Nordic | F6F5F2 / 26292C / 5F7A76 / 3D4F4C / D08C60 / B9B4AA | rrect | eucalyptus sprig, line-art dots, no seal | fade · pan · push-like `p14:conveyor` |
| 法式复古 French vintage | F5EEE6 / 3A2E2E / 8C6A7A (dusty mauve) / 5E4452 / C9A15A / C8B08A | arch / oval | peony, ribbon bow, rococo cartouche, monogram seal | curtains · prestige · gallery |
| 现代轻奢 Modern luxe | F3F1EE / 1F1F1F / 2E3A3F / 15191B / C2A06B (champagne) / B9A27A | rect / snip | thin gold lines, marble texture paper, geometric ornament | fade · prism · gallery |
| 工业风 Industrial loft | E9E6E1 / 1E1E1E / 4B4F52 / 2A2D2F / B5642F (rust) / 8A8A86 | rect | concrete paper, rivet dots, blueprint grid watermark | fade · vortex(sparingly) · pan |
| 日式原木 Japanese natural | F4F0E8 / 2E2A25 / 8A7356 / 5B4A36 / 6E7F5C / B9A78A | rrect | maple/ginkgo leaves, noren stripe, round 印 | fade · reveal · pan |

Recipe use: `derive_theme.py` with the palette (fill the other 8 colours by lightening/darkening), `--paper` from the
paper recipes in `paper.py`, a `--botanical-map` that moves greens/purples/pinks to the new hues, `--frame`. When the
motif shape must change (bamboo for 新中式), render/draw new `branch_tr/corner_tl/sprig` art and keep the file names.
Also re-render 3D maps with a matching `palette` in the map configs.

## Layout constants (keep consistent)
Margins 0.5–0.95 in · title at (1.45, 0.34) 26 pt bold primary_dk · English caption 9.5 pt italic line, spacing 2.6 ·
body 10.5–13 pt ink_soft, line 1.3–1.45 · card gap 0.2–0.35 in · folio bottom-right 9.5 pt · content images get
a 0.1–0.17 in offset frame in `line` colour + soft shadow.
