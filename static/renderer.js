// import './styles/style.css'

// import * as THREE from './node_modules/three';
import * as THREE from 'https://cdn.skypack.dev/three@0.132.2'
import { STLLoader } from 'https://cdn.jsdelivr.net/npm/three@0.110.0/examples/jsm/loaders/STLLoader.js'
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.110.0/examples/jsm/controls/OrbitControls.js'

var url_string = window.location.href
var url = new URL(url_string);
var locIndex = url.searchParams.get("location");

// Scene
const scene = new THREE.Scene();
scene.add(new THREE.AxesHelper(5));

// Lights
const light = new THREE.PointLight()
light.position.set(-500, 0, 500)
light.intensity = 0.50
// const light = new THREE.AmbientLight(0x404040)
scene.add(light) //FIXME: toggle for debugging
const light2 = new THREE.PointLight()
light2.position.set(500, 0, 500)
light2.intensity = 0.50
scene.add(light2) //FIXME: toggle for debugging
// Area light (doesn't work with Phong materials)
const light3 = new THREE.RectAreaLight(
    0xffffff, 0.5, 1000, 1000
);
light3.position.set(0,0,100);
light3.lookAt(0,0,0);
scene.add(light3)
const light4 = new THREE.PointLight()
light4.intensity = 0.1
scene.add(light4)

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
controls.screenSpacePanning = true;

// For raycasting
const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();
const cubeGeometry = new THREE.BoxGeometry(10, 10, 10);
const goalCubeMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00 })
const startCubeMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 })
const goalCube = new THREE.Mesh(cubeGeometry, goalCubeMaterial)
const startCube = new THREE.Mesh(cubeGeometry, startCubeMaterial)
scene.add(goalCube)
scene.add(startCube)
let goalPosition = [0,0]
let startPosition = [0,0]

//Define Plane Texture
let floorPlanWidth = 0
let floorPlanHeight = 0
let xOffset = 0
let yOffset = 0
const texture = new THREE.TextureLoader().load(
    `/static/floor-plans/${locIndex}.jpg`, function(texture){
        console.log(texture.image.width);
        console.log(texture.image.height);
        floorPlanWidth = texture.image.width
        floorPlanHeight = texture.image.height
        xOffset = (-1)*(floorPlanWidth/2)
        yOffset = (floorPlanHeight/2)
        
        // Geometry - Floor plan
        const planeMaterial = new THREE.MeshPhongMaterial({
            map: texture, shininess: 150
        });
        const planeGeometry = new THREE.PlaneGeometry(
            floorPlanWidth, floorPlanHeight
        )
        const plane = new THREE.Mesh(planeGeometry, planeMaterial)
        scene.add(plane)
        // plane.position.set(0, -10, 2)
        plane.position.set(0, 0, 2)

        // Geometry - Model
        const modelMaterial = new THREE.MeshStandardMaterial({
            side: THREE.DoubleSide, color: 0x292929
        })
        const loader = new STLLoader()
        loader.load(
            '/static/models/model.stl',
            function (geometry) {
                const model = new THREE.Mesh(geometry, modelMaterial)
                scene.add(model)
                model.position.set(xOffset, yOffset, 0)

                // Raycasting
                function onPointerClick(event) {

                    // calculate pointer position in normalized device coordinates
                    pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
                    pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;
                    // console.log(pointer.x)
                    // console.log(pointer.y)

                    raycaster.setFromCamera(pointer, camera)
                    const intersects = raycaster.intersectObject(model);
                    if (intersects.length > 0) {
                        console.log(intersects[0].point)
                        if (intersects[0].point.z == 0){
                            switch(event.button){
                                // Left click
                                case 0:
                                    goalCube.position.copy(intersects[0].point)
                                    goalCube.position.z = 2;
                                    goalPosition[0] = (-1) * (Math.round(goalCube.position.y) - yOffset)
                                    goalPosition[1] = Math.round(goalCube.position.x) - xOffset
                                    console.log("Goal Position: " + goalPosition)
                                    break;
                                
                                // Right click
                                case 2:
                                    startCube.position.copy(intersects[0].point)
                                    startCube.position.z = 2;
                                    startPosition[0] = (-1) * (Math.round(startCube.position.y) - yOffset)
                                    startPosition[1] = Math.round(startCube.position.x) - xOffset
                                    console.log("Start Position: " + startPosition)
                                    break;
                            }
                            
                        }
                        
                    }

                }
                // window.addEventListener('click', onPointerClick)
                window.addEventListener('pointerup', onPointerClick)
            },
            (xhr) => {
                console.log((xhr.loaded / xhr.total) * 100 + '% loaded')
            },
            (error) => {
                console.log(error)
            }
        )

        // Update light positions
        light.position.set(-500, yOffset, 500)
        light2.position.set(500, yOffset, 500)
        light4.position.set(0, -yOffset, 500)

        // Update camera position
        camera.position.setZ(floorPlanWidth>floorPlanHeight ? (floorPlanWidth/2):(floorPlanHeight/2));

    }
);

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