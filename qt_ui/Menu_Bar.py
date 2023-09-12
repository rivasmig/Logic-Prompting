from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import qt_ui.logic_window as lw
from qt_ui import createMediaDialogue
from qt_ui import createExportWindow as cew
from core import File_Manager as fm
import os

class MenuBar():
    def __init__(self):
        self.single = lw.Logic_Window.getInstance()
        # Connect the menubar actions
        self.single.ui.actionImage_Folder.triggered.connect(self.imageFolderLoad)
        self.single.ui.actionImage_Media.triggered.connect(self.addImage)
        self.single.ui.actionImage_Set.triggered.connect(self.createImageSet)
        self.single.ui.actionUndo.triggered.connect(self.thisUndo)
        self.single.ui.actionRedo.triggered.connect(self.thisRedo)
        self.single.ui.actionSave_Project.triggered.connect(self.saveProj)
        self.single.ui.actionSaveAs_Project.triggered.connect(self.saveAs)
        self.single.ui.actionLoad_Log.triggered.connect(self.loadLogFile)
        self.single.ui.actionNew.triggered.connect(self.newLogProject)
        self.single.ui.actionExport_2.triggered.connect(self.exportProj)
    
    def exportProj(self):
        self.export_window = cew.CreateExportWindow()
        self.export_window.show()

    def loadLogFile(self):
        # Open a file dialog window, only showing .logic files
        options = qtw.QFileDialog.Options()
        options |= qtw.QFileDialog.ReadOnly
        filter_string = f"*{self.single.fileManager.Logic_Extension}"
        file_path, _ = qtw.QFileDialog.getOpenFileName(self.single, "Load Logic File", "", 
                                                    f"Logic Files ({filter_string});;All Files (*)", 
                                                    options=options)
        
        # If a file was selected, load it
        if file_path:
            self.single.fileManager.Load_Logic_File(file_path)
            self.single.ui.carouselView.updateRenderer()

    def newLogProject(self):
        self.saveProj()
        self.single.fileManager = fm.File_Manager()
        self.single.ui.carouselView.updateRenderer()
        self.single.changeMouseIcon('Click')

    def saveProj(self):
        if self.single.fileManager.projectName:
            self.single.fileManager.Create_Logic_File()
        else:
            self.saveAs()

    def saveAs(self):
        # Open a save file dialog, defaulting to .logic extension
        options = qtw.QFileDialog.Options()
        filter_string = f"*{self.single.fileManager.Logic_Extension}"
        file_name, _ = qtw.QFileDialog.getSaveFileName(self.single, "Save As", "", 
                                                    f"Logic Files ({filter_string});;All Files (*)", 
                                                    options=options)
        
        # If a location was selected, save the project
        if file_name:
            # Ensure the filename ends with .logic
            if not file_name.endswith(self.single.fileManager.Logic_Extension):
                file_name += self.single.fileManager.Logic_Extension

            # Set the project name to the base name of the file (without extension)
            self.single.fileManager.projectName = os.path.splitext(os.path.basename(file_name))[0]
            
            # Set the project folder to the directory of the file
            self.single.fileManager.projectFolder = os.path.dirname(file_name)
            
            # Save the project
            self.single.fileManager.Create_Logic_File()

    def thisUndo(self):
        self.single.ui.carouselView.invoker.undo()
        self.single.fileManager.Current_Media.invoker.undo()

    def thisRedo(self):
        self.single.ui.carouselView.invoker.redo()
        self.single.fileManager.Current_Media.invoker.redo()

    def createImageSet(self):
        self.create_window = createMediaDialogue.CreateMediaWindow()
        self.create_window.show()

    def imageFolderLoad(self):
        folder_path = self.loadFolder()
        if folder_path:
            self.single.fileManager.Add_Folder_Contents(folder_path)
            self.single.ui.carouselView.updateRenderer()

    def loadFolder(self):
        # Open the folder selection dialog
        folder_path = qtw.QFileDialog.getExistingDirectory(self.single, "Select Image Folder")

        # If a folder was selected, print its path
        if folder_path:
            return folder_path
        else:
            return None
    
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

    