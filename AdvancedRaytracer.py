#! /usr/bin/env python
from rayTracer.PPM import PPMFile
from PyQt5.QtGui import QVector3D
from rayTracer.Camera import Camera
from rayTracer.TraceObjects import Sphere, Triangle, Light, Plane
from rayTracer.World import World
from rayTracer.Scene import Scene
from rayTracer.Material import  Material
import random


def main():
    WIDTH = 500
    HEIGHT = 500
    file = PPMFile("CODE.ppm", WIDTH, HEIGHT)

    camera = Camera(position=QVector3D(40, 25.0, 1000),
                    look_at=QVector3D(0, 0, 0),
                    up=QVector3D(0, 1, 0),
                    viewing_plane_distance=1)

    # objects = [
    #     Plane(normal=QVector3D(0, 1, 0).normalized(), pointInPlane=QVector3D(0, 0, 0), distance=QVector3D(0, 100, 10), color=QVector3D(10, 10, 10), material='reflective'),
    #
    #     # Triangle(QVector3D(-300, 20, -200),QVector3D(250, 20, -200),QVector3D(0, -20, 200), QVector3D(100,100,100)),
    #     #        Triangle(QVector3D(-50, -50, 100), QVector3D(0, 250, 70), QVector3D(250, 250, 90), QVector3D(60, 0, 75), material='reflective'),
    #
    #            # # Sphere(QVector3D(0, 0, 0), 90, QVector3D(.21 * 255, .34 * 255, .25 * 255)),
    #            Sphere(QVector3D(0, 0, 0), 90,  QVector3D(0.22 * 255, 0.23 * 255 ,0.36 * 255)),
    #            # # Sphere(QVector3D(70, 70, 0), 90, QVector3D(.15 * 255, .55 * 255, .97 *255)),
    #            Sphere(QVector3D(-35, 0, 100), 10, QVector3D(0, 0, 200), material='reflective'),
    #            Sphere(QVector3D(35, 0, 100), 10, QVector3D(0, 0, 200)),
    #            Sphere(QVector3D(0, 50, 300), 20, QVector3D(255, 255, 255), material='dielectric'),
    #     #        Sphere(QVector3D(50, -50, 20), 10, QVector3D(1, 1, 200)),
    #     #         Sphere(QVector3D(0, 0, 0), 5, QVector3D(200, 200, 200))
    #            ]
    # for i in range(10):
    #     s = Sphere(QVector3D(random.randrange(-WIDTH/2,WIDTH/2), random.randrange(-WIDTH/2, HEIGHT/2), random.randrange(-1000, 500)), random.randrange(5,60), QVector3D(random.randrange(5,200), random.randrange(0,255), random.randrange(0,200)))
    #     objects.append(s)


    objects = [
        # Plane(normal=QVector3D(0, 1, 0).normalized(), pointInPlane=QVector3D(0, 0, 0), distance=QVector3D(0, 100, 10),
        #       material=Default(color=QVector3D(200, 200, 200))),
        # Plane(normal=QVector3D(0, 0, 1).normalized(), pointInPlane=QVector3D(0, 0, -500), distance=QVector3D(0, 100, 10),
        #       material=Default(color=QVector3D(50, 50, 50))),
        # Plane(normal=QVector3D(1, 0, 0).normalized(), pointInPlane=QVector3D(-250, 0, 0), distance=QVector3D(0, 100, 10),
        #       material=Default( color=QVector3D(100, 0, 0))),
        # Plane(normal=QVector3D(-1, 0, 0).normalized(), pointInPlane=QVector3D(250, 0, 0), distance=QVector3D(0, 100, 10),
        #       material=Default(color=QVector3D(0, 100, 0))),
        # Plane(normal=QVector3D(0, 1, 0).normalized(), pointInPlane=QVector3D(0, 250, 0), distance=QVector3D(0, 100, 10),
        #       material=Default(color=QVector3D(10, 10, 10))),
        Sphere(QVector3D(0, 0, -200), 50,
               material=Material(Material.Type.Default, color=QVector3D(100, 100, 100))),
        Sphere(QVector3D(-200, -50, -250), 50,
               material=Material(Material.Type.Default, color=QVector3D(0.70 * 255, 0.60 * 255, 0.36 * 255))),
        Sphere(QVector3D(200, -50, -250), 50,
               material=Material(Material.Type.Reflective, color=QVector3D(0.42 * 255, 30, 0.66 * 255))),
        Sphere(QVector3D(0, 200, 500), 50,
               material=Material(type=Material.Type.Dielectric,
                                 color=QVector3D(0.36 * 255, 0.65 * 255, 0.53 * 255),
                                 n=3.5)),
        # Sphere(QVector3D(-30, -50, -350), 50, QVector3D(0.96 * 255, 0.40* 255, 0.54 * 255)),
        # Sphere(QVector3D(30, -50, -250), 50, QVector3D(100, 220, 100),
        #        material='reflective'),
       # Sphere(QVector3D(0, 0, 0), 90,  QVector3D(0.22 * 255, 0.23 * 255 ,0.36 * 255), material='reflective'),
       # Sphere(QVector3D(-35, 0, 100), 10, QVector3D(0, 0, 200), material='reflective'),
       # Sphere(QVector3D(35, 0, 100), 10, QVector3D(0, 0, 200)),
       # Sphere(QVector3D(0, 50, 300), 20, QVector3D(255, 255, 255), material='dielectric'),

    ]

    scene = Scene(objects)
    scene.add_light(Light(QVector3D(-150, 130, -200), 2, color=QVector3D(200, 0, 0), shininess=64))
    Light(QVector3D(150, 130, -200), 2, color=QVector3D(0, 0, 200), shininess=64)
    world = World(background=QVector3D(0, 0, 0), antialiasing_level=1, dept=0)
    world.render_to_file(camera=camera, scene=scene, max_t=10000.0, file=file)
    print(file.name)


if __name__ == "__main__":
    main()
    print("DONE rendering")
    exit(0)

