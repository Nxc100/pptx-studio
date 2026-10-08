"""Line icons (lucide) -> 256px transparent PNGs in theme colours.

  python icons.py OUT_DIR --colors primary=5E6B3D light=FFFFFF accent=B0623A [--names user,sun,...] [--stroke 1.75]

Writes OUT_DIR/<name>_<variant>.png (the naming Deck.icon() expects). SVGs are cached in OUT_DIR/_svg
(downloaded from unpkg lucide-static on first use; needs network once). Default name list = the 46 icons
used by the archetypes + common extras. Browse names at https://lucide.dev/icons
"""
import argparse, os, re, urllib.request
from playwright.sync_api import sync_playwright

DEFAULT = ('user users baby book-open piano flower-2 flower coffee sun cloud-rain droplets thermometer wind train-front '
           'landmark graduation-cap hospital trees home ruler palette sofa bed-double utensils-crossed bath shirt door-open '
           'armchair lamp-ceiling map-pin compass layers sparkles leaf heart car school shopping-bag footprints route sprout '
           'gem brick-wall castle church wheat lightbulb target trending-up chart-column calendar clock award star '
           'building-2 store briefcase mountain waves tree-pine')

ap = argparse.ArgumentParser()
ap.add_argument('out'); ap.add_argument('--colors', nargs='+', default=['primary=5E6B3D', 'light=FFFFFF', 'accent=B0623A'])
ap.add_argument('--names', default=DEFAULT.replace(' ', ',')); ap.add_argument('--stroke', default='1.75')
ap.add_argument('--size', type=int, default=256)
a = ap.parse_args()
cols = dict(c.split('=') for c in a.colors)
cache = os.path.join(a.out, '_svg'); os.makedirs(cache, exist_ok=True)
names = [n.strip() for n in a.names.split(',') if n.strip()]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': a.size + 40, 'height': a.size + 40})
    for n in names:
        f = os.path.join(cache, n + '.svg')
        if not os.path.exists(f):
            try:
                urllib.request.urlretrieve(f'https://unpkg.com/lucide-static@latest/icons/{n}.svg', f)
            except Exception as e:
                print('skip', n, e); continue
        svg = open(f, encoding='utf8').read()
        svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S)
        svg = re.sub(r'width="24"', f'width="{a.size}"', svg, count=1)
        svg = re.sub(r'height="24"', f'height="{a.size}"', svg, count=1)
        svg = re.sub(r'stroke-width="[0-9.]+"', f'stroke-width="{a.stroke}"', svg)
        for var, hx in cols.items():
            pg.set_content(f'<html><body style="margin:0;background:transparent">{svg.replace("currentColor", "#" + hx.lstrip("#"))}</body></html>')
            pg.locator('svg').first.screenshot(path=os.path.join(a.out, f'{n}_{var}.png'), omit_background=True)
    b.close()
print('icons ->', a.out)
