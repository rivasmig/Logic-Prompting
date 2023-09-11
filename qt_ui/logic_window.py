import os
from PyQt5.QtWidgets import QLineEdit, QLabel
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt
from PyQt5 import uic

BASEDIR = os.path.dirname(__file__)

Ui_Logic_Window, logic_baseclass = uic.loadUiType(os.path.join(BASEDIR,'LP_Design02.ui' ))

# Main application logic
class Logic_Window(logic_baseclass):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self, *args, **kwargs):
        if Logic_Window._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            super().__init__(*args, **kwargs)
            self.ui = Ui_Logic_Window()
            self.ui.setupUi(self)
            self.labelTab = None
            self.createTab = None
            self.menubarCode = None
            self.fileManager = None
            self.createdLineEdit = None
            self.createdLabels = []
            self.creationRGB = [0,0,255]
            self.CurrentXY = (0,0)
            self.CurrentWH = (0,0)
            self.BASEDIR = BASEDIR

            # Set the _instance attribute here
            Logic_Window._instance = self
    
    def setBASEDIR(self, new):
        self.BASEDIR = new
    
    def tabResize(self):
        if self.labelTab is not None:
            self.labelTab.thisResizeEvent()
        if self.createTab is not None:
            self.createTab.thisResizeEvent()

    def makeLineEdit(self, x, y, width, height):
        # Create a line edit at x,y with width and height
        line_edit = QLineEdit(self)
        line_edit.setGeometry(x, y, width, height)

        # Set background color to the desired RGBA color
        palette = line_edit.palette()
        palette.setColor(QPalette.Base, QColor(255, 255, 255, 127))  # Example RGBA color (you can change as needed)
        line_edit.setPalette(palette)

        # Connect the returnPressed signal to the deleteAndReplace method
        line_edit.returnPressed.connect(self.deleteAndReplace)

        # Store the line edit in self.createdLineEdit
        self.createdLineEdit = line_edit
        line_edit.show()
        line_edit.setFocus()

    def deleteAndReplace(self):
        print('Deleted')

        if self.createdLineEdit:
            # Create a QLabel at the line edit's x and y, smaller width and height
            x, y, width, height = self.createdLineEdit.geometry().getRect()
            new_width = width - 10  # Example adjusted width
            new_height = height - 10  # Example adjusted height

            label = QLabel(self.createdLineEdit.text(), self)
            label.setGeometry(x, y, new_width, new_height)

            # Set the text color to self.creationRGB
            palette = label.palette()
            palette.setColor(QPalette.WindowText, QColor(*self.creationRGB))
            label.setPalette(palette)

            # Add to self.createdLabels
            self.createdLabels.append(label)
            label.show()

            # Delete the line edit
            self.createdLineEdit.deleteLater()
            self.createdLineEdit = None

    def resizeEvent(self, event):
        self.tabResize()
    