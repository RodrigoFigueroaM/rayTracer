#! /usr/bin/env python
from PyQt5.QtGui import QVector3D
from rayTracer.TraceObjects import Surface, Light
from rayTracer.PPM import PPMFile
from rayTracer.Ray import Ray
from rayTracer.Auxiliary3DMath import reflect
import math

EPSILON = 0.0000001


class World(object):
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
    if dept > 0:
        return QVector3D(0, 0, 0)
    ambientLightColor = QVector3D(10, 10, 10)
    t, objHit = hit(ray, scene, maxT)
    if objHit:
        p = ray.e + ray.d * t
        pixelColor = ambientLightColor + objHit.color
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
            # shader = Light.computeBlinnPhongLight(normal=normal,
            #                                      lightDirection=lightDir,
            #                                      diffuseColor=QVector3D(0.5, 0.5, 0.5),
            #                                      lightColor=light.color,
            #                                      halfVector=H,
            #                                      specularColor=QVector3D(1, 1, 1),
            #                                      shininess=light.shininess)
            NdotL = QVector3D.dotProduct(normal, lightDir)
            reflectVect = reflect(lightDir, normal)
            shader = Light.computeGoochLight(objHit.color, NdotL, reflectVect, camera.position)
            pixelColor = shader + objHit.color
            # pixelColor = o + shader
            # Multiple Point Lights
            # pixel = (ambientLight * 0.6) + pixel

        # Refraction
        # Dielectrics we need some  refractive index n, lets use optical glass: 1.49–1.92;
        # if p on Dalectric
        if objHit.material == 'dielectric':
            reflectionRefractionRayDirection = reflect(eyeDir, normal)
            if QVector3D.dotProduct(eyeDir, normal) < 0:
                isRayRefracted, refracterRayDir = refract(eyeDir, normal, 1.5)
                # print("eyeDir", eyeDir)
                # print("refractDirection", refractDirection)
                cosTheta = QVector3D.dotProduct(-eyeDir, normal)
                reflectionColor = QVector3D(255, 255, 255)
            else:
                # ?????????????
                a = 1.5
                kr = math.exp(- math.log(a) * t)
                kg = math.exp(- math.log(a) * t)
                kb = math.exp(- math.log(a) * t)
                isRayRefracted, refracterRayDir = refract(eyeDir, normal, 1/1.5)
                if isRayRefracted:
                    cosTheta = QVector3D.dotProduct(refracterRayDir, normal)
                else:
                    reflectionColor = QVector3D(kr, kg, kb)
                    print(reflectionColor * pixelColor)
                    return reflectionColor * pixelColor
            R0 = ((1.5 - 1) * (1.5 - 1)) / ((1.5 + 1) * (1.5 + 1))
            R = R0 + (1 - R0) * (1 - cosTheta) ** 5
            return R * pixelColor + (1 - R) * pixelColor
        if objHit.material == 'reflective':
            # Ideal specular
            # reflect eye direction on N
            reflectionRayDirection = reflect((p - camera.position), normal)
            reflectionRay = Ray(p, reflectionRayDirection)
            reflectiveMaxT = 10000
            # see what it hits first
            # compute illumination from ray * reflective constant
            pixelColor += 0.2 * rayHitColor(reflectionRay, camera, light, scene, objHit.epsilon, reflectiveMaxT, dept+1)

        return pixelColor
    return QVector3D(0, 0, 0)


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
    indexOfrefractionOriginal = 1.0
    refractiveIndex = indexOfrefractionOriginal / indexOfrefractionNew
    DdotN = QVector3D.dotProduct(d, n)
    insidephi = 1 - (refractiveIndex * refractiveIndex * (1 - (DdotN * DdotN)))
    t = None
    isRayRefracted = False
    if insidephi > 0.00001:  # if negative theres no ray, all of the energy is reflected. known as total internal reflection
        cosphi = math.sqrt(insidephi)
        t = refractiveIndex * (d - n * DdotN) - n * cosphi
        isRayRefracted = True
    return isRayRefracted, t