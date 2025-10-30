import os
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mannequin — Lamp Demo", layout="wide")
st.title("🕯️ Realistic Lamp + Mannequin Walk")

# Try to read uploaded image at known path and embed as data URL for client-side use
image_path = "/mnt/data/animated guy.webp"
texture_data_url = ""
if os.path.exists(image_path):
    try:
        with open(image_path, "rb") as f:
            b = f.read()
        texture_data_url = "data:image/webp;base64," + base64.b64encode(b).decode("ascii")
    except Exception as e:
        texture_data_url = ""
else:
    texture_data_url = ""  # fallback: no texture

# Inline HTML+JS. We insert texture_data_url into JS variable `MANNEQUIN_TEXTURE`.
html_code = f"""
<div id="container" style="width:100%; height:720px; position:relative;"></div>

<script src="https://cdn.jsdelivr.net/npm/three@0.152.2/build/three.min.js"></script>
<script>
const MANNEQUIN_TEXTURE = "{texture_data_url}"; // empty string if not provided

(function(){{
  const container = document.getElementById('container');

  // Scene / renderer / camera
  const scene = new THREE.Scene();
  // subtle fog kept minimal so lamp glow remains crisp
  // scene.fog = new THREE.FogExp2(0x000000, 0.01);

  const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 100);
  camera.position.set(0, 3.0, 8);
  camera.lookAt(0, 0.6, 0);

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setClearColor(0x000000); // black room
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  container.appendChild(renderer.domElement);

  // Floor
  const floorGeo = new THREE.PlaneGeometry(40, 40);
  const floorMat = new THREE.MeshStandardMaterial({ color: 0x070707, roughness: 0.95, metalness: 0.0 });
  const floor = new THREE.Mesh(floorGeo, floorMat);
  floor.rotation.x = -Math.PI/2;
  floor.position.y = -2.5;
  floor.receiveShadow = true;
  scene.add(floor);

  // Walls (dark)
  const wallMat = new THREE.MeshStandardMaterial({ color: 0x020202, roughness: 1 });
  const backWall = new THREE.Mesh(new THREE.PlaneGeometry(40, 12), wallMat);
  backWall.position.set(0, 4, -20);
  scene.add(backWall);

  const leftWall = new THREE.Mesh(new THREE.PlaneGeometry(40, 12), wallMat);
  leftWall.rotation.y = Math.PI/2;
  leftWall.position.set(-20, 4, 0);
  scene.add(leftWall);

  const rightWall = new THREE.Mesh(new THREE.PlaneGeometry(40, 12), wallMat);
  rightWall.rotation.y = -Math.PI/2;
  rightWall.position.set(20, 4, 0);
  scene.add(rightWall);

  // Ambient very dim fill so shadows aren't pure black
  const ambient = new THREE.AmbientLight(0x101010);
  scene.add(ambient);

  // Lamp: visible shade + glowing bulb + spot light
  // Lamp position
  const lampX = 0, lampY = 6.5, lampZ = 0;

  // Metal shade (visible)
  const shadeGeo = new THREE.ConeGeometry(0.7, 0.6, 32);
  const shadeMat = new THREE.MeshStandardMaterial({ color: 0x222222, metalness: 0.9, roughness: 0.25 });
  const shade = new THREE.Mesh(shadeGeo, shadeMat);
  shade.position.set(lampX, lampY - 0.2, lampZ);
  shade.rotation.x = Math.PI; // cup downward
  shade.castShadow = false;
  scene.add(shade);

  // Bulb mesh (emissive)
  const bulbGeo = new THREE.SphereGeometry(0.12, 16, 12);
  const bulbMat = new THREE.MeshStandardMaterial({ color: 0xffffee, emissive: 0xffffcc, emissiveIntensity: 3, roughness: 0.2, metalness: 0.0 });
  const bulb = new THREE.Mesh(bulbGeo, bulbMat);
  bulb.position.set(lampX, lampY - 0.42, lampZ);
  scene.add(bulb);

  // SpotLight (the actual illuminating light)
  const spot = new THREE.SpotLight(0xfff7e6, 2.6, 30, Math.PI/6, 0.5, 1);
  spot.position.set(lampX, lampY, lampZ);
  spot.castShadow = true;
  spot.shadow.mapSize.width = 2048;
  spot.shadow.mapSize.height = 2048;
  spot.shadow.radius = 6;
  spot.penumbra = 0.4;
  spot.target.position.set(0, 0.6, 0); // point at stage center initially
  scene.add(spot);
  scene.add(spot.target);

  // Add subtle point light at bulb for fill
  const bulbLight = new THREE.PointLight(0xfff3d9, 0.6, 6);
  bulbLight.position.copy(bulb.position);
  scene.add(bulbLight);

  // Volumetric cone (fake) to show the lamp's glow: transparent cone with additive blending
  const coneGeo = new THREE.ConeGeometry(2.6, 6.4, 32, 1, true);
  const coneMat = new THREE.MeshBasicMaterial({
    color: 0xfff4d6,
    transparent: true,
    opacity: 0.06,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    side: THREE.DoubleSide
  });
  const cone = new THREE.Mesh(coneGeo, coneMat);
  cone.position.set(lampX, lampY - 3.0, lampZ);
  cone.rotation.x = Math.PI; // point down
  scene.add(cone);

  // Create a procedural mannequin group
  const mannequin = new THREE.Group();

  // Material: gray
  const mannequinMat = new THREE.MeshStandardMaterial({ color: 0x7f7f7f, roughness: 0.5, metalness: 0.05 });

  // Optionally load texture for torso if image embedded
  let torsoMaterial = mannequinMat;
  if(MANNEQUIN_TEXTURE && MANNEQUIN_TEXTURE.length > 10){
    const texLoader = new THREE.TextureLoader();
    const tex = texLoader.load(MANNEQUIN_TEXTURE);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(1,1);
    torsoMaterial = new THREE.MeshStandardMaterial({ map: tex, roughness: 0.6, metalness: 0.05 });
  }

  // torso
  const torsoGeo = new THREE.CylinderGeometry(0.6, 0.6, 1.4, 24);
  const torsoMesh = new THREE.Mesh(torsoGeo, torsoMaterial);
  torsoMesh.position.y = 0.0;
  mannequin.add(torsoMesh);

  // head
  const headGeo = new THREE.SphereGeometry(0.35, 24, 24);
  const headMesh = new THREE.Mesh(headGeo, mannequinMat);
  headMesh.position.y = 1.15;
  mannequin.add(headMesh);

  // neck
  const neckGeo = new THREE.CylinderGeometry(0.15, 0.15, 0.2, 12);
  const neck = new THREE.Mesh(neckGeo, mannequinMat);
  neck.position.y = 0.9;
  mannequin.add(neck);

  // hips
  const hipGeo = new THREE.BoxGeometry(0.9, 0.25, 0.5);
  const hips = new THREE.Mesh(hipGeo, mannequinMat);
  hips.position.y = -0.55;
  mannequin.add(hips);

  // arms and legs (simplified)
  const upperArmGeo = new THREE.CylinderGeometry(0.12, 0.12, 0.8, 12);
  const lowerArmGeo = new THREE.CylinderGeometry(0.11, 0.11, 0.7, 12);
  const upperLegGeo = new THREE.CylinderGeometry(0.14, 0.14, 0.9, 12);
  const lowerLegGeo = new THREE.CylinderGeometry(0.13, 0.13, 0.9, 12);
  const footGeo = new THREE.BoxGeometry(0.28, 0.1, 0.48);

  // left upper/lower
  const leftUpper = new THREE.Mesh(upperArmGeo, mannequinMat);
  leftUpper.position.set(-0.9, 0.45, 0.0);
  leftUpper.rotation.z = Math.PI/12;
  leftUpper.name = 'leftUpper';
  mannequin.add(leftUpper);

  const leftLower = new THREE.Mesh(lowerArmGeo, mannequinMat);
  leftLower.position.set(-1.4, -0.05, 0.0);
  leftLower.rotation.z = -Math.PI/6;
  leftLower.name = 'leftLower';
  mannequin.add(leftLower);

  // right upper/lower
  const rightUpper = new THREE.Mesh(upperArmGeo, mannequinMat);
  rightUpper.position.set(0.9, 0.45, 0.0);
  rightUpper.rotation.z = -Math.PI/12;
  rightUpper.name = 'rightUpper';
  mannequin.add(rightUpper);

  const rightLower = new THREE.Mesh(lowerArmGeo, mannequinMat);
  rightLower.position.set(1.4, -0.05, 0.0);
  rightLower.rotation.z = Math.PI/6;
  rightLower.name = 'rightLower';
  mannequin.add(rightLower);

  // legs
  const leftThigh = new THREE.Mesh(upperLegGeo, mannequinMat);
  leftThigh.position.set(-0.28, -1.25, 0.0);
  leftThigh.name = 'leftThigh';
  mannequin.add(leftThigh);

  const leftShin = new THREE.Mesh(lowerLegGeo, mannequinMat);
  leftShin.position.set(-0.28, -2.05, 0.0);
  leftShin.name = 'leftShin';
  mannequin.add(leftShin);

  const rightThigh = new THREE.Mesh(upperLegGeo, mannequinMat);
  rightThigh.position.set(0.28, -1.25, 0.0);
  rightThigh.name = 'rightThigh';
  mannequin.add(rightThigh);

  const rightShin = new THREE.Mesh(lowerLegGeo, mannequinMat);
  rightShin.position.set(0.28, -2.05, 0.0);
  mannequin.add(rightShin);

  const leftFoot = new THREE.Mesh(footGeo, mannequinMat);
  leftFoot.position.set(-0.28, -2.45, 0.12);
  mannequin.add(leftFoot);

  const rightFoot = new THREE.Mesh(footGeo, mannequinMat);
  rightFoot.position.set(0.28, -2.45, 0.12);
  mannequin.add(rightFoot);

  // set shadows for mannequin parts
  mannequin.traverse(obj => {{
    if(obj.isMesh) {{
      obj.castShadow = true;
      obj.receiveShadow = false;
    }}
  }});

  // initial position
  const walkDistance = 6;
  mannequin.position.set(-walkDistance/2, 0, 0);
  scene.add(mannequin);

  // subtle rim fill light
  const rim = new THREE.PointLight(0x404050, 0.3, 10);
  rim.position.set(-4, 3, 5);
  scene.add(rim);

  // walking animation helpers
  const clock = new THREE.Clock();
  let elapsed = 0;
  const walkSpeed = 0.9;

  // Update function
  function update() {{
    const dt = clock.getDelta();
    if(isAnimating) elapsed += dt;

    // walking phase using sine for smooth back/forth
    const phase = elapsed * walkSpeed;
    const x = Math.sin(phase) * (walkDistance/2);
    mannequin.position.x = x;

    // torso bob
    torsoY = 0.12 * Math.abs(Math.sin(phase * 2));
    torsoMesh.position.y = torsoY;

    // limb swing
    const swing = Math.sin(phase * 2) * 0.6;

    const lu = mannequin.getObjectByName('leftUpper');
    const ru = mannequin.getObjectByName('rightUpper');
    const ll = mannequin.getObjectByName('leftLower');
    const rl = mannequin.getObjectByName('rightLower');
    const lt = mannequin.getObjectByName('leftThigh');
    const rt = mannequin.getObjectByName('rightThigh');
    const ls = mannequin.getObjectByName('leftShin');
    const rs = mannequin.getObjectByName('rightShin');

    if(lu && ru) {{
      lu.rotation.x = 0.2 + swing * 0.5;
      ru.rotation.x = 0.2 - swing * 0.5;
    }}
    if(ll && rl) {{
      ll.rotation.x = -0.4 + (-swing) * 0.2;
      rl.rotation.x = -0.4 + (swing) * 0.2;
    }}
    if(lt && rt) {{
      lt.rotation.x = 0.2 + (-swing) * 0.7;
      rt.rotation.x = 0.2 + (swing) * 0.7;
    }}
    if(ls && rs) {{
      ls.rotation.x = -0.2 + Math.max(0, -swing) * 0.5;
      rs.rotation.x = -0.2 + Math.max(0, swing) * 0.5;
    }}

    // spotlight target follows mannequin center for dramatic lighting
    spot.target.position.set(mannequin.position.x, 0.6, 0);

    // bulb flicker (tiny natural variation)
    const flicker = 1.0 + Math.sin(elapsed * 12.0) * 0.02;
    bulb.material.emissiveIntensity = 3.0 * flicker;
    bulbLight.intensity = 0.6 * flicker;
    spot.intensity = 2.6 * (0.95 + Math.abs(Math.sin(elapsed * 1.2)) * 0.05);

    renderer.render(scene, camera);
  }}

  // loop
  function loop() {{
    requestAnimationFrame(loop);
    update();
  }}

  // Buttons inside the container (so they appear in the same iframe)
  const startBtn = document.createElement('button');
  startBtn.textContent = 'Start';
  startBtn.style.position = 'absolute';
  startBtn.style.top = '10px';
  startBtn.style.left = '10px';
  startBtn.style.padding = '8px 12px';
  startBtn.onclick = function() {{ isAnimating = true; clock.start(); }};

  const stopBtn = document.createElement('button');
  stopBtn.textContent = 'Stop';
  stopBtn.style.position = 'absolute';
  stopBtn.style.top = '10px';
  stopBtn.style.left = '80px';
  stopBtn.style.padding = '8px 12px';
  stopBtn.onclick = function() {{ isAnimating = false; clock.stop(); }};

  container.appendChild(startBtn);
  container.appendChild(stopBtn);

  // resize
  window.addEventListener('resize', () => {{
    const w = container.clientWidth;
    const h = container.clientHeight;
    renderer.setSize(w,h);
    camera.aspect = w/h;
    camera.updateProjectionMatrix();
  }});

  // start
  clock.start();
  isAnimating = true;
  loop();

}})(); // IIFE
</script>
"""

components.html(html_code, height=720, scrolling=False)
