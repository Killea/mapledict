from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import codecs, os
from PyQt5.QtWebEngineWidgets import *

from readmdict import MDX, MDD
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl
from mdict_query import IndexBuilder


class MyGui(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('mainForm.ui', self)  # 请用qt-designer随意编辑ui

        contentFolder= os.path.join(os.path.dirname(__file__), "content")
        if not os.path.isdir(contentFolder):
            os.mkdir(contentFolder)
        tempFolder = os.path.join(os.path.dirname(__file__), "temp")
        if not os.path.isdir(tempFolder):
            os.mkdir(tempFolder)

        # self.pushButton.setObjectName('pushButton')
        # self.pushButton.clicked.connect(self.on_click)
        self.comboBox.currentIndexChanged.connect(self.on_changeWord)
        self.show()


    def on_click(self):
        pass

    def on_changeWord(self):
        # print(i,self.comboBox.currentText())

        builder = IndexBuilder('test.mdx')
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
            self.widget_2.load(QUrl(file_path))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    win = MyGui()
    sys.exit(app.exec_())
