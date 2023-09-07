import sys
import os
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import uic
from qt_ui import GL_Renderer as gr
from core import File_Manager as fm

BASEDIR = os.path.dirname(__file__)

Ui_Logic_Window, logic_baseclass = uic.loadUiType(os.path.join(BASEDIR,'qt_ui\LP_Design02.ui' ))

class Logic_Window(logic_baseclass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Logic_Window()
        self.ui.setupUi(self)

        # Create an instance of GL_Renderer
        self.glWidget = gr.GL_Renderer(self)

        # Connect the actionImage_Folder triggered signal to the slot
        self.ui.actionImage_Folder.triggered.connect(self.loadImageFolder)

        # Replace carouselView with glWidget
        layout = self.ui.carouselView.parent().layout()
        if layout:
            index = layout.indexOf(self.ui.carouselView)
            layout.removeWidget(self.ui.carouselView)
            self.ui.carouselView.deleteLater()
            layout.insertWidget(index, self.glWidget)
        else:
            self.glWidget.setParent(self.ui.carouselView.parent())
            self.glWidget.setGeometry(self.ui.carouselView.geometry())
            self.ui.carouselView.deleteLater()
        self.ui.carouselView = self.glWidget
        
        timer = qtc.QTimer(self)
        timer.setInterval(20)   # period, in milliseconds
        timer.timeout.connect(self.ui.carouselView.update)
        timer.start()

        # Ensure that frames overlay on the carouselView
        self.ui.actionTypeFrame.raise_()
        self.ui.swapFrame.raise_()
        self.ui.toolsFrame.raise_()
        
        #specialized vars
        self.resizeOffset = 20
        self.fileManager = fm.File_Manager()

        self.show()

    def loadImageFolder(self):
        # Open the folder selection dialog
        folder_path = qtw.QFileDialog.getExistingDirectory(self, "Select Image Folder")

        # If a folder was selected, print its path
        if folder_path:
            self.fileManager.Add_Folder_Path(folder_path)

    def resizeEvent(self, event):
        # Manually adjust the size of carouselView
        self.ui.carouselView.resize(self.ui.imageLabelMode.size())

        # Reposition the frames
        # Here's an example: (Adjust as needed)
        self.ui.actionTypeFrame.move(self.resizeOffset, self.resizeOffset)  # Move to top-left corner of carouselView
        self.ui.swapFrame.move(self.ui.carouselView.width() - self.ui.swapFrame.width() - self.resizeOffset, self.resizeOffset)  # Top-right
        self.ui.toolsFrame.move(self.resizeOffset, self.ui.carouselView.height() - self.ui.toolsFrame.height() - self.resizeOffset)  # Bottom-left

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    lw = Logic_Window()
    sys.exit(app.exec())
