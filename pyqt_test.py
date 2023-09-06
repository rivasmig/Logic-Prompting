import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class HelloWorldApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window size and title
        self.resize(400, 300)
        self.setWindowTitle('Hello World App')

        # Set background color
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(128, 128, 128))  # Grey color
        self.setPalette(palette)

        # Create a button
        self.btn = QPushButton('Hello World', self)
        self.btn.resize(150, 50)
        self.btn.move((self.width() - self.btn.width()) // 2, (self.height() - self.btn.height()) // 2)
        self.btn.clicked.connect(self.on_click)

        # Button hover effect
        self.btn.setStyleSheet(
            "QPushButton:hover {"
            "background-color: #D0D0D0;"
            "}"
            "QPushButton {"
            "background-color: white;"
            "}"
        )

    def on_click(self):
        print("Hello World")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HelloWorldApp()
    ex.show()
    sys.exit(app.exec_())
