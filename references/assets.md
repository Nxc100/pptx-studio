# Assets: photos, decor, icons, 3D, boards

Run everything with `PYTHONIOENCODING=utf-8`. `S` = skill dir. Project layout used by specs:
```
project/assets/photos/*.jpg|png   (converted renders, plans, material textures)
project/assets/crops/*.jpg        (detail crops, 600px wide; 3:4 for frames, square for circles)
project/assets/3d/*.png + *_meta.json
project/assets/board/board.jpg
```

## Photos
```
python S/scripts/assets/photo_prep.py sheet  素材 sheet.jpg                 # one look at everything
python S/scripts/assets/photo_prep.py convert 素材 assets/photos --map names.json   # {"客厅效果图角度1.jpg":"living1",...}
python S/scripts/assets/photo_prep.py preview assets/photos previews        # grid-labelled copies to pick crop boxes
python S/scripts/assets/photo_prep.py crops assets/photos crops.json assets/crops
python S/scripts/assets/photo_prep.py palette assets/photos                 # k-means colours for the palette slide
```
Crop ideas per render: chandelier/ceiling, arch/door, window, fabric close-up, shelf/joinery, lamp, chair, floor
(for material "application" circles), wall finish. Keep crop boxes inside the image (script clamps, but check).
Plans with dimension text clipped at the edge: crop 10–15 px off and pass `offset=(n, n)` in the spec.

## Theme decor
* Derive from an existing theme: `derive_theme.py` (see design-system.md) — recolours botanicals by hue ranges,
  tints ornaments/seal/node, re-tints icons, generates paper. ~1 minute, no drawing.
* Paper only: `paper.py OUT.jpg --base F4EDE0 --edge E9DDC7`.
* Recolour single files: `recolor.py in.png out.png --tint HEX` or `--map "60-170:HEX,230-320:HEX"`.
* Procedural SVG (watercolour): `render_svg.py botanical olive 1500 1000 out.png [--mirror] [--colormap map.json]`
  kinds olive/lavender/rose/leaf1-3/petal1-2; `render_svg.py ornament quatrefoil out.png` kinds quatrefoil,
  quatrefoil_small(_olive), divider, corner_filigree, fleur, wax_seal, arch_window.
  Main hex colours inside the generators (for `--colormap`): leaves 5E6B3D 6F7B4A 7E8A5C 8C9673 9AA483 56603A A7AE90;
  stems 6E5E40 76664A 6E6040; olives 3F3542 4B3E4E; lavender 8E7BAA B3A4C8 7A6898 9D8BBA; roses D6A39A C98E84 E3BDB1 B9776E;
  ribbon C98E84 A9685F; gold gradient 9A7644 C6A66B B08D57 D4BA85 977341; olive fill 55613A 5E6B3D 6C7A48; wax A9503F 8E3B2E 6A2720.
* Icons: `icons.py THEME_DIR/icons --colors primary=HEX light=FFFFFF accent=HEX [--names a,b,c]` (lucide, cached).

## 3D maps (three.js, `scripts/three/render3d.py`)
GeoJSON for China admin areas: `https://geo.datav.aliyun.com/areas_v3/bound/<adcode>_full.json` (children) or
`<adcode>.json` (outline). Country 100000, province e.g. 510000, city 510100, district 510107.
Map config keys (`page: map3d.html`): `name, geojson, highlight (adcode), groups {adcode: hex} (mid tier),
heights {base, group, highlight, slab}, pin (bool), pin_scale, special_contains ("JD" = China nine-dash line),
slab (bool, single region as thick block), pois [[name, lat, lon]], palette {regions[], side, edge, hl_top, hl_side,
hl_edge, group_side, pin, pole, slab_top, slab_side, slab_edge, special}, camera {elev, azim, fov, zoom},
light {hemi, sun}, size [w,h], dpr`. Output `<name>.png` (transparent, trimmed) + `<name>_meta.json`
(`labels` region centres, `pins` pin heads, in final PNG pixels) — used directly by `location_levels`/`poi_map`.
Example configs: `examples/ba_wujie/three/map_*.json`.
```
python S/scripts/three/render3d.py assets/3d three/map_china.json three/map_sichuan.json three/map_chengdu.json three/map_wuhou.json
```
Verify POIs fall inside the polygon (shapely or a quick point-in-polygon) and say "示意位置" — coordinates are approximate.

## 3D floor plan
1. `prep_plan.py three/plan_cfg.json` — wall colour sampled from the 彩平图 (e.g. 181,163,136), columns from the line
   plan, rooms {rect, zone, label}, zone colours → `plan_work/plan_geo.json`, `floor_tex.png`, `floor_zones.png`,
   `debug_mask.png` (check it: red walls, green columns, blue footprint).
2. `render3d.py assets/3d three/plan3d.json three/plan3d_zones.json --same-trim` (identical camera + trim so labels
   match), optional `plan3d_hero.json` (low warm angle for a section image).
Keys (`page: plan3d.html`): `geo, floor, wall_h (80 ≈ 1.1 m cut-away), low_walls_x_gt (railings), hero,
camera {elev, azim, fov, dist, tx, tz}, colors {slab_top, slab_side, cap, wall, col_cap, col_side, edge}, size`.

## Exhibition board / posters
Copy `templates/board_a1.html` (3-column A1 grid, CSS vars from theme), edit text/images, then
`python S/scripts/board/render_html.py board.html assets/board/board.jpg --theme <t> --assets assets --scale 2.5`
(slide image) and `--scale 2.952` for A1@150 dpi print file.

## Fork-agent prompts (run in parallel while you write the spec)
**3D fork** — "Render with `S/scripts/three/render3d.py`: (1) maps for adcodes … highlight …, pin on …; slab map of
… with POIs [name, lat, lon]… (check inside polygon, report outliers); (2) prep_plan + plan3d/plan3d_zones
(--same-trim) [+ hero] from <彩平图> / <平面布置图>, wall colour …, rooms …. Palette = theme <t>. Outputs to
`assets/3d/`. Look at every PNG, iterate camera/heights until clean (no clipping, soft shadows, transparent bg).
Report file sizes and meta keys only."
**Decor fork** (only if the theme is new and needs new shapes) — "Create in `themes/<t>/`: paper.jpg (paper.py
recipe …), corner_tl.png, branch_tr.png, sprig.png, garland.png, floater1-3.png (motif: …, watercolour, transparent,
premultiplied edges), ornament/bullet/node/divider/seal/watermark (line motif: …, colour …), icons (icons.py
colours …). Extend botanical.js/ornament.js for new shapes. View every PNG composited on the paper; fix halos."
**Board fork** — "Fill templates/board_a1.html for <project> with assets …, render at 2.5 and 2.952, check overlaps."
