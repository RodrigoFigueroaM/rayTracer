#! /usr/bin/env python
from PyQt5.QtGui import QVector3D
from rayTracer.TraceObjects import Surface, Light
from rayTracer.PPM import PPMFile
from rayTracer.Ray import Ray
from rayTracer.Auxiliary3DMath import reflect

EPSILON = 0.0000001


class World(object):
    @staticmethod
    def renderToFile(camera, scene, maxT, file):
        light = scene.lights[0]
        for y in range(0, file.height):
            for x in range(0, file.width):
                t = maxT
                PrimaryRay = camera.rayTrace(x, y, file.height, file.width)
                pixel = rayHitColor(PrimaryRay, camera, light, scene, 0, t, dept=-5)
                pixel = PPMFile.clampPixel(pixel=pixel)
                file.writeQVector3DTofile(pixel)
        file.close()


def rayHitColor(ray, camera, light, scene, minT, maxT, dept):
    if dept > 0:
        return QVector3D(0, 0, 0)
    ambientLightColor = QVector3D(10, 10, 10)
    t, objHit = hit(ray, scene, maxT)
    if objHit:
        p = ray.e + ray.d * t
        pixel = ambientLightColor + objHit.color
        lightDir = (light.c - p).normalized()  # L

        # extra computation ??????
        normal = objHit.normalAt(p)  # N
        eyeDir = (camera.position - p).normalized()  # V
        H = (eyeDir + lightDir).normalized()

        # shadows
        shadowRay = Ray(p, lightDir)
        distanceToLight = p.distanceToPoint(light.c)
        shadowT, shadowObj = hit(shadowRay, scene, distanceToLight)
        if not shadowObj:
            shader = Light.computeBlinnPhongLight(normal=normal,
                                                 lightDirection=lightDir,
                                                 diffuseColor=QVector3D(0.5, 0.5, 0.5),
                                                 lightColor=light.color,
                                                 halfVector=H,
                                                 specularColor=QVector3D(1, 1, 1),
                                                 shininess=light.shininess)
            pixel = pixel + shader
            # Multiple Point Lights
            # pixel = (ambientLight * 0.6) + pixel

        # Ideal specular
        # reflect eye direction on N
        reflectionRayDirection = reflect((p - camera.position), normal)
        reflectionRay = Ray(p, reflectionRayDirection)
        reflectiveMaxT = 10000
        # see what it hits first
        # compute illumination from ray * reflective constant
        pixel += 0.2 * rayHitColor(reflectionRay, camera, light, scene, objHit.epsilon, reflectiveMaxT, dept+1)
        return pixel
    return QVector3D(0, 0, 0)


def hit(ray, scene, infinity):
    t = infinity
    objHit = None
    for obj in scene.objects:
        rayhit = obj.intersect(ray, t0=obj.epsilon, t1=t)
        if rayhit > EPSILON:
            if rayhit < t:
                t = rayhit
                objHit = obj
    return (t, objHit) if t != infinity else (False, objHit)
