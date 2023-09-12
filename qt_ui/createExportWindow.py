import os
import sys
import urllib.parse
from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import pyqtSignal
from qt_ui import logic_window as lw
import requests # pip install requests #to sent GET requests
from bs4 import BeautifulSoup # pip install bs4 #to parse html(getting data out from html, xml or other markup languages)

BASEDIR = os.path.dirname(__file__)
Ui_Export_Window, export_baseclass = uic.loadUiType(os.path.join(BASEDIR,'exportWindow.ui' ))

class CreateExportWindow(export_baseclass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Export_Window()
        self.ui.setupUi(self)
        self.single = lw.Logic_Window.getInstance()
        self.show()