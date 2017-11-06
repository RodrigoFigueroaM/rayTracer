#! /usr/bin/env python
import math
import os
from random import random, sample
from multiprocessing import cpu_count, Pool , current_process
from multiprocessing import Pool

from PyQt5.QtGui import QVector3D, QVector2D
from rayTracer.PrimitiveObjects import Surface, Light
from rayTracer.PPM import PPMFile
from rayTracer.Ray import Ray
from rayTracer.Auxiliary3DMath import reflect
from rayTracer.Material import Material

EPSILON = 0.0000001


def refract(d, n, new_index_of_refraction):
    """
    :param d: eye dir
    :param n: normal
    :param new_index_of_refraction:
    :return:
    """
    original_index_of_refraction = 1.0  # air
    refractive_index = original_index_of_refraction / new_index_of_refraction
    DdotN = QVector3D.dotProduct(d, n)
    inside_phi = 1 - (refractive_index * refractive_index * (1 - (DdotN * DdotN)))
    t = None
    is_ray_refracted = False
    # if negative there's no ray, all of the energy is reflected. known as total internal reflection
    if inside_phi > 0.0:
        cos_phi = math.sqrt(inside_phi)
        t = refractive_index * (d - n * DdotN) - n * cos_phi
        is_ray_refracted = True
    return is_ray_refracted, t


class World(object):
    def __init__(self, background=QVector3D(0, 0, 0),  ambient_color = QVector3D(10, 10, 10), antialiasing_level=1, dept=0):
        self.background = background
        self.ambient_color = ambient_color
        self.antialiasing_level = antialiasing_level
        self.depth = dept
        self.camera = None
        self.scene = None
        self.file = None

    def render_to_file_using_treads_per_pixel(self, camera, scene, max_t, file, num_threads):
        """ computing parallel per pixel """
        self.scene = scene
        self.camera = camera
        self.file = file

        num_cores = num_threads
        pool = Pool(processes=num_cores)
        print("Using", num_cores, " Cores")
        print("pool", pool)

        # color = pool.apply_async(self.worker_per_pixel, range(file.width * file.height))
        # color = pool.map(self.worker_per_pixel,(yx,))[0]
        # color = pool.apply(self.worker_per_pixel,(yx,) )
        # color = pool.map_async(self.worker_per_pixel, range( file.width * file.height)).get()
        color = pool.map(self.worker_per_pixel, range( file.width * file.height))

        pool.close()
        pool.join()
        file.start()
        file.write_list_to_file(color)
        file.close()

    def worker_per_pixel(self, yx):
        t = 10000.0
        pixel = QVector3D()
        # for loops for  Antialiasing using jittering
        for p in range(0, self.antialiasing_level):
            for q in range(0, self.antialiasing_level):
                for light in self.scene.lights:
                    primary_ray = self.camera.ray_trace((yx % self.file.width) + (p + random()) / self.antialiasing_level,
                                                   (yx // self.file.width) + (q + random()) / self.antialiasing_level,
                                                   self.file.height,
                                                   self.file.width)
                    pixel += self.__ray_hit_color(primary_ray, self.camera, self.scene, 0, t, dept=self.depth,
                                                             light=light)
        pixel = pixel / (self.antialiasing_level * self.antialiasing_level)
        pixel = PPMFile.clamp_pixel(pixel=pixel)
        return pixel

    def __ray_hit_color(self, ray, camera, scene, min_t, max_t, dept, light):
        if light.intersect(ray, t0=min_t, t1=max_t) > EPSILON:
            return light.color

        if dept > 0:
            return self.background

        t, obj_hit = self.hit(ray,  max_t)
        if obj_hit:
            p = ray.e + ray.d * t
            pixel_color = self.ambient_color + obj_hit.shader.color

            # shadows
            shadow_ray = Ray(p, light.direction(p))
            distance_to_light = p.distanceToPoint(light.c)
            shadow_t, shadow_obj = self.hit(shadow_ray, distance_to_light)
            if not shadow_obj:
                shader = obj_hit.shader.compute( point=p, object=obj_hit, light=light, camera=camera)
                pixel_color = shader + obj_hit.shader.color
                # Multiple Point Lights
                pixel_color = (self.ambient_color * 0.6) + pixel_color

            # Reflective
            if obj_hit.material.type == Material.Type.Reflective:
                pixel_color += self.reflective(obj_hit, p, dept, light)

            # Refraction
            if obj_hit.material.type == Material.Type.Dielectric:
                dielectric = self.dielectric(obj_hit, ray, t)
                return dielectric if dielectric else pixel_color
            return pixel_color
        return self.background

    def reflective(self, obj_hit, point, dept, light):
        # Ideal specular
        # reflect eye direction on N
        normal = obj_hit.normal_at(point)
        reflection_ray_direction = reflect((point - self.camera.position), normal)
        reflection_ray = Ray(point, reflection_ray_direction)
        reflective_max_t = 10000
        # see what the new ray hits first
        # compute illumination from ray * reflective constant
        return 0.2 * self.__ray_hit_color(reflection_ray, self.camera, self.scene, obj_hit.epsilon,
                                                      reflective_max_t, dept + 1, light)

    def dielectric(self, obj_hit, ray, t):
        p = ray.e + ray.d * t
        n = obj_hit.material.n
        normal = obj_hit.normal_at(p)
        reflection_refraction_ray_direction = reflect(ray.d, normal)
        if QVector3D.dotProduct(ray.d, normal) < 0:
            refraction_ray_dir = refract(ray.d, normal, n)[1]
            cos_theta = QVector3D.dotProduct(-ray.d, normal)
            kr = kg = kb = 255
        else:
            a = 1.57
            kr = math.exp(- math.log(a) * t)
            kg = math.exp(- math.log(a) * t)
            kb = math.exp(- math.log(a) * t)
            is_ray_refracted, refraction_ray_dir = refract(ray.d, -normal, n / 0.5)
            if is_ray_refracted:
                cos_theta = QVector3D.dotProduct(refraction_ray_dir, normal)
            else:
                reflection_color = QVector3D(kr, kg, kb)
                color = self.hit(Ray(p, reflection_refraction_ray_direction), 10000)[1]
                return reflection_color * color.color
        R0 = ((n - 1) * (n - 1)) / ((n + 1) * (n + 1))
        R = R0 + (1 - R0) * (1 - cos_theta) ** 5
        reflection_object = self.hit(Ray(p, reflection_refraction_ray_direction), 10000)[1]
        reflection_object2 = self.hit(Ray(p, refraction_ray_dir), 10000)[1]
        if reflection_object and reflection_object2:
            return R * reflection_object.shader.color + (1 - R) * reflection_object2.shader.color + obj_hit.shader.color
        if reflection_object and not reflection_object2:
            return R * reflection_object.shader.color + obj_hit.shader.color
        if reflection_object2 and not reflection_object:
            return (1 - R) * reflection_object2.shader.color + obj_hit.shader.color
        # else:
        #     return QVector3D(0, 0, 0)

    def hit(self, ray, infinity):
        t = infinity
        obj_hit = None
        for obj in self.scene.objects:
            rayhit = obj.intersect(ray, t0=obj.epsilon, t1=t)
            if rayhit > obj.epsilon:
                if rayhit < t:
                    t = rayhit
                    obj_hit = obj
        return (t, obj_hit) if t != infinity else (False, obj_hit)
