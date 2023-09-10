import math
from PyQt5 import QtOpenGL, QtGui, QtCore
from PyQt5.QtWidgets import QOpenGLWidget, QLineEdit
from PyQt5.QtCore import Qt
import OpenGL.GL as gl
from OpenGL import GLU
from typing import List
from PyQt5.QtGui import QSurfaceFormat, QVector4D, QMatrix4x4
from draw_elements import point, element
from core import Canvas_Manager as cm
from .logic_window import Logic_Window
from .GL_Geometry import *

class GL_Renderer(QOpenGLWidget):
    def __init__(self, parent=None, bckColor=(152,255,174,217)):
        format = QSurfaceFormat()
        format.setOption(QSurfaceFormat.DebugContext)
        QSurfaceFormat.setDefaultFormat(format)
        super(GL_Renderer, self).__init__(parent)
        self.single = Logic_Window.getInstance()
        self.parent = parent
        self.geometries: List[BaseGeometry] = [None] * 5
        self.canvasElements: List[BaseGeometry] = []
        self.c = (bckColor[0]/255, bckColor[1]/255, bckColor[2]/255, 1)

        # ui movement stuff
        self.cameraPosition = (0, 0, -30)  # Initialize with default camera position
        self.zoomSpeed = 0.5 # speed of zooming in and out
        self.isPanning = False  # To check if panning is currently active
        self.panSpeed = 0.04  # Adjust this value to control the panning speed
        self.lastMousePos = None  # Store the last mouse position

    def initializeGeometries(self):
        for geometry in self.geometries:
            if isinstance(geometry, Image):
                geometry.setCameraPos(self.cameraPosition)
                geometry.initGeometry()
                geometry.initializeTextures()

    def initializeCanvasElements(self):
        for ce in self.canvasElements:
            ce.setCameraPos(self.cameraPosition)
            ce.initGeometry()
            ce.initializeTextures()

    def paintCanvasElements(self):
        for ce in self.canvasElements:
            gl.glPushMatrix()
            ce.paintGL()
            gl.glPopMatrix()

    def horizontalOffset(self, index, sWidth, sHeight, oWidth):
        if index == 0 or index == 4:
            return oWidth/2 + sWidth/2
        else:
            return (sWidth/(sWidth/sHeight)) + oWidth/(sWidth/sHeight)
    
    def depthOffset(self, index):
        if index == 0 or index == 4:
            return 1.2
        else:
            return 1.05

    def drawGeometryWithTranslation(self, index):
        geometry = self.geometries[index]
        if not isinstance(geometry, Image):
            return
        # Center image: No translations
        if index == 2:
            gl.glPushMatrix()
            geometry.paintGL()
            gl.glPopMatrix()
            return

        # For images 1 and 3
        center_image = self.geometries[2]
        if isinstance(center_image, Image):
            if index == 1:  # Left of center
                translation_x = -1*self.horizontalOffset(1, self.geometries[1].width, 
                                                         self.geometries[1].height, center_image.width)
                translation_z = -1*self.depthOffset(1)
            elif index == 3:  # Right of center
                translation_x = self.horizontalOffset(3, self.geometries[3].width, 
                                                      self.geometries[3].height, center_image.width)
                translation_z = -1*self.depthOffset(3)
        else:
            return

        # For images 0 and 4
        if index == 0 or index == 4:
            cumulative_width = 0
            for i in [1, 2, 3]:
                img = self.geometries[i]
                if isinstance(img, Image):
                    cumulative_width += img.width
            
            if index == 0:  # Leftmost
                translation_x = -1*self.horizontalOffset(0, self.geometries[0].width, 
                                                         self.geometries[0].height, cumulative_width)
                translation_z = -1*self.depthOffset(0)
            else:  # Rightmost
                translation_x = self.horizontalOffset(4, self.geometries[4].width, 
                                                      self.geometries[4].height, cumulative_width)
                translation_z = -1*self.depthOffset(4)

        gl.glPushMatrix()
        gl.glTranslatef(translation_x, 0, translation_z)
        geometry.paintGL()
        gl.glPopMatrix()

    def paintGeometries(self):
        self.drawGeometryWithTranslation(0)
        self.drawGeometryWithTranslation(4)
        self.drawGeometryWithTranslation(1)
        self.drawGeometryWithTranslation(3)
        self.drawGeometryWithTranslation(2)

    def initializeGL(self):
        gl.glClearColor(self.c[0], self.c[1], self.c[2], self.c[3])
        gl.glEnable(gl.GL_DEPTH_TEST)
        self.initializeGeometries()
        self.initializeCanvasElements()

    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)
        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def updateRenderer(self):
        media_index = self.single.fileManager.get_media_index()

        # Reset the geometries list
        self.geometries = [None] * 5

        # Set the center geometry
        center_path = self.single.fileManager.get_media_path_by_index(media_index)
        self.geometries[2] = Image(image_path=center_path) if center_path else None

        # Set the geometries to the right of center
        for offset in range(1, 3):  # for indices 3 and 4
            path = self.single.fileManager.get_media_path_by_index(media_index + offset)
            if path:
                self.geometries[2 + offset] = Image(image_path=path)

        # Set the geometries to the left of center
        for offset in range(1, 3):  # for indices 1 and 0
            path = self.single.fileManager.get_media_path_by_index(media_index - offset)
            if path:
                self.geometries[2 - offset] = Image(image_path=path)

        self.initializeGeometries()

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.paintGeometries()
        self.paintCanvasElements()

    def moveCamera(self, x: float, y: float, z: float):
        # Update the camera position
        oldPos = self.cameraPosition
        newPos = (oldPos[0]+x, oldPos[1]+y, oldPos[2]+z)
        self.cameraPosition = newPos

    def getViewExtentsAtDepth(self):
        # Assuming you have a vertical field of view of 45 degrees for simplicity
        # Adjust as necessary
        depth = self.cameraPosition[2]
        fovY = math.radians(45.0)
        
        # Calculate aspect ratio
        aspectRatio = self.width() / float(self.height())
        
        # Calculate frustum dimensions at the given depth
        frustumHeight = 2.0 * math.tan(fovY / 2) * depth
        frustumWidth = frustumHeight * aspectRatio
        
        # Calculate min and max values
        maxX = frustumWidth / 2
        minX = -maxX
        maxY = frustumHeight / 2
        minY = -maxY
        
        return maxX, minX, maxY, minY

    def screenPosToGLPos(self, sx, sy):
        widget_cW = self.width()
        widget_cH = self.height()
        global_position = self.mapToGlobal(self.pos())
        global_x = global_position.x()
        global_y = global_position.y()
        maxX, minX, maxY, minY = self.getViewExtentsAtDepth()
        heightFract = (sy-global_y)/widget_cH
        widthFract = (sx-global_x)/widget_cW
        
        if heightFract <= 0.5:
            newY = maxY*(heightFract+heightFract)
        else:
            newY = minY*(heightFract+heightFract)
        if widthFract <= 0.5:
            newX = maxX*(widthFract+widthFract)
        else:
            newX = minX*(widthFract+widthFract)

        return newX, newY

    def wheelEvent(self, event):
        # Zoom In
        if event.angleDelta().y() > 0:
            self.moveCamera(0, 0, self.zoomSpeed)
        # Zoom Out
        elif event.angleDelta().y() < 0:
            self.moveCamera(0, 0, -1*self.zoomSpeed)
        self.initializeGL()
        self.paintGL()

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.isPanning = True
            self.lastMousePos = (event.x(), event.y())
        if event.button() == Qt.LeftButton:
            if self.single.fileManager.Current_Media is not None:
                draw_mode = self.single.fileManager.Current_Media.get_draw_mode()
                nx, ny = self.screenPosToGLPos(event.x(), event.y())
                if draw_mode=='Point':
                    newPoint = point.Point()
                    newPoint.add_pos_attribute(nx, ny)

                    #add image for the point
                    pointImage = Image(image_path=newPoint.image, width=1, height=1, 
                                       position=(nx, ny, 0), isIcon=True)
                    self.canvasElements.append(pointImage)
                    self.initializeGL()
                    self.paintGL()
                    
                    #create Line Edit
                    textAttributeEdit = QLineEdit(self.single)
                    textAttributeEdit.move(event.x(), event.y())

                    self.single.fileManager.Current_Media.add_element(newPoint)
    
    def mouseMoveEvent(self, event):
        if self.isPanning:
            dx = event.x() - self.lastMousePos[0]
            dy = event.y() - self.lastMousePos[1]
            self.moveCamera(dx * self.panSpeed, -dy * self.panSpeed, 0)  # Negative dx because moving mouse right should move camera left
            self.lastMousePos = (event.x(), event.y())
            self.initializeGL()
            self.paintGL()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.isPanning = False
            self.lastMousePos = None

