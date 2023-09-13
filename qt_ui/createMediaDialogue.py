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

Google_Image = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'
u_agnt = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
} #write: 'my user agent' in browser to get your browser user agent details
Ui_Create_Window, create_baseclass = uic.loadUiType(os.path.join(BASEDIR,'ui_files/folderCreate.ui' ))

class CreateMediaWindow(create_baseclass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Create_Window()
        self.ui.setupUi(self)
        self.single = lw.Logic_Window.getInstance()
        self.show()
        self.folderPath = ''
        self.keyword = ''
        self.fileType = ''
        self.imageNumberCount = ''

        self.ui.createMediaButton.clicked.connect(self.createMedia)  # Assuming closeButton is the name of your button
        self.ui.FileBrowseButton.clicked.connect(self.fileBrowse)
        self.ui.mediaProgressBar.setMaximum(100)
        self.ui.mediaProgressBar.setValue(0)
        self.ui.creationAction.setText('')

    def format_keyword(self, keyword):
        # Encode the keyword into 'URL percent-encoded' format
        formatted_keyword = urllib.parse.quote_plus(keyword)
        return formatted_keyword

    def fileBrowse(self):
        # Open the folder selection dialog
        folder_path = qtw.QFileDialog.getExistingDirectory(self, "Select Image Folder")
        # If a folder was selected, print its path
        if folder_path:
            self.folderPath = folder_path
            self.ui.FileLocationLineEdit.setText(folder_path)
            
    def createMedia(self):
        self.download_images()
        self.single.fileManager.Add_Folder_Contents(self.folderPath)
        self.single.ui.carouselView.updateRenderer()
        self.close()
    
    def download_images(self):
        if self.folderPath == '':
            return None
        Image_Folder_Path = self.folderPath
        if self.ui.keywordLineEdit.text() == '':
            return None
        keyword = self.format_keyword(self.ui.keywordLineEdit.text())
        if self.ui.numImgLineEdit.text() == '':
            return None
        image_num = int(self.ui.numImgLineEdit.text())
        self.ui.mediaProgressBar.setMaximum(image_num)
        self.ui.mediaProgressBar.setValue(0)

        self.ui.creationAction.setText('Searching Images ...')
        
        search_url = Google_Image + 'q=' + keyword #'q=' because its a query
        
        # request url, without u_agnt the permission gets denied
        response = requests.get(search_url, headers=u_agnt)
        html = response.text #To get actual result i.e. to read the html data in text mode
        
        # find all img where class='rg_i Q4LuWd'
        b_soup = BeautifulSoup(html, 'html.parser') #html.parser is used to parse/extract features from HTML files
        results = b_soup.findAll('img', {'class': 'rg_i Q4LuWd'})
        
        #extract the links of requested number of images with 'data-src' attribute and appended those links to a list 'imagelinks'
        #allow to continue the loop in case query fails for non-data-src attributes
        count = 0
        imagelinks= []
        for res in results:
            try:
                link = res['data-src']
                self.ui.creationAction.setText('Trying' + str(link))
                imagelinks.append(link)
                count = count + 1
                if (count >= image_num):
                    break
                
            except KeyError:
                continue
        
        self.ui.creationAction.setText(f'Found {len(imagelinks)} images')
        self.ui.creationAction.setText('Start downloading...')

        for i, imagelink in enumerate(imagelinks):
            # open each image link and save the file
            response = requests.get(imagelink)
            
            imagename = Image_Folder_Path + '/' + self.ui.keywordLineEdit.text() + str(i+1) + '.png'
            self.ui.creationAction.setText(str(imagename))
            self.ui.mediaProgressBar.setValue(i)
            with open(imagename, 'wb') as file:
                file.write(response.content)

        self.ui.creationAction.setText('Download Completed')
