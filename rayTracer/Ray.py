#! /usr/bin/env python
class Ray(object):
    """Generate a ray = e + td"""
    def __init__(self, origin, direction):
        self.e = origin
        self.d = direction

    def __str__(self):
        return "e = {}\nd = {}".format(self.e, self.d)