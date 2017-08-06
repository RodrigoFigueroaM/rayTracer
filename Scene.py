#!/usr/bin/env python
import ctypes

import OpenGL.GL as GL
from PyQt5.Qt import Qt
from PyQt5.QtCore import QElapsedTimer
from PyQt5.QtGui import QMatrix4x4, QVector3D

from Widgets.GLStandardWindow3D import GLStandardWindow3D
from pyEngine.Camera import Camera
from pyEngine.GLProgram import GLProgram
from pyEngine.Geometry.Grid import Grid
from pyEngine.Model import Model
from pyEngine.TrackBall import TrackBall

# TODO: fix obj loader indices(texture)(normals?)
# TODO: model class :- refractor and make functional model class
# TODO: new window system
# TODO: refactor


# IMG_FILE = '/Users/rui/Desktop/githubStuff/ComputerGraphics/ShaderToy/textures/zen.jpg'


VERT_FILE2 = './shaders/shafae_blinn_phong.vert'
FRAG_FILE2 = './shaders/shafae_blinn_phong.frag'

VERT_FILE = './shaders/blinPhong.vert'
FRAG_FILE = './shaders/blinPhong.frag'
MODEL_FILE = '/Users/rui/Desktop/githubStuff/ComputerGraphics/ShaderToy/objs/Cerberus.obj'

GRID_VERT = './shaders/grid.vert'
GRID_FRAG = './shaders/grid.frag'


class Scene(GLStandardWindow3D):
    def __init__(self):
        super(Scene, self).__init__()
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)

        self._camera = Camera()

        # properties
        self.trackBall = TrackBall()
        self.rotation = QMatrix4x4()
        self.normalMatrix = QMatrix4x4()

        # properties interaction
        self.key = None
        self.showWireFrame = True

        # methods
        self.initCamera()
        self.model = Model(MODEL_FILE)

        #grid lists
        self.grid = Grid()

        # GLPROGRAMS
        self.program = GLProgram(self, numAttibutesInvbo=3)
        self.gridProgram = GLProgram(self, numAttibutesInvbo=3)

    def initializeGL(self):
        super(Scene, self).initializeGL()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glClearColor(0.36, 0.36, 0.36, 1.0)
        # self.program.addTexture(IMG_FILE)

        self.program.initProgram(VERT_FILE,
                                 FRAG_FILE,
                                 self.model.drawingVertices,
                                 self.model.verticesIndices,
                                 attribs=[0, 1, 2])

        self.gridProgram.initProgram(GRID_VERT,
                                     GRID_FRAG,
                                     self.grid.drawingVertices,
                                     self.grid.verticesIndices,
                                     attribs=[0, 1, 2])

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glViewport(0, 0, self.width, self.height)

        self.ratio = self.width / self.height
        self.camera.setPerspective(self.camera.fov, self.ratio, 0.1, 100.0)

        self.camera.lookAtCenter()
        self.camera.position = self.rotation * self.camera.position

        if self.showWireFrame:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        else:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)

        self.drawProgramSubroutine(self.program, GL.GL_TRIANGLES)
        self.drawProgramSubroutine(self.gridProgram, GL.GL_LINES)
        # self.update()

    def initCamera(self):
        self._camera = Camera(position=QVector3D(1.5, 1, 1.5),
                              direction=QVector3D(0.5, 0, 0.5),
                              up=QVector3D(0, 1, 0),
                              fov=90)

    def drawProgramSubroutine(self, program, mode=GL.GL_TRIANGLE_STRIP):
        nullptr = ctypes.c_void_p(0)
        program.bind()
        program.bindTimer()
        program.setUniformValue('modelViewMatrix', self.camera.modelViewMatrix)
        program.setUniformValue('normalMatrix', self.camera.normalMatrix)
        program.setUniformValue('projectionMatrix', self.camera.projectionMatrix)
        # GL.glDrawArrays(GL.GL_TRIANGLES, 0, (len(program.vertices)//8))
        GL.glDrawElements(mode, len(program.indices), GL.GL_UNSIGNED_INT, nullptr)
        program.unbind()

    def mousePressEvent(self, event):
        self.pressClick = QVector3D(event.x(), self.height - event.y(), 0)
        self.trackBall.clicked(event.x(), event.y(), self.width, self.height)
        self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.releaseClick = QVector3D(event.x(), self.height - event.y(), 0)
            self.rotation = self.trackBall.move(event.x(), event.y(), self.width, self.height)
            self.update()

    def mouseReleaseEvent(self, event):
        self.key = None

    def wheelEvent(self, QWheelEvent):
        self.camera.fov -= QWheelEvent.angleDelta().y() / 40
        self.update()

    def keyPressEvent(self, QKeyEvent):
        self.key = QKeyEvent.key()
        if QKeyEvent.key() == Qt.Key_R:
            self.showWireFrame = not self.showWireFrame
            self.update()

    @property
    def camera(self):
        return self._camera


def initTimer(interval=100):
    timer = QElapsedTimer()
    timer.start()
    return timer