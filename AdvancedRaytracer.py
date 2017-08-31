#! /usr/bin/env python
from rayTracer.PPM import PPMFile
from PyQt5.QtGui import QVector3D
from rayTracer.Camera import Camera
from rayTracer.TraceObjects import Sphere, Triangle, Light, Plane
from rayTracer.World import World
from rayTracer.Scene import Scene

import random


def main():
    WIDTH = 500
    HEIGHT = 500
    file = PPMFile("rayTracerSHIT.ppm", WIDTH, HEIGHT)

    camera = Camera(position=QVector3D(40, 25.0, 1000),
                    lookAt=QVector3D(0, 0, 0),
                    up=QVector3D(0, 1, 0),
                    viewingPlaneDistance=1)

    objects = [
        Plane(normal=QVector3D(0, 1, 0).normalized(), pointInPlane=QVector3D(0, 0, 0), distance=QVector3D(0, 100, 10),
              color=QVector3D(200, 200, 200)),
        Plane(normal=QVector3D(0, 0, 1).normalized(), pointInPlane=QVector3D(0, 0, -500), distance=QVector3D(0, 100, 10),
              color=QVector3D(50, 50, 50)),
        Plane(normal=QVector3D(1, 0, 0).normalized(), pointInPlane=QVector3D(-250, 0, 0), distance=QVector3D(0, 100, 10),
              color=QVector3D(100, 0, 0)),
        Plane(normal=QVector3D(-1, 0, 0).normalized(), pointInPlane=QVector3D(250, 0, 0), distance=QVector3D(0, 100, 10),
              color=QVector3D(0, 100, 0)),
        Plane(normal=QVector3D(0, 1, 0).normalized(), pointInPlane=QVector3D(0, 250, 0), distance=QVector3D(0, 100, 10),
              color=QVector3D(10, 10, 10)),
        Sphere(QVector3D(-200, -50, -250), 50, QVector3D(0.70 * 255, 0.60 * 255, 0.36 * 255)),
        Sphere(QVector3D(200, -50, -250), 50, QVector3D(0.42 * 255, 30, 0.66 * 255),
               material='reflective'),
        Sphere(QVector3D(0, 0, -100), 50, QVector3D(0.36 * 255, 0.65 * 255, 0.53 * 255),
               material='dielectric'),
        Sphere(QVector3D(-30, -50, -350), 50, QVector3D(0.96 * 255, 0.40* 255, 0.54 * 255)),
        Sphere(QVector3D(30, -50, -250), 50, QVector3D(100, 220, 100),
               material='reflective')
    ]

    light = Light(QVector3D(0, 130, -200), 2, color=QVector3D(200, 200, 200), shininess=100)
    scene = Scene(objects)
    scene.addLight(light)

    World.renderToFile(camera=camera, scene=scene, maxT=10000.0, file=file)
    print(file.name)


if __name__ == "__main__":
    main()
    print("DONE rendering")
    exit(0)

