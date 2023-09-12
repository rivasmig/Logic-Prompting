from qt_ui import logic_window as lw
from qt_ui import GL_Renderer as gr

import os
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

class GenericTab():
    def __init__(self):
        self.single = lw.Logic_Window.getInstance()
    
    def thisResizeEvent(self):
        pass

class LabelTab(GenericTab):
    def __init__(self):
        super().__init__()
        self.initializeFunction()

    def buttonConnections(self):
        self.single.ui.pointButton.clicked.connect(self.pointButtonClick)
        self.single.ui.handButton.clicked.connect(self.handButtonClick)
        self.single.ui.forwardButton.clicked.connect(self.forwardButtonClick)
        self.single.ui.rewindButton.clicked.connect(self.rewindButtonClick)
        self.single.ui.boxButton.clicked.connect(self.boxButtonClick)
        self.single.ui.polygonButton.clicked.connect(self.polygonButtonClick)
        self.single.ui.arrowButton.clicked.connect(self.arrowButtonClick)

    def initializeFunction(self):
        self.buttonConnections()

        self.resizeOffset = 20
        tabColor = self.single.ui.logicModes.palette().midlight().color().getRgb()
        self.glWidget = gr.GL_Renderer(self.single, bckColor=(tabColor))

        # Get the parent of the carouselView
        parent_widget = self.single.ui.carouselView.parent()

        # Remove the carouselView from its parent's layout (if it has one)
        layout = parent_widget.layout()

        # Delete the carouselView
        self.single.ui.carouselView.deleteLater()

        # Set the geometry of the glWidget to match the old carouselView's geometry
        self.glWidget.setGeometry(self.single.ui.carouselView.geometry())

        # If there was a layout, add the glWidget to the layout
        if layout:
            layout.addWidget(self.glWidget)
        else:
            # If there was no layout, just set the parent of the glWidget directly
            self.glWidget.setParent(parent_widget)

        # Update the carouselView reference in Logic_Window to point to the glWidget
        self.single.ui.carouselView = self.glWidget

        # Ensure the OpenGL context is current
        self.single.ui.carouselView.makeCurrent()

        timer = qtc.QTimer(self.single)
        timer.setInterval(20)  # period, in milliseconds
        timer.timeout.connect(self.single.ui.carouselView.update)
        timer.start()

        self.raiseFrames()

    def raiseFrames(self):
        # Ensuring that frames overlay on the carouselView (unchanged)
        self.single.ui.actionTypeFrame.raise_()
        self.single.ui.swapFrame.raise_()
        self.single.ui.toolsFrame.raise_()

    def thisResizeEvent(self):
        super().__init__()
        # Manually adjust the size of carouselView
        self.single.ui.carouselView.resize(self.single.ui.imageLabelMode.size())

        # Reposition the frames
        # Here's an example: (Adjust as needed)
        self.single.ui.actionTypeFrame.move(self.resizeOffset, self.resizeOffset)  # Move to top-left corner of carouselView
        self.single.ui.swapFrame.move(self.single.ui.carouselView.width() - self.single.ui.swapFrame.width()
                                       - self.resizeOffset, self.resizeOffset)  # Top-right
        self.single.ui.toolsFrame.move(self.resizeOffset, self.single.ui.carouselView.height() - 
                                       self.single.ui.toolsFrame.height() - self.resizeOffset)  # Bottom-left

    def pointButtonClick(self):
        if self.single.fileManager.Current_Media is not None:
            self.single.changeMouseIcon('Point')
            self.single.fileManager.Current_Media.set_draw_mode('Point')
    
    def handButtonClick(self):
        if self.single.fileManager.Current_Media is not None:
            self.single.changeMouseIcon('Default')
            self.single.fileManager.Current_Media.set_draw_mode('Click')
    
    def forwardButtonClick(self):
        if self.single.fileManager.Current_Media is not None:
            curIndex = self.single.fileManager.get_media_index()
            self.single.fileManager.update_index(curIndex+1)
            self.single.ui.carouselView.updateRenderer()
            self.single.changeMouseIcon('Default')
            self.single.fileManager.Current_Media.set_draw_mode('Click')
        self.single.clearNotNeeded()

    def rewindButtonClick(self):
        if self.single.fileManager.Current_Media is not None:
            curIndex = self.single.fileManager.get_media_index()
            self.single.fileManager.update_index(curIndex-1)
            self.single.ui.carouselView.updateRenderer()
            self.single.changeMouseIcon('Default')
            self.single.fileManager.Current_Media.set_draw_mode('Click')
        self.single.clearNotNeeded()

    def boxButtonClick(self):
        if self.single.fileManager.Current_Media is not None:
            self.single.changeMouseIcon('Circle')
            self.single.fileManager.Current_Media.set_draw_mode('Box')

    def polygonButtonClick(self):
        if self.single.fileManager.Current_Media is not None:
            self.single.changeMouseIcon('Circle')
            self.single.fileManager.Current_Media.set_draw_mode('Polygon')

    def arrowButtonClick(self):
        if self.single.fileManager.Current_Media is not None:
            self.single.changeMouseIcon('Diamond')
            self.single.fileManager.Current_Media.set_draw_mode('Arrow')

    

class CreateTab(GenericTab):
    pass