#! /usr/bin/env python
from time import time
from rayTracer.PPM import PPMFile
from PyQt5.QtGui import QVector3D
from rayTracer.Camera import Camera
from rayTracer.PrimitiveObjects import Sphere, Light, Plane
from rayTracer.World import World
from rayTracer.Scene import Scene
from rayTracer.Material import Material
from rayTracer.Shader import Blinn_Phong, Matte, Specular



def main(num_threads):
    WIDTH = 300
    HEIGHT = 300
    file = PPMFile("lights" + str(WIDTH) + "x" + str(HEIGHT) + ".ppm", WIDTH, HEIGHT)
    print('WORKING ON ', file.name)

    camera = Camera(position=QVector3D(0, 1, 300),
                    look_at=QVector3D(0, 0, 0),
                    up=QVector3D(0, 1, 0),
                    viewing_plane_distance=1)

    objects = [
        Plane(normal=QVector3D(0, 1, 0).normalized(), pointInPlane=QVector3D(0, 0, 0),
              distance=QVector3D(100, 0, 10),
              material=Material(Material.Type.Reflective),
              shader=Blinn_Phong(QVector3D(30, 30, 50))),

        Sphere(QVector3D(0, 1, -100), 50,
               material=Material(type=Material.Type.Default),
               shader=Matte(QVector3D(10, 10, 10))),


        Sphere(QVector3D(0, 75, 0), 50,
               material=Material(type=Material.Type.Reflective),
               shader=Blinn_Phong(QVector3D(10,10,10))),

        Sphere(QVector3D(0, -50, 0), 50,
               material=Material(type=Material.Type.Default),
               shader=Specular(QVector3D(10, 10, 10))),
    ]

    scene = Scene(objects)
    scene.add_light(Light(QVector3D(100, 50, -200), 2, color=QVector3D(200, 0, 0), shininess=100))
    scene.add_light(Light(QVector3D(-100, 50, -200), 2, color=QVector3D(200, 0, 0), shininess=100))
    scene.add_light(Light(QVector3D(-100, 50, 200), 2, color=QVector3D(0, 200, 0), shininess=100))

    world = World(background=QVector3D(0, 0, 0), antialiasing_level=4, dept=-1)
    world.render_to_file_using_treads_per_pixel(camera=camera, scene=scene, max_t=10000.0, file=file, num_threads=num_threads)

    print(file.name)

def mainRunner(num_threads):
    start = time()
    main(num_threads=int(num_threads))
    end = time()
    # print(end - start)
    # print("DONE rendering")

    return (end - start)

if __name__ == "__main__":
    mainRunner(2)
    exit(0)


