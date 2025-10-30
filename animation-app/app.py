import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="🎬 3D Cutscene (Smooth)", layout="wide")
st.title("🎬 Smooth 3D Cutscene Animation Example")

html_code = """
<div id="container" style="width:100%; height:700px;"></div>

<script src="https://cdn.jsdelivr.net/npm/three@0.152.2/build/three.min.js"></script>

<script>
let scene, camera, renderer, sphere, floor, light;
let isAnimating = false;
let velocity = 0.05;
let direction = 1;
let time = 0;
let currentScene = 0;

// Camera positions for each scene
const cameraPositions = [
  new THREE.Vector3(0, 5, 10),  // Scene 1 - wide
  new THREE.Vector3(5, 2, 5),   // Scene 2 - side
  new THREE.Vector3(0, 10, 0)   // Scene 3 - overhead
];
let targetPos = cameraPositions[0].clone();

function init() {
  const container = document.getElementById('container');

  scene = new THREE.Scene();
  scene.fog = new THREE.Fog(0x000000, 10, 40);

  camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setClearColor(0x000000);
  renderer.shadowMap.enabled = true;
  container.appendChild(renderer.domElement);

  // Sphere (bouncing ball)
  const sphereGeo = new THREE.SphereGeometry(1, 32, 32);
  const sphereMat = new THREE.MeshStandardMaterial({ color: 0x0077ff, roughness: 0.3, metalness: 0.6 });
  sphere = new THREE.Mesh(sphereGeo, sphereMat);
  sphere.castShadow = true;
  scene.add(sphere);

  // Floor
  const floorGeo = new THREE.PlaneGeometry(30, 30);
  const floorMat = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 1 });
  floor = new THREE.Mesh(floorGeo, floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -2.5;
  floor.receiveShadow = true;
  scene.add(floor);

  // Lights
  const ambient = new THREE.AmbientLight(0x404040);
  scene.add(ambient);

  light = new THREE.SpotLight(0xffffff, 2);
  light.position.set(5, 5, 5);
  light.castShadow = true;
  light.angle = Math.PI / 5;
  light.penumbra = 0.3;
  scene.add(light);

  camera.position.copy(cameraPositions[0]);
  camera.lookAt(0, 0, 0);

  renderer.render(scene, camera);
}

function animate() {
  if (!isAnimating) return;
  requestAnimationFrame(animate);
  time += 1;

  // Bounce the ball
  sphere.position.y += velocity * direction;
  if (sphere.position.y > 2 || sphere.position.y < -2) direction *= -1;

  // Every 200 frames, change scene
  if (time % 200 === 0) {
    currentScene = (currentScene + 1) % cameraPositions.length;
    targetPos.copy(cameraPositions[currentScene]);
  }

  // Smoothly move camera toward target position
  camera.position.lerp(targetPos, 0.02);
  camera.lookAt(sphere.position);

  // Keep the light following the camera
  light.position.copy(camera.position);

  renderer.render(scene, camera);
}

function startAnimation() {
  if (!isAnimating) {
    isAnimating = true;
    animate();
  }
}

function stopAnimation() {
  isAnimating = false;
}

// UI Buttons
const containerDiv = document.getElementById('container');
const startBtn = document.createElement('button');
startBtn.innerHTML = '🎬 Start Cutscene';
startBtn.style.position = 'absolute';
startBtn.style.top = '10px';
startBtn.style.left = '10px';
startBtn.onclick = startAnimation;

const stopBtn = document.createElement('button');
stopBtn.innerHTML = '⏹ Stop';
stopBtn.style.position = 'absolute';
stopBtn.style.top = '10px';
stopBtn.style.left = '150px';
stopBtn.onclick = stopAnimation;

containerDiv.appendChild(startBtn);
containerDiv.appendChild(stopBtn);

window.addEventListener('resize', () => {
  camera.aspect = containerDiv.clientWidth / containerDiv.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(containerDiv.clientWidth, containerDiv.clientHeight);
});

init();
</script>
"""

components.html(html_code, height=700, scrolling=False)
