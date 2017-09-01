#! /usr/bin/env python
from PyQt5.QtGui import QVector3D
from rayTracer.Ray import Ray


class Camera(object):
    """docstring for Camera"""
    def __init__(self, position=QVector3D(0, 0, 3),
                 look_at=QVector3D(0, 0, 0),
                 up=QVector3D(0, 1, 0),
                 viewing_plane_distance = 1):
        super(Camera, self).__init__()
        self.position = position
        self.look_at = look_at
        self.viewing_plane_distance = viewing_plane_distance
        #compute uvw
        self._dir = (look_at - self.position).normalized()
        self._back = (self.position - look_at).normalized()
        self._right = QVector3D.crossProduct(up, self._back) # change order?
        self._up = QVector3D.crossProduct(self._back, self._right)
        self._center = self.position + self.direction

    @property
    def direction(self):
        self._dir = self.look_at - self.position
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

    def ray_trace(self, x, y, width, height, s=1.0):
        y = height - y
        xw = s * (x - 0.5 * (width + 1.0))
        yw = s * (y - 0.5 * (height + 1.0))
        sw = xw * self._right + yw * self._up - self._back * self.viewing_plane_distance
        return Ray(self.position, (sw - self.position).normalized())
