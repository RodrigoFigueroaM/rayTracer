#! /usr/bin/env python
from PyQt5.QtGui import QVector3D
from rayTracer.TraceObjects import Surface, Light
from rayTracer.PPM import PPMFile
from rayTracer.Ray import Ray
from rayTracer.Auxiliary3DMath import reflect
import math

EPSILON = 0.0000001

background = QVector3D(20, 20, 100)


class World(object):
    def __init__(self, background = QVector3D(0,0,0)):
        self.background = background
    @staticmethod
    def renderToFile(camera, scene, maxT, file):
        light = scene.lights[0]
        for y in range(0, file.height):
            for x in range(0, file.width):
                t = maxT
                PrimaryRay = camera.rayTrace(x, y, file.height, file.width)
                pixelColor = rayHitColor(PrimaryRay, camera, light, scene, 0, t, dept=-5)
                pixelColor = PPMFile.clampPixel(pixel=pixelColor)
                file.writeQVector3DTofile(pixelColor)
        file.close()


def rayHitColor(ray, camera, light, scene, minT, maxT, dept):
    if light.intersect(ray, t0=minT, t1=maxT) > EPSILON:
        return light.color

    if dept > 0:
        return background
    ambientLightColor = QVector3D(10, 10, 10)
    t, objHit = hit(ray, scene, maxT)
    if objHit:
        p = ray.e + ray.d * t
        pixelColor = ambientLightColor + objHit.color
        lightDir = (light.c - p).normalized()  # L
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
            pixelColor = shader + objHit.color
            # Multiple Point Lights
            # pixel = (ambientLight * 0.6) + pixel



        # Ideal specular
        if objHit.material == 'reflective':
            # reflect eye direction on N
            reflectionRayDirection = reflect((p - camera.position), normal)
            reflectionRay = Ray(p, reflectionRayDirection)
            reflectiveMaxT = 10000
            # see what it hits first
            # compute illumination from ray * reflective constant
            pixelColor += 0.2 * rayHitColor(reflectionRay, camera, light, scene, objHit.epsilon, reflectiveMaxT, dept+1)



        # Refraction
        # Dielectrics we need some refractive index n, lets use optical glass: 1.49–1.92;
        # if p on Dalectric
        n = 1.5
        if objHit.material == 'dielectric':
            reflectionRefractionRayDirection = reflect(ray.d, normal)
            if QVector3D.dotProduct(ray.d, normal) < 0:
                refractionRayDir = refract(ray.d, normal, n)[1]
                cosTheta = QVector3D.dotProduct(-ray.d, normal)
                kr = kg = kb = 255
            else:
                # ?????????????
                a = 1.57
                kr = math.exp(- math.log(a) * t)
                kg = math.exp(- math.log(a) * t)
                kb = math.exp(- math.log(a) * t)
                isRayRefracted, refractionRayDir = refract(ray.d, -normal, 1/n)
                if isRayRefracted:
                    cosTheta = QVector3D.dotProduct(refractionRayDir, normal)
                else:
                    reflectionColor = QVector3D(kr, kg, kb)
                    color = hit(Ray(p, reflectionRefractionRayDirection), scene, 10000)[1]
                    #MAYBE
                    return reflectionColor * color.color
            R0 = ((n - 1) * (n - 1)) / ((n + 1) * (n + 1))
            R = R0 + (1 - R0) * (1 - cosTheta) ** 5
            color = hit(Ray(p, reflectionRefractionRayDirection), scene, 10000)[1]
            color2 = hit(Ray(p, refractionRayDir), scene, 10000)[1]
            if color and color2:
                return R * color.color + (1 - R) * color2.color
            if color and not color2:
                return R * color.color
            if color2 and not color:
                return (1 - R) * color2.color
        return pixelColor
    return background


def hit(ray, scene, infinity):
    t = infinity
    objHit = None
    for obj in scene.objects:
        rayhit = obj.intersect(ray, t0=obj.epsilon, t1=t)
        if rayhit > obj.epsilon:
            if rayhit < t:
                t = rayhit
                objHit = obj
    return (t, objHit) if t != infinity else (False, objHit)


def refract(d, n, indexOfrefractionNew):
    """
    :param d: eye dir
    :param n: normal
    :param refractiveIndex:
    :return:
    """
    indexOfrefractionOriginal = 1.0 # air
    refractiveIndex = indexOfrefractionOriginal / indexOfrefractionNew
    DdotN = QVector3D.dotProduct(d, n)
    insidephi = 1 - (refractiveIndex * refractiveIndex * (1 - (DdotN * DdotN)))
    t = None
    isRayRefracted = False
    if insidephi > 0.0:  # if negative theres no ray, all of the energy is reflected. known as total internal reflection
        cosphi = math.sqrt(insidephi)
        t = refractiveIndex * (d - n * DdotN) - n * cosphi
        isRayRefracted = True
    return isRayRefracted, t