import os
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

    def resizeEvent(self, event):
        self.tabResize()
    