import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from OpenGL.GL import *

class OpenGLInfoWidget(QOpenGLWidget):
    def initializeGL(self):
        print("GL_VENDOR:", glGetString(GL_VENDOR).decode('utf-8'))
        print("GL_RENDERER:", glGetString(GL_RENDERER).decode('utf-8'))
        print("GL_VERSION:", glGetString(GL_VERSION).decode('utf-8'))
        print("GL_SHADING_LANGUAGE_VERSION:", glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8'))

        # Extensions
        extensions = glGetString(GL_EXTENSIONS)
        if extensions:
            extensions = extensions.decode('utf-8').split()
            print("\nExtensions:")
            for ext in extensions:
                print("  -", ext)

        # Check if glGenBuffers is callable
        is_glGenBuffers_callable = bool(glGenBuffers)
        print("\nIs glGenBuffers callable?", is_glGenBuffers_callable)

        # Close the application after printing the info
        QApplication.quit()

app = QApplication([])
window = QMainWindow()
widget = OpenGLInfoWidget(window)
window.setCentralWidget(widget)
window.show()
sys.exit(app.exec_())
