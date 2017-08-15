#! /usr/bin/env python
import abc
import math
from PyQt5.QtGui import QMatrix4x4, QVector3D

EPSILON = 0.0000001


class Surface(abc.ABC):
    def __init__(self, color=QVector3D(255, 255, 255), material=None):
        self.color = color
        self.material = material
        self._epsilon = EPSILON

    @abc.abstractmethod
    def intersect(self, ray, t0=0, t1=10000):
        pass

    @abc.abstractmethod
    def epsilon(self):
        return self._epsilon


class Sphere(Surface):
    """A sphere is defined with center c = (xc,yc,zc) and radius R """

    def __init__(self, center=QVector3D(0, 0, 0), radius=1.0, color=QVector3D(255, 255, 255)):
        """
        :param center:  QVector3D
        :param radius:  QVector3D
        :param color:  QVector3D
        """
        super().__init__(color)
        self.c = center
        self.r = radius
        self._epsilon = 0.1

    def normalAt(self, p):
        """ The normal vector at point p is given by the gradient n = 2(p − c).
            The unit normal is (p − c)/R.
        :param p:  a QVector3D to reference the desired point in the sphere
        :return:
            a QVector3D with the normal at a given point p
        """
        return (p - self.c).normalized()

    def intersect(self, ray, t0=0, t1=10000):
        """ Given a ray p(t) = e + td and an implicit surface f(p) = 0.
            We can represent a sphere in vector form:
            (p−c)·(p−c)−R2 = 0.
            Any point p that satisfies this equation is on the sphere.
            plug in p(t) in previous equation yields:
            (e+td−c)·(e+td−c)−R2 = 0
            which can be rearranged as :
            (d·d)t2 +2d·(e−c)t+(e−c)·(e−c)−R2 =0.
            giving us a quadratic equation, for which we can solve for t
            :param ray:  a Ray to p(t) = e + td
            :return:
                False if the discriminant is negative
                True if discriminant is positive and there are two solution
        """
        ec = ray.e - self.c
        A = QVector3D.dotProduct(ray.d, ray.d)
        B = QVector3D.dotProduct(2 * ray.d, ec)
        C = QVector3D.dotProduct(ec, ec) - self.r * self.r
        discriminant = B * B - 4 * A * C
        if discriminant < EPSILON:
            return -1.0
        localt0 = (- B + math.sqrt(discriminant)) / 2 * A
        localt1 = (- B - math.sqrt(discriminant)) / 2 * A
        t = min(localt0, localt1)
        return min(t, t1)

    @property
    def epsilon(self):
        return self._epsilon

    @epsilon.setter
    def epsilon(self, epsilon):
        self._epsilon = epsilon

    def __str__(self):
        return "{}".format(self.color)


class Triangle(Surface):
    """A triangle can be defined only with three vertices """

    def __init__(self, a=QVector3D(0, 0, 0), b=QVector3D(0, 2, 0), c=QVector3D(2, 0, 0),
                 color=QVector3D(255, 255, 255)):
        """
        :param a:  QVector3D
        :param b:  QVector3D
        :param c:  QVector3D
        """
        super().__init__(color)
        self.a = a
        self.b = b
        self.c = c
        self._normal = self.normal
        self._epsilon = 0.001

    def intersect(self, ray, t0=0, t1=10000):
        """ To determine intersection we need a system of linear equations:
            e+td=f(u,v), we have three unknowns t,u, and v.
            The intersection will occur when
            e + td = a + β(b − a) + γ(c − a)
            The intersection is inside the triangle if and only if β > 0, γ > 0, and β + γ < 1.
            Otherwise, the ray has hit the plane outside the triangle.
            If there are no solutions, either the triangle is degenerate or
            the ray is parallel to the plane containing the triangle.
        :param ray:  a Ray to p(t) = e + td
        :return:
            True if and only if β > 0, γ > 0, and β + γ < 1.
        """
        A = QMatrix4x4(self.a.x() - self.b.x(), self.a.x() - self.c.x(), ray.d.x(), 0,
                       self.a.y() - self.b.y(), self.a.y() - self.c.y(), ray.d.y(), 0,
                       self.a.z() - self.b.z(), self.a.z() - self.c.z(), ray.d.z(), 0,
                       0, 0, 0, 1)

        B = QMatrix4x4(self.a.x() - ray.e.x(), self.a.x() - self.c.x(), ray.d.x(), 0,
                       self.a.y() - ray.e.y(), self.a.y() - self.c.y(), ray.d.y(), 0,
                       self.a.z() - ray.e.z(), self.a.z() - self.c.z(), ray.d.z(), 0,
                       0, 0, 0, 1)

        Y = QMatrix4x4(self.a.x() - self.b.x(), self.a.x() - ray.e.x(), ray.d.x(), 0,
                       self.a.y() - self.b.y(), self.a.y() - ray.e.y(), ray.d.y(), 0,
                       self.a.z() - self.b.z(), self.a.z() - ray.e.z(), ray.d.z(), 0,
                       0, 0, 0, 1)

        T = QMatrix4x4(self.a.x() - self.b.x(), self.a.x() - self.c.x(), self.a.x() - ray.e.x(), 0,
                       self.a.y() - self.b.y(), self.a.y() - self.c.y(), self.a.y() - ray.e.y(), 0,
                       self.a.z() - self.b.z(), self.a.z() - self.c.z(), self.a.z() - ray.e.z(), 0,
                       0, 0, 0, 1)

        if not A.determinant() == 0:
            t = T.determinant() / A.determinant()
            # First compute t
            if t1 < t < t0:
                return False
            # Then compute γ
            y = Y.determinant() / A.determinant()
            if (y < 0) or (y > 1):
                return False
            # Finally compute β
            b = B.determinant() / A.determinant()
            if (b < 0) or (b > 1 - y):
                return False
        return t

    def normalAt(self, p):
        return self._normal

    @property
    def normal(self):
        return QVector3D.crossProduct(self.c - self.a, self.b - self.a).normalized()

    @property
    def epsilon(self):
        return self._epsilon

    @epsilon.setter
    def epsilon(self, epsilon):
        self._epsilon = epsilon


class Polygon(Surface):
    """A Polygon m vertices p1 through pm"""

    def __init__(self, vertices=[], color=QVector3D(255, 255, 255)):
        """
        :param vertices: list of QVector3D
        :param color:
        """
        super().__init__(color)
        self.vertices = vertices
        self._normal = self.normal

    def intersect(self, ray):
        p1 = self.vertices[0]
        denom = QVector3D.dotProduct(ray.d, self._normal)
        t = QVector3D.dotProduct(p1 - ray.e, self._normal) / denom
        if abs(denom) < EPSILON:  # the  polygon is parallel to the ray
            return False
        p = ray.e + t * ray.d
        return True

    def normalAt(self, p):
        return self._normal

    @property
    def normal(self):
        a = self.vertices[0]
        b = self.vertices[1]
        c = self.vertices[2]
        return QVector3D.crossProduct(c - a, b - a)


class Light(Sphere):
    def __init__(self, origin, direction, color, shininess = 1.0):
        super().__init__(origin, direction, color)
        self.shininess = shininess

    def intersect(self, ray, t0=0, t1=10000):
        return super().intersect(ray, t0, t1)

    @staticmethod
    def computeBlinnPhongLight(normal, lightDirection, diffuseColor, lightColor, halfVector, specularColor, shininess):
        """ Compute light for Blinn-Phong shader
        :param normal:  QVector3D normal at point t
        :param lightDirection:  QVector3D direction of light
        :param diffuseColor:  QVector3D
        :param lightColor:  QVector3D
        :param halfVector:  QVector3D
        :param specularColor:  QVector3D
        :param shininess:  QVector3D
        :return:
            QVector3D with calculated value for lambert + specular
        """
        NdotL = QVector3D.dotProduct(normal, lightDirection)
        lambert = diffuseColor * lightColor * max(NdotL, 0.0)
        NdotH = QVector3D.dotProduct(normal, halfVector)
        specular = lightColor * specularColor * pow(max(NdotH, 0.0), shininess)
        return lambert + specular