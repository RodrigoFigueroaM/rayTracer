#! /usr/bin/env python
from rayTracer.PrimitiveObjects import Surface, Light


class Scene:
    def __init__(self, objects=[], lights=[]):
        self.objects = objects[:]
        self.lights = lights[:]

    def add_object(self, item):
        if type(item) == type(Surface()):
            self.objects.append(item)

    def add_light(self, item):
        self.lights.append(item)