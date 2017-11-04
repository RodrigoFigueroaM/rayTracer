#! /usr/bin/env python
from PyQt5.QtGui import QMatrix4x4, QVector3D
import pyassimp
import pyassimp.postprocess
from rayTracer.PrimitiveObjects import Triangle


class Model:
    def __init__(self, file_name=None, material=None, shader=None):
        self.name = file_name
        self.material = material
        self.shader = shader
        self.triangles = []
        self.__load()

    def __load(self):
        scene = pyassimp.load(self.name, processing=pyassimp.postprocess.aiProcess_Triangulate)
        meshes = scene.meshes
        vertices = []
        for mesh in meshes:
            vertices.append(mesh.vertices)
        for i in range(0, len(vertices[0]), 3):
            first = i
            second = i + 1
            third = i + 2
            self.triangles.append(Triangle(a=QVector3D(vertices[0][first][0],  vertices[0][first][1],  vertices[0][first][2]),
                                           b=QVector3D(vertices[0][second][0], vertices[0][second][1], vertices[0][second][2]),
                                           c=QVector3D(vertices[0][third][0],  vertices[0][third][1],  vertices[0][third][2]),
                                           material=self.material
                                            ))


if __name__ == '__main__':
    model = Model('/Cerberus.obj')
    print(model.triangles)
