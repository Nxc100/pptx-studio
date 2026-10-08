"""Render an HTML composition (exhibition board, poster, infographic, cover art) to a high-res image.

  python render_html.py TEMPLATE.html OUT.jpg --theme medieval_pastoral --assets PROJECT_ASSETS
                        [--w 1682 --h 1188] [--scale 2.952]   # A1 landscape @150dpi = 4965x3507

Placeholders filled before rendering: {{ASSETS}} {{THEME}} {{C.<palette name>}} {{F.head|body|latin}}.
Copy templates/board_a1.html into the project, edit its text/images, then render.  Scale guide:
2.5 → 4205px (screen/slide), 2.952 → A1@150dpi (print), 4.0 → A1@200dpi.
"""
import argparse, json, os, pathlib, re, tempfile
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
ap = argparse.ArgumentParser()
ap.add_argument('template'); ap.add_argument('out')
ap.add_argument('--theme', default='medieval_pastoral'); ap.add_argument('--assets', default='.')
ap.add_argument('--w', type=int, default=1682); ap.add_argument('--h', type=int, default=1188)
ap.add_argument('--scale', type=float, default=2.5); ap.add_argument('--quality', type=int, default=92)
a = ap.parse_args()
tp = pathlib.Path(a.theme)
if not tp.exists():
    tp = ROOT / 'themes' / (a.theme if a.theme.endswith('.json') else a.theme + '.json')
T = json.loads(tp.read_text(encoding='utf8'))
theme_dir = (tp.parent / T.get('asset_dir', '')).resolve()
html = pathlib.Path(a.template).read_text(encoding='utf8')
html = html.replace('{{ASSETS}}', pathlib.Path(a.assets).resolve().as_uri()).replace('{{THEME}}', theme_dir.as_uri())
html = re.sub(r'\{\{C\.(\w+)\}\}', lambda m: '#' + T['colors'].get(m.group(1), '888888'), html)
html = re.sub(r'\{\{F\.(\w+)\}\}', lambda m: T['fonts'].get(m.group(1), 'serif'), html)
tmp = pathlib.Path(tempfile.mkdtemp()) / 'page.html'
tmp.write_text(html, encoding='utf8')
png = str(pathlib.Path(a.out).with_suffix('.png'))
with sync_playwright() as p:
    b = p.chromium.launch(args=['--allow-file-access-from-files'])
    pg = b.new_page(viewport={'width': a.w, 'height': a.h}, device_scale_factor=a.scale)
    pg.goto(tmp.as_uri()); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(800)
    pg.screenshot(path=png)
    b.close()
if not a.out.lower().endswith('.png'):
    im = Image.open(png).convert('RGB'); im.save(a.out, quality=a.quality, dpi=(150, 150)); os.remove(png)
print('saved', a.out, Image.open(a.out).size)
