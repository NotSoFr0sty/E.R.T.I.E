// import './styles/style.css'

// import * as THREE from './node_modules/three';
import * as THREE from 'https://cdn.skypack.dev/three@0.132.2'
import { STLLoader } from 'https://cdn.jsdelivr.net/npm/three@0.110.0/examples/jsm/loaders/STLLoader.js'
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.110.0/examples/jsm/controls/OrbitControls.js'

// Scene
const scene = new THREE.Scene();
scene.add(new THREE.AxesHelper(5));

// Lights
const light = new THREE.PointLight()
light.position.set(-500, 0, 500)
light.intensity = 0.50
// const light = new THREE.AmbientLight(0x404040)
scene.add(light)
const light2 = new THREE.PointLight()
light2.position.set(500, 0, 500)
light2.intensity = 0.50
scene.add(light2)
// Area light (doesn't work with Phong materials)
// const light3 = new THREE.RectAreaLight(
//     0xffffff, 1000, 10, 10
// );
// light3.position.set(0,0,50);
// light3.lookAt(0,0,0);
// scene.add(light3)

// Camera
const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    5000
);

// Renderer
const renderer = new THREE.WebGLRenderer({
    canvas: document.querySelector('#bg'),
});
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
camera.position.setZ(100);
// camera.position.setX(100);
// camera.position.setY(-100);

// Orbit Controls
const controls = new OrbitControls(camera, renderer.domElement)
controls.enableDamping = true

// Geometry - Model
const material = new THREE.MeshPhongMaterial({
    color: 0x404040, shininess: 10, side: THREE.DoubleSide
})
const loader = new STLLoader()
loader.load(
    '/static/v1.stl',
    function (geometry) {
        const mesh = new THREE.Mesh(geometry, material)
        scene.add(mesh)
        mesh.position.set(-400, 300, 0)
    },
    (xhr) => {
        console.log((xhr.loaded / xhr.total) * 100 + '% loaded')
    },
    (error) => {
        console.log(error)
    }
)

// Geometry - Floor plan
const texture = new THREE.TextureLoader().load(
    '/static/TestOutput.png'
);
const planeMaterial = new THREE.MeshPhongMaterial({
    map: texture, shininess: 150
});
const planeGeometry = new THREE.PlaneGeometry(
    800, 619
)
const plane = new THREE.Mesh(planeGeometry, planeMaterial)
scene.add(plane)
plane.position.set(0, -10, 2)

// Resizer
window.addEventListener('resize', onWindowResize, false)
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()
    renderer.setSize(window.innerWidth, window.innerHeight)
    render()
}

// Animation
function animate(){
    requestAnimationFrame(animate);
    controls.update();
    render();
}

function render() {
    renderer.render(scene, camera)
}

animate()