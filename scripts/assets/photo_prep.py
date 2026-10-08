"""Prepare project photos (renders, plans, materials) for the deck.

  python photo_prep.py convert SRC_DIR OUT_DIR [--map map.json] [--max 2000]
        -> RGBA->RGB, JPEG q92 (plans/drawings stay PNG), optional rename map {"客厅效果图角度1.jpg": "living1"}
  python photo_prep.py preview OUT_DIR PREVIEW_DIR
        -> each photo with a 100px coordinate grid (labels = source pixels) for picking crop boxes cheaply
  python photo_prep.py crops OUT_DIR crops.json CROPS_DIR [--w 600]
        -> crops.json: {"chandelier": ["living2.jpg", [820,0,1220,533]], ...}  (portrait 3:4 suits arch frames)
  python photo_prep.py palette OUT_DIR [--k 12]
        -> k-means colours over all photos (hex + share) to seed the colour-analysis slide
  python photo_prep.py sheet DIR OUT.jpg   -> contact sheet of every image in DIR (one look instead of many)
"""
import argparse, glob, json, os
from PIL import Image, ImageDraw, ImageFont

IMG = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')


def font(sz):
    for f in ('C:/Windows/Fonts/msyh.ttc', 'arial.ttf', '/System/Library/Fonts/PingFang.ttc'):
        try:
            return ImageFont.truetype(f, sz)
        except Exception:
            pass
    return None


def convert(a):
    mp = json.load(open(a.map, encoding='utf8')) if a.map else {}
    os.makedirs(a.out, exist_ok=True)
    for f in sorted(os.listdir(a.src)):
        if not f.lower().endswith(IMG):
            continue
        im = Image.open(os.path.join(a.src, f))
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA'); bg = Image.new('RGB', im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[-1]); im = bg
        else:
            im = im.convert('RGB')
        if max(im.size) > a.max:
            im.thumbnail((a.max, a.max), Image.LANCZOS)
        name = mp.get(f, os.path.splitext(f)[0])
        drawing = any(k in f for k in ('平面', '立面', '剖面', 'plan', 'elev')) or name.startswith('plan')
        out = os.path.join(a.out, name + ('.png' if drawing else '.jpg'))
        im.save(out, optimize=True) if drawing else im.save(out, quality=92)
        print(f, '->', os.path.basename(out), im.size)


def preview(a):
    os.makedirs(a.preview, exist_ok=True); ft = font(28)
    for f in sorted(glob.glob(os.path.join(a.out, '*'))):
        if not f.lower().endswith(IMG):
            continue
        g = Image.open(f).convert('RGB'); d = ImageDraw.Draw(g)
        for x in range(0, g.width, 100):
            d.line([(x, 0), (x, g.height)], fill=(255, 0, 0) if x % 500 == 0 else (255, 160, 160), width=2 if x % 500 == 0 else 1)
        for y in range(0, g.height, 100):
            d.line([(0, y), (g.width, y)], fill=(255, 0, 0) if y % 500 == 0 else (255, 160, 160), width=2 if y % 500 == 0 else 1)
        for x in range(0, g.width, 200):
            for y in range(0, g.height, 200):
                d.text((x + 3, y + 3), f'{x},{y}', fill=(255, 255, 0), font=ft)
        g.thumbnail((1100, 1100)); g.save(os.path.join(a.preview, os.path.basename(f).rsplit('.', 1)[0] + '.jpg'), quality=80)
    print('previews ->', a.preview)


def crops(a):
    os.makedirs(a.crops_dir, exist_ok=True)
    for k, (src, box) in json.load(open(a.spec, encoding='utf8')).items():
        im = Image.open(os.path.join(a.out, src)).convert('RGB')
        box = [max(0, box[0]), max(0, box[1]), min(im.width, box[2]), min(im.height, box[3])]   # never pad with black
        c = im.crop(box); c = c.resize((a.w, int(a.w * c.height / c.width)), Image.LANCZOS)
        c.save(os.path.join(a.crops_dir, k + '.jpg'), quality=92); print(k, box)


def palette(a):
    import numpy as np, cv2
    px = [np.array(Image.open(f).convert('RGB').resize((300, 220))).reshape(-1, 3) for f in glob.glob(os.path.join(a.out, '*.jpg'))]
    X = np.concatenate(px).astype(np.float32)
    _, lab, cen = cv2.kmeans(X, a.k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.5), 5, cv2.KMEANS_PP_CENTERS)
    cnt = np.bincount(lab.ravel())
    for i in np.argsort(-cnt):
        print('%02X%02X%02X' % tuple(cen[i].astype(int)), f'{cnt[i] / len(X) * 100:.1f}%')


def sheet(a):
    fs = [f for f in sorted(glob.glob(os.path.join(a.dir, '*'))) if f.lower().endswith(IMG)]
    W, Hh, cols = 420, 340, 4; rows = (len(fs) + cols - 1) // cols; ft = font(18)
    g = Image.new('RGB', (cols * (W + 10) + 10, rows * (Hh + 34) + 10), 'white'); d = ImageDraw.Draw(g)
    for i, f in enumerate(fs):
        im = Image.open(f).convert('RGB'); im.thumbnail((W, Hh)); r, c = divmod(i, cols)
        x, y = 10 + c * (W + 10), 10 + r * (Hh + 34)
        d.text((x, y), os.path.basename(f), fill='red', font=ft); g.paste(im, (x, y + 26))
    g.save(a.out_img, quality=85); print('sheet ->', a.out_img)


ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd', required=True)
p = sp.add_parser('convert'); p.add_argument('src'); p.add_argument('out'); p.add_argument('--map'); p.add_argument('--max', type=int, default=2000)
p = sp.add_parser('preview'); p.add_argument('out'); p.add_argument('preview')
p = sp.add_parser('crops'); p.add_argument('out'); p.add_argument('spec'); p.add_argument('crops_dir'); p.add_argument('--w', type=int, default=600)
p = sp.add_parser('palette'); p.add_argument('out'); p.add_argument('--k', type=int, default=12)
p = sp.add_parser('sheet'); p.add_argument('dir'); p.add_argument('out_img')
a = ap.parse_args()
{'convert': convert, 'preview': preview, 'crops': crops, 'palette': palette, 'sheet': sheet}[a.cmd](a)
