import sys
import os
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import uic
from qt_ui import GL_Renderer as gr
from core import File_Manager as fm
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtGui import QSurfaceFormat

BASEDIR = os.path.dirname(__file__)

Ui_Logic_Window, logic_baseclass = uic.loadUiType(os.path.join(BASEDIR,'qt_ui\LP_Design02.ui' ))

class Logic_Window_alpha(logic_baseclass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Logic_Window()
        self.ui.setupUi(self)

        # Create an instance of GL_Renderer
        tabColor = self.ui.logicModes.palette().midlight().color().getRgb()
        self.glWidget = gr.GL_Renderer(self, bckColor=(tabColor))
        
        # Connect the menubar actions
        self.ui.actionImage_Folder.triggered.connect(self.loadFolder)
        self.ui.actionImage_Media.triggered.connect(self.addImage)

        # Connect label tab buttons
        self.ui.pointButton.clicked.connect(self.pointButtonClick)
        self.ui.handButton.clicked.connect(self.handButtonClick)

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
        self.ui.carouselView.makeCurrent()
        
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

    def loadFolder(self):
        # Open the folder selection dialog
        folder_path = qtw.QFileDialog.getExistingDirectory(self, "Select Image Folder")

        # If a folder was selected, print its path
        if folder_path:
            self.fileManager.Add_Folder_Contents(folder_path)

    def resizeEvent(self, event):
        # Manually adjust the size of carouselView
        self.ui.carouselView.resize(self.ui.imageLabelMode.size())

        # Reposition the frames
        # Here's an example: (Adjust as needed)
        self.ui.actionTypeFrame.move(self.resizeOffset, self.resizeOffset)  # Move to top-left corner of carouselView
        self.ui.swapFrame.move(self.ui.carouselView.width() - self.ui.swapFrame.width() - self.resizeOffset, self.resizeOffset)  # Top-right
        self.ui.toolsFrame.move(self.resizeOffset, self.ui.carouselView.height() - self.ui.toolsFrame.height() - self.resizeOffset)  # Bottom-left

    def pointButtonClick(self):
        self.changeMouseIcon('Point')
        #I'll put other stuff in here later

    def handButtonClick(self):
        self.changeMouseIcon('Hand')

    def changeMouseIcon(self, button_name):
        add_Icon = None
        if button_name == 'Point':
            add_Icon = os.path.join(BASEDIR, 'assets/icons/target.png')
        if button_name == 'Hand':
            add_Icon = None
        
        if add_Icon:
            pixmap = qtg.QPixmap(add_Icon).scaled(32, 32, qtc.Qt.KeepAspectRatio, qtc.Qt.SmoothTransformation)
            cursor = qtg.QCursor(pixmap)
            qtw.QApplication.setOverrideCursor(cursor)
        else:
            qtw.QApplication.restoreOverrideCursor()

    def addImage(self):
        # Extract image extensions from the Media_Types_and_Extensions dictionary
        image_extensions = self.fileManager.Media_Types_and_Extensions['Image']
        
        # Convert the list of extensions into the format: "*.png *.jpg *.jpeg"
        filter_string = " ".join(f"*{ext}" for ext in image_extensions)
        options = qtw.QFileDialog.Options()
        options |= qtw.QFileDialog.ReadOnly
        file_name, _ = qtw.QFileDialog.getOpenFileName(self, "Add Image", "", f"Images ({filter_string});;All Files (*)", options=options)
        
        if file_name:
            self.fileManager.Add_Media_By_Path(file_name)
            if isinstance(self.ui.carouselView, gr.GL_Renderer):
                self.ui.carouselView.glAddImage(file_name)


    def blah():
        pass

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    lw = Logic_Window_alpha()
    sys.exit(app.exec())
