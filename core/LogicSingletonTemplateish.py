class LogicSingleton:
    __instance = None

    @staticmethod
    def getInstance():
        """Static access method."""
        if LogicSingleton.__instance == None:
            LogicSingleton()
        return LogicSingleton.__instance

    def __init__(self):
        """Virtually private constructor."""
        if LogicSingleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            LogicSingleton.__instance = self
            self.BASEDIR = None
            self.ui = None
            self.glWidget = None
            self.fileManager = None
            self.labelTab = None
            self.createTab = None
            self.menubar = None

    def setBASEDIR(self, BASEDIR):
        self.BASEDIR = BASEDIR

    def getBASEDIR(self):
        return self.BASEDIR

    def setUI(self, ui):
        self.ui = ui

    def getUI(self):
        return self.ui

    def setGLWidget(self, glWidget):
        self.glWidget = glWidget

    def getGLWidget(self):
        return self.glWidget

    def setFileManager(self, fileManager):
        self.fileManager = fileManager

    def getFileManager(self):
        return self.fileManager

    def setTab(self, tabName, tab):
        if tabName is 'Label':
            self.labelTab = tab
        if tabName is 'Create':
            self.createTab = tab
    
    def setMenuBar(self, bar):
        self.menubar = bar
    
