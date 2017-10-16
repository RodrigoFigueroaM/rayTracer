#! /usr/bin/env python
from PyQt5.QtGui import QMatrix4x4, QVector3D
from enum import Enum


class Material:
    class Type(Enum):
        Default, Reflective, Dielectric = range(3)

    def __init__(self, type=None, color=QVector3D(255, 255, 255), n=None):
        self.type = type
        self.color = color
        self.n = n
        
        if self.type == self.Type.Dielectric and self.n < 1.0:
            raise ValueError('n on Dialectric has to be greater than 1')