import sys
import os
from PyQt5 import QtWidgets as qtw

from qt_ui import logic_window as lw
from qt_ui import Menu_Bar as mb
from qt_ui import Media_Tabs as mt
from core import File_Manager as fm

BASEDIR = os.path.dirname(__file__)

def main():
    app = qtw.QApplication(sys.argv)
    window = lw.Logic_Window.getInstance()
    window.setBASEDIR(BASEDIR)
    window.fileManager = fm.File_Manager()
    window.labelTab = mt.LabelTab()
    window.createTab = mt.CreateTab()
    window.menubarCode = mb.MenuBar()
    window.show()
    window.tabResize() # for correct initial views
    sys.exit(app.exec())

if __name__ == '__main__':
    main()