import math
from PyQt5 import QtOpenGL, QtGui, QtCore
from PyQt5.QtWidgets import QOpenGLWidget, QLineEdit
from PyQt5.QtCore import Qt
import OpenGL.GL as gl
from OpenGL import GLU
from typing import List
from PyQt5.QtGui import QSurfaceFormat, QVector4D, QMatrix4x4
from draw_elements import point, element
from .logic_window import Logic_Window
from .GL_Geometry import *

class GL_Renderer(QOpenGLWidget):
    def __init__(self, parent=None, bckColor=(152,255,174,217)):
        self.invoker = RendererInvoker()
        format = QSurfaceFormat()
        format.setOption(QSurfaceFormat.DebugContext)
        QSurfaceFormat.setDefaultFormat(format)
        super(GL_Renderer, self).__init__(parent)
        self.single = Logic_Window.getInstance()
        self.parent = parent
        self.geometries: List[BaseGeometry] = [None] * 5
        self.canvasElements: List[BaseGeometry] = []
        self.iconSize = 0.5
        self.setMouseTracking(True)
        self.c = (bckColor[0]/255, bckColor[1]/255, bckColor[2]/255, 1)

        self.highlightedCanvasElement = None

        # ui movement stuff
        self.cameraPosition = (0, 0, -30)  # Initialize with default camera position
        self.zoomSpeed = 0.5 # speed of zooming in and out
        self.isPanning = False  # To check if panning is currently active
        self.panSpeed = 0.04  # Adjust this value to control the panning speed
        self.lastMousePos = None  # Store the last mouse position

        self.MaX, self.miX, self.MaY, self.miY = self.getViewExtentsAtDepth()

    def initializeGeometries(self):
        for geometry in self.geometries:
            if isinstance(geometry, Image):
                geometry.setCameraPos(self.cameraPosition)
                geometry.initGeometry()
                geometry.initializeTextures()

    def initializeCanvasElements(self):
        for ce in self.canvasElements:
            for ele in self.single.fileManager.Current_Media.get_elements():
                if ce.parentElement == ele:
                    ce.setParentElement(ele)
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
        if media_index != -1:
            self.canvasElements.clear()
            mediaElements = self.single.fileManager.Current_Media.get_elements()
            if mediaElements:
                for e in mediaElements:
                    ex, ey = 0 , 0
                    if e.attributes:
                        posIndex = e.attributes.index('Position')
                        ex = e.attributes[posIndex+1][0]
                        ey = e.attributes[posIndex+1][1]
                        #add image for the point
                        pointImage = Image(width=self.iconSize, height=self.iconSize, 
                                           position=(ex, ey, 0), parentElement=e)
                        self.canvasElements.append(pointImage)
                        self.initializeGL()
                        self.paintGL()

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
        else:
            self.geometries = [None] * 5
            self.canvasElements = []
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
        depth = -self.cameraPosition[2]  # Depth should be positive. Assuming negative Z values are forward in your setup.
        fovY = math.radians(45.0)

        # Calculate aspect ratio
        aspectRatio = self.width() / float(self.height())

        # Calculate frustum dimensions at the given depth
        frustumHeight = 2.0 * math.tan(fovY / 2) * depth
        frustumWidth = frustumHeight * aspectRatio

        # Calculate min and max values considering the camera's panning
        halfWidth = frustumWidth / 2
        halfHeight = frustumHeight / 2

        maxX = halfWidth
        minX = -halfWidth
        maxY = halfHeight
        minY = -halfHeight

        return maxX, minX, maxY, minY

    def screenPosToGLPos(self, sx, sy):
        # Dimensions of the OpenGL widget
        widget_cW = self.width()
        widget_cH = self.height()

        # Get the extents of the view at the current depth
        maxX, minX, maxY, minY = self.getViewExtentsAtDepth()

        # Calculate the fractions of the width and height that the screen coordinates represent
        widthFract = sx / widget_cW
        heightFract = 1 - (sy / widget_cH)  # Subtracting from 1 because OpenGL's origin is bottom-left, while QWidget's is top-left

        # Map these fractions to the OpenGL coordinate space
        newX = (minX + widthFract * (maxX - minX)) - self.cameraPosition[0]
        newY = (minY + heightFract * (maxY - minY)) - self.cameraPosition[1]

        return (newX), (newY)

    def wheelEvent(self, event):
        # Zoom In
        if event.angleDelta().y() > 0:
            self.moveCamera(0, 0, self.zoomSpeed)
        # Zoom Out
        elif event.angleDelta().y() < 0:
            self.moveCamera(0, 0, -1*self.zoomSpeed)
        self.initializeGL()
        self.paintGL()

    def addPoint(self, log_single, elementList, screenToGL, initializeThis, paintThis, eventX, eventY):
        if log_single.fileManager.Current_Media is not None:
                draw_mode = log_single.fileManager.Current_Media.get_draw_mode()
                nx, ny = screenToGL(eventX, eventY)
                if draw_mode=='Point':
                    newPoint = point.Point()
                    newPoint.add_pos_attribute(nx, ny)

                    #add image for the point
                    pointImage = Image(image_path=newPoint.image, width=2, height=2, 
                                       position=(nx, ny, 0), isIcon=True)
                    elementList.append(pointImage)
                    initializeThis()
                    paintThis()

                    log_single.fileManager.Current_Media.add_element(newPoint)
                    self.logSingle.makeLineEdit(self.eventX, self.eventY, 50, 30)

    def mouseInOutCanvasElements(self, mouseX, mouseY, mouseInBound, mouseOutBound):
        changed = False
        mx, my = self.screenPosToGLPos(mouseX, mouseY)
        for c in self.canvasElements:
            if c.checkCollisionXY(mx, my):  # Modify the method to return True if changes are made
                changed = True
                if c.isHighlighted:
                    self.highlightedCanvasElement = c
                    mouseInBound(c, mouseX, mouseY)
                else:
                    self.highlightedCanvasElement = None
                    mouseOutBound(c, mouseX, mouseY)
        if changed:  # Only update OpenGL if changes were made
            self.initializeGL()
            self.paintGL()

    def makeUILabel(self, canvasElement, mouseX, mouseY):
        myEle = None
        for e in self.single.fileManager.Current_Media.get_elements():
            if e.localName == canvasElement.elementName:
                myEle = e
        if myEle is not None:
            self.single.makeLabelAtPos(mouseX, mouseY, 
                                    70, 20, myEle.getTextAttribute())
    
    def deleteUILabel(self, canvasElement, mouseX, mouseY):
        self.single.deleteExistingLabel()

    def deleteCanvasElement(self, canvasElement):
        print('got in here')
        delete_point_cmd = DeletePoint(self, canvasElement)
        self.invoker.storeAndExecute(delete_point_cmd)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.isPanning = True
            self.lastMousePos = (event.x(), event.y())
        if event.button() == Qt.LeftButton:
            add_point_cmd = AddPoint(self, self.single, event.x(), event.y())
            self.invoker.storeAndExecute(add_point_cmd)
        if event.button() == Qt.RightButton:
            if self.highlightedCanvasElement is not None:
                self.deleteCanvasElement(self.highlightedCanvasElement)
    
    def mouseMoveEvent(self, event):
        if self.isPanning:
            dx = event.x() - self.lastMousePos[0]
            dy = event.y() - self.lastMousePos[1]
            self.moveCamera(dx * self.panSpeed, -dy * self.panSpeed, 0)  # Negative dx because moving mouse right should move camera left
            self.lastMousePos = (event.x(), event.y())
            self.initializeGL()
            self.paintGL()
        self.mouseInOutCanvasElements(event.x(), event.y(), 
                                 self.makeUILabel, self.deleteUILabel)
        
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.isPanning = False
            self.lastMousePos = None

class RendererInterface():
    def __init__(self, renderer):
        self.renderer: GL_Renderer = renderer
        self.previous = None
        self.next = None

    def execute(self):
        pass

    def undo(self):
        self.renderer.initializeGL()
        self.renderer.paintGL()

    def redo(self):
        self.renderer.initializeGL()
        self.renderer.paintGL()

class AddPoint(RendererInterface):
    def __init__(self, GLRenderer, log_single, eventX, eventY):
        super().__init__(GLRenderer)
        self.logSingle = log_single
        self.eventX = eventX
        self.eventY = eventY
    
    def execute(self):
        if self.logSingle.fileManager.Current_Media is not None:
            draw_mode = self.logSingle.fileManager.Current_Media.get_draw_mode()
            nx, ny = self.renderer.screenPosToGLPos(self.eventX, self.eventY)
            if draw_mode == 'Point':
                newPoint = point.Point()
                addedType = self.renderer.single.fileManager.addedType
                if addedType is not None:
                    newPoint.add_standardized_attribute(addedType)
                newPoint.add_pos_attribute(nx, ny)
                # add image for the point
                pointImage = Image(width=self.renderer.iconSize, height=self.renderer.iconSize, 
                                   position=(nx, ny, 0), parentElement=newPoint)
                self.renderer.canvasElements.append(pointImage)
                self.renderer.initializeGL()
                self.renderer.paintGL()

                self.logSingle.makeLineEdit(self.eventX, self.eventY, 80, 30)
                self.logSingle.fileManager.Current_Media.add_element(newPoint)
                
    def undo(self):
        if self.renderer.canvasElements:
            self.renderer.canvasElements.pop()
        super().undo()
    
    def redo(self):
        self.execute()
        super().redo()

class DeletePoint(RendererInterface):
    def __init__(self, renderer, canvasElement):
        super().__init__(renderer)
        self.canvaselement = canvasElement
        self.ele_index_removed = None
        self.canvas_index = None
    def execute(self):
        for canvas_index, c in enumerate(self.renderer.canvasElements):
            if c == self.canvaselement:
                self.canvas_index = canvas_index
                for idx, e in enumerate(self.renderer.single.fileManager.Current_Media.get_elements()):
                    if e.localName == self.canvaselement.elementName:
                        self.ele_index_removed = idx
                        self.renderer.single.fileManager.Current_Media.delete_element(e)
                        break
                self.renderer.canvasElements.remove(c)
                self.renderer.single.clearNotNeeded()
                break
        super().execute()
    def undo(self):
        if self.canvas_index:
            self.renderer.canvasElements.insert(self.canvas_index, self.canvaselement)
        super().undo()
    def redo(self):
        self.execute()
        super().redo()

class RendererInvoker():
    def __init__(self):
        self.command_history = []  # This will store the history of commands for undo functionality
        self.undo_stack = []  # This will store commands that have been undone for redo functionality
    
    def storeAndExecute(self, cmd):
        """
        Store the command and execute it.
        """
        cmd.execute()
        self.command_history.append(cmd)
        # Clear the undo stack because a new command has been executed
        self.undo_stack.clear()
    
    def undo(self):
        """
        Undo the last command.
        """
        if not self.command_history:
            return
        cmd = self.command_history.pop()
        cmd.undo()
        self.undo_stack.append(cmd)
    
    def redo(self):
        """
        Redo the last undone command.
        """
        if not self.undo_stack:
            return
        cmd = self.undo_stack.pop()
        cmd.redo()
        self.command_history.append(cmd)
