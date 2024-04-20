// import './styles/style.css'

// import * as THREE from './node_modules/three';
import * as THREE from 'https://cdn.skypack.dev/three@0.132.2'
import { STLLoader } from 'https://cdn.jsdelivr.net/npm/three@0.110.0/examples/jsm/loaders/STLLoader.js'
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.110.0/examples/jsm/controls/OrbitControls.js'
import { GUI } from 'https://cdn.skypack.dev/dat.gui';

var url_string = window.location.href
var url = new URL(url_string);
var locIndex = url.searchParams.get("location");
let pathFound = Number(url.searchParams.get("pathFound"));
let biggerDimensionOfFloorPlan

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

// Cameras
// Perspective camera
const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    5000
);
camera.position.setZ(500);
let activeCamera = camera;
// Orthographic camera
let cameraOrtho = new THREE.OrthographicCamera(
    window.innerWidth / -2,
    window.innerWidth / 2,
    window.innerHeight / 2,
    window.innerHeight / -2,
    0.1,
    1000
);
cameraOrtho.position.setZ(500);

// Renderer
const renderer = new THREE.WebGLRenderer({
    canvas: document.querySelector('#bg'),
});
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.toneMapping = THREE.ACESFilmicToneMapping;

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
goalCube.visible = false;
startCube.visible = false;
let goalPosition = [0,0]
let startPosition = [0,0]
// For distinguishing mouse clicks from drags
const delta = 6;
let startX;
let startY;

// GUI
const gui = new GUI();
// Pathfinding GUI
const pathfindingGUI = gui.addFolder('Pathfinding')
let pathfindingParams = {
    isPathfindingActive: false,
    submitPathfindingImageCoordinates: false
};
let submitButtonParams = {
    submitForm:function(){
        document.forms[0].submit()
    }
}
let submitButton;
pathfindingGUI
    .add(pathfindingParams, "isPathfindingActive")
    .name("Enable pathfinding")
    .onChange(
        function(){ // show/hide the pathfinding marker cubes + Calculate path button
            if (pathfindingParams.isPathfindingActive){
                goalCube.visible = true;
                startCube.visible = true;
                submitButton = pathfindingGUI.add(submitButtonParams, "submitForm").name("Calculate path")
                // set active camera to orthocam
                activeCamera = cameraOrtho
            } else{
                goalCube.visible = false;
                startCube.visible = false;
                pathfindingGUI.remove(submitButton)
                activeCamera = camera
            }
        }
    )
// Camera GUI
let cameraParams = {
    resetCamera:function(){
        controls.reset();
    }
}
const cameraGUI = gui.addFolder('Camera')
cameraGUI.add(cameraParams, "resetCamera").name("Reset camera")

// Normal UI
let collapsible = document.getElementsByClassName("collapsible");
let i;
for (i = 0; i<collapsible.length; i++){
    collapsible[i].addEventListener("click", function(){
        this.classList.toggle("active");
        let content = this.nextElementSibling;
        if(content.style.display === "block"){
            content.style.display = "none";
        } else{
            content.style.display = "block";
        }
    });
}

//Define Plane Texture
let floorPlanWidth = 0
let floorPlanHeight = 0
let xOffset = 0
let yOffset = 0
const floorPlanFilePath = pathFound ? (`/static/floor-plans/path.png`) : (`/static/floor-plans/${locIndex}.jpg`);
console.log(floorPlanFilePath)
const texture = new THREE.TextureLoader().load(
    floorPlanFilePath, function(texture){
        console.log(texture.image.width);
        console.log(texture.image.height);
        floorPlanWidth = texture.image.width
        floorPlanHeight = texture.image.height
        xOffset = (-1)*(floorPlanWidth/2)
        yOffset = (floorPlanHeight/2)
        biggerDimensionOfFloorPlan = floorPlanWidth>floorPlanHeight?floorPlanWidth:floorPlanHeight

        // Orthocam
        // cameraOrtho = new THREE.OrthographicCamera(
        //     floorPlanWidth / -2,
        //     floorPlanWidth / 2,
        //     floorPlanHeight / 2,
        //     floorPlanHeight / -2,
        //     0.1,
        //     1000

        // );

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
                function onPointerDown(event){
                    startX = event.pageX
                    startY = event.pageY
                }
                function onPointerUp(event) {
                    // If pathfinding isn't enabled, then return.
                    if (pathfindingParams.isPathfindingActive === false){
                        return
                    }

                    // If it's not a mouseClick, then return.
                    const diffX = Math.abs(event.pageX - startX);
                    const diffY = Math.abs(event.pageY - startY);
                    if (!(diffX < delta && diffY < delta)){
                        return
                    }

                    // calculate pointer position in normalized device coordinates
                    pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
                    pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;
                    // console.log(pointer.x)
                    // console.log(pointer.y)

                    raycaster.setFromCamera(pointer, activeCamera)
                    const intersects = raycaster.intersectObject(model);
                    if (intersects.length > 0) {
                        console.log(intersects[0].point)
                        if (intersects[0].point.z < 1){
                            switch(event.button){
                                // Left click
                                case 0:
                                    goalCube.position.copy(intersects[0].point)
                                    goalCube.position.z = 2;
                                    goalPosition[0] = (-1) * (Math.round((goalCube.position.y) - yOffset))
                                    goalPosition[1] = Math.round((goalCube.position.x) - xOffset)
                                    console.log("Goal Position: " + goalPosition)
                                    document.getElementById("goalX").value = goalPosition[0].toString();
                                    document.getElementById("goalY").value = goalPosition[1].toString();
                                    break;
                                
                                // Right click
                                case 2:
                                    startCube.position.copy(intersects[0].point)
                                    startCube.position.z = 2;
                                    startPosition[0] = (-1) * (Math.round((startCube.position.y) - yOffset))
                                    startPosition[1] = Math.round((startCube.position.x) - xOffset)
                                    console.log("Start Position: " + startPosition)
                                    document.getElementById("startX").value = startPosition[0].toString();
                                    document.getElementById("startY").value = startPosition[1].toString();
                                    break;
                            }
                            
                        }
                        
                    }

                }
                // window.addEventListener('click', onPointerClick)
                renderer.domElement.addEventListener('pointerdown', onPointerDown)
                renderer.domElement.addEventListener('pointerup', onPointerUp)
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
        camera.position.setZ(floorPlanWidth>floorPlanHeight ? (floorPlanWidth):(floorPlanHeight));

    }
);

// Resizer
window.addEventListener('resize', onWindowResize, false)
function onWindowResize() {
    // Update perspective cam
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    // Update orthocam
    cameraOrtho.left = window.innerWidth / -2
    cameraOrtho.right = window.innerWidth / 2
    cameraOrtho.top = window.innerHeight / 2
    cameraOrtho.bottom = window.innerHeight / -2
    // if biggerdimensionoffloorplan is defined then update orthocam
    if (biggerDimensionOfFloorPlan != null) {
        let aspect = window.innerWidth/window.innerHeight;
        if (aspect > 1.0){
            cameraOrtho.zoom = window.innerHeight/biggerDimensionOfFloorPlan;
        } else{
            cameraOrtho.zoom = window.innerWidth/biggerDimensionOfFloorPlan;
        }
    }
    cameraOrtho.updateProjectionMatrix();
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
    renderer.render(scene, activeCamera)
}

animate()