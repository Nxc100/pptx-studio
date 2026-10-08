"""Paper / parchment background texture (2667x1500 = 13.33in @200dpi).

  python paper.py OUT.jpg --base F4EDE0 --edge E9DDC7 [--fibres 5200] [--mottle 1.0] [--seed 7]

base = centre colour, edge = vignette colour (slightly darker/warmer). Keep it calm: text sits on it.
Recipes: parchment F4EDE0/E9DDC7 · rice paper F5F2EA/E8E2D4 · linen EEE8DF/DED5C6 · sage D9DCC8/CCD0BA ·
         warm grey EAE6E0/D9D3CB · dark slate 2B2F33/1F2226 (use --mottle 0.6 --fibres 1500 for dark)
"""
import argparse
import numpy as np, cv2
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('out'); ap.add_argument('--base', default='F4EDE0'); ap.add_argument('--edge', default='E9DDC7')
ap.add_argument('--w', type=int, default=2667); ap.add_argument('--h', type=int, default=1500)
ap.add_argument('--fibres', type=int, default=5200); ap.add_argument('--mottle', type=float, default=1.0)
ap.add_argument('--grain', type=float, default=1.6); ap.add_argument('--seed', type=int, default=7)
a = ap.parse_args()
W, H = a.w, a.h
hx = lambda s: np.array([int(s[i:i + 2], 16) for i in (0, 2, 4)], np.float32)
rng = np.random.default_rng(a.seed)


def noise(scale, seed):
    r = np.random.default_rng(seed)
    n = r.standard_normal((max(2, int(H / scale)), max(2, int(W / scale)))).astype(np.float32)
    n = cv2.GaussianBlur(cv2.resize(n, (W, H), interpolation=cv2.INTER_CUBIC), (0, 0), scale * 0.35 + 0.5)
    return n / (n.std() + 1e-6)


mott = 0.55 * noise(380, a.seed + 1) + 0.35 * noise(160, a.seed + 2) + 0.25 * noise(60, a.seed + 3)
grain = cv2.GaussianBlur(rng.standard_normal((H, W)).astype(np.float32), (0, 0), 0.7); grain /= grain.std()
fib = np.zeros((H, W), np.float32)
for _ in range(a.fibres):
    x, y = rng.uniform(0, W), rng.uniform(0, H); L = rng.uniform(8, 40)
    ang = rng.normal(0, 0.35) if rng.random() < 0.6 else rng.uniform(0, np.pi)
    cv2.line(fib, (int(x), int(y)), (int(x + L * np.cos(ang)), int(y + L * np.sin(ang))),
             float(rng.choice([-1, 1]) * rng.uniform(0.4, 1.0)), 1, cv2.LINE_AA)
fib = cv2.GaussianBlur(fib, (0, 0), 0.6)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 * 0.85 + ((yy - H / 2) / (H / 2)) ** 2)
vig = np.clip((d - 0.45) / 0.75, 0, 1) ** 1.6
base, edge = hx(a.base), hx(a.edge)
img = base[None, None] * (1 - vig[..., None]) + edge[None, None] * vig[..., None]
dark = base.mean() < 100
sign = 1 if dark else -1
img += sign * mott[..., None] * np.array([2.6, 3.0, 4.2], np.float32) * 0.9 * a.mottle
img += grain[..., None] * a.grain
img += sign * fib[..., None] * np.array([6.5, 7.0, 8.0], np.float32)
Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(a.out, quality=88, optimize=True)
print('saved', a.out)
