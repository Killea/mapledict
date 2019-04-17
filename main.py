from PyQt5 import QtCore, uic,QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import codecs, os
from PyQt5.QtWebEngineWidgets import *

from readmdict import MDX, MDD
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl
from mdict_query import IndexBuilder


class MyGui(QMainWindow):

    def start_check_dict(self):
        content_folder = os.path.join(os.path.dirname(__file__), "content")
        if not os.path.isdir(content_folder):
            os.mkdir(content_folder)
        temp_folder = os.path.join(os.path.dirname(__file__), "temp")
        if not os.path.isdir(temp_folder):
            os.mkdir(temp_folder)
        
        for root, dirs, files in os.walk(content_folder):   
          print( files)

    def on_changeWord(self):
        # print(i,self.comboBox.currentText())
        print( os.path.join(os.path.dirname(__file__),  "content/OALD8.mdx"))


        builder = IndexBuilder( os.path.join(os.path.dirname(__file__), "content/OALD8.mdx"))
        

        result_text = builder.mdx_lookup(self.comboBox.currentText())
        print(result_text)
        # QApplication.processEvents()
        if result_text != '':
            tempFolder = os.path.join(os.path.dirname(__file__), "temp")
            file_path = os.path.abspath(os.path.join(tempFolder, "dict.html"))
            file_path = file_path.replace('\\', '/')
            with codecs.open(file_path, "w", "utf-8-sig") as text_file:
                text_file.write(result_text[0])
            print(file_path)
            self.widget_2.load(QUrl('file://'+file_path))

    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'ui/mainForm.ui')
        ico_path = os.path.join(os.path.dirname(__file__), 'ui/maple-leaf.png')
        loadUi(ui_path, self)  # 请用qt-designer随意编辑ui
        self.start_check_dict()
        # self.pushButton.setObjectName('pushButton')
        # self.pushButton.clicked.connect(self.on_click)
        self.comboBox.currentIndexChanged.connect(self.on_changeWord)
        self.setWindowIcon(QtGui.QIcon(ico_path))
        self.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = MyGui()
    #sys.exit(app.exec_())
    app.exec_()
