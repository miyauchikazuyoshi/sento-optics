// === Hero Particle Animation: Delocalization ===
// Lightweight version: no createRadialGradient in loop, pure arc + fillStyle only.
// Particles have depth (size/alpha) and cool-tone hue gradient.
(function initHeroParticles() {
  const canvas = document.getElementById('hero-particles');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let W = 0, H = 0;
  let mouse = { x: -9999, y: -9999 };
  const COUNT = 90;
  const MOUSE_R = 200;

  function resize() {
    const hero = document.getElementById('hero');
    if (!hero) return;
    W = canvas.width = hero.offsetWidth;
    H = canvas.height = hero.offsetHeight;
  }

  // Simple particle
  function makeParticle() {
    const depth = Math.random();
    const homeX = Math.random() * W;
    const homeY = Math.random() * H;
    // Cool-tone hue: 200 (cyan) → 260 (blue-violet) based on x-position
    const hue = 200 + (W > 0 ? homeX / W : Math.random()) * 60 + (Math.random() - 0.5) * 15;
    // Start scattered with initial velocity — looks alive from frame 1
    const initAngle = Math.random() * Math.PI * 2;
    const initR = 20 + Math.random() * 50;
    return {
      homeX, homeY,
      x: homeX + Math.cos(initAngle) * initR,
      y: homeY + Math.sin(initAngle) * initR,
      vx: (Math.random() - 0.5) * 0.5,
      vy: (Math.random() - 0.5) * 0.5,
      depth,
      // Size: depth² for strong contrast (0.5 → 5px)
      size: 0.5 + depth * depth * 4.5,
      alpha: 0.12 + depth * 0.5,
      hue,
      phase: Math.random() * Math.PI * 2,
      freq: 0.001 + Math.random() * 0.002,
      amp: (15 + Math.random() * 25) * (0.5 + depth * 0.5),
      spread: 1, // 0=localized, 1=delocalized
      targetSpread: 1,
    };
  }

  let particles = [];

  function init() {
    resize();
    particles = [];
    for (let i = 0; i < COUNT; i++) particles.push(makeParticle());
    particles.sort((a, b) => a.depth - b.depth);
  }

  function update(p, time) {
    const dx = p.x - mouse.x;
    const dy = p.y - mouse.y;
    const dist = Math.sqrt(dx * dx + dy * dy);

    if (dist < MOUSE_R) {
      const f = (MOUSE_R - dist) / MOUSE_R;
      p.vx += (dx / (dist || 1)) * f * 0.25;
      p.vy += (dy / (dist || 1)) * f * 0.25;
      p.targetSpread = 0.05;
    } else {
      p.targetSpread = 1;
    }

    p.spread += (p.targetSpread - p.spread) * 0.015;

    const wave = Math.sin(time * p.freq + p.phase);
    const wx = wave * p.amp * p.spread * 0.4;
    const wy = Math.cos(time * p.freq * 0.7 + p.phase) * p.amp * p.spread * 0.25;

    p.vx += (p.homeX + wx - p.x) * 0.008;
    p.vy += (p.homeY + wy - p.y) * 0.008;
    p.vx *= 0.985;
    p.vy *= 0.985;
    p.x += p.vx;
    p.y += p.vy;

    if (!isFinite(p.x)) { p.x = p.homeX; p.vx = 0; }
    if (!isFinite(p.y)) { p.y = p.homeY; p.vy = 0; }
  }

  function draw(p, time) {
    const s = p.spread;
    const h = (p.hue + time * 0.001) % 360;
    const sat = 45; // desaturated, cool

    if (s > 0.3) {
      // Delocalized: soft cloud copies
      const n = 3 + Math.floor(s * 3);
      for (let i = 0; i < n; i++) {
        const a = (i / n) * Math.PI * 2 + time * 0.0003;
        const r = p.amp * 0.3 * s * (0.4 + 0.6 * Math.sin(time * 0.0008 + p.phase + i));
        const cx = p.x + Math.cos(a) * r;
        const cy = p.y + Math.sin(a) * r;
        const al = p.alpha * (0.15 + 0.2 * (1 - i / n)) * s;
        const ch = (h + i * 10) % 360;
        ctx.beginPath();
        ctx.arc(cx, cy, p.size * (0.7 + s * 0.4), 0, Math.PI * 2);
        ctx.fillStyle = `hsla(${ch},${sat}%,60%,${al})`;
        ctx.fill();
      }
      // Soft glow (single large circle, no gradient — fast)
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size * 3 + s * 8, 0, Math.PI * 2);
      ctx.fillStyle = `hsla(${h},${sat}%,55%,${0.03 * s * p.depth})`;
      ctx.fill();
    } else {
      // Localized: sharp dot
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = `hsla(${h},${sat}%,65%,${p.alpha})`;
      ctx.fill();
      // White core for near particles
      if (p.depth > 0.5) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size * 0.35, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255,255,255,${p.alpha * 0.6})`;
        ctx.fill();
      }
    }

    // Near particles get a subtle outer glow (depth-based)
    if (p.depth > 0.7) {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size * 5, 0, Math.PI * 2);
      ctx.fillStyle = `hsla(${h},${sat}%,50%,${0.025 * p.depth})`;
      ctx.fill();
    }
  }

  function drawConnections(time) {
    for (let i = 0; i < particles.length; i++) {
      const a = particles[i];
      if (a.spread > 0.5) continue;
      for (let j = i + 1; j < particles.length; j++) {
        const b = particles[j];
        if (b.spread > 0.5) continue;
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const d = dx * dx + dy * dy;
        if (d < 12000) { // ~110px
          const al = (1 - Math.sqrt(d) / 110) * 0.12;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = `hsla(220,40%,60%,${al})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
  }

  function animate(time) {
    if (W === 0 || H === 0) { resize(); }
    ctx.clearRect(0, 0, W, H);

    for (const p of particles) update(p, time);
    drawConnections(time);
    for (const p of particles) draw(p, time);

    requestAnimationFrame(animate);
  }

  // Mouse events on hero (canvas is pointer-events:none)
  const hero = document.getElementById('hero');
  hero.addEventListener('mousemove', e => {
    const r = hero.getBoundingClientRect();
    mouse.x = e.clientX - r.left;
    mouse.y = e.clientY - r.top;
  });
  hero.addEventListener('mouseleave', () => { mouse.x = mouse.y = -9999; });
  hero.addEventListener('touchmove', e => {
    const r = hero.getBoundingClientRect();
    mouse.x = e.touches[0].clientX - r.left;
    mouse.y = e.touches[0].clientY - r.top;
  }, { passive: true });
  hero.addEventListener('touchend', () => { mouse.x = mouse.y = -9999; });

  window.addEventListener('resize', () => {
    resize();
    for (const p of particles) { p.homeX = Math.random() * W; p.homeY = Math.random() * H; }
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => { init(); requestAnimationFrame(animate); });
  } else {
    init();
    requestAnimationFrame(animate);
  }
})();

// === Language Toggle ===
// Default: English. Toggle to Japanese.
let currentLang = 'en';

function applyLang() {
  document.querySelectorAll('[data-en]').forEach(el => {
    const text = el.getAttribute('data-' + currentLang);
    if (text) {
      if ((el.tagName === 'BUTTON' || el.tagName === 'A') && !el.querySelector('*')) {
        el.textContent = text;
      } else {
        el.innerHTML = text;
      }
    }
  });
  document.getElementById('lang-label').textContent = currentLang === 'en' ? 'EN' : 'JA';
  document.documentElement.lang = currentLang;
  renderOptics();
  renderPhaseDiagram();
}

function toggleLang() {
  currentLang = currentLang === 'en' ? 'ja' : 'en';
  window.location.hash = currentLang;
  applyLang();
}

// Allow hash override
if (window.location.hash === '#ja') currentLang = 'ja';
else if (window.location.hash === '#en') currentLang = 'en';

// === Presets ===
const presets = {
  diamond:  { delta: 0.05, deff: 0 },
  c60:     { delta: 0.25, deff: 0 },
  swcnt:   { delta: 0.85, deff: 1 },
  graphene:{ delta: 0.90, deff: 2 },
  graphite:{ delta: 0.88, deff: 2 },
  metal:   { delta: 0.95, deff: 3 },
};

function setPreset(name) {
  const p = presets[name];
  document.getElementById('delta-slider').value = Math.round(p.delta * 100);
  document.getElementById('deff-slider').value = p.deff;
  renderOptics();
}

// === Optical Response Demo ===
const deltaSlider = document.getElementById('delta-slider');
const deffSlider = document.getElementById('deff-slider');
if (deltaSlider) deltaSlider.addEventListener('input', renderOptics);
if (deffSlider) deffSlider.addEventListener('input', renderOptics);

function classifyOptics(delta, deff) {
  if (delta < 0.15) return { category: { en: 'Transparent', ja: '透明' }, example: { en: 'Diamond, NaCl, h-BN', ja: 'ダイヤモンド, NaCl, h-BN' }, color: '#e0f0ff', alpha: 0.15, reflectivity: 0.04 };
  if (delta < 0.5 && deff <= 0) return { category: { en: 'Colored', ja: '有色' }, example: { en: 'C60, semiconductors', ja: 'C60, 半導体' }, color: '#8b5cf6', alpha: 0.6, reflectivity: 0.1 };
  if (delta >= 0.5 && deff <= 1) return { category: { en: 'Chirality-dependent', ja: 'カイラリティ依存' }, example: { en: 'SWCNT', ja: 'SWCNT' }, color: '#22d3ee', alpha: 0.7, reflectivity: 0.2 };
  if (delta >= 0.5 && deff === 2) return { category: { en: 'Black + cleavage luster', ja: '黒 + 劈開面光沢' }, example: { en: 'Graphite', ja: 'グラファイト' }, color: '#1e293b', alpha: 0.95, reflectivity: 0.35 };
  if (delta >= 0.5 && deff >= 3) return { category: { en: 'Metallic luster', ja: '金属光沢' }, example: { en: 'Au, Ag, Cu, Al', ja: 'Au, Ag, Cu, Al' }, color: '#d4d4d8', alpha: 1.0, reflectivity: 0.9 };
  return { category: { en: 'Low response', ja: '低応答' }, example: { en: '—', ja: '—' }, color: '#334155', alpha: 0.3, reflectivity: 0.05 };
}

function renderOptics() {
  if (!deltaSlider || !deffSlider) return;
  const delta = parseInt(deltaSlider.value) / 100;
  const deff = parseInt(deffSlider.value);
  document.getElementById('delta-val').textContent = delta.toFixed(2);
  document.getElementById('deff-val').textContent = deff;

  const result = classifyOptics(delta, deff);
  document.getElementById('optics-label').textContent = result.category[currentLang];
  document.getElementById('optics-example').textContent = result.example[currentLang];

  const canvas = document.getElementById('optics-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width, h = canvas.height;
  const cx = w / 2, cy = h / 2, r = 100;

  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, w, h);

  ctx.save();
  ctx.beginPath();
  ctx.arc(cx, cy, r, 0, Math.PI * 2);
  ctx.fillStyle = result.color;
  ctx.globalAlpha = result.alpha;
  ctx.fill();
  ctx.restore();

  if (result.reflectivity > 0.1) {
    const grad = ctx.createRadialGradient(cx - 30, cy - 30, 5, cx, cy, r);
    grad.addColorStop(0, `rgba(255,255,255,${result.reflectivity})`);
    grad.addColorStop(0.4, `rgba(255,255,255,${result.reflectivity * 0.3})`);
    grad.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fillStyle = grad; ctx.fill();
  }
  if (result.reflectivity > 0.3) {
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.strokeStyle = `rgba(255,255,255,${result.reflectivity * 0.5})`; ctx.lineWidth = 2; ctx.stroke();
  }
  if (delta < 0.15) {
    ctx.save(); ctx.globalAlpha = 0.3; ctx.strokeStyle = '#64748b'; ctx.lineWidth = 0.5;
    for (let i = cx - r; i <= cx + r; i += 15) { ctx.beginPath(); ctx.moveTo(i, cy - r); ctx.lineTo(i, cy + r); ctx.stroke(); }
    for (let j = cy - r; j <= cy + r; j += 15) { ctx.beginPath(); ctx.moveTo(cx - r, j); ctx.lineTo(cx + r, j); ctx.stroke(); }
    ctx.restore();
  }
  if (delta >= 0.5 && deff === 2) {
    ctx.save(); ctx.beginPath(); ctx.moveTo(cx - r * 0.7, cy); ctx.lineTo(cx + r * 0.7, cy);
    ctx.strokeStyle = 'rgba(255,255,255,0.5)'; ctx.lineWidth = 3; ctx.lineCap = 'round'; ctx.stroke(); ctx.restore();
  }
}

// === Phase Diagram ===
const phaseRegions = [
  { id: 'ins-sol', x: 40, y: 300, w: 150, h: 140, color: 'rgba(148,163,184,0.15)', label: { en: 'Insulating\nSolid', ja: '絶縁体\n固体' }, desc: { en: 'δ_nuc ≈ 0, δ_elec low\nDiamond, NaCl, h-BN\nParticles frozen, electrons localized', ja: 'δ_nuc ≈ 0, δ_elec 低\nダイヤモンド, NaCl, h-BN\n粒子は凍結、電子は局在' } },
  { id: 'met-sol', x: 40, y: 100, w: 150, h: 140, color: 'rgba(100,150,200,0.15)', label: { en: 'Metallic\nSolid', ja: '金属\n固体' }, desc: { en: 'δ_nuc ≈ 0, δ_elec high\nCu, Fe, Al\nParticles frozen, electrons delocalized', ja: 'δ_nuc ≈ 0, δ_elec 高\nCu, Fe, Al\n粒子は凍結、電子は非局在化' } },
  { id: 'sc', x: 40, y: 30, w: 150, h: 60, color: 'rgba(129,140,248,0.2)', label: { en: 'Superconductor', ja: '超伝導体' }, desc: { en: 'δ_nuc ≈ 0, δ_elec → MAX\nNb, YBCO, MgB₂\nCooper pairs: macroscopic quantum coherence', ja: 'δ_nuc ≈ 0, δ_elec → MAX\nNb, YBCO, MgB₂\nクーパー対: マクロ量子コヒーレンス' } },
  { id: 'liq', x: 220, y: 300, w: 150, h: 140, color: 'rgba(100,180,200,0.12)', label: { en: 'Normal\nLiquid', ja: '通常の\n液体' }, desc: { en: 'δ_nuc > 0, δ_elec > 0\nWater, ethanol\nNuclei diffuse, electrons overlap → cohesion', ja: 'δ_nuc > 0, δ_elec > 0\n水, エタノール\n核は拡散、電子が重なり→凝集力' } },
  { id: 'liq-met', x: 220, y: 100, w: 150, h: 140, color: 'rgba(80,140,200,0.12)', label: { en: 'Liquid\nMetal', ja: '液体\n金属' }, desc: { en: 'δ_nuc > 0, δ_elec high\nHg, Ga(l), Na(l)\nHigh surface tension + metallic luster', ja: 'δ_nuc > 0, δ_elec 高\nHg, Ga(l), Na(l)\n高い表面張力 + 金属光沢' } },
  { id: 'gas', x: 400, y: 340, w: 160, h: 100, color: 'rgba(148,163,184,0.08)', label: { en: 'Gas', ja: '気体' }, desc: { en: 'δ_nuc high, δ_elec ≈ 0\nN₂, Ar, H₂O(g)\nNo electronic overlap → no cohesion', ja: 'δ_nuc 高, δ_elec ≈ 0\nN₂, Ar, H₂O(g)\n電子重なりなし→凝集力なし' } },
  { id: 'plasma', x: 400, y: 100, w: 160, h: 140, color: 'rgba(130,150,200,0.12)', label: { en: 'Plasma', ja: 'プラズマ' }, desc: { en: 'δ_nuc high, δ_elec high\nSolar corona, neon sign\nIonized: electrons freed from atoms', ja: 'δ_nuc 高, δ_elec 高\n太陽コロナ, ネオンサイン\nイオン化: 電子が原子から解放' } },
  { id: 'sf', x: 400, y: 30, w: 160, h: 60, color: 'rgba(120,160,220,0.15)', label: { en: 'Superfluid', ja: '超流動' }, desc: { en: 'δ_nuc → MAX, δ_elec low\nHe-4 below Tλ\nAll atoms in single macroscopic wavefunction', ja: 'δ_nuc → MAX, δ_elec 低\nHe-4 (Tλ以下)\n全原子が単一のマクロ波動関数に' } },
];

function renderPhaseDiagram() {
  const svg = document.getElementById('phase-svg');
  if (!svg) return;
  svg.innerHTML = '';
  const ns = 'http://www.w3.org/2000/svg';
  const ac = '#475569', lc = '#94a3b8';

  // Axes
  const mkLine = (x1,y1,x2,y2) => { const l = document.createElementNS(ns,'line'); l.setAttribute('x1',x1); l.setAttribute('y1',y1); l.setAttribute('x2',x2); l.setAttribute('y2',y2); l.setAttribute('stroke',ac); l.setAttribute('stroke-width','1.5'); return l; };
  svg.appendChild(mkLine(35,25,35,460));
  svg.appendChild(mkLine(35,460,575,460));

  const mkText = (x,y,text,opts) => { const t = document.createElementNS(ns,'text'); t.setAttribute('x',x); t.setAttribute('y',y); t.setAttribute('fill',lc); t.setAttribute('font-size','13'); t.setAttribute('text-anchor','middle'); if (opts?.transform) t.setAttribute('transform',opts.transform); t.textContent = text; return t; };
  svg.appendChild(mkText(15,250, currentLang==='ja'?'δ_elec (電子非局在化)':'δ_elec (electronic)', {transform:'rotate(-90 15 250)'}));
  svg.appendChild(mkText(310,490, currentLang==='ja'?'δ_nuc (核非局在化)':'δ_nuc (nuclear)'));

  // Arrows
  [{x:575,y:460,pts:p=>`${p.x},${p.y-4} ${p.x+8},${p.y} ${p.x},${p.y+4}`},{x:35,y:25,pts:p=>`${p.x-4},${p.y} ${p.x},${p.y-8} ${p.x+4},${p.y}`}].forEach(a => {
    const ar = document.createElementNS(ns,'polygon'); ar.setAttribute('fill',ac); ar.setAttribute('points',a.pts(a)); svg.appendChild(ar);
  });

  phaseRegions.forEach(region => {
    const g = document.createElementNS(ns,'g'); g.style.cursor = 'pointer';
    const rect = document.createElementNS(ns,'rect');
    ['x','y','width','height'].forEach((k,i)=>rect.setAttribute(k,[region.x,region.y,region.w,region.h][i]));
    rect.setAttribute('rx','8'); rect.setAttribute('fill',region.color); rect.setAttribute('stroke','#2a3550'); rect.setAttribute('stroke-width','1');
    g.appendChild(rect);

    region.label[currentLang].split('\n').forEach((line,i,arr) => {
      const t = document.createElementNS(ns,'text');
      t.setAttribute('x',region.x+region.w/2); t.setAttribute('y',region.y+region.h/2+(i-(arr.length-1)/2)*18);
      t.setAttribute('fill','#cbd5e1'); t.setAttribute('font-size','13'); t.setAttribute('text-anchor','middle'); t.setAttribute('dominant-baseline','central');
      t.textContent = line; g.appendChild(t);
    });

    function showTip() {
      rect.setAttribute('stroke','#38bdf8'); rect.setAttribute('stroke-width','2');
      const tt = document.getElementById('phase-tooltip'); tt.style.display='block';
      tt.innerHTML = region.desc[currentLang].replace(/\n/g,'<br>');
      const sr = svg.getBoundingClientRect();
      tt.style.left = ((region.x+region.w+10)*sr.width/600)+'px';
      tt.style.top = (region.y*sr.height/500)+'px';
    }
    function hideTip() {
      rect.setAttribute('stroke','#2a3550'); rect.setAttribute('stroke-width','1');
      document.getElementById('phase-tooltip').style.display='none';
    }
    g.addEventListener('mouseenter', showTip);
    g.addEventListener('mouseleave', hideTip);
    // Touch: tap to toggle tooltip
    g.addEventListener('click', (e) => {
      e.stopPropagation();
      const tt = document.getElementById('phase-tooltip');
      if (tt.style.display === 'block') hideTip(); else showTip();
    });
    svg.appendChild(g);
  });

  // Tap outside SVG closes tooltip (only add once)
  if (!window._phaseClickRegistered) {
    document.addEventListener('click', () => {
      const tt = document.getElementById('phase-tooltip');
      if (tt) tt.style.display = 'none';
      const s = document.getElementById('phase-svg');
      if (s) s.querySelectorAll('rect').forEach(r => { r.setAttribute('stroke','#2a3550'); r.setAttribute('stroke-width','1'); });
    });
    window._phaseClickRegistered = true;
  }
}

// === Water Heating Path Animation ===
let waterPathAnimating = false;
function animateWaterPath() {
  if (waterPathAnimating) return;
  waterPathAnimating = true;
  const svg = document.getElementById('phase-svg');
  const ns = 'http://www.w3.org/2000/svg';
  const old = document.getElementById('water-path-group'); if (old) old.remove();
  const g = document.createElementNS(ns,'g'); g.id='water-path-group'; svg.appendChild(g);
  // Cool-tone path color
  const pathColor = '#7dd3fc';
  const points = [
    {x:80,y:350,label:{en:'Ice',ja:'氷'}},{x:280,y:330,label:{en:'Water',ja:'水'}},
    {x:460,y:390,label:{en:'Steam',ja:'蒸気'}},{x:470,y:160,label:{en:'Plasma',ja:'プラズマ'}}
  ];
  let step = 0;
  function drawStep(){
    if(step>=points.length){waterPathAnimating=false;return;}
    const p=points[step];
    const c=document.createElementNS(ns,'circle'); c.setAttribute('cx',p.x); c.setAttribute('cy',p.y); c.setAttribute('r','0'); c.setAttribute('fill',pathColor); g.appendChild(c);
    let r=0; const gi=setInterval(()=>{r+=0.5;c.setAttribute('r',Math.min(r,6));if(r>=6)clearInterval(gi);},20);
    const t=document.createElementNS(ns,'text'); t.setAttribute('x',p.x); t.setAttribute('y',p.y-14); t.setAttribute('fill',pathColor); t.setAttribute('font-size','12'); t.setAttribute('font-weight','600'); t.setAttribute('text-anchor','middle'); t.setAttribute('opacity','0'); t.textContent=p.label[currentLang]; g.appendChild(t);
    let op=0; const fi=setInterval(()=>{op+=0.05;t.setAttribute('opacity',Math.min(op,1));if(op>=1)clearInterval(fi);},20);
    if(step>0){const prev=points[step-1];const l=document.createElementNS(ns,'line');l.setAttribute('x1',prev.x);l.setAttribute('y1',prev.y);l.setAttribute('x2',prev.x);l.setAttribute('y2',prev.y);l.setAttribute('stroke',pathColor);l.setAttribute('stroke-width','2');l.setAttribute('stroke-dasharray','6 4');l.setAttribute('opacity','0.7');g.appendChild(l);let pr=0;const al=setInterval(()=>{pr+=0.03;if(pr>=1){pr=1;clearInterval(al);}l.setAttribute('x2',prev.x+(p.x-prev.x)*pr);l.setAttribute('y2',prev.y+(p.y-prev.y)*pr);},16);}
    step++; setTimeout(drawStep,800);
  }
  drawStep();
}

// === Init ===
document.addEventListener('DOMContentLoaded', () => { applyLang(); });
