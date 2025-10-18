from math import sin, cos

class vec2:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __mul__(self, c):
        return vec2(self.x * c, self.y * c)
    
    def __truediv__(self, c):
        return vec2(self.x / c, self.y / c)
    
    def __add__(self, v):
        return vec2(self.x + v.x, self.y + v.y)
    
    __radd__ = __add__
    __rmul__ = __mul__

    def toScreen(self, width, height):
        # Ajuste le ratio pour un terminal monospace macOS
        ratio = 2.0  
        return vec2((ratio * height / width * self.x + 1) * width / 2,
                    (-self.y + 1) * height / 2)

class vec3:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, c):
        return vec3(self.x * c, self.y * c, self.z * c)

    def __truediv__(self, c):
        return vec3(self.x / c, self.y / c, self.z / c)
    
    def __add__(self, v):
        return vec3(self.x + v.x, self.y + v.y, self.z + v.z)
    
    __radd__ = __add__
    __rmul__ = __mul__

    def projection(self, focalLength):
        return vec2(self.x * focalLength / self.z, self.y * focalLength / self.z)
    
    def rotationX(self, pitch):
        y1 = cos(pitch) * self.y - sin(pitch) * self.z
        z1 = sin(pitch) * self.y + cos(pitch) * self.z
        return vec3(self.x, y1, z1)

    def rotationY(self, yaw):
        x1 = cos(yaw) * self.x + sin(yaw) * self.z
        z1 = -sin(yaw) * self.x + cos(yaw) * self.z
        return vec3(x1, self.y, z1)


class Triangle2D:
    def __init__(self, v1, v2, v3) -> None:
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def toScreen(self, width, height):
        return Triangle2D(
            self.v1.toScreen(width, height),
            self.v2.toScreen(width, height),
            self.v3.toScreen(width, height)
        )


class Triangle3D:
    def __init__(self, v1, v2, v3) -> None:
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def projection(self, focalLength):
        return Triangle2D(
            self.v1.projection(focalLength),
            self.v2.projection(focalLength),
            self.v3.projection(focalLength)
        )

    def translate(self, v: vec3):
        return Triangle3D(self.v1 + v, self.v2 + v, self.v3 + v)

    def rotationX(self, pitch):
        return Triangle3D(
            self.v1.rotationX(pitch),
            self.v2.rotationX(pitch),
            self.v3.rotationX(pitch)
        )
    
    def rotationY(self, yaw):
        return Triangle3D(
            self.v1.rotationY(yaw),
            self.v2.rotationY(yaw),
            self.v3.rotationY(yaw)
        )
