from PyQt5 import QtCore, uic,QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
import os



class MyGui(QMainWindow):

    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'ui/dictManage.ui')
        ico_path = os.path.join(os.path.dirname(__file__), 'ui/maple-leaf.png')
        loadUi(ui_path, self)  # 请用qt-designer随意编辑ui
        self.show()





if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = MyGui()
    #sys.exit(app.exec_())
    app.exec_()
