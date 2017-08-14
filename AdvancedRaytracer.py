#! /usr/bin/env python
from rayTracer.PPM import PPMFile
from PyQt5.QtGui import QVector3D
from rayTracer.Camera import Camera
from rayTracer.TraceObjects import Sphere, Triangle, Light
from rayTracer.World import World
from rayTracer.Scene import Scene

def main():
    WIDTH = 150
    HEIGHT = 150
    file = PPMFile("rayTracer.ppm", WIDTH, HEIGHT)

    camera = Camera(position=QVector3D(0, 0, 1000),
                    lookAt=QVector3D(0, 0, 0),
                    up=QVector3D(0, 1, 0),
                    viewingPlaneDistance=100)

    objects = [Sphere(QVector3D(0, 0, 0), 40, QVector3D(150, 0, 0)),
              Sphere(QVector3D(0, 35, 40), 10, QVector3D(0, 0, 255))
               ]
    light = Light(QVector3D(-500, 500, 1050), 2, color=QVector3D(200, 200, 200), shininess=75)

    scene = Scene(objects)
    scene.addLight(light)

    World.renderToFile(camera=camera, scene=scene, maxT=10000.0, file=file)
    print(file.name)


if __name__ == "__main__":
    main()
    print("DONE rendering")
    exit(0)

