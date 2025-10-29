import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="3D Bouncing Ball", layout="wide")
st.title("🎨 3D Bouncing Ball in Streamlit")

html_code = """
<div id="container" style="width:100%; height:700px;"></div>

<script src="https://cdn.jsdelivr.net/npm/three@0.152.2/build/three.min.js"></script>
<script>
let scene, camera, renderer, sphere, cube, light, floor;
let isAnimating = false;
let velocity = 0.05;
let direction = 1;
let angle = 0;

function init() {
    const container = document.getElementById('container');

    scene = new THREE.Scene(); // no fog

    camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true }); // alpha true for transparency
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    // Sphere
    const sphereGeo = new THREE.SphereGeometry(1, 32, 32);
    const sphereMat = new THREE.MeshStandardMaterial({ color: 0x0077ff, roughness:0.3, metalness:0.6 });
    sphere = new THREE.Mesh(sphereGeo, sphereMat);
    sphere.castShadow = true;
    scene.add(sphere);

    // Cube
    const cubeGeo = new THREE.BoxGeometry(0.7,0.7,0.7);
    const cubeMat = new THREE.MeshStandardMaterial({ color:0xff3333, roughness:0.8, metalness:0.2 });
    cube = n
