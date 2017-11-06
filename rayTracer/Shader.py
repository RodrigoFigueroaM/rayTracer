#! /usr/bin/env python
import abc
from rayTracer.Auxiliary3DMath import reflect
from PyQt5.QtGui import QMatrix4x4, QVector3D


class Shader(abc.ABC):
    def __init__(self, color=QVector3D(255, 255, 255)):
        self.color = color

    @abc.abstractmethod
    def compute(self, point, object, light, camera):
        pass


class Blinn_Phong(Shader):
    def __init__(self, color):
        super().__init__(color=color)

    def compute(self, point, object, light, camera):
        """ Compute light for Blinn-Phong shader
               :param point:  QVector3D point at point t
               :param object:  Primitive object that got hit
               :param light:  Light
               :param camera: Camera
               :return:
                   QVector3D with calculated value for lambert + specular
        """
        return Matte(self.color).compute(point, object, light, camera) + Specular(self.color).compute(point, object, light, camera)


class Phong(Shader):
    def __init__(self, color):
        super().__init__(color=color)

    def compute(self, point, object, light, camera):
        """ Compute light for Blinn-Phong shader
               :param point:  QVector3D point at point t
               :param object:  Primitive object that got hit
               :param light:  Light
               :param camera: Camera
               :return:
                   QVector3D with calculated value for lambert + specular
        """
        specular_color = QVector3D(1.0, 1.0, 1.0)
        ambient_color = QVector3D(0.2,0.2,0.2)
        light_dir = light.direction(point)  # L
        normal = object.normal_at(point)  # N
        eye_dir = (camera.position - point).normalized()  # V
        R = reflect(light_dir, normal)  # R
        NdotR = QVector3D.dotProduct(-R, normal)
        specular = light.color * specular_color * pow(max(NdotR, 0.0), light.shininess)
        return Matte(self.color).compute(point, object, light, camera) + specular


class Matte(Shader):
    def __init__(self, color):
        super().__init__(color=color)

    def compute(self, point, object, light, camera):
        """ Compute light for matte shader
                      :param point:  QVector3D point at point t
                      :param object:  Primitive object that got hit
                      :param light:  Light
                      :param camera: Camera
                      :return:
                          QVector3D with calculated value for lambert
               """
        diffuse_Color = QVector3D(0.5, 0.5, 0.5)
        diffuse_coefficient = 0.9
        light_dir = light.direction(point)  # L
        normal = object.normal_at(point)  # N
        NdotL = QVector3D.dotProduct(light_dir, normal)
        lambert = diffuse_coefficient * diffuse_Color * light.color * max(NdotL, 0.0)
        return lambert


class Specular(Shader):
    def __init__(self, color):
        super().__init__(color=color)

    def compute(self, point, object, light, camera):
        """ Compute light for matte shader
                      :param point:  QVector3D point at point t
                      :param object:  Primitive object that got hit
                      :param light:  Light
                      :param camera: Camera
                      :return:
                          QVector3D with calculated value for lambert
               """
        specular_color = QVector3D(1.0, 1.0, 1.0)
        light_dir = light.direction(point)  # L
        normal = object.normal_at(point)  # N
        eye_dir = (camera.position - point).normalized()  # V
        half_vector = (eye_dir + light_dir).normalized()
        NdotH = QVector3D.dotProduct(normal, half_vector)
        specular = light.color * specular_color * pow(max(NdotH, 0.0), light.shininess)
        return specular