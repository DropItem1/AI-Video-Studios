import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="3D Bouncing Ball", layout="wide")
st.title("🎨 3D Bouncing Ball in Streamlit")

html_code = """
<div id="container" style="width:100%; height:700px;"></div>

<script src="https://cdn.jsdelivr.net/npm/three@0.152.2/build/three.min.js"></script>
<script>
let scene, camera, renderer, sphere, light, floor;
let isAnimating = false;
let velocity = 0.05;
let direction = 1;
let angle = 0;

function init() {
    const container = document.getElementById('container');

    scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x000000, 10, 40); // keeps cinematic depth

    camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setClearColor(0x000000); // black background
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    // Sphere (the bouncing ball)
    const sphereGeo = new THREE.SphereGeometry(1, 32, 32);
    const sphereMat = new THREE.MeshStandardMaterial({ color: 0x0077ff, roughness:0.3, metalness:0.6 });
    sphere = new THREE.Mesh(sphereGeo, sphereMat);
    sphere.castShadow = true;
    scene.add(sphere);

    // Floor
    const floorGeo = new THREE.PlaneGeometry(30,30);
    const floorMat = new THREE.MeshStandardMaterial({ color:0x111111, roughness:1 });
    floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI/2;
    floor.position.y=-2.5;
    floor.receiveShadow = true;
    scene.add(floor);

    // Lights
    const ambient = new THREE.AmbientLight(0x404040);
    scene.add(ambient);

    light = new THREE.SpotLight(0xffffff,2);
    light.position.set(5,5,5);
    light.castShadow = true;
    light.angle = Math.PI/5;
    light.penumbra = 0.3;
    scene.add(light);

    camera.position.set(0,3,8);
    camera.lookAt(0,0,0);

    renderer.render(scene,camera);
}

function animate() {
    if(!isAnimating) return;
    requestAnimationFrame(animate);

    // Ball bounce
    sphere.position.y += velocity*direction;
    if(sphere.position.y>2 || sphere.position.y<-2) direction*=-1;

    // Camera orbit
    angle +=0.01;
    camera.position.x = 8*Math.sin(angle);
    camera.position.z = 8*Math.cos(angle);
    camera.lookAt(sphere.position);

    light.position.copy(camera.position);
    renderer.render(scene,camera);
}

init();

function startAnimation(){ if(!isAnimating){ isAnimating=true; animate(); } }
function stopAnimation(){ isAnimating=false; }

const containerDiv = document.getElementById('container');
const startBtn = document.createElement('button');
startBtn.innerHTML='Start';
startBtn.style.position='absolute';
startBtn.style.top='10px';
startBtn.style.left='10px';
startBtn.onclick=startAnimation;

const stopBtn = document.createElement('button');
stopBtn.innerHTML='Stop';
stopBtn.style.position='absolute';
stopBtn.style.top='10px';
stopBtn.style.left='90px';
stopBtn.onclick=stopAnimation;

containerDiv.appendChild(startBtn);
containerDiv.appendChild(stopBtn);

window.addEventListener('resize', ()=>{
    camera.aspect = containerDiv.clientWidth / containerDiv.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(containerDiv.clientWidth, containerDiv.clientHeight);
});
</script>
"""

components.html(html_code, height=700, scrolling=False)

let time = 0;

function animate() {
    requestAnimationFrame(animate);

    time += 1; // increment time/frame counter

    // Cutscene 1: wide shot
    if(time < 200){
        camera.position.set(0, 5, 10);
        camera.lookAt(sphere.position);
    }
    // Cutscene 2: closer angle
    else if(time < 400){
        camera.position.set(3, 2, 5);
        camera.lookAt(sphere.position);
    }
    // Cutscene 3: overhead
    else if(time < 600){
        camera.position.set(0, 10, 0);
        camera.lookAt(sphere.position);
    }

    // Ball animation
    sphere.position.y += velocity*direction;
    if(sphere.position.y>2 || sphere.position.y<-2) direction*=-1;

    renderer.render(scene,camera);
}

