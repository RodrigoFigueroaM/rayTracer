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

class World(object):
    def __init__(self, background=QVector3D(0, 0, 0), antialiasing_level=1, dept=0):
        self.background = background
        self.antialiasing_level = antialiasing_level
        self.depth = dept

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

    def render_to_file_using_treads_per_ray(self, camera, scene, max_t, file):
        """Computing paraller per ray"""
        self.scene = scene
        self.camera = camera
        self.file = file

        num_cores = cpu_count()
        pool = ThreadPool(processes=num_cores)

        pixels = [Pixel() for i in range(0, file.width * file.height)]
        for yx in range(0, file.width * file.height):
            t = max_t
            pixels[yx].color = QVector3D()
            for p in range(0, self.antialiasing_level):
                for q in range(0, self.antialiasing_level):
                    for light in self.scene.lights:
                        color = pool.apply_async(self.worker_per_ray, (yx, t, p, q, light))
                        pixels[yx].color += color.get()
            pixels[yx].color = pixels[yx].color / (self.antialiasing_level * self.antialiasing_level)
            pixels[yx].clamp()
        pool.close()
        pool.join()
        pixel_color = [pix.color for pix in pixels]
        file.start()
        file.write_list_to_file(pixel_color)
        file.close()

    def worker_per_ray(self, yx, t, p, q, light):
        primary_ray = self.camera.ray_trace((yx % self.file.width) + (p + random()) / self.antialiasing_level,
                                            (yx // self.file.width) + (q + random()) / self.antialiasing_level,
                                            self.file.height,
                                            self.file.width)
        return self.__ray_hit_color(primary_ray, self.camera, self.scene, 0, t, dept=self.depth,
                                            light=light)

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


    def render_to_file(self, camera, scene, max_t, file):
        pixels = []
        for y in range(0, file.height):
            for x in range(0, file.width):
                t = max_t
                # for loops for  Antialiasing using jittering
                pixel_color = QVector3D()
                for p in range(0, self.antialiasing_level):
                    for q in range(0, self.antialiasing_level):
                        for light in scene.lights:
                            primary_ray = camera.ray_trace(x + (p + random()) / self.antialiasing_level,
                                                           y + (q + random()) / self.antialiasing_level, file.height,
                                                           file.width)
                            pixel_color += self.__ray_hit_color(primary_ray, camera, scene, 0, t, dept=self.depth, light=light)

                pixel_color = PPMFile.clamp_pixel( pixel=pixel_color / (self.antialiasing_level * self.antialiasing_level))
                pixels.append(pixel_color)
        file.start()
        file.write_list_to_file(pixels)
        file.close()

    def __ray_hit_color(self, ray, camera, scene, min_t, max_t, dept, light):
        if light.intersect(ray, t0=min_t, t1=max_t) > EPSILON:
            return light.color

        if dept > 0:
            return self.background

        ambient_light_color = QVector3D(10, 10, 10)
        t, obj_hit = hit(ray, scene, max_t)
        if obj_hit:
            p = ray.e + ray.d * t
            pixel_color = ambient_light_color + obj_hit.material.color
            light_dir = (light.c - p).normalized()  # L
            normal = obj_hit.normal_at(p)  # N
            eye_dir = (camera.position - p).normalized()  # V
            H = (eye_dir + light_dir).normalized()

            # shadows
            shadow_ray = Ray(p, light_dir)
            distance_to_light = p.distanceToPoint(light.c)
            shadow_t, shadow_obj = hit(shadow_ray, scene, distance_to_light)
            if not shadow_obj:
                shader = Light.compute_Blinn_Phong_light(normal=normal,
                                                         light_direction=light_dir,
                                                         diffuse_Color=QVector3D(0.5, 0.5, 0.5),
                                                         light_color=light.color,
                                                         half_vector=H,
                                                         specular_color=QVector3D(1, 1, 1),
                                                         shininess=light.shininess)
                pixel_color = shader + obj_hit.material.color
                # Multiple Point Lights
                pixel_color = (ambient_light_color * 0.6) + pixel_color

            # Ideal specular
            if obj_hit.material.type == Material.Type.Reflective:
                # reflect eye direction on N
                reflection_ray_direction = reflect((p - camera.position), normal)
                reflection_ray = Ray(p, reflection_ray_direction)
                reflective_max_t = 10000
                # see what it hits first
                # compute illumination from ray * reflective constant
                pixel_color += 0.2 * self.__ray_hit_color(reflection_ray, camera, scene, obj_hit.epsilon,
                                                          reflective_max_t, dept + 1, light)

            # Refraction
            # Dielectrics we need some refractive index n, lets use optical glass: 1.49–1.92;
            # if p on dielectric
            if obj_hit.material.type == Material.Type.Dielectric:
                n = obj_hit.material.n
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
                        color = hit(Ray(p, reflection_refraction_ray_direction), scene, 10000)[1]
                        return reflection_color * color.color
                R0 = ((n - 1) * (n - 1)) / ((n + 1) * (n + 1))
                R = R0 + (1 - R0) * (1 - cos_theta) ** 5
                reflection_object = hit(Ray(p, reflection_refraction_ray_direction), scene, 10000)[1]
                reflection_object2 = hit(Ray(p, refraction_ray_dir), scene, 10000)[1]
                if reflection_object and reflection_object2:
                    return R * reflection_object.material.color + (1 - R) * reflection_object2.material.color + obj_hit.material.color
                if reflection_object and not reflection_object2:
                    return R * reflection_object.material.color + obj_hit.material.color
                if reflection_object2 and not reflection_object:
                    return (1 - R) * reflection_object2.material.color + obj_hit.material.color
            return pixel_color 
        return self.background


def hit(ray, scene, infinity):
    t = infinity
    obj_hit = None
    for obj in scene.objects:
        rayhit = obj.intersect(ray, t0=obj.epsilon, t1=t)
        if rayhit > obj.epsilon:
            if rayhit < t:
                t = rayhit
                obj_hit = obj
    return (t, obj_hit) if t != infinity else (False, obj_hit)


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
