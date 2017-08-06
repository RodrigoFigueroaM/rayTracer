#! /usr/bin/env python
import abc
import math
from PyQt5.QtGui import QMatrix4x4, QVector3D
from pyEngine.Camera import Camera


class RayTracerObject(abc.ABC):
    def __init__(self, color=QVector3D(255, 255, 255)):
        self.color = color

    @abc.abstractmethod
    def intersect(self, ray):
        pass


class Sphere(RayTracerObject):
    """A sphere is defined with center c = (xc,yc,zc) and radius R """
    def __init__(self, center=QVector3D(0, 0, 0), radius=1, color=QVector3D(255, 255, 255)):
        """
        :param center:  QVector3D
        :param radius:  QVector3D
        :param color:  QVector3D
        """
        super().__init__(color)
        self.c = center
        self.r = radius

    def normalAt(self, p):
        """ The normal vector at point p is given by the gradient n = 2(p − c).
            The unit normal is (p − c)/R.
        :param p:  a QVector3D to reference the desired point in the sphere
        :return:
            a QVector3D with the normal at a given point p
        """
        return ((p - self.c)/self.r).normalized()

    def intersect(self, ray):
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
        discriminant = B*B - 4 * A * C
        if discriminant < 0.000001:
            return False
        t0 = (- B + math.sqrt(discriminant))
        t1 = (- B - math.sqrt(discriminant))
        return True


class Triangle(RayTracerObject):
    """A triangle can be defined only with three vertices """
    def __init__(self, a=QVector3D(0, 0, 0), b=QVector3D(0, 2, 0), c=QVector3D(2, 0, 0), color=QVector3D()):
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

    def intersect(self, ray, t0=0, t1=1):
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

        t = T.determinant()/A.determinant()
        # First compute t
        if (t < t0) or (t > t1):
            return False
        # Then compute γ
        y = Y.determinant()/A.determinant()
        if (y < 0) or (y > 1):
            return False
        # Finally compute β
        b = B.determinant()/A.determinant()
        if (b < 0) or (b > 1-y):
            return False
        return True

    @property
    def normal(self):
        return QVector3D.crossProduct(self.c - self.a, self.b - self.a)


class Light(Sphere):
    def __init__(self, origin, direction, color):
        super().__init__(origin, direction, color)

    def intersect(self, ray):
        return super().intersect(ray)


class Ray:
    """generate a ray = e + td"""
    def __init__(self, origin, direction):
        self.e = origin
        self.d = direction


def initFile(filename, WIDTH=500, HEIGHT=500):
    """
    :param filename:  str to save file with given filename
    :param WIDTH:  int width for image
    :param HEIGHT:  int height for imafe
    :return:
        file outfile
    """
    outfile = open(filename, "w")
    outfile.write("P3\n")
    outfile.write("# output.ppm\n")
    outfile.write(str(WIDTH) + " " + str(HEIGHT) + "\n")
    outfile.write("255\n")
    return outfile


def computeLight(normal, lightDirection, diffuseColor, lightColor, halfVector, specularColor, shininess):
    """ Compute light for Blinn-Phon shader
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
    lambert = NdotL * diffuseColor * lightColor * max(NdotL, 0.0)
    NdotH = QVector3D.dotProduct(normal, halfVector)
    specular = lightColor * specularColor * pow(max(NdotH, 0.0), shininess)
    return lambert + specular


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
    return R

def clampPixel(pixel = QVector3D()):
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

def main():
    WIDTH = 500
    HEIGHT = 500
    file = initFile("output.ppm")
    camera = Camera( position=QVector3D(0, 1.1, -3),
                 direction=QVector3D(0, 1, 0),
                 up=QVector3D(0, 1, 0),
                 fov = 90)

    spheres = [Sphere(QVector3D(WIDTH * 0.5, HEIGHT * 0.5, 50), 50,  QVector3D(100, 0, 0)),
                Sphere(QVector3D(WIDTH * 0.5, 100 + HEIGHT * 0.5, 20), 20, QVector3D(0, 0, 0)),
                Sphere(QVector3D(WIDTH * 0.6, -100 + HEIGHT * 0.5, 25), 30, QVector3D(0, 0, 100)),
                Sphere(QVector3D(WIDTH * 0.2, HEIGHT * 0.2, 20), 20, QVector3D(200, 0, 200))]

    light = Light(QVector3D(100, 0, -200), 2, color=QVector3D(220, 220, 220))

    triangle = Triangle(a=QVector3D(0, 0, 0), b=QVector3D(0, 500, 0),
                        c=QVector3D(500, 0, 0), color=QVector3D(200, 130, 100))

    R = QMatrix4x4()
    R.rotate(60, 0, 20)
    camera.rotate(R)
    eyeDir = camera.direction
    print(camera.position)
    print(camera.direction)
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            # ra = camera.mouseRay(x,y,WIDTH,HEIGHT)
            # print(ra[0].x(), ra[0].y(), ra[0].z())
            # ray = Ray(camera.position, camera.direction )
            # ray = Ray(camera.panTo(QVector3D(x,y,0))[0], camera.panTo(QVector3D(x,y,0))[1])
            ray = Ray(QVector3D(x, y, 0), QVector3D(0, 0, 1))
            pixel = QVector3D(0, 0, 0)

            if triangle.intersect(ray):
                ambientLight = QVector3D(51, 51, 51)
                p = ray.e + ray.d
                lightDir = QVector3D.normalized(light.c - p)  # L
                normal = triangle.normal  # N
                eyeDir = QVector3D(0, 0, 0)  # V
                R = reflect(lightDir, normal)
                H = (lightDir + eyeDir).normalized()
                NdotL = QVector3D.dotProduct(normal, lightDir)

                color = computeLight(normal=normal,
                                     lightDirection=lightDir,
                                     diffuseColor=QVector3D(0.5, 0.5, 0.5),
                                     lightColor=light.color,
                                     halfVector=H,
                                     specularColor=QVector3D(1, 1, 1),
                                     shininess=3000)

                dt = QVector3D.dotProduct(lightDir.normalized(), normal.normalized())

                pixel = ambientLight + triangle.color + color
                pixel = clampPixel(pixel=pixel)

            for sphere in spheres:
                if sphere.intersect(ray):
                    ambientLight = QVector3D(51, 51, 51)
                    p = ray.e + ray.d
                    lightDir = QVector3D.normalized(light.c - p)  # L
                    normal = sphere.normalAt(p)  # N
                    eyeDir = QVector3D(0, 0, 0)  # V
                    R = reflect(lightDir, normal)
                    H = (lightDir + eyeDir).normalized()
                    NdotL = QVector3D.dotProduct(normal, lightDir)

                    color = computeLight(normal=normal,
                                         lightDirection=lightDir,
                                         diffuseColor=QVector3D(0.5, 0.5, 0.5),
                                         lightColor=light.color,
                                         halfVector=H,
                                         specularColor=QVector3D(1, 1, 1),
                                         shininess= 150)

                    dt = QVector3D.dotProduct(lightDir.normalized(), normal.normalized())

                    pixel = ambientLight + sphere.color + color
                    pixel = clampPixel(pixel=pixel)

            if light.intersect(ray):
                pixel = light.color

            file.write(str(int(pixel.x())) + " " + str(int(pixel.y())) + " " + str(int(pixel.z())) + "\n")
    file.close()


if __name__ == "__main__":
    main()
    print("DONE")
    exit(0)

