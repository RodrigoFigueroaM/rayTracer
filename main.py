#! /usr/bin/env python
import abc
import math
from PyQt5.QtGui import QMatrix4x4, QVector3D


class RayTracerObject(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def intersect(self):
        pass


class Sphere(RayTracerObject):
    def __init__(self, center = QVector3D(0, 0, 0), radius = 1, color = QVector3D(0,0,0) ):
        self.c = center
        self.r = radius
        self.color = color

    def normalAt(self, p):
        return  ((p - self.c)/self.r).normalized()

    def intersect(self, ray):
        ec = ray.e - self.c
        A = QVector3D.dotProduct(ray.d, ray.d)
        B = QVector3D.dotProduct(2 * ray.d, ec)
        C = QVector3D.dotProduct(ec, ec) - self.r * self.r
        discriminant = B*B - 4 * A * C
        if discriminant < 0.000001:
            return False
        t0 = (- B + math.sqrt(discriminant))
        t1 = (- B - math.sqrt(discriminant))
        return True

    def render(self):
        pass

class Light(Sphere):
    def __init__(self, origin, direction, color):
        super().__init__(origin, direction)
        self.color = color

    def intersect(self, ray):
        return super().intersect(ray)


class Ray:
    def __init__(self, origin, direction):
        self.e = origin
        self.d = direction


def initFile(filename, WIDTH = 500, HEIGHT = 500):
    outputfile = open(filename, "w")
    outputfile.write("P3\n")
    outputfile.write("# output.ppm\n")
    outputfile.write(str(WIDTH) + " " + str(HEIGHT) + "\n")
    outputfile.write("255\n")
    return outputfile


def computeLight(normal, lightDirection, diffuseColor, lightColor, halfVector, specularColor, shininess ):
    NdotL = QVector3D.dotProduct(normal, lightDirection)
    lambert = NdotL * diffuseColor * lightColor * max(NdotL, 0.0)
    NdotH = QVector3D.dotProduct(normal, halfVector)
    specular = lightColor * specularColor * pow(max(NdotH, 0.0), shininess)
    return lambert + specular


def reflect(I, N):
    Nnorm = N.normalize()
    R = I - 2.0 * QVector3D.dotProduct(I, N) * N
    return R


def main():
    WIDTH = 500
    HEIGHT = 500
    file = initFile("output.ppm")
    spheres = [ Sphere(QVector3D(WIDTH * 0.5, HEIGHT * 0.5, 50), 50,  QVector3D(100, 0, 0)),
                Sphere(QVector3D(-100 + WIDTH * 0.5, HEIGHT * 0.5, 20), 20, QVector3D(0, 0, 0)),
                Sphere(QVector3D(100 + WIDTH * 0.5, HEIGHT * 0.5, 25), 30, QVector3D(0, 0, 100))
              ]

    light = Light(QVector3D(200, 200, -350), 2, color=QVector3D(255, 0, 255))

    eyeDir = QVector3D(0, 0, 0)
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            # file.write("0 0 0 \n")
            ray = Ray(QVector3D(x, y, 0), QVector3D(0, 0, 1))
            pixel = QVector3D(0, 0, 0)
            for sphere in spheres:
                if sphere.intersect(ray):
                    ambientLight = QVector3D(51, 51, 51)
                    p = ray.e + ray.d
                    lightDir = QVector3D.normalized(light.c - p)  # L
                    normal = sphere.normalAt(p)  # N
                    eyeDir = QVector3D(0, 0, 0)  # V
                    R = reflect(lightDir, normal)
                    H = (lightDir + eyeDir).normalized()
                    NdotL = QVector3D.dotProduct(normal, lightDir)

                    color = computeLight(normal=normal,
                                         lightDirection = lightDir,
                                         diffuseColor=QVector3D(127, 127, 127),
                                         lightColor=light.color,
                                         halfVector= H,
                                         specularColor=QVector3D(255, 255, 255),
                                         shininess= 2)
                    dt = QVector3D.dotProduct(lightDir.normalized(), normal.normalized())

                    pixel =  sphere.color + light.color  * dt * 0.5
                    if pixel.x() > 255:
                        pixel.setX(255)
                    elif pixel.x() < 0:
                        pixel.setX(0)
                    if pixel.y() > 255:
                        pixel.setY(255)
                    elif pixel.y() < 0:
                        pixel.setY(0)
                    if pixel.z() > 255:
                        pixel.setZ(255)
                    elif pixel.z() < 0:
                        pixel.setZ(0)

            if light.intersect(ray):
                pixel = light.color

            file.write(str(int(pixel.x())) + " " + str(int(pixel.y())) + " " + str(int(pixel.z())) + "\n")
    file.close()


if __name__ == "__main__":
    main()
    print("DONE")
    exit(0)

