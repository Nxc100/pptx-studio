"""Render a .pptx to per-slide JPGs + contact-sheet grids (for cheap visual QA).

  python render_deck.py deck.pptx OUTDIR [--dpi 110] [--grid-dpi 50] [--pages 3,5-7] [--cols 3 --per 9]

Outputs: OUTDIR/deck.pdf, OUTDIR/s-01.jpg …, OUTDIR/grid-1.jpg …
Token tip: look at grid-*.jpg first (9 slides per image), open single slides only where needed.
LibreOffice is located via $SOFFICE, PATH, or the default install folders.
"""
import argparse, glob, os, shutil, subprocess, sys, tempfile


def find_soffice():
    cands = [os.environ.get('SOFFICE'), shutil.which('soffice'), shutil.which('soffice.exe'),
             r'C:\Program Files\LibreOffice\program\soffice.exe', r'C:\Program Files (x86)\LibreOffice\program\soffice.exe',
             '/Applications/LibreOffice.app/Contents/MacOS/soffice', '/usr/bin/soffice', '/usr/lib/libreoffice/program/soffice']
    for c in cands:
        if c and os.path.exists(c):
            return c
    sys.exit('LibreOffice (soffice) not found; set $SOFFICE')


def to_pdf(pptx, outdir):
    os.makedirs(outdir, exist_ok=True)
    prof = tempfile.mkdtemp(prefix='lo_prof_')
    from pathlib import Path
    cmd = [find_soffice(), f'-env:UserInstallation={Path(prof).as_uri()}', '--headless', '--convert-to', 'pdf', '--outdir', outdir, pptx]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=900)
    pdf = os.path.join(outdir, os.path.splitext(os.path.basename(pptx))[0] + '.pdf')
    if not os.path.exists(pdf):
        sys.exit('PDF conversion failed')
    return pdf


def parse_pages(spec, n):
    if not spec:
        return list(range(1, n + 1))
    out = []
    for part in spec.split(','):
        a, _, b = part.partition('-')
        out += list(range(int(a), int(b or a) + 1))
    return [p for p in out if 1 <= p <= n]


def rasterize(pdf, outdir, dpi, pages, prefix='s'):
    import fitz  # PyMuPDF
    doc = fitz.open(pdf)
    paths = []
    for p in parse_pages(pages, len(doc)):
        pix = doc[p - 1].get_pixmap(dpi=dpi)
        path = os.path.join(outdir, f'{prefix}-{p:02d}.jpg')
        pix.pil_save(path, quality=85) if hasattr(pix, 'pil_save') else pix.save(path)
        paths.append(path)
    return paths


def grids(paths, outdir, cols=3, per=9, width=640):
    from PIL import Image, ImageDraw, ImageFont
    try:
        font = ImageFont.truetype('arial.ttf', 20)
    except Exception:
        font = None
    out = []
    for gi in range(0, len(paths), per):
        chunk = paths[gi:gi + per]
        ims = [Image.open(f) for f in chunk]
        h = int(ims[0].height * width / ims[0].width)
        rows = (len(ims) + cols - 1) // cols
        g = Image.new('RGB', (cols * width + (cols + 1) * 8, rows * (h + 28) + 8), 'white')
        d = ImageDraw.Draw(g)
        for k, (f, im) in enumerate(zip(chunk, ims)):
            r, c = divmod(k, cols)
            x, y = 8 + c * (width + 8), 8 + r * (h + 28)
            g.paste(im.resize((width, h)), (x, y + 22))
            d.text((x, y), os.path.basename(f), fill='red', font=font)
        p = os.path.join(outdir, f'grid-{gi // per + 1}.jpg')
        g.save(p, quality=85)
        out.append(p)
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('pptx'); ap.add_argument('outdir')
    ap.add_argument('--dpi', type=int, default=110, help='single-slide dpi (110 ≈ 1467px wide)')
    ap.add_argument('--grid-dpi', type=int, default=50)
    ap.add_argument('--pages', default='')
    ap.add_argument('--cols', type=int, default=3); ap.add_argument('--per', type=int, default=9)
    ap.add_argument('--no-singles', action='store_true', help='only grids (cheapest)')
    a = ap.parse_args()
    for f in glob.glob(os.path.join(a.outdir, 's-*.jpg')) + glob.glob(os.path.join(a.outdir, 'g-*.jpg')) + glob.glob(os.path.join(a.outdir, 'grid-*.jpg')):
        os.remove(f)
    pdf = to_pdf(os.path.abspath(a.pptx), a.outdir)
    small = rasterize(pdf, a.outdir, a.grid_dpi, a.pages, prefix='g')
    gs = grids(small, a.outdir, a.cols, a.per)
    for f in small:
        os.remove(f)
    singles = [] if a.no_singles else rasterize(pdf, a.outdir, a.dpi, a.pages)
    print('pdf:', pdf)
    print('grids:', *gs, sep='\n  ')
    if singles:
        print('slides:', len(singles), 'files like', singles[0])
