import os
from PyQt5.QtWidgets import QLineEdit, QLabel
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import uic

BASEDIR = os.path.dirname(__file__)

Ui_Logic_Window, logic_baseclass = uic.loadUiType(os.path.join(BASEDIR,'ui_files/LP_Design02.ui' ))

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
            self.createdLabel = None
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
        line_edit.returnPressed.connect(self.deleteLineEdit)

        # Store the line edit in self.createdLineEdit
        self.createdLineEdit = line_edit
        line_edit.show()
        line_edit.setFocus()

    def makeLabelAtPos(self, x, y, width, height, text):
        label = QLabel(text, self)
        label.setGeometry(x, y, width, height)

        # Set the text color to self.creationRGB
        palette = label.palette()
        palette.setColor(QPalette.WindowText, QColor(*self.creationRGB))
        label.setPalette(palette)

        # Add to self.createdLabels
        self.createdLabel = label
        self.createdLabel.show()
    
    def deleteExistingLabel(self):
        if self.createdLabel:
            self.createdLabel.hide()
            self.createdLabel.deleteLater()
            self.createdLabel= None

    def deleteLineEdit(self):
        if self.createdLineEdit:
            text = self.createdLineEdit.text()
            media = self.fileManager.Current_Media
            if media:
                media.add_text_attribute_to_latest(text)
            
            media.print_elements()
            # Delete the line edit
            self.createdLineEdit.hide()
            self.createdLineEdit.deleteLater()
            self.createdLineEdit = None
            self.ui.carouselView.updateRenderer()
    
    def changeMouseIcon(self, assetCall):
        icon_paths = {
            'Point': (os.path.join(self.BASEDIR, 'assets/icons/target.png'), 'Normal'),
            'Circle': (os.path.join(self.BASEDIR, 'assets/icons/circle.png'), 'Smallest'),
            'Diamond': (os.path.join(self.BASEDIR, 'assets/icons/diamond.png'), 'Smaller')
        }

        size_map = {
            'Normal': (32, 32),
            'Smaller': (22, 22),
            'Smallest': (18, 18)
        }

        # If assetCall is Default or not in icon_paths, restore the cursor and return
        if assetCall == 'Default' or assetCall not in icon_paths:
            # Restore the cursor until there's no more overridden cursor
            while qtw.QApplication.overrideCursor():
                qtw.QApplication.restoreOverrideCursor()
            return

        add_Icon, sizeCall = icon_paths[assetCall]
        w, h = size_map[sizeCall]
        pixmap = qtg.QPixmap(add_Icon).scaled(w, h, qtc.Qt.KeepAspectRatio, qtc.Qt.SmoothTransformation)
        cursor = qtg.QCursor(pixmap)

        # Restore the cursor until there's no more overridden cursor to ensure the stack is empty
        while qtw.QApplication.overrideCursor():
            qtw.QApplication.restoreOverrideCursor()

        qtw.QApplication.setOverrideCursor(cursor)

    def resizeEvent(self, event):
        self.tabResize()
    
    def clearNotNeeded(self):
        if self.createdLineEdit:
            self.deleteLineEdit()
        if self.createdLabel:
            self.deleteExistingLabel()
    