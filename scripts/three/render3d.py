"""Render config-driven three.js scenes (headless Chromium + SwiftShader WebGL) to trimmed transparent PNGs
plus *_meta.json with projected label/pin pixel positions (in the final PNG).

  python render3d.py OUT_DIR cfgA.json [cfgB.json ...] [--same-trim] [--ds 2]

Each config: {"page": "map3d.html" | "plan3d.html", "name": "map_chengdu", ...page keys}
  paths inside configs (geojson / geo / floor) are relative to the config file's folder.
--same-trim: trim every output with the union bounding box (needed when two renders must overlay / share labels,
             e.g. plan3d + plan3d_zones).  --ds: downsample factor after rendering (supersampling, default 2).
Needs network once for three.js from jsdelivr (cached by the browser profile? no — keep online while rendering).
"""
import argparse, base64, functools, http.server, json, os, socketserver, sys, threading, time
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    roots = {}

    def log_message(self, *a):
        pass

    def translate_path(self, path):
        path = path.split('?', 1)[0]
        for prefix, root in self.roots.items():
            if path.startswith(prefix):
                from urllib.parse import unquote
                return os.path.join(root, unquote(path[len(prefix):]))
        return super().translate_path(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('cfgs', nargs='+')
    ap.add_argument('--same-trim', action='store_true'); ap.add_argument('--ds', type=float, default=2)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), Handler)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    raws = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        for i, cf in enumerate(a.cfgs):
            cfg = json.load(open(cf, encoding='utf8'))
            Handler.roots = {'/three/': HERE, f'/work{i}/': os.path.dirname(os.path.abspath(cf))}
            for k in ('geojson', 'geo', 'floor'):
                if k in cfg:
                    cfg[k] = f'/work{i}/' + cfg[k].replace('\\', '/')
            w, h = cfg.get('size', [2400, 1800])
            pg = b.new_page(viewport={'width': w, 'height': h})
            logs = []
            pg.on('console', lambda m: logs.append(m.text)); pg.on('pageerror', lambda e: logs.append('PAGEERROR ' + str(e)))
            pg.add_init_script(f'window.__CFG = {json.dumps(cfg, ensure_ascii=False)};')
            t0 = time.time()
            pg.goto(f'http://127.0.0.1:{port}/three/{cfg.get("page", "map3d.html")}')
            try:
                pg.wait_for_function('window.__done === true', timeout=600000, polling=500)
            except Exception as e:
                print('TIMEOUT/ERROR', cf, e, *logs[-10:], sep='\n'); continue
            raw = os.path.join(a.out, f'_raw_{cfg["name"]}.png')
            open(raw, 'wb').write(base64.b64decode(pg.evaluate('window.__png').split(',')[1]))
            raws.append((cfg['name'], raw, pg.evaluate('window.__meta || {}')))
            print(f'rendered {cfg["name"]} in {time.time() - t0:.1f}s', *(l for l in logs[-3:] if 'PAGEERROR' in l))
            pg.close()
        b.close()
    srv.shutdown()
    ims = [Image.open(r) for _, r, _ in raws]
    bbs = [im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox() for im in ims]
    for k, ((name, raw, meta), im, bb) in enumerate(zip(raws, ims, bbs)):
        if a.same_trim:
            bb = (min(x[0] for x in bbs), min(x[1] for x in bbs), max(x[2] for x in bbs), max(x[3] for x in bbs))
        pad = int(0.02 * max(bb[2] - bb[0], bb[3] - bb[1]))
        box = (max(0, bb[0] - pad), max(0, bb[1] - pad), min(im.width, bb[2] + pad), min(im.height, bb[3] + pad))
        c = im.crop(box)
        if a.ds != 1:
            c = c.convert('RGBa').resize((round(c.width / a.ds), round(c.height / a.ds)), Image.LANCZOS).convert('RGBA')
        out = os.path.join(a.out, name + '.png'); c.save(out, optimize=True)
        res = {'size': [c.width, c.height]}
        for key in ('labels', 'pins'):
            if meta.get(key):
                res[key] = {n: [round((v[0] - box[0]) / a.ds, 1), round((v[1] - box[1]) / a.ds, 1)] for n, v in meta[key].items()}
        json.dump(res, open(os.path.join(a.out, name + '_meta.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        os.remove(raw)
        print(name, c.size, os.path.getsize(out) // 1024, 'KB')


if __name__ == '__main__':
    main()
