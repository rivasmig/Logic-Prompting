import os
import sys
import urllib.parse
from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import pyqtSignal
from qt_ui import logic_window as lw
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from core import Caption
import shutil

BASEDIR = os.path.dirname(__file__)
Ui_Export_Window, export_baseclass = uic.loadUiType(os.path.join(BASEDIR,'ui_files/exportWindow.ui' ))

class CreateExportWindow(export_baseclass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Export_Window()
        self.ui.setupUi(self)
        self.single = lw.Logic_Window.getInstance()
        self.show()
        self.caption = Caption.Caption()

        self.listOfImagePaths = self.single.fileManager.get_all_image_paths()
        self.listOfCaptions = []
        for ipth in self.listOfImagePaths:
            self.listOfCaptions.append('*None Generated*')
        self.currentIndex = 0
        self.projectName = self.single.fileManager.projectName
        self.projectFolder = self.single.fileManager.projectFolder

        self.ui.nextButton.clicked.connect(self.nextButtonClicked)
        self.ui.previousButton.clicked.connect(self.previousButtonClicked)
        self.ui.exportAsPairsButton.clicked.connect(self.exportAsPairs)
        self.ui.createPairsButton.clicked.connect(self.createPairsClicked)
        # reference to the progress bar is: self.ui.exportProgressBar
        self.resetViews()
    
    def resetViews(self):
        if self.inIndexRange():
            self.putImageOnGraphicView(self.listOfImagePaths[self.currentIndex])
            self.putTextOnTextBrowser(self.listOfCaptions[self.currentIndex])
    
    def inIndexRange(self):
        if self.currentIndex >= 0 and self.currentIndex < len(self.listOfImagePaths):
            return True
        else:
            return False

    def putImageOnGraphicView(self, imagePath):
        self.scene = QGraphicsScene()
        self.scene.clear()
        self.ui.mediaGraphicsView.setScene(self.scene)
        pixmap = QPixmap(imagePath)
        self.scene.addPixmap(pixmap)
        self.ui.mediaGraphicsView.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)

    def putTextOnTextBrowser(self, text):
        self.ui.renderedPromptMediaView.setText(text)

    def createPairsClicked(self):
        # Initialize an index variable
        indx = 0
        
        # Reset the lists
        self.listOfImagePaths = self.single.fileManager.get_all_image_paths()
        self.listOfCaptions = []

        # Initialize the progress bar
        total_media = len(self.listOfImagePaths)
        self.ui.exportProgressBar.setMaximum(total_media)
        self.ui.exportProgressBar.setValue(0)

        # Loop through all media
        for ipth in self.listOfImagePaths:
            # Generate the caption for the media
            media = self.single.fileManager.get_media_obj_by_index(indx)
            thisCaption = self.caption.generate_caption_from_media(media)
            
            # Append the generated caption to the list
            self.listOfCaptions.append(thisCaption)
            
            # Update the progress bar
            self.ui.exportProgressBar.setValue(indx + 1)
            
            # Increment the index
            indx += 1
        self.ui.exportProgressBar.hide()
        self.resetViews()

    def exportAsPairs(self):
        # Open the folder selection dialog
        folder_path = qtw.QFileDialog.getExistingDirectory(self.single, "Select Image Folder")

        # If a folder was selected
        if folder_path:
            total_media = len(self.listOfImagePaths)
            
            # Create a QProgressDialog for the export process
            progress_dialog = qtw.QProgressDialog("Exporting media and captions...", "Cancel", 0, total_media, self)
            progress_dialog.setWindowTitle("Exporting...")
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.show()

            # Loop through the listOfImagePaths
            for indx, (image_path, caption_text) in enumerate(zip(self.listOfImagePaths, self.listOfCaptions)):
                # Update the progress dialog
                progress_dialog.setValue(indx)
                
                if progress_dialog.wasCanceled():
                    break

                # Construct the new image filename
                new_image_name = f"{indx:04}.png"  # Format the index to be 4 digits with leading zeros
                new_caption_name = f"{indx:04}.txt"

                # Paths for the new image and caption file in the selected directory
                new_image_path = os.path.join(folder_path, new_image_name)
                new_caption_path = os.path.join(folder_path, new_caption_name)

                # Copy the image to the selected directory
                shutil.copy2(image_path, new_image_path)

                # Write the caption to a new text file with UTF-8 encoding
                with open(new_caption_path, "w", encoding="utf-8") as caption_file:
                    caption_file.write(caption_text)

            # Close the progress dialog and window after exporting
            progress_dialog.close()
            self.close()

    def previousButtonClicked(self):
        if self.currentIndex > 0:
            self.currentIndex -= 1
            self.resetViews()

    def nextButtonClicked(self):
        if self.currentIndex < len(self.listOfImagePaths) - 1:
            self.currentIndex += 1
            self.resetViews()