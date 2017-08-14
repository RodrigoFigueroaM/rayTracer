#! /usr/bin/env python
from PyQt5.QtGui import QVector3D
from rayTracer.TraceObjects import Surface, Light
from rayTracer.PPM import PPMFile
from rayTracer.Ray import Ray

EPSILON = 0.0000001


class World(object):
    @staticmethod
    def renderToFile(camera, scene, maxT, file):
        light = scene.lights[0]
        for y in range(0, file.height):
            for x in range(0, file.width):
                t = maxT
                PrimaryRay = camera.rayTrace(x, y, file.height, file.width)
                pixel = QVector3D(0, 0, 0)

                if light.intersect(PrimaryRay, t0=0, t1=t) > EPSILON:
                    pixel = light.color

                for obj in scene.objects:
                    PrimaryRayHit = obj.intersect(PrimaryRay, t0=0, t1=t)
                    if PrimaryRayHit > EPSILON:
                        if PrimaryRayHit < t:
                            t = PrimaryRayHit
                            p = PrimaryRay.e + PrimaryRay.d * t
                            lightDir = (light.c - p).normalized()  # L
                            ambientLight = obj.color

                            normal = obj.normalAt(p)  # N
                            eyeDir = (camera.position - p).normalized()  # V
                            H = (eyeDir + lightDir).normalized()
                            color = Light.computeBlinnPhongLight(normal=normal,
                                                       lightDirection=lightDir,
                                                       diffuseColor=QVector3D(0.5, 0.5, 0.5),
                                                       lightColor=light.color,
                                                       halfVector=H,
                                                       specularColor=QVector3D(1, 1, 1),
                                                       shininess=light.shininess)
                            #  Ambient Shading
                            pixel = color
                            # Multiple Point Lights
                            pixel = (ambientLight * 0.6) + pixel

                            # #shadows
                            shadowRay = Ray(p, lightDir)
                            distanceToLight = p.distanceToPoint(light.c)
                            shadowT = distanceToLight
                            for otherObjects in scene.objects:
                                shadowRayHit = otherObjects.intersect(shadowRay, t0=0.0, t1=shadowT)
                                if shadowRayHit > otherObjects.epsilon:
                                    pixel = ambientLight * 0.6

                pixel = PPMFile.clampPixel(pixel=pixel)
                # print(pixel)
                file.writeQVector3DTofile(pixel)
        file.close()