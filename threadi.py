#! /usr/bin/env python
import math
from random import random
from multiprocessing import Process, cpu_count, Lock, Pool, Manager, Queue, current_process, Pool
from PyQt5.QtGui import QVector2D, QVector3D
from rayTracer.PPM import PPMFile
from multiprocessing.pool import ThreadPool

class Pixel:
    # lock = Lock()
    def __init__(self, color=QVector3D(0, 0, 0)):
        # self.lock = Lock()
        self.color = color

    def update_color(self, color):
        self.color = color

    def clamp(self):
        """ Clamps values for a given pixel(color) between 0 and 255
        :param pixel:  QVector3D color to be clamped
        :return:
            QVector3D clamped_pixel with values between 0 and 255 for rgb(x,y,z) parameters
        """
        if self.color.x() > 255:
            self.color.setX(255)
        elif self.color.x() < 0:
            self.color.setX(0)

        if self.color.y() > 255:
            self.color.setY(255)
        elif self.color.y() < 0:
            self.color.setY(0)

        if self.color.z() > 255:
            self.color.setZ(255)
        elif self.color.z() < 0:
            self.color.setZ(0)


def worker2(i):
    """thread worker function"""
    # print("in",pixel.lock,  pixel.lock.acquire())
    # print("IN")
    # if not pixel.lock.acquire():
    # pixel.lock.acquire()
    # print(current_process(), i)
    # pixel.update_color(QVector3D(100, 0, 100))
    # print(pixel)
    # pixel.update_color(QVector3D(100, 0, 100))
    # pixel.lock.release()
    return QVector3D(100, 0, 100)
    # pixel.color = QVector3D(0, 0, 0)
    # print("out", pixel.color)
    # lock.release()


def simple_worker(x):
    """thread worker function"""
    # print("in", x)
    # if not lock.acquire():
    # lock.acquire()
    x = 1
    # print("out", x)
    # lock.release()
    # return

def worker(num, lock, pixels_colors):
    """thread worker function"""
    print("HE")
    if not lock.acquire():
        lock.acquire()
        pixels_colors[num] = QVector3D(0, 0, 0)
        lock.release()
    return


def f(x):
    print(x)
    return x*x


def change_color():
    pixel = QVector3D(0, 0, 0)
    return  pixel


def with_no_threads():
    '''
    real    0m5.421s
    user    0m5.183s
    sys     0m0.210s
    '''
    import time
    start = time.time()
    WIDTH = 100
    HEIGHT = 100
    file = PPMFile("no_thread" + str(WIDTH) + "x" + str(HEIGHT) + ".ppm", WIDTH, HEIGHT)
    print('WORKING ON ', file.name)

    pixels = [Pixel() for i in range(0, WIDTH * HEIGHT)]
    colors = [worker2(pix) for pix in pixels]
    colors = [pix.color for pix in pixels]

    file.start()
    file.write_list_to_file(colors)
    file.close()
    end = time.time()
    print (end - start)


def with_threads():
    import time
    start = time.time()
    WIDTH = 100
    HEIGHT = 100
    file = PPMFile("thread" + str(WIDTH) + "x" + str(HEIGHT) + ".ppm", WIDTH, HEIGHT)
    print('WORKING ON ', file.name)

    pixels = [Pixel() for i in range(0, WIDTH * HEIGHT)]
    num_cores = cpu_count()
    pool =  Pool(processes=num_cores)
    # pool = ThreadPool(processes=num_cores)
    print("Using", num_cores, " Cores")
    print("pool", pool)
    print(pixels[0], pixels[0].color)
    for i in range(0, WIDTH * HEIGHT):
        r = pool.apply_async(worker2, (i,))
        pixels[i].color = r.get()
    pool.close()
    pool.join()

    # for i in range(10):
    #     print(pixels[i].color)
    colors = [pix.color for pix in pixels]
    print(pixels[0], pixels[0].color)
    file.start()
    file.write_list_to_file(colors)
    file.close()
    end = time.time()
    print (end - start)


from  PyQt5.QtCore import QThreadPool, QRunnable

class Worker(QRunnable):
    def __init__(self):
        super(Worker, self).__init__()

    def run(self):
        print("ASDASD")
        # pixel = QVector3D(100,0,100)
        # return QVector3D(100,0,100)

def with_Qthreads():
    import time
    start = time.time()
    WIDTH = 100
    HEIGHT = 100
    file = PPMFile("thread" + str(WIDTH) + "x" + str(HEIGHT) + ".ppm", WIDTH, HEIGHT)
    print('WORKING ON ', file.name)

    pixels = [Pixel() for i in range(0, WIDTH * HEIGHT)]
    num_cores = cpu_count()
    pool =  QThreadPool()
    pool.setMaxThreadCount(num_cores)
    # pool = ThreadPool(processes=num_cores)
    print("Using", num_cores, " Cores")
    print("pool", pool)
    # print(pixels[0], pixels[0].color)
    worker = Worker()
    for i in range(0, WIDTH * HEIGHT):
        r = pool.start(worker)
        print(r)
        # pixels[i].color = r.get()
    pool.close()
    pool.join()

    # for i in range(10):
    #     print(pixels[i].color)
    colors = [pix.color for pix in pixels]
    print(pixels[0], pixels[0].color)
    file.start()
    file.write_list_to_file(colors)
    file.close()
    end = time.time()
    print (end - start)


if __name__ == '__main__':
    with_Qthreads()
    # with_threads()
    # with_no_threads()
   #  p = multiprocessing.Pool()
   #  num_cores = cpu_count()
   #  p = multiprocessing.Pool(processes=num_cores)
   #  for i in range (0,100000):
   #      res = p.apply_async(f, (i,))
   #      print(res.get())
