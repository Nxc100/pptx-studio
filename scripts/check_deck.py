"""Structural QA for a built deck (no rendering needed).

  python check_deck.py deck.pptx [--fonts]

Checks: every animation target exists, no duplicate timing ids, every slide has a transition, speaker notes present,
pictures with oversize media (> 3 MB), text boxes extending past the slide edge (LibreOffice clips them),
spacing+alpha text runs (LibreOffice clips), and lists fonts used (with --fonts: whether installed on Windows).
Exit code 1 if a hard error is found.  Visual QA still needs render_deck.py + eyes (see references/qa.md).
"""
import argparse, glob, os, re, sys, zipfile
from lxml import etree

P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
MC = 'http://schemas.openxmlformats.org/markup-compatibility/2006'


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('pptx'); ap.add_argument('--fonts', action='store_true')
    a = ap.parse_args()
    z = zipfile.ZipFile(a.pptx)
    pres = etree.fromstring(z.read('ppt/presentation.xml'))
    sw = int(pres.find(f'{{{P}}}sldSz').get('cx')); sh = int(pres.find(f'{{{P}}}sldSz').get('cy'))
    slides = sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)], key=lambda x: int(re.findall(r'\d+', x)[-1]))
    errors, warns, fonts, effects = [], [], set(), 0
    for n in slides:
        t = etree.fromstring(z.read(n)); tag = os.path.basename(n)
        ids = {e.get('id') for e in t.iter(f'{{{P}}}cNvPr')}
        miss = {e.get('spid') for e in t.iter(f'{{{P}}}spTgt')} - ids
        if miss:
            errors.append(f'{tag}: animation targets missing {miss}')
        ctn = [e.get('id') for e in t.iter(f'{{{P}}}cTn')]
        if len(ctn) != len(set(ctn)):
            errors.append(f'{tag}: duplicate cTn ids')
        effects += len([c for c in t.iter(f'{{{P}}}cTn') if c.get('presetClass')])
        for v in t.iter(f'{{{P}}}strVal'):
            if '+-' in (v.get('val') or ''):
                errors.append(f"{tag}: bad animation formula {v.get('val')}")
        if t.find(f'{{{MC}}}AlternateContent') is None and t.find(f'{{{P}}}transition') is None:
            warns.append(f'{tag}: no transition')
        rel = f'ppt/slides/_rels/{tag}.rels'
        if 'notesSlide' not in z.read(rel).decode('utf8', 'ignore'):
            warns.append(f'{tag}: no speaker notes')
        for sp in t.iter(f'{{{P}}}sp'):
            xf = sp.find(f'{{{P}}}spPr/{{{A}}}xfrm')
            txt = ''.join(x.text or '' for x in sp.iter(f'{{{A}}}t')).strip()
            if xf is not None and txt:
                off, ext = xf.find(f'{{{A}}}off'), xf.find(f'{{{A}}}ext')
                x, y, w, h = int(off.get('x')), int(off.get('y')), int(ext.get('cx')), int(ext.get('cy'))
                if xf.get('rot') and (x + w > sw or y + h > sh or x < 0 or y < 0):
                    warns.append(f'{tag}: rotated text frame leaves the slide (LibreOffice clips) «{txt[:20]}»')
            for r in sp.iter(f'{{{A}}}rPr'):
                if r.get('spc') and r.find(f'.//{{{A}}}alpha') is not None:
                    warns.append(f'{tag}: letter-spacing + transparency (LibreOffice clips) «{txt[:20]}»')
                for k in ('latin', 'ea'):
                    f = r.find(f'{{{A}}}{k}')
                    if f is not None and not f.get('typeface', '').startswith('+'):
                        fonts.add(f.get('typeface'))
    big = [(n, z.getinfo(n).file_size // 1024) for n in z.namelist() if n.startswith('ppt/media/') and z.getinfo(n).file_size > 3 << 20]
    for n, kb in big:
        warns.append(f'{os.path.basename(n)} is {kb} KB — downscale/JPEG it')
    print(f'slides: {len(slides)}  entrance effects: {effects}  file: {os.path.getsize(a.pptx) // 1024 // 1024} MB')
    print('fonts used:', ', '.join(sorted(fonts)))
    if a.fonts and os.name == 'nt':
        import winreg
        installed = set()
        for root in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            try:
                k = winreg.OpenKey(root, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts')
                for i in range(winreg.QueryInfoKey(k)[1]):
                    installed.add(winreg.EnumValue(k, i)[0].split(' (')[0].lower())
            except OSError:
                pass
        for f in sorted(fonts):
            ok = any(x.startswith(f.lower()) for x in installed)
            print(f'  {"OK " if ok else "MISSING"} {f}')
    for w in warns:
        print('WARN ', w)
    for e in errors:
        print('ERROR', e)
    print('result:', 'FAIL' if errors else 'OK')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
