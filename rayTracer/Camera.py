#! /usr/bin/env python
from PyQt5.QtGui import QVector3D
from rayTracer.Ray import Ray


class Camera(object):
    """docstring for Camera"""
    def __init__(self, position=QVector3D(0, 0, 3),
                 lookAt=QVector3D(0, 0, 0),
                 up=QVector3D(0, 1, 0),
                 viewingPlaneDistance = 1):
        super(Camera, self).__init__()
        self.position = position
        self.lookAt = lookAt
        self.viewingPlaneDistance = viewingPlaneDistance
        #compute uvw
        self._dir = (lookAt - self.position).normalized()
        self._back = (self.position - lookAt).normalized()
        self._right = QVector3D.crossProduct(up, self._back) # change order?
        self._up = QVector3D.crossProduct(self._back, self._right)
        self._center = self.position + self.direction

    @property
    def direction(self):
        self._dir = self.lookAt - self.position
        return self._dir.normalized()

    @property
    def up(self):
        return self._up.normalized()

    @property
    def center(self):
        self._center = self.position + self.direction
        return self._center

    @property
    def right(self):
        return self._right

    def orthoRayCast(self, i, j, width, height):
        l = (0 - width / 2.0 + 0.5)
        r = (width - width / 2.0 + 0.5)
        b = (0 - height / 2.0 + 0.5)
        t = (500 - height / 2.0 + 0.5)
        u = l + (r - l) * (i + 0.5) / (r - l)
        v = b + (t - b) * (j + 0.5) / (t - b)
        rayOrigin = self.position + u * self._right + v * self._up
        rayDirection = self._dir
        return Ray(rayOrigin, rayDirection.normalized())

    def perspectiveRayCast(self,  i, j, width, height):
        l = (0 - width / 2.0 + 0.5)
        r = (width - width / 2.0 + 0.5)
        b = (0 - height / 2.0 + 0.5)
        t = (height - height / 2.0 + 0.5)
        u = l + (r - l) * (i + 0.5) / (r - l)
        v = b + (t - b) * (j + 0.5) / (t - b)
        rayDirection = (- self.viewingPlaneDistance * self._back + u * self._right + v * self._up) - self._pos
        return Ray(self.position, rayDirection.normalized())

    def obliqueRayCast(self, i, j, width, height):
        l = (0 - width / 2.0 + 0.5)
        r = (width - width / 2.0 + 0.5)
        b = (0 - height / 2.0 + 0.5)
        t = (height - height / 2.0 + 0.5)
        u = l + (r - l) * (i + 0.5) / (r - l)
        v = b + (t - b) * (j + 0.5) / (t - b)
        rayDirection = u * self._right + v * self._up - self._back * self.viewingPlaneDistance
        return Ray(self.position, rayDirection.normalized())

    def rayTrace(self, x, y, width, height, s=1.0):
        y = height - y
        xw = s * (x - 0.5 * (width + 1.0))
        yw = s * (y - 0.5 * (height + 1.0))
        s = xw * self._right + yw * self._up - self._back * self.viewingPlaneDistance
        return Ray(self.position, (s - self.position).normalized())
