"""Recolour transparent PNG decorations (botanicals, ornaments, seals, icons) to a new palette —
the cheapest way to derive a new theme's decorations from an existing theme folder.

  # luminance-preserving tint (best for line art / gold ornaments / single-colour icons)
  python recolor.py in.png out.png --tint 2F4A3A
  # hue-range remap (best for multi-colour watercolours): greens->moss, purples->dusty blue
  python recolor.py in.png out.png --map "60-170:7A7F5A,230-320:8C9BB0" [--sat 0.8] [--light 1.05]
  # whole folder (keeps file names)
  python recolor.py themes/medieval_pastoral themes/my_theme --map "..." --only "*.png"

Hue ranges are degrees 0-360 (red 0, yellow 60, green 120, cyan 180, blue 240, magenta 300).
Pixels outside every range are only affected by --sat/--light.  Alpha is preserved.
"""
import argparse, fnmatch, os, shutil
import numpy as np
from PIL import Image


def hex2rgb(h):
    h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255


def rgb2hsv(a):
    import colorsys
    return np.array(colorsys.rgb_to_hsv(*a))


def recolor(im, tint=None, mapping=None, sat=1.0, light=1.0):
    import cv2
    rgba = np.asarray(im.convert('RGBA')).astype(np.float32) / 255
    rgb, al = rgba[..., :3], rgba[..., 3:]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)          # H 0..360, S 0..1, V 0..1
    if tint:
        # colorize: map the image's mean luminance onto the target colour, keep relative light/dark variation
        t = hex2rgb(tint); wts = np.array([0.299, 0.587, 0.114], np.float32)
        lum = rgb @ wts; tl = float(t @ wts)
        mean_l = float((lum * al[..., 0]).sum() / max(al[..., 0].sum(), 1e-6))
        L = np.clip(lum * tl / max(mean_l, 1e-3), 0, 1)[..., None]
        rgb = np.where(L <= tl, t * (L / max(tl, 1e-3)), t + (1 - t) * ((L - tl) / max(1 - tl, 1e-3)))
    else:
        for (h0, h1), hx in (mapping or []):
            th, ts, tv = rgb2hsv(hex2rgb(hx)); th *= 360
            m = (hsv[..., 0] >= h0) & (hsv[..., 0] <= h1) & (hsv[..., 1] > 0.06)
            src = hsv[m]
            if len(src) == 0:
                continue
            ms, mv = max(src[:, 1].mean(), 1e-3), max(src[:, 2].mean(), 1e-3)
            src[:, 0] = th + (src[:, 0] - (h0 + h1) / 2) * 0.15      # keep a little of the original hue variation
            src[:, 1] = np.clip(src[:, 1] * ts / ms, 0, 1)
            src[:, 2] = np.clip(src[:, 2] * tv / mv, 0, 1)
            hsv[m] = src
        hsv[..., 0] %= 360
        rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    if sat != 1.0 or light != 1.0:
        hsv = cv2.cvtColor(np.clip(rgb, 0, 1).astype(np.float32), cv2.COLOR_RGB2HSV)
        hsv[..., 1] = np.clip(hsv[..., 1] * sat, 0, 1); hsv[..., 2] = np.clip(hsv[..., 2] * light, 0, 1)
        rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    out = np.concatenate([np.clip(rgb, 0, 1), al], -1)
    return Image.fromarray((out * 255).round().astype(np.uint8), 'RGBA')


def parse_map(s):
    out = []
    for part in (s or '').split(','):
        if part.strip():
            r, hx = part.split(':'); a, b = r.split('-'); out.append(((float(a), float(b)), hx))
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('dst')
    ap.add_argument('--tint'); ap.add_argument('--map'); ap.add_argument('--sat', type=float, default=1.0)
    ap.add_argument('--light', type=float, default=1.0); ap.add_argument('--only', default='*.png')
    a = ap.parse_args()
    mp = parse_map(a.map)
    if os.path.isdir(a.src):
        for root, _, files in os.walk(a.src):
            for f in files:
                s = os.path.join(root, f); d = os.path.join(a.dst, os.path.relpath(s, a.src))
                os.makedirs(os.path.dirname(d), exist_ok=True)
                if fnmatch.fnmatch(f, a.only):
                    recolor(Image.open(s), a.tint, mp, a.sat, a.light).save(d, optimize=True)
                elif not os.path.exists(d):
                    shutil.copy(s, d)
        print('done', a.dst)
    else:
        recolor(Image.open(a.src), a.tint, mp, a.sat, a.light).save(a.dst, optimize=True)
        print('saved', a.dst)
