"""Derive a new theme (decor folder + JSON) from an existing one in one command — no new drawing needed.

  python derive_theme.py --from medieval_pastoral --to wabi_sabi --colors wabi_colors.json \
      --paper EEE9E1:DED6CA --botanical-map "40-180:8E9282,230-330:C2B49C,330-360:B8A99A,0-30:B8A99A" --botanical-sat 0.7 \
      --ornament-tint 9C8F7E --seal-tint A0715A --frame rrect [--fonts head=..,body=..,latin=..] [--transitions t.json]

--colors: JSON of the 14 semantic colours (paper ink ink_soft primary primary_dk primary_lt accent accent2 extra line
line_lt card muted deep). Icons are re-tinted from the source theme: primary->colors.primary, accent->colors.accent.
Botanicals = branch/sprig/garland/floater files (hue remap); ornaments = ornament/bullet/node/divider/watermark/corner
files (tint); seal (tint). For motifs that must CHANGE shape (bamboo instead of olive…) render new art with
render_svg.py (or ask an agent, see references/assets.md) and drop it into the new folder with the same file name.
"""
import argparse, json, os, shutil, subprocess, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from recolor import recolor, parse_map

ap = argparse.ArgumentParser()
ap.add_argument('--from', dest='src', required=True); ap.add_argument('--to', dest='dst', required=True)
ap.add_argument('--colors', required=True); ap.add_argument('--paper', required=True, help='BASE:EDGE hex')
ap.add_argument('--botanical-map', default=''); ap.add_argument('--botanical-sat', type=float, default=1.0)
ap.add_argument('--botanical-light', type=float, default=1.0)
ap.add_argument('--ornament-tint'); ap.add_argument('--seal-tint'); ap.add_argument('--frame', default=None)
ap.add_argument('--fonts', nargs='*', default=[]); ap.add_argument('--transitions'); ap.add_argument('--name')
ap.add_argument('--description', default='')
a = ap.parse_args()
T = json.load(open(os.path.join(ROOT, 'themes', a.src + '.json'), encoding='utf8'))
sdir = os.path.join(ROOT, 'themes', T['asset_dir']); ddir = os.path.join(ROOT, 'themes', a.dst)
os.makedirs(os.path.join(ddir, 'icons'), exist_ok=True)
C = json.load(open(a.colors, encoding='utf8')) if os.path.exists(a.colors) else json.loads(a.colors)
base, edge = a.paper.split(':')
subprocess.run([sys.executable, os.path.join(HERE, 'paper.py'), os.path.join(ddir, 'paper.jpg'), '--base', base, '--edge', edge], check=True)
BOT = ('branch', 'corner_tl', 'sprig', 'garland', 'floater')
ORN = ('ornament', 'bullet', 'divider', 'watermark', 'corner_filigree', 'fleur')
mp = parse_map(a.botanical_map)
for f in sorted(os.listdir(sdir)):
    s, d = os.path.join(sdir, f), os.path.join(ddir, f)
    if not f.endswith('.png'):
        continue
    im = Image.open(s)
    if f.startswith(BOT):
        out = recolor(im, mapping=mp, sat=a.botanical_sat, light=a.botanical_light)
    elif f.startswith('node'):
        out = recolor(im, tint=C['primary'])
    elif f.startswith(ORN):
        out = recolor(im, tint=a.ornament_tint or C['line'])
    elif f.startswith('seal'):
        out = recolor(im, tint=a.seal_tint or C['accent2'])
    else:
        out = im
    out.save(d, optimize=True)
for f in sorted(os.listdir(os.path.join(sdir, 'icons'))):
    s, d = os.path.join(sdir, 'icons', f), os.path.join(ddir, 'icons', f)
    if f.endswith('_primary.png'):
        recolor(Image.open(s), tint=C['primary_dk']).save(d, optimize=True)
    elif f.endswith('_accent.png'):
        recolor(Image.open(s), tint=C['accent']).save(d, optimize=True)
    else:
        shutil.copy(s, d)
NT = dict(T)
NT.update(name=a.name or a.dst.replace('_', ' ').title(), description=a.description, asset_dir=a.dst, colors=C)
if a.frame:
    NT['frame'] = a.frame
if a.fonts:
    NT['fonts'] = dict(T['fonts'], **dict(x.split('=', 1) for x in a.fonts))
if a.transitions:
    NT['transitions'] = json.load(open(a.transitions, encoding='utf8')) if os.path.exists(a.transitions) else json.loads(a.transitions)
NT.pop('_dir', None)
json.dump(NT, open(os.path.join(ROOT, 'themes', a.dst + '.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=2)
print('theme ->', os.path.join(ROOT, 'themes', a.dst + '.json'), '+', ddir)
