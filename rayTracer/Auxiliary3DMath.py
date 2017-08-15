#! /usr/bin/env python
from PyQt5.QtGui import QMatrix4x4, QVector3D


def reflect(I, N):
    """ Calculates reflection direction using:
        I - 2.0 * dot(N, I) * N.
    :param I:  QVector3D incident vector
    :param N:  QVector3D normal vector
    :return:
            QVector3D vector reflection direction
    """
    Nnorm = N.normalize()
    R = I - 2.0 * QVector3D.dotProduct(I, N) * N
    return R.normalized()
