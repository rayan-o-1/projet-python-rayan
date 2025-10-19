import os
from lib_maths import *

width, height = os.get_terminal_size()
height -= 1
pixelBuffer = [' '] * (width * height)

class Camera:
    def __init__(self, position, pitch, yaw, focalLength=1) -> None:
        self.position = position
        self.pitch = pitch
        self.yaw = yaw
        self.focalLength = focalLength

def draw():
    print('\033[H' + ''.join(pixelBuffer), end='', flush=True)

def clear(char=' '):
    for i in range(width * height):
        pixelBuffer[i] = char

def putPixel(v, char):
    px = round(v.x)
    py = round(v.y)
    if 0 <= px < width and 0 <= py < height:
        pixelBuffer[py * width + px] = char

def putTriangle(tri, char):
    def eq(p, a, b):
        return (a.x - p.x) * (b.y - p.y) - (a.y - p.y) * (b.x - p.x)

    xmin = round(min(tri.v1.x, tri.v2.x, tri.v3.x))
    xmax = round(max(tri.v1.x, tri.v2.x, tri.v3.x)) + 1
    ymin = round(min(tri.v1.y, tri.v2.y, tri.v3.y))
    ymax = round(max(tri.v1.y, tri.v2.y, tri.v3.y)) + 1
    for y in range(ymin, ymax):
        if 0 <= y < height:
            for x in range(xmin, xmax):
                if 0 <= x < width:
                    pos = vec2(x, y)
                    w1 = eq(pos, tri.v3, tri.v1)
                    w2 = eq(pos, tri.v1, tri.v2)
                    w3 = eq(pos, tri.v2, tri.v3)
                    if (w1 >= 0 and w2 >= 0 and w3 >= 0) or (-w1 >= 0 and -w2 >= 0 and -w3 >= 0):
                        putPixel(pos, char)

def putMesh(mesh, cam):
    shading_chars = '.,-~:;=!*#$@'
    light_direction = vec3(0, 0, -1).normalize() # Lumière simple venant de face

    for triangle in mesh:
        
        transformed_tri = triangle.translate(-1 * cam.position)

        line1 = transformed_tri.v2 - transformed_tri.v1
        line2 = transformed_tri.v3 - transformed_tri.v1
        normal = line1.cross(line2).normalize()

        if normal.dot(transformed_tri.v1) >= 0:
            continue

        
        dot_product = normal.dot(light_direction)
        intensity = max(0, -dot_product) # On inverse le produit scalaire
        
        char_index = int(intensity * (len(shading_chars) - 1))
        char = shading_chars[char_index]

        projected_tri = transformed_tri.projection(cam.focalLength)
        screen_tri = projected_tri.toScreen(width, height)
        
        putTriangle(screen_tri, char)
