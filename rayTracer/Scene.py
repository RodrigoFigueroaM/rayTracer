#! /usr/bin/env python
from rayTracer.TraceObjects import Surface, Light


class Scene(object):
    def __init__(self, objects=[], lights=[]):
        self.objects = objects[:]
        self.lights = lights[:]

    def addObject(self, item):
        if type(item) == type(Surface()):
            self.objects.append(item)

    def addLight(self, item):
        self.lights.append(item)