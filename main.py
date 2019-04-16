from PyQt5 import QtCore, uic 
from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.uic import loadUi
class MyGui(QMainWindow): 
    def __init__(self):
        super().__init__()
        loadUi('mainForm.ui',self) #请用qt-designer随意编辑ui
        #self.pushButton.setObjectName('pushButton')
        #self.pushButton.clicked.connect(self.on_click)
        self.show()  
    def on_click(self):
        pass
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = MyGui()
    sys.exit(app.exec_())