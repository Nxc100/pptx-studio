"""Vectorise a coloured floor plan into wall/column polygons + floor textures for plan3d.html.

  python prep_plan.py plan_cfg.json

plan_cfg.json (paths relative to the cfg file):
{
  "color_plan": "彩平图.png",            # coloured plan (walls drawn in one flat colour)
  "line_plan":  "平面布置图.png",        # optional, same pixel grid; used to find solid structural columns
  "wall_rgb": [181,163,136], "wall_tol": 22,          # sample the wall colour with photo_prep preview / a colour picker
  "column_rgb": [75,75,75],  "column_tol": 60,
  "bbox": [195,80,1175,1100],          # building area (excludes dimension lines)
  "footprint": [[200,180],[405,180], ...],   # optional outline polygon; omitted -> auto (closing + fill)
  "rooms": {"客厅": {"rect": [600,470,1040,800], "zone": "active", "label": [830,640]}, ...},
  "zone_colors": {"active": "E8B99A", "quiet": "B7C09F", "service": "E3CF9F"},
  "out": "plan_work"                   # writes plan_geo.json, floor_tex.png, floor_zones.png, debug_mask.png
}
Then render with render3d.py using configs {"page":"plan3d.html","name":"plan3d","geo":"plan_work/plan_geo.json",
"floor":"plan_work/floor_tex.png", ...} and the same with floor_zones.png (+ --same-trim).
Check debug_mask.png (red=walls, green=columns, blue=footprint) before rendering.
"""
import json, os, sys
import cv2, numpy as np
from PIL import Image

cfg_path = sys.argv[1]
base = os.path.dirname(os.path.abspath(cfg_path))
C = json.load(open(cfg_path, encoding='utf8'))
R = lambda p: os.path.join(base, p)
out = R(C.get('out', 'plan_work')); os.makedirs(out, exist_ok=True)
cp = np.array(Image.open(R(C['color_plan'])).convert('RGB')).astype(int)
H, W = cp.shape[:2]
bb = np.zeros((H, W), np.uint8)
x0, y0, x1, y1 = C.get('bbox', [0, 0, W, H]); bb[y0:y1, x0:x1] = 255
wall = ((np.abs(cp - np.array(C['wall_rgb'])).sum(-1) < C.get('wall_tol', 22)) * 255).astype(np.uint8)
wall = cv2.morphologyEx(cv2.bitwise_and(wall, bb), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(wall)
clean = np.zeros_like(wall)
for i in range(1, n):
    if st[i, 4] >= C.get('min_area', 150):
        clean[lab == i] = 255
colmask = np.zeros_like(clean)
if C.get('line_plan'):
    lp = np.array(Image.open(R(C['line_plan'])).convert('RGB')).astype(int)
    lp = np.pad(lp, ((0, max(0, H - lp.shape[0])), (0, max(0, W - lp.shape[1])), (0, 0)), constant_values=255)[:H, :W]
    col = ((np.abs(lp - np.array(C.get('column_rgb', [75, 75, 75]))).sum(-1) < C.get('column_tol', 60)) * 255).astype(np.uint8)
    col = cv2.bitwise_and(cv2.morphologyEx(col, cv2.MORPH_OPEN, np.ones((15, 15), np.uint8)), bb)
    n, lab, st, _ = cv2.connectedComponentsWithStats(col)
    for i in range(1, n):
        if st[i, 4] > 150:
            colmask[lab == i] = 255
wall_only = cv2.bitwise_and(clean, cv2.bitwise_not(cv2.dilate(colmask, np.ones((3, 3), np.uint8))))


def polys(mask, eps=1.2):
    cs, hier = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    res = []
    if hier is None:
        return res
    for i, c in enumerate(cs):
        if hier[0][i][3] != -1 or cv2.contourArea(c) < 40:
            continue
        holes, j = [], hier[0][i][2]
        while j != -1:
            if cv2.contourArea(cs[j]) >= 20:
                holes.append(cv2.approxPolyDP(cs[j], eps, True).reshape(-1, 2).tolist())
            j = hier[0][j][0]
        res.append({'outer': cv2.approxPolyDP(c, eps, True).reshape(-1, 2).tolist(), 'holes': holes})
    return res


if C.get('footprint'):
    FP = [tuple(p) for p in C['footprint']]
else:   # auto: close openings (doors/windows), fill holes, take the largest outline
    m = cv2.morphologyEx(cv2.bitwise_or(clean, colmask), cv2.MORPH_CLOSE, np.ones((45, 45), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    big = max(cs, key=cv2.contourArea)
    FP = [tuple(p) for p in cv2.approxPolyDP(big, 4, True).reshape(-1, 2).tolist()]
fp = np.zeros((H, W), np.uint8); cv2.fillPoly(fp, [np.array(FP, np.int32)], 255)
Image.fromarray(np.dstack([cp.astype(np.uint8), fp]), 'RGBA').save(os.path.join(out, 'floor_tex.png'))
rooms = C.get('rooms', {})
zc = {k: [int(v[i:i + 2], 16) for i in (0, 2, 4)] for k, v in C.get('zone_colors', {}).items()}
if rooms and zc:
    zl = np.zeros((H, W, 3), float); zm = np.zeros((H, W), bool)
    for name, r in sorted(rooms.items(), key=lambda kv: -(kv[1]['rect'][2] - kv[1]['rect'][0]) * (kv[1]['rect'][3] - kv[1]['rect'][1])):
        if r.get('zone') in zc:
            a, b, c, d = r['rect']; zl[b:d, a:c] = zc[r['zone']]; zm[b:d, a:c] = True
    tex = 0.5 * cp + 0.5 * cp.mean(-1, keepdims=True)
    mix = np.where(zm[..., None], 0.35 * tex + 0.65 * zl, cp * 0.85 + np.array([239, 227, 204]) * 0.15)
    Image.fromarray(np.dstack([mix.clip(0, 255).astype(np.uint8), fp]), 'RGBA').save(os.path.join(out, 'floor_zones.png'))
labels = {k: (v.get('label') or [(v['rect'][0] + v['rect'][2]) / 2, (v['rect'][1] + v['rect'][3]) / 2]) for k, v in rooms.items()}
json.dump({'W': W, 'H': H, 'footprint': FP, 'walls': polys(wall_only), 'columns': polys(colmask, 0.8), 'labels': labels},
          open(os.path.join(out, 'plan_geo.json'), 'w', encoding='utf8'), ensure_ascii=False)
Image.fromarray(np.dstack([clean, colmask, fp // 3])).save(os.path.join(out, 'debug_mask.png'))
print('walls', len(polys(wall_only)), 'columns', len(polys(colmask, 0.8)), '->', out)
