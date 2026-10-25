// Hunch laptop station: a laptop on a stand near the start point. Walk up, press F (or tap the
// prompt) and the real Hunch "Hotspots & 3D Offices" view opens on its screen. Clicking a
// hotspot card walks you into that city's office render.
import * as THREE from 'three';

// Hunch hotspot id (data-hcity) → office render
export const CITY_PAGES = {
  kazakhstan: 'astana-office.html',
  slc: 'slc-office.html',
  dallas: 'dallas-office.html',
};

const REACH = 1.6; // how close you need to be to open it (world units)

function screenTexture() {
  const c = document.createElement('canvas'); c.width = 512; c.height = 320;
  const g = c.getContext('2d');
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const draw = (logo) => {
    g.fillStyle = '#FAF9F6'; g.fillRect(0, 0, 512, 320);
    g.fillStyle = '#171716'; g.fillRect(0, 0, 512, 44);
    if (logo) g.drawImage(logo, 14, 7, 30, 30);
    g.fillStyle = '#FAF9F6'; g.font = '600 20px Inter, system-ui, sans-serif'; g.fillText('Hunch', 52, 29);
    g.fillStyle = '#171716'; g.font = 'italic 34px "Instrument Serif", Georgia, serif'; g.fillText('Hotspots & 3D Offices', 24, 100);
    const rows = [['Astana / Almaty', '84%'], ['Salt Lake City', '89%'], ['Dallas', '91%']];
    rows.forEach(([n, p], i) => {
      const y = 132 + i * 50;
      g.fillStyle = '#FFFFFF'; g.fillRect(24, y, 464, 40);
      g.strokeStyle = '#E4E1DA'; g.strokeRect(24, y, 464, 40);
      g.fillStyle = '#171716'; g.font = '500 18px Inter, system-ui, sans-serif'; g.fillText(n, 38, y + 26);
      g.fillStyle = '#E1381C'; g.fillText(p + ' Hot', 400, y + 26);
    });
    g.fillStyle = '#6B6860'; g.font = '500 15px Inter, system-ui, sans-serif'; g.fillText('Press F to open', 24, 304);
    tex.needsUpdate = true;
  };
  draw(null);
  const img = new Image(); img.onload = () => draw(img); img.src = '/logo.svg';
  return tex;
}

function buildLaptop() {
  const g = new THREE.Group();
  const alu = new THREE.MeshStandardMaterial({ color: 0xb9bcc1, metalness: 0.7, roughness: 0.35 });
  const dark = new THREE.MeshStandardMaterial({ color: 0x1b1c1e, roughness: 0.6 });
  // stand: a slim pedestal so the station works whatever furniture the room has
  const top = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.025, 0.34), new THREE.MeshStandardMaterial({ color: 0x2a2b2d, roughness: 0.5 }));
  g.add(top);
  const post = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 1, 12), dark);
  post.name = 'post'; g.add(post);
  const foot = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.18, 0.02, 24), dark);
  foot.name = 'foot'; g.add(foot);
  // laptop
  const base = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.012, 0.22), alu);
  base.position.y = 0.019; g.add(base);
  const keys = new THREE.Mesh(new THREE.PlaneGeometry(0.27, 0.1), dark);
  keys.rotation.x = -Math.PI / 2; keys.position.set(0, 0.026, -0.02); g.add(keys);
  const lid = new THREE.Group(); lid.position.set(0, 0.025, -0.11); lid.rotation.x = -0.28; g.add(lid);
  const shell = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.21, 0.008), alu);
  shell.position.y = 0.105; lid.add(shell);
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(0.3, 0.188), new THREE.MeshBasicMaterial({ map: screenTexture(), toneMapped: false }));
  screen.position.set(0, 0.105, 0.0045); lid.add(screen);
  // soft glow so it reads as "on" from a distance
  const glow = new THREE.PointLight(0xfff2e0, 0.4, 1.2); glow.position.set(0, 0.15, 0.1); g.add(glow);
  return g;
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
  // you're already standing in the render, so the laptop's Hunch shows the city model instead
  // (set the mode directly: Hunch may not have wired its toggle yet, but it checks this before loading)
  const stage = doc.getElementById('app-canvas-box');
  if (stage) stage.dataset.mode = 'model';
  doc.querySelectorAll('.app-render-toggle button').forEach(el => el.classList.toggle('active', el.dataset.rmode === 'model'));
  doc.getElementById('app-office-render')?.removeAttribute('src');
  // land on the card for the city you're in, with the city list in view
  doc.querySelector(`.app-hs-card[data-hcity="${city}"]`)?.click();
  setTimeout(() => doc.getElementById('app-hotspot-list')?.scrollIntoView({ block: 'start' }), 300);
}

export function setupStation({ scene, camera, renderer, pos, getYaw, city }) {
  const laptop = buildLaptop();
  // a metre or so in front of the start view, a little to the right, turned to face you
  const yaw = getYaw();
  const fwd = new THREE.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw));
  const right = new THREE.Vector3(Math.cos(yaw), 0, -Math.sin(yaw));
  const spot = pos.clone().addScaledVector(fwd, 1.05).addScaledVector(right, 0.35);
  laptop.position.set(spot.x, pos.y - 0.32, spot.z);
  laptop.lookAt(pos.x, laptop.position.y, pos.z);
  scene.add(laptop);

  let open = false;
  const close = () => {
    open = false; ui.wrap.style.display = 'none';
  };
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
  // clicking the laptop itself also opens it
  const ray = new THREE.Raycaster(), center = new THREE.Vector2(0, 0);
  renderer.domElement.addEventListener('click', () => {
    if (!near) return;
    ray.setFromCamera(center, camera);
    if (ray.intersectObject(laptop, true).length) openLaptop();
  });

  return {
    isOpen: () => open,
    // drop the stand to the floor once the room's floor height is known
    setFloor(floorDist) {
      if (!isFinite(floorDist)) return;
      const h = Math.max(0.2, floorDist - 0.32);
      const post = laptop.getObjectByName('post'), foot = laptop.getObjectByName('foot');
      post.scale.y = h; post.position.y = -h / 2;
      foot.position.y = -h;
    },
    update() {
      near = !open && pos.distanceTo(laptop.position.clone().setY(pos.y)) < REACH;
      ui.prompt.style.display = near ? 'block' : 'none';
    },
  };
}
