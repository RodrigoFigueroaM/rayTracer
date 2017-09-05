#! /usr/bin/env python
from PyQt5.QtGui import QVector3D


class PPMFile(object):
    def __init__(self, file_name, width, height):
        """
        :param file_name:  str to save file with given filename
        :param WIDTH:  int width for image
        :param HEIGHT:  int height for imafe
        :return:
            file outfile
        """
        self.name = file_name
        self.width = width
        self.height = height
        self.file = None

    def start(self):
        self.file = open(self.name, "w")
        self.file.write("P3\n")
        self.file.write("# {}.ppm\n".format(self.name))
        self.file.write(str(self.width) + " " + str(self.height) + "\n")
        self.file.write("255\n")

    def write_QVector3D_to_file(self, vector=None):
        self.file.write(str(int(vector.x())) + " " + str(int(vector.y())) + " " + str(int(vector.z())) + "\n")

    def write_plain_string(self, str):
        self.file.write(str)

    def write_list_to_file(self, vectorList=None):
        for vector in vectorList:
            self.file.write(str(int(vector.x())) + " " + str(int(vector.y())) + " " + str(int(vector.z())) + "\n")

    def close(self):
        self.file.close()

    @staticmethod
    def clamp_pixel(pixel=QVector3D()):
        """ Clamps values for a given pixel(color) between 0 and 255
        :param pixel:  QVector3D color to be clamped
        :return:
            QVector3D clamped_pixel with values between 0 and 255 for rgb(x,y,z) parameters
        """
        clamped_pixel = QVector3D()
        if pixel.x() > 255:
            clamped_pixel.setX(255)
        elif pixel.x() < 0:
            clamped_pixel.setX(0)
        else:
            clamped_pixel.setX(pixel.x())
        if pixel.y() > 255:
            clamped_pixel.setY(255)
        elif pixel.y() < 0:
            clamped_pixel.setY(0)
        else:
            clamped_pixel.setY(pixel.y())
        if pixel.z() > 255:
            clamped_pixel.setZ(255)
        elif pixel.z() < 0:
            clamped_pixel.setZ(0)
        else:
            clamped_pixel.setZ(pixel.z())
        del pixel
        return clamped_pixel
