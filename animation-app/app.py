import os
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="🕯️ Mannequin Lamp Scene", layout="wide")
st.title("🕯️ Realistic Lamp + Mannequin Walk")

# Optional: image for mannequin texture
image_path = "/mnt/data/animated guy.webp"
texture_data_url = ""
if os.path.exists(image_path):
    with open(image_path, "rb") as f:
        texture_data_url = "data:image/webp;base64," + base64.b64encode(f.read()).decode("ascii")

# The JavaScript scene goes inside triple quotes so Python treats it as one string
html_code = f"""
<div id="container" style="width:100%; height:720px; position:relative;"></div>
<script src="https://cdn.jsdelivr.net/npm/three@0.152.2/build/three.min.js"></script>

<script>
const MANNEQUIN_TEXTURE = "{texture_data_url}";

(function(){{
  const container = document.getElementById('container');

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 100);
  camera.position.set(0, 3.0, 8);
  camera.lookAt(0, 0.6, 0);

  const renderer = new THREE.WebGLRenderer({{ antialias: true }});
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setClearColor(0x000000);
  renderer.shadowMap.enabled = true;
  container.appendChild(renderer.domElement);

  const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(40, 40),
    new THREE.MeshStandardMaterial({{ color: 0x070707, roughness: 0.95 }})
  );
  floor.rotation.x = -Math.PI/2;
  floor.position.y = -2.5;
  floor.receiveShadow = true;
  scene.add(floor);

  const ambient = new THREE.AmbientLight(0x101010);
  scene.add(ambient);

  // Lamp
  const lampY = 6.5;
  const bulb = new THREE.Mesh(
    new THREE.SphereGeometry(0.12, 16, 12),
    new THREE.MeshStandardMaterial({{ color: 0xffffee, emissive: 0xffffcc, emissiveIntensity: 3 }})
  );
  bulb.position.y = lampY - 0.42;
  scene.add(bulb);

  const spot = new THREE.SpotLight(0xfff7e6, 2.6, 30, Math.PI/6, 0.5);
  spot.position.set(0, lampY, 0);
  spot.target.position.set(0, 0.6, 0);
  spot.castShadow = true;
  scene.add(spot);
  scene.add(spot.target);

  // Mannequin
  const mannequin = new THREE.Group();
  const mat = new THREE.MeshStandardMaterial({{ color: 0x7f7f7f }});
  const torsoMat = MANNEQUIN_TEXTURE
    ? new THREE.MeshStandardMaterial({{ map: new THREE.TextureLoader().load(MANNEQUIN_TEXTURE) }})
    : mat;

  const torso = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.6, 1.4, 24), torsoMat);
  mannequin.add(torso);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.35, 24, 24), mat);
  head.position.y = 1.15;
  mannequin.add(head);
  mannequin.position.set(-3, 0, 0);
  scene.add(mannequin);

  let clock = new THREE.Clock();
  let elapsed = 0;
  let isAnimating = true;

  function animate() {{
    requestAnimationFrame(animate);
    if(isAnimating) elapsed += clock.getDelta();
    mannequin.position.x = Math.sin(elapsed) * 3;
    spot.target.position.x = mannequin.position.x;
    renderer.render(scene, camera);
  }}

  const startBtn = document.createElement('button');
  startBtn.textContent = 'Start';
  startBtn.style.position = 'absolute';
  startBtn.style.top = '10px';
  startBtn.style.left = '10px';
  startBtn.onclick = () => isAnimating = true;
  container.appendChild(startBtn);

  const stopBtn = document.createElement('button');
  stopBtn.textContent = 'Stop';
  stopBtn.style.position = 'absolute';
  stopBtn.style.top = '10px';
  stopBtn.style.left = '80px';
  stopBtn.onclick = () => isAnimating = false;
  container.appendChild(stopBtn);

  animate();
}})();
</script>
"""

components.html(html_code, height=720, scrolling=False)
