"""One-shot analysis of a reference (or draft) deck -> compact markdown report + contact sheets.

  python analyze_deck.py ref.pptx OUTDIR [--brief] [--no-render] [--max-shapes 40]

Report (OUTDIR/report.md) covers, per deck: slide size, theme colours/fonts, layouts (name, which slides use
them, background/decor images, layout-level transitions), media inventory; per slide: layout, transition,
text (font/size/colour), pictures & shapes with positions, and the animation timeline
(effect, trigger, delay, duration, target). Also writes OUTDIR/grid-*.jpg via render_deck.py.
Read report.md + grids instead of dumping XML by hand — it is ~10x cheaper in tokens.
"""
import argparse, collections, os, re, sys, zipfile
from lxml import etree

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006'}
EMU = 914400
PRESET = {0: 'custom', 1: 'appear', 2: 'fly-in', 3: 'blinds', 4: 'box', 5: 'checkerboard', 6: 'circle/shape', 9: 'dissolve',
          10: 'fade', 12: 'peek', 14: 'random-bars', 16: 'split', 17: 'stretch', 18: 'strips', 21: 'wheel', 22: 'wipe',
          23: 'zoom(basic)', 26: 'bounce', 37: 'rise-up', 42: 'ascend/float', 47: 'descend', 49: 'grow&turn', 53: 'zoom(fade)',
          55: 'swivel', 10_001: '?'}


def rels(z, part):
    d = os.path.dirname(part); rp = f'{d}/_rels/{os.path.basename(part)}.rels'
    if rp not in z.namelist():
        return {}
    t = etree.fromstring(z.read(rp))
    out = {}
    for r in t:
        tgt = r.get('Target')
        out[r.get('Id')] = os.path.normpath(os.path.join(d, tgt)).replace('\\', '/') if not tgt.startswith('http') else tgt
    return out


def transition(t):
    alt = t.find('mc:AlternateContent', NS)
    tr = None
    if alt is not None:
        tr = alt.find('mc:Choice/p:transition', NS)
    if tr is None:
        tr = t.find('p:transition', NS)
    if tr is None:
        return None
    kids = [etree.QName(k).localname + ('(' + ','.join(f'{a}={v}' for a, v in k.attrib.items()) + ')' if k.attrib else '') for k in tr]
    attrs = {etree.QName(k).localname: v for k, v in tr.attrib.items()}
    return f"{'/'.join(kids) or 'none'} {attrs}"


def shape_rows(t, rel, z, maxn, brief=False):
    rows = []
    for el in t.iter('{%s}sp' % NS['p'], '{%s}pic' % NS['p'], '{%s}graphicFrame' % NS['p'], '{%s}cxnSp' % NS['p']):
        nv = el.find('.//p:cNvPr', NS)
        xf = el.find('p:spPr/a:xfrm', NS)
        if xf is None:
            xf = el.find('p:xfrm', NS)
        if xf is None:
            xf = el.find('p:grpSpPr/a:xfrm', NS)
        off = xf.find('a:off', NS) if xf is not None else None
        ext = xf.find('a:ext', NS) if xf is not None else None
        pos = ''
        if off is not None and ext is not None and ext.get('cx') is not None:
            pos = '@(%.2f,%.2f %.2fx%.2f)' % (int(off.get('x')) / EMU, int(off.get('y')) / EMU, int(ext.get('cx')) / EMU, int(ext.get('cy')) / EMU)
        kind = etree.QName(el).localname
        geom = el.find('.//a:prstGeom', NS)
        g = geom.get('prst') if geom is not None else ('custGeom' if el.find('.//a:custGeom', NS) is not None else '')
        txt = ''.join(x.text or '' for x in el.iter('{%s}t' % NS['a'])).strip()
        fonts = set()
        for r in el.iter('{%s}rPr' % NS['a'], '{%s}defRPr' % NS['a']):
            sz = r.get('sz'); ea = r.find('a:ea', NS); la = r.find('a:latin', NS)
            col = r.find('.//a:srgbClr', NS)
            fonts.add('%s/%s %s%s' % (ea.get('typeface') if ea is not None else '', la.get('typeface') if la is not None else '',
                                      (int(sz) / 100 if sz else ''), (' #' + col.get('val')) if col is not None else ''))
        img = ''
        blip = el.find('.//a:blip', NS)
        if blip is not None:
            rid = blip.get('{%s}embed' % NS['r'])
            p = rel.get(rid, '')
            if p in z.namelist():
                img = f' img={os.path.basename(p)}({len(z.read(p)) // 1024}KB)'
        fill = el.find('p:spPr/a:solidFill/a:srgbClr', NS)
        fl = f' fill=#{fill.get("val")}' if fill is not None else ''
        if brief and not (txt or img):
            continue
        rows.append(f"- {kind} {g} {pos}{img}{fl} '{nv.get('name') if nv is not None else ''}'"
                    + (f' «{txt[:90]}» fonts={sorted(fonts)[:3]}' if txt else ''))
        if len(rows) >= maxn:
            rows.append('- …'); break
    return rows


def timeline(t):
    names = {e.get('id'): e.get('name') for e in t.iter('{%s}cNvPr' % NS['p'])}
    out = []
    for c in t.iter('{%s}cTn' % NS['p']):
        pid = c.get('presetID')
        if pid is None:
            continue
        cond = c.find('p:stCondLst/p:cond', NS)
        tg = c.find('.//p:spTgt', NS)
        filt = [e.get('filter') for e in c.iter('{%s}animEffect' % NS['p'])]
        attrs = sorted({e.text for e in c.iter('{%s}attrName' % NS['p'])} - {'style.visibility'})
        durs = [x.get('dur') for x in c.iter('{%s}cTn' % NS['p']) if x.get('dur') not in (None, '1', 'indefinite')]
        it = c.find('p:iterate', NS)
        par = c.getparent().getparent().getparent()  # step par cTn
        step_delay = par.find('p:stCondLst/p:cond', NS).get('delay') if par is not None and par.find('p:stCondLst/p:cond', NS) is not None else '?'
        sid = tg.get('spid') if tg is not None else None
        out.append(f"  {c.get('presetClass')}:{PRESET.get(int(pid), pid)}[{pid}/{c.get('presetSubtype')}] {c.get('nodeType')} "
                   f"step@{step_delay} +{cond.get('delay') if cond is not None else 0}ms dur={durs[:1]} {filt}{attrs if attrs else ''}"
                   f"{' by-letter' if it is not None and it.get('type') == 'lt' else ''} -> '{names.get(sid)}'")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pptx'); ap.add_argument('outdir')
    ap.add_argument('--no-render', action='store_true'); ap.add_argument('--max-shapes', type=int, default=40)
    ap.add_argument('--brief', action='store_true', help='only text/picture shapes (≈half the size)')
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    z = zipfile.ZipFile(a.pptx)
    names = z.namelist()
    pres = etree.fromstring(z.read('ppt/presentation.xml'))
    sz = pres.find('p:sldSz', NS)
    L = [f'# Deck analysis: {os.path.basename(a.pptx)}', '',
         f"- size: {int(sz.get('cx')) / EMU:.3f} x {int(sz.get('cy')) / EMU:.3f} in; file {os.path.getsize(a.pptx) // 1024 // 1024} MB"]
    th = [n for n in names if re.match(r'ppt/theme/theme\d+\.xml', n)]
    if th:
        t = etree.fromstring(z.read(th[0]))
        cols = {etree.QName(e).localname: (e.find('a:srgbClr', NS).get('val') if e.find('a:srgbClr', NS) is not None else e[0].get('lastClr'))
                for e in t.find('.//a:clrScheme', NS)}
        L.append(f'- theme colours: {cols}')
        for tag in ('majorFont', 'minorFont'):
            f = t.find(f'.//a:{tag}', NS)
            L.append(f"- {tag}: latin={f.find('a:latin', NS).get('typeface')} ea={f.find('a:ea', NS).get('typeface')}")
    media = sorted([(n, z.getinfo(n).file_size) for n in names if n.startswith('ppt/media/')], key=lambda x: -x[1])
    L.append(f'- media: {len(media)} files, {sum(s for _, s in media) // 1024 // 1024} MB; largest: ' +
             ', '.join(f'{os.path.basename(n)} {s // 1024}KB' for n, s in media[:6]))
    slides = sorted([n for n in names if re.match(r'ppt/slides/slide\d+\.xml$', n)], key=lambda x: int(re.findall(r'\d+', x)[-1]))
    # order by presentation sldIdLst
    prel = rels(z, 'ppt/presentation.xml')
    order = [prel[s.get('{%s}id' % NS['r'])] for s in pres.find('p:sldIdLst', NS)]
    slides = [s for s in order if s in names] or slides
    lay_use = collections.defaultdict(list)
    slide_layout = {}
    for i, s in enumerate(slides, 1):
        lay = [v for v in rels(z, s).values() if 'slideLayout' in v]
        if lay:
            lay_use[lay[0]].append(i); slide_layout[s] = lay[0]
    L += ['', '## Layouts (used)']
    for lay, used in sorted(lay_use.items(), key=lambda kv: kv[1][0]):
        t = etree.fromstring(z.read(lay)); r = rels(z, lay)
        nm = t.find('p:cSld', NS).get('name')
        pics = [f"{os.path.basename(r.get(b.get('{%s}embed' % NS['r']), '?'))}" for b in t.iter('{%s}blip' % NS['a'])]
        L.append(f"- {os.path.basename(lay)} '{nm}' slides {used}; images {pics}; transition: {transition(t)}")
    mst = [n for n in names if re.match(r'ppt/slideMasters/slideMaster\d+\.xml', n)]
    for m in mst:
        t = etree.fromstring(z.read(m)); r = rels(z, m)
        bg = t.find('p:cSld/p:bg', NS)
        bgb = bg.find('.//a:blip', NS) if bg is not None else None
        L.append(f"- master {os.path.basename(m)} bg={'image ' + os.path.basename(r.get(bgb.get('{%s}embed' % NS['r']), '')) if bgb is not None else ('fill' if bg is not None else 'none')}; transition: {transition(t)}")
    summary = collections.Counter()
    L += ['', '## Slides']
    for i, s in enumerate(slides, 1):
        t = etree.fromstring(z.read(s)); r = rels(z, s)
        lay = slide_layout.get(s, '')
        lname = etree.fromstring(z.read(lay)).find('p:cSld', NS).get('name') if lay else ''
        tr = transition(t)
        tlines = timeline(t)
        for x in tlines:
            summary[x.split()[0].split('[')[0]] += 1
        L += ['', f"### Slide {i} — layout '{lname}' — transition: {tr or 'none (inherits layout/master)'} — {len(tlines)} animations"]
        L += shape_rows(t, r, z, a.max_shapes, a.brief)
        if tlines:
            L.append('- timeline:'); L += tlines
        nt = [v for v in r.values() if 'notesSlide' in v]
        if nt:
            txt = ''.join(x.text or '' for x in etree.fromstring(z.read(nt[0])).iter('{%s}t' % NS['a'])).strip()
            if txt:
                L.append(f'- notes: {txt[:160]}')
    L += ['', '## Animation vocabulary (count)', ''] + [f'- {k}: {v}' for k, v in summary.most_common()]
    open(os.path.join(a.outdir, 'report.md'), 'w', encoding='utf8').write('\n'.join(L))
    print('report:', os.path.join(a.outdir, 'report.md'), f'({len(L)} lines)')
    if not a.no_render:
        here = os.path.dirname(os.path.abspath(__file__))
        os.system(f'"{sys.executable}" "{os.path.join(here, "render_deck.py")}" "{a.pptx}" "{a.outdir}" --no-singles')


if __name__ == '__main__':
    main()
