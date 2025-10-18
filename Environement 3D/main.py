import time
import math
import affichage_graphique as mg
from lib_maths import vec3, Triangle3D

# Cube : 12 triangles
carre = [
    # Face avant
    Triangle3D(vec3(-0.5, -0.5, 0.5), vec3(0.5, -0.5, 0.5), vec3(0.5, 0.5, 0.5)),
    Triangle3D(vec3(-0.5, -0.5, 0.5), vec3(0.5, 0.5, 0.5), vec3(-0.5, 0.5, 0.5)),

    # Face arrière
    Triangle3D(vec3(-0.5, -0.5, -0.5), vec3(0.5, -0.5, -0.5), vec3(0.5, 0.5, -0.5)),
    Triangle3D(vec3(-0.5, -0.5, -0.5), vec3(0.5, 0.5, -0.5), vec3(-0.5, 0.5, -0.5)),
]

cam = mg.Camera(vec3(0, 0, -2), 0.0, 0.0, focalLength=1)

angle = 0
angle = 0
rayon = 2 

while True:
    mg.clear(' ')

    
    cam.position = vec3(math.sin(angle) * rayon, 0, math.cos(angle) * rayon)

    
    cam.yaw = -angle
    cam.pitch = 0  # ou ajoute une oscillation si tu veux un effet "orbital"
    
    mg.putMesh(carre, cam)
    mg.draw()

    angle += 0.05
    time.sleep(0.05)
