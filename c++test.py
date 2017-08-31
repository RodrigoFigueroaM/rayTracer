#! /usr/bin/env python
from rayTracer.PPM import PPMFile
from PyQt5.QtGui import QVector3D
from rayTracer.Camera import Camera
from rayTracer.TraceObjects import Sphere, Triangle, Light, Plane
from rayTracer.World import World
from rayTracer.Scene import Scene

import random


def main():
    WIDTH = 100
    HEIGHT = 100
    file = PPMFile("rayTracerTest.ppm", WIDTH, HEIGHT)

    camera = Camera(position=QVector3D(40, 25.0, 1000),
                    lookAt=QVector3D(0, 0, 0),
                    up=QVector3D(0, 1, 0),
                    viewingPlaneDistance=1)

    objects = [Sphere(QVector3D(0,0,0), 20.0, QVector3D(125,240,250))]
    light = Light(QVector3D(0, 300, 0), 2, color=QVector3D(200, 200, 200), shininess=100)
    scene = Scene(objects)
    scene.addLight(light)

    World.renderToFile(camera=camera, scene=scene, maxT=10000.0, file=file)
    print(file.name)


if __name__ == "__main__":
    main()
    print("DONE rendering")
    exit(0)

