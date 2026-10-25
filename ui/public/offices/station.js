// Hunch laptop station: a laptop sitting on a real table in the render. Walk up to it, press F
// (or click it, or tap the prompt) and the real Hunch "Hotspots & 3D Offices" view opens on its
// screen. Clicking a hotspot card walks you into that city's office render.
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

// Hunch hotspot id (data-hcity) → office render
export const CITY_PAGES = {
  kazakhstan: 'astana-office.html',
  slc: 'slc-office.html',
  dallas: 'dallas-office.html',
};

const REACH_M = 1.8;            // how close you need to be to open it, in metres
const TABLE_MIN_M = 0.6;        // what counts as a tabletop, in metres above the floor
const TABLE_MAX_M = 1.15;

function screenTexture() {
  const c = document.createElement('canvas'); c.width = 1024; c.height = 656;
  const g = c.getContext('2d');
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const draw = (logo) => {
    g.fillStyle = '#FAF9F6'; g.fillRect(0, 0, 1024, 656);
    g.fillStyle = '#171716'; g.fillRect(0, 0, 1024, 84);
    if (logo) g.drawImage(logo, 26, 16, 52, 52);
    g.fillStyle = '#FAF9F6'; g.font = '600 36px Inter, system-ui, sans-serif'; g.fillText('Hunch', 96, 56);
    g.fillStyle = '#171716'; g.font = 'italic 64px "Instrument Serif", Georgia, serif'; g.fillText('Hotspots & 3D Offices', 48, 190);
    [['Astana / Almaty, Kazakhstan', '84%'], ['Salt Lake City, Utah', '89%'], ['Dallas, Texas', '91%']].forEach(([n, p], i) => {
      const y = 250 + i * 104;
      g.fillStyle = '#FFFFFF'; g.fillRect(48, y, 928, 84);
      g.strokeStyle = '#E4E1DA'; g.lineWidth = 3; g.strokeRect(48, y, 928, 84);
      g.fillStyle = '#171716'; g.font = '500 34px Inter, system-ui, sans-serif'; g.fillText(n, 76, y + 54);
      g.fillStyle = '#E1381C'; g.font = '600 32px Inter, system-ui, sans-serif'; g.fillText(p + ' Hot', 820, y + 54);
    });
    g.fillStyle = '#6B6860'; g.font = '500 28px Inter, system-ui, sans-serif'; g.fillText('Press F to open', 48, 626);
    tex.needsUpdate = true;
  };
  draw(null);
  const img = new Image(); img.onload = () => draw(img); img.src = '/logo.svg';
  return tex;
}

// soft dark blob that grounds the laptop on the photographed tabletop
function contactShadow() {
  const c = document.createElement('canvas'); c.width = c.height = 128;
  const g = c.getContext('2d');
  const grd = g.createRadialGradient(64, 64, 8, 64, 64, 64);
  grd.addColorStop(0, 'rgba(0,0,0,0.55)'); grd.addColorStop(1, 'rgba(0,0,0,0)');
  g.fillStyle = grd; g.fillRect(0, 0, 128, 128);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(0.42, 0.32),
    new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(c), transparent: true, depthWrite: false }));
  m.rotation.x = -Math.PI / 2; m.position.y = 0.0008;
  return m;
}

// A 13-inch aluminium laptop, built in metres: body, keyboard, trackpad, hinged lid with display.
function buildLaptop() {
  const g = new THREE.Group();
  const alu = new THREE.MeshStandardMaterial({ color: 0x8a8d92, metalness: 0.9, roughness: 0.32 });
  const keyMat = new THREE.MeshStandardMaterial({ color: 0x141416, roughness: 0.55 });
  const well = new THREE.MeshStandardMaterial({ color: 0x5c5f64, metalness: 0.8, roughness: 0.45 });
  const W = 0.304, D = 0.215, T = 0.0155;

  g.add(contactShadow());
  const base = new THREE.Mesh(new RoundedBoxGeometry(W, T, D, 4, 0.006), alu);
  base.position.y = T / 2; g.add(base);
  const top = T + 0.0002;
  // keyboard well and keys
  const kw = new THREE.Mesh(new THREE.PlaneGeometry(0.276, 0.118), well);
  kw.rotation.x = -Math.PI / 2; kw.position.set(0, top, -0.033); g.add(kw);
  const cols = 14, rows = 6, ks = 0.0158, gap = 0.0033;
  const keys = new THREE.InstancedMesh(new RoundedBoxGeometry(ks, 0.0016, ks, 2, 0.0012), keyMat, cols * rows);
  const o = new THREE.Object3D(); let i = 0;
  const pitch = ks + gap, x0 = -((cols - 1) * pitch) / 2;
  for (let r = 0; r < rows; r++) for (let k = 0; k < cols; k++) {
    o.position.set(x0 + k * pitch, top + 0.0008, -0.081 + r * pitch);
    o.scale.set(1, 1, r === 0 ? 0.55 : 1); // slim function-key row
    if (r === rows - 1 && k >= 4 && k <= 9) {
      // one wide spacebar in place of keys 4–9
      o.scale.set(k === 4 ? (6 * pitch - gap) / ks : 0, 1, 1);
      o.position.x = x0 + 6.5 * pitch;
    }
    o.updateMatrix(); keys.setMatrixAt(i++, o.matrix);
  }
  g.add(keys);
  // trackpad
  const pad = new THREE.Mesh(new RoundedBoxGeometry(0.128, 0.0006, 0.08, 2, 0.004),
    new THREE.MeshStandardMaterial({ color: 0x7c7f84, metalness: 0.75, roughness: 0.22 }));
  pad.position.set(0, top, 0.058); g.add(pad);
  // lid, hinged at the back edge and opened about 110°
  const lid = new THREE.Group(); lid.position.set(0, T, -D / 2 + 0.004); lid.rotation.x = -0.33; g.add(lid);
  const shell = new THREE.Mesh(new RoundedBoxGeometry(W, 0.212, 0.0055, 4, 0.005), alu);
  shell.position.set(0, 0.106, -0.0028); lid.add(shell);
  const bezel = new THREE.Mesh(new THREE.PlaneGeometry(0.296, 0.205), new THREE.MeshStandardMaterial({ color: 0x0b0b0c, roughness: 0.2 }));
  bezel.position.set(0, 0.106, 0.0001); lid.add(bezel);
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(0.284, 0.182), new THREE.MeshBasicMaterial({ map: screenTexture(), toneMapped: false }));
  screen.position.set(0, 0.108, 0.0003); lid.add(screen);
  const hinge = new THREE.Mesh(new THREE.CylinderGeometry(0.0045, 0.0045, 0.24, 16), well);
  hinge.rotation.z = Math.PI / 2; hinge.position.set(0, T, -D / 2 + 0.004); g.add(hinge);
  // the screen's own light spilling onto the keyboard
  const glow = new THREE.PointLight(0xf3f6ff, 0.25, 0.6); glow.position.set(0, 0.12, 0.06); g.add(glow);
  return g;
}

// floating marker so you can find the laptop from across the room
function marker() {
  const c = document.createElement('canvas'); c.width = 256; c.height = 72;
  const g = c.getContext('2d');
  g.fillStyle = 'rgba(23,23,22,.88)'; g.beginPath(); g.roundRect(2, 2, 252, 68, 34); g.fill();
  g.fillStyle = '#E1381C'; g.beginPath(); g.arc(40, 36, 10, 0, 7); g.fill();
  g.fillStyle = '#FAF9F6'; g.font = '600 30px Inter, system-ui, sans-serif'; g.fillText('Hunch', 62, 47);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, depthTest: false, transparent: true }));
  s.scale.set(0.2, 0.056, 1); s.renderOrder = 10;
  return s;
}

function overlayDom(city, onClose) {
  const css = document.createElement('style');
  css.textContent = `
    #hunch-prompt{position:fixed;left:50%;bottom:28px;transform:translateX(-50%);background:rgba(23,23,22,.86);color:#FAF9F6;
      font:500 14px Inter,system-ui,sans-serif;padding:10px 16px;border-radius:999px;border:0;cursor:pointer;display:none;z-index:20}
    #hunch-prompt b{color:#E1381C}
    #hunch-laptop{position:fixed;inset:0;display:none;align-items:center;justify-content:center;flex-direction:column;
      background:rgba(10,10,10,.55);backdrop-filter:blur(3px);z-index:30;padding:16px;box-sizing:border-box}
    #hunch-laptop .lid{width:min(1180px,96vw);aspect-ratio:16/10;max-height:84vh;background:#1b1c1e;border-radius:18px 18px 6px 6px;
      padding:14px 14px 22px;box-sizing:border-box;box-shadow:0 30px 80px rgba(0,0,0,.5);position:relative}
    #hunch-laptop .lid::after{content:"";position:absolute;bottom:7px;left:50%;width:6px;height:6px;margin-left:-3px;border-radius:50%;background:#333}
    #hunch-laptop iframe{width:100%;height:100%;border:0;border-radius:6px;background:#FAF9F6}
    #hunch-laptop .base{width:min(1260px,100vw);height:14px;background:linear-gradient(#c9ccd1,#9a9da2);border-radius:0 0 14px 14px}
    #hunch-laptop .close{margin-top:14px;background:#FAF9F6;color:#171716;border:0;border-radius:999px;padding:8px 16px;
      font:600 13px Inter,system-ui,sans-serif;cursor:pointer}`;
  document.head.appendChild(css);
  const prompt = document.createElement('button');
  prompt.id = 'hunch-prompt'; prompt.innerHTML = 'Press <b>F</b> to open the Hunch laptop';
  document.body.appendChild(prompt);
  const wrap = document.createElement('div');
  wrap.id = 'hunch-laptop';
  wrap.innerHTML = `<div class="lid"><iframe title="Hunch hotspots"></iframe></div><div class="base"></div>
    <button class="close" type="button">Close laptop (Esc)</button>`;
  document.body.appendChild(wrap);
  wrap.querySelector('.close').onclick = onClose;
  const frame = wrap.querySelector('iframe');
  frame.addEventListener('load', () => wireHunch(frame, city));
  return { prompt, wrap, frame };
}

// Make each hotspot card in the Hunch page a door to that city's office.
function wireHunch(frame, city) {
  let doc;
  try { doc = frame.contentDocument; } catch { return; }
  if (!doc) return;
  const st = doc.createElement('style');
  st.textContent = `.app-hs-card[data-hcity]{cursor:pointer}
    .hunch-go{display:inline-block;margin-top:8px;font:600 12px Inter,system-ui,sans-serif;color:#FFF;background:#171716;
      padding:5px 10px;border-radius:999px}
    .hunch-go.here{background:#E1381C}`;
  doc.head.appendChild(st);
  doc.querySelectorAll('.app-hs-card[data-hcity]').forEach(card => {
    const id = card.dataset.hcity, page = CITY_PAGES[id];
    if (!page) return;
    const tag = doc.createElement('span');
    tag.className = 'hunch-go' + (id === city ? ' here' : '');
    tag.textContent = id === city ? 'You are here' : 'Walk into this office →';
    card.appendChild(tag);
    card.addEventListener('click', () => { if (id !== city) location.href = page; });
  });
  // land on the card for the city you're in, with the city list in view
  // Hunch wires its cards only after its data fetch, so wait until its 3D stage has loaded a render
  const card = doc.querySelector(`.app-hs-card[data-hcity="${city}"]`);
  const ready = setInterval(() => {
    if (!doc.getElementById('app-office-render')?.getAttribute('src')) return;
    clearInterval(ready);
    card?.click();
  }, 150);
  setTimeout(() => clearInterval(ready), 8000);
  setTimeout(() => doc.getElementById('app-hotspot-list')?.scrollIntoView({ block: 'start' }), 300);
}

// table: {x, z} in world units, a spot on a real tabletop picked from the collider; optional h is
// the tabletop height in metres when the collider can't be trusted there.
// metersPerUnit: the world's metric_scale_factor from World Labs.
export function setupStation({ scene, camera, renderer, pos, city, table, metersPerUnit }) {
  const unit = 1 / metersPerUnit; // one metre, in world units
  const laptop = buildLaptop();
  laptop.scale.setScalar(unit);
  laptop.visible = false; // shown once it has been set down on the table
  scene.add(laptop);
  const pin = marker(); pin.scale.multiplyScalar(unit * 2.2); pin.visible = false; scene.add(pin);

  // light and reflections for the laptop only (the splats are unlit)
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8a8478, 0.9));

  let open = false;
  const close = () => { open = false; ui.wrap.style.display = 'none'; };
  const ui = overlayDom(city, close);
  const openLaptop = () => {
    if (open) return;
    open = true;
    document.exitPointerLock?.();
    if (!ui.frame.src) ui.frame.src = '/index.html?view=hotspots';
    ui.wrap.style.display = 'flex';
    ui.prompt.style.display = 'none';
  };
  ui.prompt.onclick = (e) => { e.stopPropagation(); openLaptop(); };
  let near = false;
  addEventListener('keydown', e => {
    if (e.code === 'KeyF' && near) openLaptop();
    else if (e.code === 'Escape' && open) close();
  });
  const ray = new THREE.Raycaster(), center = new THREE.Vector2(0, 0);
  renderer.domElement.addEventListener('click', () => {
    if (!near) return;
    ray.setFromCamera(center, camera);
    if (ray.intersectObject(laptop, true).length) openLaptop();
  });

  return {
    isOpen: () => open,
    // Set the laptop down on the tabletop once the collider is in: probe straight down around the
    // chosen spot and take the closest point that sits at table height.
    setFloor(floorDist, surfaceAt) {
      if (!isFinite(floorDist) || !table) return;
      const floorY = pos.y - floorDist;
      let best = null;
      // a thin bar the collider barely catches can give its height directly (table.h, metres)
      if (table.h) best = { x: table.x, y: floorY + table.h * unit, z: table.z };
      else for (let r = 0; r <= 0.4; r += 0.05) for (let a = 0; a < (r ? 12 : 1); a++) {
        const x = table.x + Math.cos(a / 12 * Math.PI * 2) * r * unit, z = table.z + Math.sin(a / 12 * Math.PI * 2) * r * unit;
        const y = surfaceAt(x, z);
        if (y === null) continue;
        const h = (y - floorY) / unit;
        if (h > TABLE_MIN_M && h < TABLE_MAX_M) { best = { x, y, z }; break; }
      }
      if (!best) best = { x: table.x, y: floorY + 0.9 * unit, z: table.z };
      // the collider runs a little under the photographed surface, so lift it to sit on top
      laptop.position.set(best.x, best.y + 0.025 * unit, best.z);
      // screen facing where you start
      laptop.rotation.y = Math.atan2(pos.x - best.x, pos.z - best.z);
      pin.position.set(best.x, best.y + 0.42 * unit, best.z);
      laptop.visible = pin.visible = true;
    },
    update() {
      if (!laptop.visible) return;
      const d = Math.hypot(pos.x - laptop.position.x, pos.z - laptop.position.z) / unit;
      near = !open && d < REACH_M;
      ui.prompt.style.display = near ? 'block' : 'none';
      pin.visible = d > 1.2; // the marker only matters from a distance
    },
  };
}
