#! /usr/bin/env python
from time import time
from rayTracer.PPM import PPMFile
from PyQt5.QtGui import QVector3D, QMatrix4x4
from rayTracer.Camera import Camera
from rayTracer.PrimitiveObjects import Sphere, Light, Plane
from rayTracer.World import World
from rayTracer.Scene import Scene
from rayTracer.Material import Material
from rayTracer.Model import Model


def main():
    WIDTH = 250
    HEIGHT = 250
    file = PPMFile("Model" + str(WIDTH)+"x" + str(HEIGHT) + ".ppm", WIDTH, HEIGHT)
    print('WORKING ON ', file.name)

    camera = Camera(position=QVector3D(0, 1, 300.0),
                    look_at=QVector3D(0, 0, 0),
                    up=QVector3D(0, 1, 0),
                    viewing_plane_distance=1)

    objects = [
        Sphere(QVector3D(100, 1, -50), 70,
               material=Material(Material.Type.Reflective, color=QVector3D(180, 0, 100))),

        Plane(normal=QVector3D(0, 1, 0).normalized(), pointInPlane=QVector3D(0, -100, 0), distance=QVector3D(100, 0, 10),
              material=Material(Material.Type.Default, color=QVector3D(200, 200, 200))),
        Plane(normal=QVector3D(0, 0, 1).normalized(), pointInPlane=QVector3D(0, 0, -500), distance=QVector3D(0, 100, 10),
              material=Material(Material.Type.Default, color=QVector3D(50, 50, 50))),
        Plane(normal=QVector3D(1, 0, 0).normalized(), pointInPlane=QVector3D(-250, 0, 0), distance=QVector3D(0, 100, 10),
              material=Material(Material.Type.Default, color=QVector3D(100, 0, 0))),
        Plane(normal=QVector3D(-1, 0, 0).normalized(), pointInPlane=QVector3D(250, 0, 0), distance=QVector3D(0, 100, 10),
              material=Material(Material.Type.Default, color=QVector3D(0, 0, 100))),
        Plane(normal=QVector3D(0, 1, 0).normalized(), pointInPlane=QVector3D(0, 250, 0), distance=QVector3D(0, 100, 10),
              material=Material(Material.Type.Default, color=QVector3D(10, 10, 10))),
    ]

    model = Model('./objs/cube.obj',  material=Material(Material.Type.Dielectric, color=QVector3D(10, 10, 10), n=3.45))
    model2 = Model('./objs/t.obj', material=Material(Material.Type.Default, color=QVector3D(100, 0, 00)))

    T = QMatrix4x4()
    T.rotate(70, 0, 1, 1)
    T.rotate(60, 1, 0, 0)
    T.scale(70)

    for obj in model.triangles:
        obj.a = T * obj.a
        obj.b = T * obj.b
        obj.c = T * obj.c

    T.setToIdentity()
    T.rotate(50, 1,0,0)
    T.translate(0, 0, -100)
    T.scale(50)
    for obj in model2.triangles:
        obj.a = T * obj.a
        obj.b = T * obj.b
        obj.c = T * obj.c

    objects.extend(model.triangles)
    objects.extend(model2.triangles)

    scene = Scene(objects)
    scene.add_light(Light(QVector3D(0, 100, 200), 2, color=QVector3D(100, 100, 100), shininess=5))

    world = World(background=QVector3D(0, 0, 0), antialiasing_level=4, dept=-1)
    # world.render_to_file(camera=camera, scene=scene, max_t=10000.0, file=file)
    world.render_to_file_using_treads_per_pixel(camera=camera, scene=scene, max_t=10000.0, file=file)
    print(file.name)


if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print(end-start)
    print("DONE rendering")
    exit(0)

