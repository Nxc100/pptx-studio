"""Render procedural SVG decorations (watercolour botanicals / gold ornaments) to transparent PNGs.

  python render_svg.py botanical olive 1500 1000 OUT.png [--seed 11] [--colormap map.json] [--mirror]
  python render_svg.py ornament quatrefoil OUT.png [--colormap map.json]

botanical kinds (botanical.js build(kind,W,H,seed)): olive  lavender  rose  leaf1 leaf2 leaf3  petal1 petal2
ornament kinds  (ornament.js orn(kind)):             quatrefoil quatrefoil_small quatrefoil_small_olive divider
                                                     corner_filigree fleur wax_seal arch_window
--colormap: JSON {"#5E6B3D": "#2F4A3A", ...} applied to every hex colour in the SVG before rasterising
(cheap re-theming; the generators' main colours are listed in references/assets.md). For a NEW motif
(bamboo, ginkgo, eucalyptus, art-deco fan …) add a function to botanical.js/ornament.js following the same
watercolour filter recipe (feTurbulence + feDisplacementMap + layered translucent fills).
Output is trimmed to content with premultiplied-alpha downsampling (no fringe).
"""
import argparse, io, json, os, re
from PIL import Image, ImageOps
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('lib', choices=['botanical', 'ornament']); ap.add_argument('kind'); ap.add_argument('rest', nargs='+')
ap.add_argument('--seed', type=int, default=11); ap.add_argument('--colormap'); ap.add_argument('--mirror', action='store_true')
ap.add_argument('--rotate', type=float, default=0); ap.add_argument('--scale', type=float, default=2)
a = ap.parse_args()
js = open(os.path.join(HERE, a.lib + '.js'), encoding='utf8').read()
cmap = {k.upper(): v for k, v in json.load(open(a.colormap, encoding='utf8')).items()} if a.colormap else {}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1600, 'height': 1400}, device_scale_factor=a.scale)
    pg.set_content('<html><body style="margin:0;background:transparent"><div id="c"></div></body></html>')
    pg.add_script_tag(content=js)
    if a.lib == 'botanical':
        W, H, out = int(a.rest[0]), int(a.rest[1]), a.rest[2]
        svg = pg.evaluate(f"build('{a.kind}',{W},{H},{a.seed})")
    else:
        out = a.rest[0]
        r = pg.evaluate(f"orn('{a.kind}')"); svg, W, H = r['svg'], r['W'], r['H']
    if cmap:
        svg = re.sub(r'#[0-9A-Fa-f]{6}', lambda m: cmap.get(m.group(0).upper(), m.group(0)), svg)
    pg.set_viewport_size({'width': W + 20, 'height': H + 20})
    pg.evaluate("s=>{document.getElementById('c').innerHTML=s}", svg)
    png = pg.locator('#c svg').screenshot(omit_background=True)
    b.close()
im = Image.open(io.BytesIO(png)).convert('RGBA').convert('RGBa').resize((W, H), Image.LANCZOS).convert('RGBA')
if a.mirror:
    im = ImageOps.mirror(im)
if a.rotate:
    im = im.rotate(a.rotate, expand=True, resample=Image.BICUBIC)
bb = im.getchannel('A').point(lambda v: 255 if v > 6 else 0).getbbox()
if bb:
    im = im.crop(bb)
im.save(out, optimize=True)
print('saved', out, im.size)
