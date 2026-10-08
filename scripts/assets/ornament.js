// Gold line-art ornaments. window.orn(kind) -> {svg, W, H}
const GOLD_DEFS = (W,H) => `<defs>
  <linearGradient id="gold" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="${W}" y2="${H}">
    <stop offset="0" stop-color="#9A7644"/><stop offset="0.3" stop-color="#C6A66B"/>
    <stop offset="0.5" stop-color="#B08D57"/><stop offset="0.72" stop-color="#D4BA85"/>
    <stop offset="1" stop-color="#977341"/></linearGradient>
  <linearGradient id="olive" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="${W}" y2="${H}">
    <stop offset="0" stop-color="#55613A"/><stop offset="0.5" stop-color="#5E6B3D"/><stop offset="1" stop-color="#6C7A48"/></linearGradient>
  <radialGradient id="wax" cx="0.42" cy="0.38" r="0.7">
    <stop offset="0" stop-color="#A9503F"/><stop offset="0.55" stop-color="#8E3B2E"/><stop offset="1" stop-color="#6A2720"/></radialGradient>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>`;
const f = v => (+v).toFixed(2);

function circInter(c1, c2, r) { // outer intersection of two equal circles (away from origin)
  const mx = (c1[0] + c2[0]) / 2, my = (c1[1] + c2[1]) / 2;
  const dx = c2[0] - c1[0], dy = c2[1] - c1[1]; const D = Math.hypot(dx, dy);
  const h = Math.sqrt(Math.max(0, r * r - (D / 2) ** 2));
  const ux = -dy / D, uy = dx / D;
  const p1 = [mx + ux * h, my + uy * h], p2 = [mx - ux * h, my - uy * h];
  return Math.hypot(...p1) > Math.hypot(...p2) ? p1 : p2;
}
// quatrefoil outline centered at origin: lobe offset d, lobe radius r
function qfPath(d, r, cx = 0, cy = 0) {
  const L = [[d, 0], [0, d], [-d, 0], [0, -d]];
  const P = [];
  for (let i = 0; i < 4; i++) P.push(circInter(L[(i + 3) % 4], L[i], r)); // P[i] = between lobe i-1 and lobe i
  let s = `M${f(P[0][0] + cx)},${f(P[0][1] + cy)}`;
  for (let i = 0; i < 4; i++) {
    const a = P[i], b = P[(i + 1) % 4], c = L[i];
    const a0 = Math.atan2(a[1] - c[1], a[0] - c[0]), a1 = Math.atan2(b[1] - c[1], b[0] - c[0]);
    let span = a1 - a0; while (span < 0) span += 2 * Math.PI;
    s += ` A${f(r)},${f(r)} 0 ${span > Math.PI ? 1 : 0} 1 ${f(b[0] + cx)},${f(b[1] + cy)}`;
  }
  return { d: s + 'Z', pts: P };
}
function fleurPath() { // 100x100 box
  const R = `M54,63 C58,50 68,39 81,40 C93,41 97,54 90,61 C86,65 79,64 78,58 C77.5,54 81,52.5 84,54.5 C84,49 77,47 71,51 C64,55.5 60,62 58.5,67Z`;
  const Lm = R.replace(/(-?\d+\.?\d*),(-?\d+\.?\d*)/g, (m, x, y) => `${100 - x},${y}`);
  return [
    `M50,4 C57,15 64,29 61.5,45 C60,55 55,62 52.5,67 L47.5,67 C45,62 40,55 38.5,45 C36,29 43,15 50,4Z`,
    R, Lm,
    `M33,64.5 L67,64.5 Q69,64.5 69,67 L69,69.5 Q69,72 67,72 L33,72 Q31,72 31,69.5 L31,67 Q31,64.5 33,64.5Z`,
    `M46.5,72 C45,80 46.5,88 50,96 C53.5,88 55,80 53.5,72Z`,
    `M43,72 C37,74.5 30,78.5 26.5,87 C34,85 40,81 45.5,74.5Z`,
    `M57,72 C63,74.5 70,78.5 73.5,87 C66,85 60,81 54.5,74.5Z`];
}
function taperLine(x0, y0, x1, y1, w0, w1, fill) {
  const dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy), nx = -dy / L, ny = dx / L;
  return `<path d="M${f(x0 + nx * w0 / 2)},${f(y0 + ny * w0 / 2)} L${f(x1 + nx * w1 / 2)},${f(y1 + ny * w1 / 2)} L${f(x1 - nx * w1 / 2)},${f(y1 - ny * w1 / 2)} L${f(x0 - nx * w0 / 2)},${f(y0 - ny * w0 / 2)}Z" fill="${fill}"/>`;
}
function spiral(cx, cy, r0, turns, dir, startAng) { // logarithmic-ish spiral inward
  let s = ''; const N = 80;
  for (let i = 0; i <= N; i++) {
    const t = i / N; const a = startAng + dir * t * turns * 2 * Math.PI; const r = r0 * Math.pow(0.18, t);
    s += (i ? 'L' : 'M') + f(cx + Math.cos(a) * r) + ',' + f(cy + Math.sin(a) * r);
  }
  return s;
}
function teardrop(x, y, a, len, wid, fill) {
  return `<path transform="translate(${f(x)},${f(y)}) rotate(${f(a)})" d="M0,0 C${f(len * 0.3)},${f(-wid)} ${f(len * 0.8)},${f(-wid * 0.7)} ${f(len)},0 C${f(len * 0.8)},${f(wid * 0.7)} ${f(len * 0.3)},${f(wid)} 0,0Z" fill="${fill}"/>`;
}

window.orn = function (kind) {
  let W, H, body = '';
  const G = 'url(#gold)';
  if (kind === 'quatrefoil') {
    W = H = 800; const c = 400;
    body += `<g transform="translate(${c},${c})" fill="none" stroke="${G}" stroke-linecap="round" stroke-linejoin="round">`;
    body += `<circle r="378" stroke-width="3"/><circle r="364" stroke-width="1.2"/>`;
    const q1 = qfPath(150, 192), q2 = qfPath(150, 176);
    body += `<path d="${q1.d}" stroke-width="3"/><path d="${q2.d}" stroke-width="1.3"/>`;
    // cusps on diagonals: dagger from intersection toward ring
    for (const p of q1.pts) {
      const a = Math.atan2(p[1], p[0]); const r1 = Math.hypot(...p);
      const ca = Math.cos(a), sa = Math.sin(a), na = -sa, nb = ca;
      const tip = 352, mid = (r1 + tip) / 2;
      body += `<path d="M${f(ca * r1)},${f(sa * r1)} L${f(ca * mid + na * 9)},${f(sa * mid + nb * 9)} L${f(ca * tip)},${f(sa * tip)} L${f(ca * mid - na * 9)},${f(sa * mid - nb * 9)}Z" stroke-width="1.6"/>`;
      body += `<circle cx="${f(ca * mid)}" cy="${f(sa * mid)}" r="3.2" fill="${G}" stroke="none"/>`;
    }
    // small trefoils on axes just outside lobes
    for (let k = 0; k < 4; k++) {
      const a = k * Math.PI / 2; const ca = Math.cos(a), sa = Math.sin(a);
      body += `<circle cx="${f(ca * 352)}" cy="${f(sa * 352)}" r="4" fill="${G}" stroke="none"/>`;
    }
    // inner rosette
    const q3 = qfPath(26, 34);
    body += `<path d="${q3.d}" stroke-width="2"/><circle r="9" fill="${G}" stroke="none"/>`;
    for (let k = 0; k < 4; k++) { const a = k * Math.PI / 2 + Math.PI / 4; body += `<circle cx="${f(Math.cos(a) * 90)}" cy="${f(Math.sin(a) * 90)}" r="3" fill="${G}" stroke="none"/>`; }
    body += `<circle r="118" stroke-width="1" stroke-dasharray="2 9"/>`;
    body += '</g>';
  } else if (kind === 'quatrefoil_small' || kind === 'quatrefoil_small_olive') {
    W = H = 240; const fill = kind.endsWith('olive') ? 'url(#olive)' : G;
    const q = qfPath(46, 62), qi = qfPath(46, 50);
    body += `<g transform="translate(120,120)"><path d="${q.d}" fill="${fill}"/>
      <path d="${qi.d}" fill="none" stroke="#F4EDE0" stroke-width="3" opacity="0.85"/>
      <circle r="13" fill="#F4EDE0" opacity="0.92"/><circle r="6" fill="${fill}"/></g>`;
  } else if (kind === 'divider') {
    W = 1400; H = 80; const cx = 700, cy = 40;
    body += taperLine(560, cy, 30, cy, 2.6, 0.2, G) + taperLine(840, cy, 1370, cy, 2.6, 0.2, G);
    body += taperLine(556, cy + 7, 200, cy + 7, 1.0, 0.1, G) + taperLine(844, cy + 7, 1200, cy + 7, 1.0, 0.1, G);
    body += `<circle cx="22" cy="${cy}" r="3" fill="${G}"/><circle cx="1378" cy="${cy}" r="3" fill="${G}"/>`;
    // scrolls flanking centre: S-curve rising from the gem, curling into a spiral; lower sweep rejoins the rule
    for (const s of [-1, 1]) {
      const x0 = cx + s * 24;
      const scx = cx + s * 62, scy = cy - 9;
      let sp = ''; const N = 60;
      for (let i = 0; i <= N; i++) { const t = i / N; const a = (s > 0 ? -Math.PI * 0.05 : Math.PI * 1.05) + s * -t * 1.6 * 2 * Math.PI * -1; const r = 13 * Math.pow(0.22, t); sp += (i ? 'L' : 'M') + f(scx + Math.cos(a) * r) + ',' + f(scy + Math.sin(a) * r); }
      body += `<path d="M${x0},${cy} C${x0 + s * 10},${cy - 18} ${scx + s * 4},${cy - 30} ${scx + s * 13},${scy}" fill="none" stroke="${G}" stroke-width="2" stroke-linecap="round"/>`;
      body += `<path d="${sp}" fill="none" stroke="${G}" stroke-width="1.8" stroke-linecap="round"/>`;
      body += `<path d="M${cx + s * 44},${cy + 9} C${cx + s * 66},${cy + 15} ${cx + s * 100},${cy + 12} ${cx + s * 122},${cy}" fill="none" stroke="${G}" stroke-width="1.6" stroke-linecap="round"/>`;
      body += `<path d="M${x0},${cy} C${x0 + s * 8},${cy + 8} ${cx + s * 36},${cy + 9} ${cx + s * 44},${cy + 9}" fill="none" stroke="${G}" stroke-width="1.2" stroke-linecap="round" opacity="0"/>`;
      body += teardrop(cx + s * 84, cy - 3, s > 0 ? -20 : 200, 20, 5.5, G);
      body += teardrop(cx + s * 98, cy + 9, s > 0 ? 20 : 160, 14, 4, G);
      body += `<circle cx="${cx + s * 128}" cy="${cy}" r="3" fill="${G}"/>`;
    }
    body += `<path d="M${cx},${cy - 16} L${cx + 16},${cy} L${cx},${cy + 16} L${cx - 16},${cy}Z" fill="none" stroke="${G}" stroke-width="1.8"/>`;
    const q = qfPath(5.5, 7.5); body += `<path transform="translate(${cx},${cy})" d="${q.d}" fill="${G}"/>`;
  } else if (kind === 'corner_filigree') {
    W = H = 700;
    // double rules along top and left
    body += taperLine(132, 40, 690, 40, 3.2, 0.2, G) + taperLine(132, 52, 560, 52, 1.2, 0.1, G);
    body += taperLine(40, 132, 40, 690, 3.2, 0.2, G) + taperLine(52, 132, 52, 560, 1.2, 0.1, G);
    // corner block with quatrefoil
    body += `<rect x="28" y="28" width="90" height="90" fill="none" stroke="${G}" stroke-width="2.6"/>`;
    body += `<rect x="38" y="38" width="70" height="70" fill="none" stroke="${G}" stroke-width="1"/>`;
    const q = qfPath(13, 18); body += `<path transform="translate(73,73)" d="${q.d}" fill="${G}"/><circle cx="73" cy="73" r="5" fill="#F4EDE0"/>`;
    // tendrils mirrored over diagonal
    const tend = (sw) => { // sw=false: along top; true: along left (swap x/y)
      const P = (x, y) => sw ? `${f(y)},${f(x)}` : `${f(x)},${f(y)}`;
      let s = `<path d="M${P(118, 64)} C${P(170, 66)} ${P(205, 90)} ${P(232, 118)} C${P(258, 146)} ${P(300, 150)} ${P(318, 128)}" fill="none" stroke="${G}" stroke-width="2.4" stroke-linecap="round"/>`;
      // spiral at end
      let sp = ''; const cx = 300, cy = 112; const N = 70;
      for (let i = 0; i <= N; i++) { const t = i / N; const a = 0.9 + t * 1.7 * 2 * Math.PI * -1; const r = 26 * Math.pow(0.2, t); sp += (i ? 'L' : 'M') + P(cx + Math.cos(a) * r, cy + Math.sin(a) * r); }
      s += `<path d="${sp}" fill="none" stroke="${G}" stroke-width="2" stroke-linecap="round"/>`;
      // second smaller curl inward toward corner
      s += `<path d="M${P(180, 78)} C${P(190, 110)} ${P(160, 135)} ${P(140, 125)} C${P(126, 118)} ${P(132, 100)} ${P(146, 104)}" fill="none" stroke="${G}" stroke-width="1.6" stroke-linecap="round"/>`;
      // long fine tendril continuing along rule
      s += `<path d="M${P(318, 128)} C${P(340, 100)} ${P(380, 70)} ${P(440, 62)}" fill="none" stroke="${G}" stroke-width="1.3" stroke-linecap="round"/>`;
      // leaves
      const leafs = [[205, 92, 40], [250, 140, -20], [360, 82, -25], [410, 66, -12], [158, 70, 15]];
      for (const [x, y, a] of leafs) { const aa = sw ? 90 - a : a; s += `<g transform="translate(${P(x, y)})">${teardrop(0, 0, aa, 26, 7, G)}</g>`; }
      for (const [x, y, r] of [[455, 61, 3], [470, 60, 2], [338, 150, 2.6], [225, 70, 2.2]]) s += `<circle cx="${sw ? y : x}" cy="${sw ? x : y}" r="${r}" fill="${G}"/>`;
      return s;
    };
    body += tend(false) + tend(true);
    // diagonal fleuron
    body += teardrop(118, 118, 45, 40, 10, G) + `<circle cx="170" cy="170" r="3.5" fill="${G}"/>`;
  } else if (kind === 'fleur') {
    W = H = 300;
    body += `<g transform="translate(18,12) scale(2.64)">` + fleurPath().map(d => `<path d="${d}" fill="${G}"/>`).join('') + `</g>`;
  } else if (kind === 'wax_seal') {
    W = H = 500; const c = 250;
    // irregular blob edge
    let pts = []; const N = 180;
    for (let i = 0; i < N; i++) {
      const a = i / N * 2 * Math.PI;
      const r = 200 + 7 * Math.sin(5 * a + 0.6) + 5 * Math.sin(9 * a + 2.1) + 3 * Math.sin(17 * a) + (Math.sin(3 * a + 1) > 0.85 ? 10 * (Math.sin(3 * a + 1) - 0.85) / 0.15 : 0);
      pts.push([c + Math.cos(a) * r, c + Math.sin(a) * r]);
    }
    const blob = 'M' + pts.map(p => f(p[0]) + ',' + f(p[1])).join('L') + 'Z';
    body += `<path d="${blob}" transform="translate(6,10)" fill="#3B1A15" opacity="0.35" filter="url(#soft)"/>`;
    body += `<path d="${blob}" fill="url(#wax)"/>`;
    // pressed inner disc (slightly darker) with bevel ring
    body += `<circle cx="${c}" cy="${c}" r="152" fill="#7E3227" opacity="0.55"/>`;
    body += `<circle cx="${c + 2}" cy="${c + 2}" r="156" fill="none" stroke="#B9624F" stroke-width="5" opacity="0.7"/>`;
    body += `<circle cx="${c - 1.5}" cy="${c - 1.5}" r="153" fill="none" stroke="#5A2019" stroke-width="5" opacity="0.75"/>`;
    body += `<circle cx="${c}" cy="${c}" r="136" fill="none" stroke="#5A2019" stroke-width="1.5" opacity="0.6" stroke-dasharray="3 6"/>`;
    // embossed fleur: highlight / shadow / face
    const fl = fleurPath();
    const g = (dx, dy, col, op) => `<g transform="translate(${c - 105 + dx},${c - 110 + dy}) scale(2.1)" opacity="${op}">` + fl.map(d => `<path d="${d}" fill="${col}"/>`).join('') + `</g>`;
    body += g(3, 3, '#C26A55', 0.85) + g(-2.5, -2.5, '#4E1B15', 0.9) + g(0, 0, '#8A3A2D', 1);
    // gloss
    body += `<ellipse cx="${c - 70}" cy="${c - 95}" rx="70" ry="34" transform="rotate(-30 ${c - 70} ${c - 95})" fill="#FFFFFF" opacity="0.13" filter="url(#soft)"/>`;
    body += `<path d="${blob}" fill="none" stroke="#5A2019" stroke-width="2" opacity="0.5"/>`;
  } else if (kind === 'arch_window') {
    W = 900; H = 1300; const cx = 450, sy = 470;
    body += `<g fill="none" stroke="${G}" stroke-linecap="round" stroke-linejoin="round">`;
    const arch = (x0, x1, yTop, yBot, sw) => { const r = (x1 - x0) / 2, m = (x0 + x1) / 2; return `<path d="M${x0},${yBot} L${x0},${yTop} A${r},${r} 0 0 1 ${x1},${yTop} L${x1},${yBot}" stroke-width="${sw}"/>`; };
    body += arch(100, 800, sy, 1250, 4) + arch(126, 774, sy, 1250, 1.6);
    // voussoirs between outer and inner arch
    for (let k = 0; k <= 16; k++) { const a = Math.PI + k * Math.PI / 16; const r0 = 324, r1 = 350; body += `<line x1="${f(cx + Math.cos(a) * r0)}" y1="${f(sy + Math.sin(a) * r0)}" x2="${f(cx + Math.cos(a) * r1)}" y2="${f(sy + Math.sin(a) * r1)}" stroke-width="1.4"/>`; }
    body += `<path d="M${cx - 16},${sy - 352} L${cx + 16},${sy - 352} L${cx + 11},${sy - 318} L${cx - 11},${sy - 318}Z" stroke-width="2"/>`;
    // two lights
    body += arch(176, 432, 790, 1190, 3) + arch(192, 416, 790, 1190, 1.2);
    body += arch(468, 724, 790, 1190, 3) + arch(484, 708, 790, 1190, 1.2);
    // mullion capitals
    body += `<rect x="432" y="760" width="36" height="16" stroke-width="2"/><line x1="450" y1="776" x2="450" y2="1190" stroke-width="1.2"/>`;
    // oculus with quatrefoil
    body += `<circle cx="${cx}" cy="${sy + 20}" r="128" stroke-width="3"/><circle cx="${cx}" cy="${sy + 20}" r="116" stroke-width="1.2"/>`;
    const q = qfPath(44, 58), qi = qfPath(44, 50);
    body += `<path transform="translate(${cx},${sy + 20})" d="${q.d}" stroke-width="2.4"/><path transform="translate(${cx},${sy + 20})" d="${qi.d}" stroke-width="1"/>`;
    body += `<circle cx="${cx}" cy="${sy + 20}" r="8" fill="${G}" stroke="none"/>`;
    // leaded diamond glazing hint in lights (sparse)
    for (const [x0, x1] of [[192, 416], [484, 708]]) {
      for (let y = 840; y < 1190; y += 70) body += `<line x1="${x0}" y1="${y}" x2="${x1}" y2="${y}" stroke-width="0.7" opacity="0.55"/>`;
    }
    // sill
    body += `<path d="M70,1250 L830,1250 M60,1272 L840,1272 M70,1250 L60,1272 M830,1250 L840,1272" stroke-width="2.6"/>`;
    body += `<path d="M90,1290 L810,1290" stroke-width="1"/>`;
    body += '</g>';
  }
  return { W, H, svg: `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">${GOLD_DEFS(W, H)}${body}</svg>` };
};
