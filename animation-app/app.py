import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mannequin Walk Demo", layout="wide")
st.title("🕯️ Mannequin Walk — Procedural 3D Scene")

html_code = """
<div id="container" style="width:100%; height:720px; position:relative;"></div>

<!-- load Three.js -->
<script src="https://cdn.jsdelivr.net/npm/three@0.152.2/build/three.min.js"></script>

<script>
(function(){
  // --- scene variables ---
  let container = document.getElementById('container');
  let scene, camera, renderer;
  let mannequin = new THREE.Group();
  let clock = new THREE.Clock();
  let lamp;
  let isAnimating = true;

  // walking parameters
  let walkDistance = 6;     // how far left-right the mannequin walks (total)
  let walkSpeed = 0.8;      // how fast the mannequin moves along path
  let torso;                // reference to torso for slight bob
  let direction = 1;        // moving +x or -x

  // init
  function init(){
    // renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setClearColor(0x000000); // black background
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    // attach
    container.appendChild(renderer.domElement);

    // scene
    scene = new THREE.Scene();

    // camera
    camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 100);
    camera.position.set(0, 3, 10);
    camera.lookAt(0, 0.7, 0);

    // floor (receives shadow)
    const floorGeo = new THREE.PlaneGeometry(40, 40);
    const floorMat = new THREE.MeshStandardMaterial({ color: 0x070707, roughness: 0.9, metalness: 0.0 });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.position.y = -2.5;
    floor.receiveShadow = true;
    scene.add(floor);

    // 4 dark walls to form a simple room (subtle, not fully enclosing)
    const wallMat = new THREE.MeshStandardMaterial({ color: 0x020202, roughness: 1 });
    const wallGeoW = new THREE.PlaneGeometry(40, 12);

    const backWall = new THREE.Mesh(wallGeoW, wallMat);
    backWall.position.set(0, 4, -20);
    scene.add(backWall);

    const leftWall = new THREE.Mesh(wallGeoW, wallMat);
    leftWall.rotation.y = Math.PI / 2;
    leftWall.position.set(-20, 4, 0);
    scene.add(leftWall);

    const rightWall = new THREE.Mesh(wallGeoW, wallMat);
    rightWall.rotation.y = -Math.PI / 2;
    rightWall.position.set(20, 4, 0);
    scene.add(rightWall);

    // Ambient subtle fill (very dim)
    const amb = new THREE.AmbientLight(0x202020);
    scene.add(amb);

    // Hanging lamp - a physical spot light with soft shadow
    lamp = new THREE.SpotLight(0xffffff, 2.2, 30, Math.PI/6, 0.4, 1);
    lamp.position.set(0, 6.5, 0);
    lamp.castShadow = true;
    lamp.shadow.mapSize.width = 2048;
    lamp.shadow.mapSize.height = 2048;
    lamp.shadow.radius = 8;
    scene.add(lamp);

    // small lamp geometry (to show the lamp physically)
    const lampGeo = new THREE.CylinderGeometry(0.08, 0.12, 0.4, 12);
    const lampMat = new THREE.MeshStandardMaterial({ color: 0x333333, metalness: 0.6, roughness: 0.4 });
    const lampMesh = new THREE.Mesh(lampGeo, lampMat);
    lampMesh.position.copy(lamp.position);
    lampMesh.position.y -= 0.25;
    lampMesh.castShadow = false;
    scene.add(lampMesh);

    // light helper (comment out for production)
    // const spotHelper = new THREE.SpotLightHelper(lamp);
    // scene.add(spotHelper);

    // --- create procedural mannequin (grouped) ---
    buildMannequin();

    // add mannequin to scene
    scene.add(mannequin);

    // slight fill light low for ambient bounce
    const rim = new THREE.PointLight(0x404050, 0.4);
    rim.position.set(-5, 3, 5);
    scene.add(rim);

    // initial render
    renderer.render(scene, camera);
  }

  function buildMannequin(){
    // common material - gray synthetic
    const mat = new THREE.MeshStandardMaterial({ color: 0x808080, roughness: 0.6, metalness: 0.05 });

    // torso - cylinder
    const torsoGeo = new THREE.CylinderGeometry(0.6, 0.6, 1.4, 24);
    torso = new THREE.Mesh(torsoGeo, mat);
    torso.position.y = 0.0;
    mannequin.add(torso);

    // head - sphere
    const headGeo = new THREE.SphereGeometry(0.35, 24, 24);
    const head = new THREE.Mesh(headGeo, mat);
    head.position.y = 1.15;
    mannequin.add(head);

    // neck
    const neckGeo = new THREE.CylinderGeometry(0.15, 0.15, 0.2, 12);
    const neck = new THREE.Mesh(neckGeo, mat);
    neck.position.y = 0.9;
    mannequin.add(neck);

    // hips/pelvis as small box
    const hipGeo = new THREE.BoxGeometry(0.9, 0.25, 0.5);
    const hips = new THREE.Mesh(hipGeo, mat);
    hips.position.y = -0.55;
    mannequin.add(hips);

    // arms (left and right) - upper and lower
    const upperArmGeo = new THREE.CylinderGeometry(0.12, 0.12, 0.8, 12);
    const lowerArmGeo = new THREE.CylinderGeometry(0.11, 0.11, 0.7, 12);

    // left arm
    const leftUpper = new THREE.Mesh(upperArmGeo, mat);
    leftUpper.position.set(-0.9, 0.45, 0.0);
    leftUpper.rotation.z = Math.PI / 12;
    leftUpper.name = 'leftUpper';
    mannequin.add(leftUpper);

    const leftLower = new THREE.Mesh(lowerArmGeo, mat);
    leftLower.position.set(-1.4, -0.05, 0.0);
    leftLower.rotation.z = -Math.PI / 6;
    leftLower.name = 'leftLower';
    mannequin.add(leftLower);

    // right arm
    const rightUpper = new THREE.Mesh(upperArmGeo, mat);
    rightUpper.position.set(0.9, 0.45, 0.0);
    rightUpper.rotation.z = -Math.PI / 12;
    rightUpper.name = 'rightUpper';
    mannequin.add(rightUpper);

    const rightLower = new THREE.Mesh(lowerArmGeo, mat);
    rightLower.position.set(1.4, -0.05, 0.0);
    rightLower.rotation.z = Math.PI / 6;
    rightLower.name = 'rightLower';
    mannequin.add(rightLower);

    // legs (upper and lower)
    const upperLegGeo = new THREE.CylinderGeometry(0.14, 0.14, 0.9, 12);
    const lowerLegGeo = new THREE.CylinderGeometry(0.13, 0.13, 0.9, 12);

    // left leg
    const leftThigh = new THREE.Mesh(upperLegGeo, mat);
    leftThigh.position.set(-0.28, -1.25, 0.0);
    leftThigh.rotation.x = 0;
    leftThigh.name = 'leftThigh';
    mannequin.add(leftThigh);

    const leftShin = new THREE.Mesh(lowerLegGeo, mat);
    leftShin.position.set(-0.28, -2.05, 0.0);
    leftShin.name = 'leftShin';
    mannequin.add(leftShin);

    // right leg
    const rightThigh = new THREE.Mesh(upperLegGeo, mat);
    rightThigh.position.set(0.28, -1.25, 0.0);
    rightThigh.name = 'rightThigh';
    mannequin.add(rightThigh);

    const rightShin = new THREE.Mesh(lowerLegGeo, mat);
    rightShin.position.set(0.28, -2.05, 0.0);
    mannequin.add(rightShin);

    // small feet as boxes
    const footGeo = new THREE.BoxGeometry(0.28, 0.1, 0.48);
    const leftFoot = new THREE.Mesh(footGeo, mat);
    leftFoot.position.set(-0.28, -2.45, 0.12);
    mannequin.add(leftFoot);

    const rightFoot = new THREE.Mesh(footGeo, mat);
    rightFoot.position.set(0.28, -2.45, 0.12);
    mannequin.add(rightFoot);

    // set shadow casting for mannequin children
    mannequin.traverse(function(obj){
      if(obj.isMesh){
        obj.castShadow = true;
        obj.receiveShadow = false;
      }
    });

    // start position
    mannequin.position.set(-walkDistance/2, 0, 0);
  }

  // animate function - walking motion + lamp illumination follow
  let elapsed = 0;
  function update(){
    if(!isAnimating){
      renderer.render(scene, camera);
      return;
    }

    const dt = clock.getDelta();
    elapsed += dt;

    // simple back-and-forth position using sine time
    const phase = (elapsed * walkSpeed) % (Math.PI * 2);
    const x = Math.sin(phase) * (walkDistance/2);
    mannequin.position.x = x;

    // small torso bob to feel like walking
    torso.position.y = 0.12 * Math.abs(Math.sin(phase * 2));

    // limb swing (simple)
    const swing = Math.sin(phase * 2) * 0.6; // swing amplitude
    // arms (opposite to legs)
    const leftUpper = mannequin.getObjectByName('leftUpper');
    const rightUpper = mannequin.getObjectByName('rightUpper');
    const leftLower = mannequin.getObjectByName('leftLower');
    const rightLower = mannequin.getObjectByName('rightLower');

    if(leftUpper && rightUpper){
      leftUpper.rotation.x = 0.2 + swing * 0.5;
      rightUpper.rotation.x = 0.2 - swing * 0.5;
    }
    if(leftLower && rightLower){
      leftLower.rotation.x = -0.4 + (-swing) * 0.2;
      rightLower.rotation.x = -0.4 + (swing) * 0.2;
    }

    // legs
    const leftThigh = mannequin.getObjectByName('leftThigh');
    const rightThigh = mannequin.getObjectByName('rightThigh');
    const leftShin = mannequin.getObjectByName('leftShin');
    const rightShin = mannequin.getObjectByName('rightShin');

    if(leftThigh && rightThigh){
      leftThigh.rotation.x = 0.2 + (-swing) * 0.7;
      rightThigh.rotation.x = 0.2 + (swing) * 0.7;
    }
    if(leftShin && rightShin){
      leftShin.rotation.x = -0.2 + Math.max(0, -swing) * 0.5;
      rightShin.rotation.x = -0.2 + Math.max(0, swing) * 0.5;
    }

    // lamp follows camera a bit? keep it stationary about center above stage
    // but spotlight target should follow mannequin for dramatic effect
    lamp.target = mannequin; // spotlight target pointing roughly at mannequin
    lamp.position.set(0, 6.5, 0);

    // slight camera subtle orbit for cinematic view
    const camAngle = elapsed * 0.15;
    camera.position.x = 6 * Math.sin(camAngle);
    camera.position.z = 6 * Math.cos(camAngle);
    camera.lookAt(new THREE.Vector3(mannequin.position.x, 0.6, 0));

    renderer.render(scene, camera);
  }

  // main loop
  function loop(){
    requestAnimationFrame(loop);
    update();
  }

  // UI buttons (in-container) so they appear inside Streamlit iframe
  function createButtons(){
    const startBtn = document.createElement('button');
    startBtn.textContent = 'Start';
    startBtn.style.position = 'absolute';
    startBtn.style.top = '10px';
    startBtn.style.left = '10px';
    startBtn.style.padding = '8px 12px';
    startBtn.onclick = function(){ isAnimating = true; clock.start(); };

    const stopBtn = document.createElement('button');
    stopBtn.textContent = 'Stop';
    stopBtn.style.position = 'absolute';
    stopBtn.style.top = '10px';
    stopBtn.style.left = '80px';
    stopBtn.style.padding = '8px 12px';
    stopBtn.onclick = function(){ isAnimating = false; clock.stop(); };

    container.appendChild(startBtn);
    container.appendChild(stopBtn);
  }

  // resize handler
  function onResize(){
    if(!renderer) return;
    const w = container.clientWidth;
    const h = container.clientHeight;
    renderer.setSize(w,h);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  window.addEventListener('resize', onResize);

  // initialize and start
  init();
  createButtons();
  clock.start();
  isAnimating = true;
  loop();

})(); // end IIFE
</script>
"""

components.html(html_code, height=720, scrolling=False)
