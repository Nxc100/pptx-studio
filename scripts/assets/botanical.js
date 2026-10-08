// Procedural watercolor botanical generator (SVG). window.build(kind,W,H,seed) -> svg string
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
let R=mulberry32(11);
const rnd=(a,b)=>a+(b-a)*R();
const pick=a=>a[Math.floor(R()*a.length)];
function hex2rgb(h){h=h.replace('#','');return[parseInt(h.slice(0,2),16),parseInt(h.slice(2,4),16),parseInt(h.slice(4,6),16)]}
function rgb2hex(c){return '#'+c.map(v=>Math.max(0,Math.min(255,Math.round(v))).toString(16).padStart(2,'0')).join('')}
function mix(a,b,t){a=hex2rgb(a);b=hex2rgb(b);return rgb2hex(a.map((v,i)=>v+(b[i]-v)*t))}
function jitter(c,amt){const a=hex2rgb(c);const d=rnd(-amt,amt);return rgb2hex(a.map(v=>v+d+rnd(-amt/2,amt/2)))}

function filters(){
  let s='<defs>';
  for(let i=0;i<6;i++){
    const seed=Math.floor(rnd(1,999));
    s+=`<filter id="wc${i}" x="-30%" y="-30%" width="160%" height="160%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="${rnd(0.025,0.045).toFixed(3)}" numOctaves="3" seed="${seed}" result="n1"/>
      <feDisplacementMap in="SourceGraphic" in2="n1" scale="${rnd(4,7).toFixed(1)}" xChannelSelector="R" yChannelSelector="G" result="d"/>
      <feGaussianBlur in="d" stdDeviation="2.2" result="b"/>
      <feComposite in="d" in2="b" operator="arithmetic" k1="0" k2="1.75" k3="-0.95" k4="0" result="edge"/>
      <feGaussianBlur in="edge" stdDeviation="0.45" result="edge2"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="${seed+7}" result="g"/>
      <feColorMatrix in="g" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0.9 0.9 0 0 -0.35" result="ga"/>
      <feComposite in="edge2" in2="ga" operator="arithmetic" k1="0.32" k2="0.8" k3="0" k4="0"/>
    </filter>`;
  }
  s+=`<filter id="wash" x="-30%" y="-30%" width="160%" height="160%">
      <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="5" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="10" xChannelSelector="R" yChannelSelector="G" result="d"/>
      <feGaussianBlur in="d" stdDeviation="2.5"/></filter>`;
  s+=`<filter id="line" x="-20%" y="-20%" width="140%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="9" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="2.5" xChannelSelector="R" yChannelSelector="G" result="d"/>
      <feGaussianBlur in="d" stdDeviation="0.35"/></filter>`;
  s+='</defs>';
  return s;
}
const F=()=>`url(#wc${Math.floor(R()*6)})`;

function bez(p0,p1,p2,p3,t){const u=1-t;return[u*u*u*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t*t*t*p3[0],u*u*u*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t*t*t*p3[1]]}
function bezd(p0,p1,p2,p3,t){const u=1-t;return[3*u*u*(p1[0]-p0[0])+6*u*t*(p2[0]-p1[0])+3*t*t*(p3[0]-p2[0]),3*u*u*(p1[1]-p0[1])+6*u*t*(p2[1]-p1[1])+3*t*t*(p3[1]-p2[1])]}
function ang(P,t){const d=bezd(...P,t);return Math.atan2(d[1],d[0])*180/Math.PI}
function taper(P,w0,w1,col,op){
  const L=[],Rr=[];const N=60;
  for(let i=0;i<=N;i++){const t=i/N;const p=bez(...P,t);const d=bezd(...P,t);const l=Math.hypot(d[0],d[1])||1;const n=[-d[1]/l,d[0]/l];const w=(w0+(w1-w0)*t)/2*(1+0.08*Math.sin(t*17));L.push([p[0]+n[0]*w,p[1]+n[1]*w]);Rr.push([p[0]-n[0]*w,p[1]-n[1]*w]);}
  const pts=L.concat(Rr.reverse());
  return `<path d="M${pts.map(p=>p[0].toFixed(1)+','+p[1].toFixed(1)).join('L')}Z" fill="${col}" opacity="${op}" filter="url(#line)"/>`;
}
function leafD(len,wid,bend){
  const b=bend*len;
  return `M0,0 C${len*0.25},${-wid*0.95+b*0.06} ${len*0.7},${-wid*0.75+b*0.5} ${len},${b} C${len*0.7},${wid*0.7+b*0.5} ${len*0.25},${wid*0.9+b*0.06} 0,0Z`;
}
function leaf(x,y,a,len,wid,base,opts={}){
  const bend=opts.bend??rnd(-0.12,0.12);
  const col=jitter(base,10);
  const light=mix(col,'#F4EDE0',0.35);
  const dark=mix(col,'#2E3320',0.35);
  const d=leafD(len,wid,bend);
  const b=bend*len;
  let s=`<g transform="translate(${x.toFixed(1)},${y.toFixed(1)}) rotate(${a.toFixed(1)})">`;
  s+=`<path d="${leafD(len*1.04,wid*1.15,bend)}" fill="${light}" opacity="0.32" filter="url(#wash)"/>`;
  s+=`<path d="${d}" fill="${col}" opacity="${(opts.op??0.82).toFixed(2)}" filter="${F()}"/>`;
  s+=`<path d="M0,0 C${len*0.25},${-wid*0.95+b*0.06} ${len*0.7},${-wid*0.75+b*0.5} ${len},${b} C${len*0.6},${b*0.36-wid*0.08} ${len*0.3},${b*0.09-wid*0.05} 0,0Z" fill="${dark}" opacity="0.22" filter="${F()}"/>`;
  s+=`<path d="M${len*0.02},0 Q${len*0.5},${b*0.25} ${len*0.94},${b*0.88}" stroke="${dark}" stroke-width="${Math.max(0.8,wid*0.09).toFixed(2)}" fill="none" opacity="0.45" stroke-linecap="round" filter="url(#line)"/>`;
  s+='</g>';
  return s;
}
function olive(x,y,a,rx,ry,col){
  const hl=mix(col,'#FFFFFF',0.45);
  return `<g transform="translate(${x.toFixed(1)},${y.toFixed(1)}) rotate(${a.toFixed(1)})">
    <path d="M0,0 L${rx*0.4},0" stroke="#6E6040" stroke-width="2" opacity="0.7" filter="url(#line)"/>
    <ellipse cx="${rx*1.3}" cy="0" rx="${rx}" ry="${ry}" fill="${col}" opacity="0.88" filter="${F()}"/>
    <ellipse cx="${rx*1.55}" cy="${-ry*0.35}" rx="${rx*0.32}" ry="${ry*0.22}" fill="${hl}" opacity="0.55" filter="url(#wash)"/>
  </g>`;
}
function twig(TP,w0,w1,spacing,leafBase,out,opts={}){
  out.twigs.push(taper(TP,w0,w1,opts.col||'#76664A',0.82));
  const len=Math.hypot(TP[3][0]-TP[0][0],TP[3][1]-TP[0][1]);
  const n=Math.max(2,Math.floor(len/spacing));
  for(let i=1;i<=n;i++){
    const tt=i/(n+0.5);const q=bez(...TP,tt);const qa=ang(TP,tt);
    const L=rnd(100,140)*(1-tt*0.22)*(opts.scale||1);const Wd=L*rnd(0.13,0.16);
    for(const side of [-1,1]){ if(R()<0.1) continue;
      out.leaves.push(leaf(q[0],q[1],qa+side*rnd(28,52),L,Wd,pick(leafBase)));}
  }
  out.leaves.push(leaf(TP[3][0],TP[3][1],ang(TP,1)+rnd(-8,8),rnd(115,145)*(opts.scale||1),rnd(16,20),pick(leafBase)));
}
function olivesAt(TP,k,side,out){
  const tt=rnd(0.35,0.75);const q=bez(...TP,tt);const a0=ang(TP,tt);
  for(let j=0;j<k;j++){
    out.fruit.push(olive(q[0]+rnd(-6,6),q[1]+rnd(-6,6),a0+side*(70+j*28+rnd(-10,10)),rnd(16,20),rnd(12,14),pick(['#3F3542','#4B3E4E','#55465A','#3A3138','#4A3F47'])));}
}
function oliveBranch(W,H){
  const leafBase=['#5E6B3D','#6F7B4A','#7E8A5C','#8C9673','#9AA483','#56603A','#A7AE90'];
  const out={twigs:[],leaves:[],fruit:[]};
  // main sweep along the top edge, from the top-right corner toward the left
  const P=[[W+12,34],[W*0.80,22],[W*0.55,H*0.14],[W*0.22,H*0.44]];
  // secondary drooping branch hugging the right edge
  const Q=[[W*0.93,30],[W*0.86,H*0.25],[W*0.88,H*0.48],[W*0.78,H*0.80]];
  out.twigs.push(taper(P,15,3.5,'#6E5E40',0.88));
  out.twigs.push(taper(Q,9,2.5,'#6E5E40',0.85));
  const spec=[[P,0.2,170,-14],[P,0.36,240,34],[P,0.52,200,-22],[P,0.66,220,40],[P,0.82,150,-18],[Q,0.3,170,40],[Q,0.55,160,-36],[Q,0.78,120,35]];
  spec.forEach(([B,t,len,off],idx)=>{
    const p=bez(...B,t);const a=ang(B,t)+off;const ar=a*Math.PI/180;
    const end=[p[0]+Math.cos(ar)*len,p[1]+Math.sin(ar)*len];
    const bendS=off>0?1:-1;
    const TP=[p,[p[0]+Math.cos(ar)*len*0.35,p[1]+Math.sin(ar)*len*0.35+bendS*8],[p[0]+Math.cos(ar)*len*0.7,p[1]+Math.sin(ar)*len*0.7+bendS*16],end];
    twig(TP,6,1.6,40,leafBase,out,{scale:0.95});
    if(idx===1||idx===3||idx===5) olivesAt(TP,idx===3?3:2,bendS,out);
  });
  // leaves along the main stems
  for(const [B,n,t0,t1] of [[P,22,0.03,0.97],[Q,10,0.08,0.95]]){
    for(let i=0;i<n;i++){
      const t=t0+(t1-t0)*i/(n-1);const q=bez(...B,t);const qa=ang(B,t);
      const side=i%2?1:-1;const L=rnd(105,150);
      out.leaves.push(leaf(q[0],q[1],qa+side*rnd(26,46),L,L*rnd(0.13,0.16),pick(leafBase)));
    }
    out.leaves.push(leaf(B[3][0],B[3][1],ang(B,1),rnd(130,150),19,pick(leafBase)));
  }
  out.leaves.sort(()=>R()-0.5);
  return out.twigs.join('')+out.leaves.join('')+out.fruit.join('');
}

function lavender(W,H){
  const stems=[],buds=[],leaves=[],calyx=[];
  const bx=W*0.5, by=H*0.78;
  const n=7;
  const order=[3,2,4,1,5,0,6];
  for(const i of order){
    const spread=(i-(n-1)/2)/((n-1)/2);
    const topX=W*0.5+spread*W*0.34+rnd(-15,15);const topY=H*0.05+Math.pow(Math.abs(spread),1.3)*H*0.14+rnd(0,30);
    const bottom=[bx-spread*26+rnd(-6,6),H*0.97];
    const P=[bottom,[bx+spread*6,by+20],[topX-spread*70,H*0.36],[topX,topY]];
    stems.push(taper(P,6,2.4,pick(['#8A9670','#7C8862','#93A07C']),0.88));
    const whorls=20, t0=0.58;
    for(let k=0;k<whorls;k++){
      const t=t0+k*((1-t0)/whorls);const q=bez(...P,t);const d=bezd(...P,t);
      const a=Math.atan2(d[1],d[0]);const nx=-Math.sin(a),ny=Math.cos(a);
      const prog=(t-t0)/(1-t0);
      const sz=1-prog*0.55;
      const gap=(k%3===0&&prog<0.5)?0.55:1; // occasional sparser whorls lower down
      const cnt=Math.round((5+sz*5)*gap);
      for(let m=0;m<cnt;m++){
        const off=rnd(-1,1)*15*sz;const along=rnd(-7,7);
        const x=q[0]+nx*off+Math.cos(a)*along, y=q[1]+ny*off+Math.sin(a)*along;
        const col=pick(['#8E7BAA','#B3A4C8','#7A6898','#9D8BBA','#A897C4','#6E5E8C','#C2B5D6']);
        const rx=rnd(6,9.5)*sz+2.5, ry=rnd(4,6.5)*sz+2;
        buds.push(`<ellipse cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" rx="${rx.toFixed(1)}" ry="${ry.toFixed(1)}" transform="rotate(${(a*180/Math.PI+rnd(-60,60)).toFixed(0)} ${x.toFixed(1)} ${y.toFixed(1)})" fill="${col}" opacity="${rnd(0.62,0.9).toFixed(2)}" filter="${F()}"/>`);
        if(R()<0.35) calyx.push(`<circle cx="${(x+rnd(-2,2)).toFixed(1)}" cy="${(y+rnd(-2,2)).toFixed(1)}" r="${(rnd(1.5,2.6)*sz+0.8).toFixed(1)}" fill="#4E3F66" opacity="0.5" filter="url(#line)"/>`);
      }
    }
    if(R()<0.8){const t=rnd(0.3,0.5);const q=bez(...P,t);const a=ang(P,t);
      leaves.push(leaf(q[0],q[1],a+(R()<0.5?1:-1)*rnd(12,24),rnd(100,140),rnd(6,8),pick(['#8A9670','#9AA483','#7C8862','#A7AE90']),{bend:rnd(-0.06,0.06)}));}
  }
  const rib='#C98E84', ribD='#A9685F';
  const y0=by;
  const bow=`<g filter="url(#wc1)">
    <path d="M${bx-30},${y0-9} Q${bx},${y0+4} ${bx+30},${y0-9} L${bx+30},${y0+9} Q${bx},${y0+22} ${bx-30},${y0+9}Z" fill="${rib}" opacity="0.9"/>
    <path d="M${bx},${y0} C${bx-55},${y0-65} ${bx-125},${y0-20} ${bx-78},${y0+20} C${bx-50},${y0+38} ${bx-16},${y0+12} ${bx},${y0}Z" fill="${rib}" opacity="0.82"/>
    <path d="M${bx},${y0} C${bx+55},${y0-65} ${bx+125},${y0-20} ${bx+78},${y0+20} C${bx+50},${y0+38} ${bx+16},${y0+12} ${bx},${y0}Z" fill="${rib}" opacity="0.82"/>
    <path d="M${bx-20},${y0-30} C${bx-50},${y0-45} ${bx-85},${y0-20} ${bx-70},${y0+5}" stroke="${ribD}" stroke-width="3" fill="none" opacity="0.45"/>
    <path d="M${bx+20},${y0-30} C${bx+50},${y0-45} ${bx+85},${y0-20} ${bx+70},${y0+5}" stroke="${ribD}" stroke-width="3" fill="none" opacity="0.45"/>
    <path d="M${bx-4},${y0+6} C${bx-18},${y0+55} ${bx-38},${y0+100} ${bx-64},${y0+150} L${bx-44},${y0+152} C${bx-22},${y0+108} ${bx-6},${y0+60} ${bx+4},${y0+8}Z" fill="${ribD}" opacity="0.78"/>
    <path d="M${bx+4},${y0+6} C${bx+22},${y0+52} ${bx+46},${y0+96} ${bx+78},${y0+136} L${bx+94},${y0+124} C${bx+58},${y0+92} ${bx+30},${y0+52} ${bx+8},${y0+4}Z" fill="${ribD}" opacity="0.78"/>
    <ellipse cx="${bx}" cy="${y0+2}" rx="14" ry="12" fill="${ribD}" opacity="0.95"/></g>`;
  return stems.join('')+leaves.join('')+buds.join('')+calyx.join('')+bow;
}

function crescent(r,w,a0,span,col,op){
  // filled crescent band between radius r and r-w, from angle a0 spanning span (radians), tapered ends
  const N=24;const outer=[],inner=[];
  for(let i=0;i<=N;i++){const t=i/N;const a=a0+span*t;const ww=w*Math.sin(Math.PI*t);
    outer.push([Math.cos(a)*r,Math.sin(a)*r]);inner.push([Math.cos(a)*(r-ww),Math.sin(a)*(r-ww)]);}
  const pts=outer.concat(inner.reverse());
  return `<path d="M${pts.map(p=>p[0].toFixed(1)+','+p[1].toFixed(1)).join('L')}Z" fill="${col}" opacity="${op}" filter="${F()}"/>`;
}
function rose(x,y,r,rot,base){
  const light=mix(base,'#FBF3EC',0.5), mid=base, dark=mix(base,'#5E2523',0.42);
  let s=`<g transform="translate(${x.toFixed(1)},${y.toFixed(1)}) rotate(${rot.toFixed(1)})">`;
  s+=`<circle r="${(r*1.0).toFixed(1)}" fill="${light}" opacity="0.22" filter="url(#wash)"/>`;
  s+=`<circle r="${(r*0.86).toFixed(1)}" fill="${mix(light,'#F4EDE0',0.3)}" opacity="0.95"/>`;
  // outer cupped petals
  const np=7;
  for(let i=0;i<np;i++){const a=i*360/np+rnd(-12,12);const pr=r*rnd(0.9,1.08);
    s+=`<g transform="rotate(${a.toFixed(1)})"><path d="M${pr*0.15},0 C${pr*0.35},${-pr*0.62} ${pr*1.05},${-pr*0.55} ${pr*1.02},${-pr*0.05} C${pr*1.0},${pr*0.42} ${pr*0.45},${pr*0.55} ${pr*0.15},0Z" fill="${jitter(i%2?light:mix(light,mid,0.45),8)}" opacity="0.78" filter="${F()}"/></g>`;}
  // body
  s+=`<circle r="${(r*0.66).toFixed(1)}" fill="${mix(light,mid,0.6)}" opacity="0.6" filter="${F()}"/>`;
  // concentric rolled petals (crescents), darker inward
  const rings=[[0.78,0.2,mix(mid,light,0.2),0.55],[0.6,0.18,mid,0.6],[0.44,0.16,mix(mid,dark,0.35),0.62],[0.3,0.13,mix(mid,dark,0.6),0.65]];
  rings.forEach(([rr,ww,c,op],k)=>{
    const m=k<2?3:2;
    for(let j=0;j<m;j++){const a0=rnd(0,6.28);s+=crescent(r*rr,r*ww,a0,rnd(1.6,2.4),jitter(c,6),op);}
  });
  s+=`<ellipse rx="${(r*0.14).toFixed(1)}" ry="${(r*0.1).toFixed(1)}" fill="${dark}" opacity="0.7" filter="${F()}"/>`;
  s+=`<path d="M${-r*0.12},${r*0.04} Q0,${-r*0.18} ${r*0.16},${r*0.02}" stroke="${dark}" stroke-width="${(r*0.05).toFixed(1)}" fill="none" opacity="0.55" stroke-linecap="round" filter="url(#line)"/>`;
  s+='</g>';return s;
}
function roseLeaf(x,y,a,len,base){
  const wid=len*0.34;
  const col=jitter(base,10),dark=mix(col,'#22281A',0.4),light=mix(col,'#F4EDE0',0.3);
  let pts=[];const N=24;
  for(let i=0;i<=N;i++){const t=i/N;const w=Math.sin(Math.PI*Math.pow(t,0.8))*wid*(1+((i%2)?0.05:-0.03));pts.push([t*len,-w]);}
  for(let i=N;i>=0;i--){const t=i/N;const w=Math.sin(Math.PI*Math.pow(t,0.8))*wid*(1+((i%2)?0.05:-0.03));pts.push([t*len,w]);}
  const d='M'+pts.map(p=>p[0].toFixed(1)+','+p[1].toFixed(1)).join('L')+'Z';
  return `<g transform="translate(${x.toFixed(1)},${y.toFixed(1)}) rotate(${a.toFixed(1)})">
    <path d="${d}" fill="${light}" opacity="0.3" filter="url(#wash)"/>
    <path d="${d}" fill="${col}" opacity="0.82" filter="${F()}"/>
    <path d="M0,0 ${pts.slice(0,N+1).map(p=>`L${p[0].toFixed(1)},${(p[1]*0.98).toFixed(1)}`).join('')} L${len*0.95},0Z" fill="${dark}" opacity="0.18" filter="${F()}"/>
    <path d="M0,0 L${len*0.95},0" stroke="${dark}" stroke-width="1.6" opacity="0.42" filter="url(#line)"/>
    ${[0.22,0.42,0.62].map(t=>`<path d="M${len*t},0 L${len*(t+0.16)},${-wid*0.62} M${len*t},0 L${len*(t+0.16)},${wid*0.62}" stroke="${dark}" stroke-width="1" opacity="0.28" filter="url(#line)"/>`).join('')}
  </g>`;
}
function leafSet(x,y,a,sz,cols,out){ // compound rose leaf: petiole + 3 leaflets
  const ar=a*Math.PI/180;const L=sz*1.25;
  const ex=x+Math.cos(ar)*L, ey=y+Math.sin(ar)*L;
  out.push(`<path d="M${x.toFixed(1)},${y.toFixed(1)} L${ex.toFixed(1)},${ey.toFixed(1)}" stroke="#6E6040" stroke-width="2.4" opacity="0.75" filter="url(#line)"/>`);
  const mx=x+Math.cos(ar)*L*0.45, my=y+Math.sin(ar)*L*0.45;
  out.push(roseLeaf(mx,my,a-rnd(45,60),sz*0.72,pick(cols)));
  out.push(roseLeaf(mx,my,a+rnd(45,60),sz*0.72,pick(cols)));
  out.push(roseLeaf(ex,ey,a+rnd(-10,10),sz*0.9,pick(cols)));
}
function bud(x,y,a,sz,base){
  return `<g transform="translate(${x.toFixed(1)},${y.toFixed(1)}) rotate(${a.toFixed(1)})">
   <path d="M0,0 L${sz*0.3},0" stroke="#6E6040" stroke-width="2.4" opacity="0.8"/>
   <path d="M${sz*0.2},0 C${sz*0.35},${-sz*0.6} ${sz*1.15},${-sz*0.55} ${sz*1.4},0 C${sz*1.15},${sz*0.55} ${sz*0.35},${sz*0.6} ${sz*0.2},0Z" fill="${base}" opacity="0.8" filter="${F()}"/>
   <path d="M${sz*0.7},${-sz*0.2} Q${sz*1.05},${-sz*0.35} ${sz*1.3},${-sz*0.02}" stroke="${mix(base,'#5E2523',0.4)}" stroke-width="1.6" fill="none" opacity="0.5" filter="url(#line)"/>
   <path d="M${sz*0.2},0 C${sz*0.45},${-sz*0.55} ${sz*0.75},${-sz*0.45} ${sz*0.95},${-sz*0.5} C${sz*0.7},${-sz*0.18} ${sz*0.4},${-sz*0.06} ${sz*0.2},0Z M${sz*0.2},0 C${sz*0.45},${sz*0.55} ${sz*0.75},${sz*0.45} ${sz*0.95},${sz*0.5} C${sz*0.7},${sz*0.18} ${sz*0.4},${sz*0.06} ${sz*0.2},0Z" fill="#6F7B4A" opacity="0.88" filter="${F()}"/>
  </g>`;
}
function roseVine(W,H){
  const stems=[],lv=[],fl=[],fill=[];
  const P=[[90,H*0.80],[W*0.27,H*0.20],[W*0.72,H*0.14],[W-90,H*0.72]];
  stems.push(taper(P,10,4,'#6E6040',0.88));
  for(let i=0;i<16;i++){const t=0.04+i*0.06;const q=bez(...P,t);const d=bezd(...P,t);const a=Math.atan2(d[1],d[0]);const s=(i%2?1:-1);
    const nx=-Math.sin(a)*s, ny=Math.cos(a)*s;
    stems.push(`<path d="M${(q[0]-Math.cos(a)*5).toFixed(1)},${(q[1]-Math.sin(a)*5).toFixed(1)} L${(q[0]+nx*9+Math.cos(a)*5).toFixed(1)},${(q[1]+ny*9+Math.sin(a)*5).toFixed(1)} L${(q[0]+Math.cos(a)*5).toFixed(1)},${(q[1]+Math.sin(a)*5).toFixed(1)}Z" fill="#6E6040" opacity="0.7" filter="url(#line)"/>`);}
  const leafCols=['#5E6B3D','#6F7B4A','#7E8A5C','#56603A','#8C9673'];
  const n=16;
  for(let i=0;i<n;i++){const t=0.02+0.96*i/(n-1)+rnd(-0.015,0.015);const q=bez(...P,t);const a=ang(P,t);const s=i%2?1:-1;
    leafSet(q[0],q[1],a+s*rnd(28,50),rnd(52,74),leafCols,lv);}
  const roses=[[0.14,46,'#D6A39A',1],[0.3,56,'#C98E84',-1],[0.45,62,'#D6A39A',1],[0.52,74,'#C98E84',-1],[0.62,54,'#E3BDB1',1],[0.76,50,'#B9776E',-1],[0.9,40,'#D6A39A',1]];
  roses.forEach(([t,r,c,s])=>{
    const q=bez(...P,t);const a=ang(P,t)*Math.PI/180;
    const off=r*0.5;const x=q[0]-Math.sin(a)*s*off+Math.cos(a)*rnd(-8,8), y=q[1]+Math.cos(a)*s*off;
    stems.push(`<path d="M${q[0].toFixed(1)},${q[1].toFixed(1)} L${x.toFixed(1)},${y.toFixed(1)}" stroke="#6E6040" stroke-width="3" opacity="0.8" filter="url(#line)"/>`);
    fl.push(rose(x,y,r,rnd(0,360),c));
  });
  for(const [t,s] of [[0.04,-1],[0.22,1],[0.37,-1],[0.69,1],[0.84,1],[0.97,-1]]){const q=bez(...P,t);const a=ang(P,t);
    fl.push(bud(q[0],q[1],a+s*rnd(40,70),rnd(20,27),pick(['#C98E84','#B9776E','#D6A39A'])));}
  for(let i=0;i<46;i++){const t=rnd(0.05,0.95);const q=bez(...P,t);
    const cx=q[0]+rnd(-95,95), cy=q[1]+rnd(-85,75);
    fill.push(`<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="${rnd(3.5,6.5).toFixed(1)}" fill="${pick(['#F8F1EA','#EFDCCF','#F1E3C8'])}" opacity="0.95" filter="${F()}"/>`);
    fill.push(`<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="1.4" fill="#C9A86A" opacity="0.7"/>`);}
  return stems.join('')+lv.join('')+fill.join('')+fl.join('');
}

window.build=function(kind,W,H,seed){
  R=mulberry32(seed||11);
  let body='';
  if(kind==='olive') body=oliveBranch(W,H);
  else if(kind==='lavender') body=lavender(W,H);
  else if(kind==='rose') body=roseVine(W,H);
  else if(kind.startsWith('leaf')){const cfg={leaf1:['#6F7B4A',0.06],leaf2:['#9AA483',-0.08],leaf3:['#5E6B3D',0.1]}[kind];
    const len=W*0.74, wid=len*0.15;
    body=`<g transform="translate(${W/2-len/2},${H/2})"><path d="M${-W*0.06},${len*0.01} L0,0" stroke="#6E6040" stroke-width="${W*0.012}" stroke-linecap="round" opacity="0.8"/></g>`+leaf(W/2-len/2,H/2,0,len,wid,cfg[0],{bend:cfg[1],op:0.86});}
  else if(kind.startsWith('petal')){const col=kind==='petal1'?'#D6A39A':'#C98E84';const w=W*0.78,h=H*0.82;
    const d=`M0,${h*0.44} C${-w*0.42},${h*0.2} ${-w*0.6},${-h*0.3} ${-w*0.2},${-h*0.44} Q0,${-h*0.38} ${w*0.18},${-h*0.45} C${w*0.6},${-h*0.32} ${w*0.44},${h*0.18} 0,${h*0.44}Z`;
    body=`<g transform="translate(${W/2},${H/2})">
      <path d="${d}" fill="${mix(col,'#FBF3EC',0.35)}" opacity="0.35" filter="url(#wash)"/>
      <path d="${d}" fill="${col}" opacity="0.78" filter="url(#wc2)"/>
      <ellipse cx="0" cy="${h*0.33}" rx="${w*0.1}" ry="${h*0.1}" fill="${mix(col,"#8A4A44",0.3)}" opacity="0.16" filter="url(#wash)"/>
      <path d="M${-w*0.36},${-h*0.18} C${-w*0.3},${-h*0.38} ${-w*0.12},${-h*0.42} ${-w*0.02},${-h*0.38}" stroke="${mix(col,'#FFFFFF',0.55)}" stroke-width="${W*0.03}" fill="none" opacity="0.5" stroke-linecap="round" filter="url(#wash)"/>
      <path d="M0,${h*0.38} C${w*0.04},${h*0.1} ${w*0.02},${-h*0.15} ${-w*0.04},${-h*0.32}" stroke="${mix(col,'#7A3A33',0.4)}" stroke-width="${W*0.008}" fill="none" opacity="0.28" filter="url(#line)"/>
    </g>`;}
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">${filters()}${body}</svg>`;
};
