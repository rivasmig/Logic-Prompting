from PyQt5 import QtOpenGL
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import OpenGL.GL as gl
from OpenGL import GLU
from OpenGL.arrays import vbo
import numpy as np

from .GL_Geometry import Cube

class GL_Renderer(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.thisCube = Cube()

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0, 255))    # initialize the screen to blue
        gl.glEnable(gl.GL_DEPTH_TEST)
        self.thisCube.initGeometry()
    
    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
    
    def mousePressEvent(self, event):
        # Get the click position
        x = event.x()
        y = event.y()
        
        # Check which mouse button was pressed
        if event.button() == Qt.LeftButton:
            print(f"Left button clicked at ({x}, {y})")
        elif event.button() == Qt.RightButton:
            print(f"Right button clicked at ({x}, {y})")
        elif event.button() == Qt.MiddleButton:
            print(f"Middle button clicked at ({x}, {y})")
        self.thisCube.move(x=x, y=y)
        # If you need to pass the event up the chain (to parent widgets or to perform default behavior), 
        # you can call the base class's implementation:
        super().mousePressEvent(event)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.thisCube.paintGL()
