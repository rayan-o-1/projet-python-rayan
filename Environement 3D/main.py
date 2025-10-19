import time
import math
import affichage_graphique as mg
from lib_maths import vec3, Triangle3D

# modèle modifiable par coordonée de cube 3D (12 triangles uniquement)
cube = [
    # Face avant
    Triangle3D(vec3(-0.5, -0.5, 0.5), vec3(0.5, -0.5, 0.5), vec3(0.5, 0.5, 0.5)),
    Triangle3D(vec3(-0.5, -0.5, 0.5), vec3(0.5, 0.5, 0.5), vec3(-0.5, 0.5, 0.5)),
    # Face arrière
    Triangle3D(vec3(0.5, -0.5, -0.5), vec3(-0.5, -0.5, -0.5), vec3(-0.5, 0.5, -0.5)),
    Triangle3D(vec3(0.5, -0.5, -0.5), vec3(-0.5, 0.5, -0.5), vec3(0.5, 0.5, -0.5)),
    # Face droite
    Triangle3D(vec3(0.5, -0.5, 0.5), vec3(0.5, -0.5, -0.5), vec3(0.5, 0.5, -0.5)),
    Triangle3D(vec3(0.5, -0.5, 0.5), vec3(0.5, 0.5, -0.5), vec3(0.5, 0.5, 0.5)),
    # Face gauche
    Triangle3D(vec3(-0.5, -0.5, -0.5), vec3(-0.5, -0.5, 0.5), vec3(-0.5, 0.5, 0.5)),
    Triangle3D(vec3(-0.5, -0.5, -0.5), vec3(-0.5, 0.5, 0.5), vec3(-0.5, 0.5, -0.5)),
    # Face dessus
    Triangle3D(vec3(-0.5, 0.5, 0.5), vec3(0.5, 0.5, 0.5), vec3(0.5, 0.5, -0.5)),
    Triangle3D(vec3(-0.5, 0.5, 0.5), vec3(0.5, 0.5, -0.5), vec3(-0.5, 0.5, -0.5)),
    # Face dessous
    Triangle3D(vec3(0.5, -0.5, 0.5), vec3(-0.5, -0.5, 0.5), vec3(-0.5, -0.5, -0.5)),
    Triangle3D(vec3(0.5, -0.5, 0.5), vec3(-0.5, -0.5, -0.5), vec3(0.5, -0.5, -0.5)),
]

# Caméra avec une focale plus grande pour un effet de zoom
cam = mg.Camera(vec3(0, 0, 3.5), 0.0, 0.0, focalLength=2.5)

angle_x = 0
angle_y = 0

while True:
    mg.clear(' ')

    rotated_cube = []
    for tri in cube:
        rotated_tri = tri.rotationX(angle_x).rotationY(angle_y)
        rotated_cube.append(rotated_tri)
    
    mg.putMesh(rotated_cube, cam)
    mg.draw()

    angle_x += 0.02
    angle_y += 0.03
    time.sleep(0.02)




#projet terminer le fichier main correspond a ce que l on souhaite afficher graphiquement(donc tout type de forme en fonction du nombre de triangle celle si)
