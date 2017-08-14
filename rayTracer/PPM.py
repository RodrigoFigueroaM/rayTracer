#! /usr/bin/env python
from PyQt5.QtGui import QVector3D


class PPMFile(object):
    def __init__(self, filename, width, height):
        """
        :param filename:  str to save file with given filename
        :param WIDTH:  int width for image
        :param HEIGHT:  int height for imafe
        :return:
            file outfile
        """
        self.name = filename
        self.width = width
        self.height = height
        self.file = open(filename, "w")
        self.file.write("P3\n")
        self.file.write("# {}.ppm\n".format(filename))
        self.file.write(str(width) + " " + str(height) + "\n")
        self.file.write("255\n")

    def writeQVector3DTofile(self, vector=None):
        self.file.write(str(int(vector.x())) + " " + str(int(vector.y())) + " " + str(int(vector.z())) + "\n")

    def writePlainString(self, str):
        self.file.write(str)

    def writeListToFile(self, vectorList=None):
        for vector in vectorList:
            self.file.write(str(int(vector.x())) + " " + str(int(vector.y())) + " " + str(int(vector.z())) + "\n")

    def close(self):
        self.file.close()

    @staticmethod
    def clampPixel(pixel=QVector3D()):
        """ Clamps values for a given pixel(color) between 0 and 255
        :param pixel:  QVector3D color to be clamped
        :return:
            QVector3D clampedPixel with values between 0 and 255 for rgb(x,y,z) parameters
        """
        clampedPixel = QVector3D()
        if pixel.x() > 255:
            clampedPixel.setX(255)
        elif pixel.x() < 0:
            clampedPixel.setX(0)
        else:
            clampedPixel.setX(pixel.x())
        if pixel.y() > 255:
            clampedPixel.setY(255)
        elif pixel.y() < 0:
            clampedPixel.setY(0)
        else:
            clampedPixel.setY(pixel.y())
        if pixel.z() > 255:
            clampedPixel.setZ(255)
        elif pixel.z() < 0:
            clampedPixel.setZ(0)
        else:
            clampedPixel.setZ(pixel.z())
        del pixel
        return clampedPixel
