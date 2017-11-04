#! /usr/bin/env python
from enum import Enum

class Material(object):
    class Type(Enum):
        Default, Reflective, Dielectric = range(3)

    def __init__(self, type=None, n=None):
        self.type = type
        self.n = n

        if self.type == self.Type.Dielectric and self.n < 1.0:
            raise ValueError('n on Dialectric has to be greater than 1')