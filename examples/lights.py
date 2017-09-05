#! /usr/bin/env python
from time import time
from rayTracer.PPM import PPMFile
from PyQt5.QtGui import QVector3D, QMatrix4x4
from rayTracer.Camera import Camera
from rayTracer.PrimitiveObjects import Sphere, Triangle, Light, Plane
from rayTracer.World import World
from rayTracer.Scene import Scene
from rayTracer.Material import Material
from rayTracer.Model import Model


def main():
    WIDTH = 200
    HEIGHT = 200
    file = PPMFile("lights" + str(WIDTH) + "x" + str(HEIGHT) + ".ppm", WIDTH, HEIGHT)
    print('WORKING ON ', file.name)

    camera = Camera(position=QVector3D(0, 1, 300),
                    look_at=QVector3D(0, 0, 0),
                    up=QVector3D(0, 1, 0),
                    viewing_plane_distance=1)

    objects = [
        Sphere(QVector3D(0, 1, -100), 70,
               material=Material(Material.Type.Reflective, color=QVector3D(100, 100, 100))),
    ]

    scene = Scene(objects)
    scene.add_light(Light(QVector3D(100, 100, -100), 2, color=QVector3D(200, 0, 0), shininess=10))
    scene.add_light(Light(QVector3D(-100, 100, -100), 2, color=QVector3D(0, 200, 0), shininess=10))

    world = World(background=QVector3D(0, 0, 0), antialiasing_level=1, dept=0)
    world.render_to_file_using_treads_per_pixel(camera=camera, scene=scene, max_t=10000.0, file=file)
    print(file.name)


if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print(end - start)
    print("DONE rendering")
    exit(0)

