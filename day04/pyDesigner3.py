import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic  # .ui 파일을 불러오기 위한 모듈

class WindowClass(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = uic.loadUi("designer.ui", self)
        self.ui.show()

    def slot1(self):
        self.ui.label.setText("Left button clicked")

    def slot2(self):
        self.ui.label.setText("Right button clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    app.exec_()