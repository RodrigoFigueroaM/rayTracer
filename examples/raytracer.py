#! /usr/bin/env python
from time import time
from rayTracer.PPM import PPMFile
from PyQt5.QtGui import QVector3D
from rayTracer.Camera import Camera
from rayTracer.PrimitiveObjects import Sphere, Light, Plane
from rayTracer.World import World
from rayTracer.Scene import Scene
from rayTracer.Material import  Material


def main():
    WIDTH = 100
    HEIGHT = 100
    file = PPMFile("raytracer" + str(WIDTH)+"x" + str(HEIGHT) + ".ppm", WIDTH, HEIGHT)
    print('WORKING ON ', file.name)

    camera = Camera(position=QVector3D(0, 0, 300),
                     look_at=QVector3D(0, 1, 0),
                    up=QVector3D(0, 1, 0),
                    viewing_plane_distance=1)

    objects = [
        Plane(normal=QVector3D(0, 1, 0).normalized(), pointInPlane=QVector3D(0, -100, 0), distance=QVector3D(100, 0, 10),
              material=Material(Material.Type.Reflective, color=QVector3D(200, 200, 200))),
        Plane(normal=QVector3D(0, 0, 1).normalized(), pointInPlane=QVector3D(0, 0, -500), distance=QVector3D(0, 100, 10),
              material=Material(Material.Type.Default, color=QVector3D(50, 50, 50))),
        Plane(normal=QVector3D(1, 0, 0).normalized(), pointInPlane=QVector3D(-250, 0, 0), distance=QVector3D(0, 100, 10),
              material=Material(Material.Type.Default, color=QVector3D(100, 0, 0))),
        Plane(normal=QVector3D(-1, 0, 0).normalized(), pointInPlane=QVector3D(250, 0, 0), distance=QVector3D(0, 100, 10),
              material=Material(Material.Type.Default, color=QVector3D(0, 100, 0))),
        Plane(normal=QVector3D(0, 1, 0).normalized(), pointInPlane=QVector3D(0, 250, 0), distance=QVector3D(0, 100, 10),
              material=Material(Material.Type.Default, color=QVector3D(10, 10, 10))),
        Sphere(QVector3D(0, 1, -200), 70,
               material=Material(Material.Type.Reflective, color=QVector3D(100, 0, 100))),
        Sphere(QVector3D(-200, -50, -250), 50,
               material=Material(Material.Type.Reflective, color=QVector3D(0.70 * 255, 0.60 * 255, 0.36 * 255))),
        Sphere(QVector3D(200, -50, -250), 25,
               material=Material(Material.Type.Default, color=QVector3D(0.42 * 255, 30, 0.66 * 255))),
        Sphere(QVector3D(50, 0, 100), 50,
               material=Material(type=Material.Type.Dielectric,
                                 color=QVector3D(0.36 * 255, 0.65 * 255, 0.53 * 255),
                                 n=2.5)),
        Sphere(QVector3D(100, 50, 100), 30,
               material=Material(type=Material.Type.Dielectric,
                                 color=QVector3D( 200, 40, 0.80 * 255),
                                 n=1.5)),

        Sphere(QVector3D(-100, -50, 100), 20,
               material=Material(type=Material.Type.Dielectric,
                                 color=QVector3D(200, 40, 0.80 * 255),
                                 n=3.5)),
    ]

    scene = Scene(objects)
    scene.add_light(Light(QVector3D(0, 100, -100), 2, color=QVector3D(100, 100, 100), shininess=5))

    world = World(background=QVector3D(0, 0, 0), antialiasing_level=1, dept=0)
    world.render_to_file(camera=camera, scene=scene, max_t=10000.0, file=file)
    print(file.name)

if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print(end-start)
    print("DONE rendering")
    exit(0)

