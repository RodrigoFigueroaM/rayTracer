#! /usr/bin/env python
from rayTracer.PPM import PPMFile
from PyQt5.QtGui import QVector3D
from rayTracer.Camera import Camera
from rayTracer.TraceObjects import Sphere, Triangle, Light
from rayTracer.World import World
from rayTracer.Scene import Scene

import random


def main():
    WIDTH = 500
    HEIGHT = 500
    file = PPMFile("rayTracerdepth5.ppm", WIDTH, HEIGHT)

    camera = Camera(position=QVector3D(0, 0, 1000),
                    lookAt=QVector3D(0, 0, 0),
                    up=QVector3D(0, 1, 0),
                    viewingPlaneDistance=100)

    objects = [
        # # Triangle(QVector3D(-300, 20, -200),QVector3D(250, 20, -200),QVector3D(0, -20, 200), QVector3D(100,100,100)),
        # #        Triangle(QVector3D(0, 100, -400), QVector3D(-100, 0, -200), QVector3D(100, 20, 300),
        # #                 QVector3D(60, 0, 75)),
        #
               # Sphere(QVector3D(-70, 70, 0), 90, QVector3D(.21 * 255, .34 * 255, .25 * 255)),
               # Sphere(QVector3D(0, -70, 0), 90,  QVector3D(175.95, 0, 61.2)),
               # Sphere(QVector3D(70, 70, 0), 90, QVector3D(.15 * 255, .55 * 255, .97 *255)),
        #        # Sphere(QVector3D(-35, 0, 40), 10, QVector3D(0, 0, 200)),
        #        # Sphere(QVector3D(35, 0, 40), 10, QVector3D(0, 0, 200)),
        #        Sphere(QVector3D(0, -35, 40), 10, QVector3D(0, 0, 200)),
        #        Sphere(QVector3D(50, -50, 20), 10, QVector3D(1, 1, 200)),
        #         Sphere(QVector3D(0, 0, 0), 5, QVector3D(200, 200, 200))
               ]
    for i in range(50):
        s = Sphere(QVector3D(random.randrange(-WIDTH/2,WIDTH/2), random.randrange(-WIDTH/2, HEIGHT/2), random.randrange(-1000, 500)), random.randrange(5,60), QVector3D(random.randrange(5,200), random.randrange(0,255), random.randrange(0,200)))
        objects.append(s)

    light = Light(QVector3D(200, 1000, 1000), 2, color=QVector3D(200, 200, 200), shininess=100)
    scene = Scene(objects)
    scene.addLight(light)

    World.renderToFile(camera=camera, scene=scene, maxT=10000.0, file=file)
    print(file.name)


if __name__ == "__main__":
    main()
    print("DONE rendering")
    exit(0)

