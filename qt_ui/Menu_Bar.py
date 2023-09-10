from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import qt_ui.logic_window as lw
from qt_ui import createMediaDialogue

class MenuBar():
    def __init__(self):
        self.single = lw.Logic_Window.getInstance()
        # Connect the menubar actions
        self.single.ui.actionImage_Folder.triggered.connect(self.loadFolder)
        self.single.ui.actionImage_Media.triggered.connect(self.addImage)
        self.single.ui.actionImage_Set.triggered.connect(self.createImageSet)

    def createImageSet(self):
        self.create_window = createMediaDialogue.CreateMediaWindow()
        self.create_window.show()

    def loadFolder(self):
        # Open the folder selection dialog
        folder_path = qtw.QFileDialog.getExistingDirectory(self.single, "Select Image Folder")

        # If a folder was selected, print its path
        if folder_path:
            self.single.fileManager.Add_Folder_Contents(folder_path)
            self.single.ui.carouselView.updateRenderer()
    
    def addImage(self):
        # Extract image extensions from the Media_Types_and_Extensions dictionary
        image_extensions = self.single.fileManager.Media_Types_and_Extensions['Image']
        
        # Convert the list of extensions into the format: "*.png *.jpg *.jpeg"
        filter_string = " ".join(f"*{ext}" for ext in image_extensions)
        options = qtw.QFileDialog.Options()
        options |= qtw.QFileDialog.ReadOnly
        file_name, _ = qtw.QFileDialog.getOpenFileName(self.single, "Add Image", "", 
                                                       f"Images ({filter_string});;All Files (*)", 
                                                       options=options)
        
        if file_name:
            self.single.fileManager.Add_Media_By_Path(file_name)
            self.single.ui.carouselView.updateRenderer()

    