# This is the main script, run from here
from PyQt5 import QtCore, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem
import codecs
import os
import sys
import base64
import shutil
from PyQt5.QtWebEngineWidgets import *
from bs4 import BeautifulSoup
from PyQt5.QtWebChannel import QWebChannel
from readmdict import MDX, MDD
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl, QObject, pyqtSlot
from mdict_query import IndexBuilder
from sys import platform
from collections import Counter
import re


def words(text): return re.findall(r'\w+', text.lower())


WORDS = Counter(words(open('big.txt').read()))
all_dict = list()

win = None  # win = MyGui()




def empty_temp():
    folder = os.path.join(os.path.dirname(__file__), "temp/")
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


class CallHandler(QObject):
    @pyqtSlot(str)
    def myTest(self, test):
        # print(test)
        test = test.strip()
        if test != '':
            print(test)
            win.look_up_word(test)

    @pyqtSlot(str, result=str)
    def myMouseClick(self, test):
        print(test)

    @pyqtSlot(str)
    def playSound(self, spxfile):
        with open(os.path.join(os.path.dirname(__file__), "temp/" + spxfile), 'rb') as f:
            data = f.read()
            data_base64 = base64.b64encode(data)
            data_base64_string = data_base64.decode()
            # print(data_base64_string)
            win.widget_2.page().runJavaScript('decodeFile(`' + data_base64_string + '`);')


channel = QWebChannel()
handler = CallHandler()
channel.registerObject('pyjs', handler) 


class MyGui(QMainWindow):
    def treeview_item_on_click(self, item, column):

        # print(self.treeWidget.currentIndex().row())
        idx = self.treeWidget.currentIndex().row()
        win.widget_2.page().runJavaScript('QTscrollTo("part'+str(idx)+'")')

    def on_search_click(self):
        print('click')
        win.widget_2.page().runJavaScript('QTscrollTo("part1")')

    def start_check_dict(self):

        content_folder = os.path.join(os.path.dirname(__file__), "content")
        if not os.path.isdir(content_folder):
            os.mkdir(content_folder)
        temp_folder = os.path.join(os.path.dirname(__file__), "temp")
        if not os.path.isdir(temp_folder):
            os.mkdir(temp_folder)

        for root, dirs, files in os.walk(content_folder):
            print(root, dirs, files)
            for d in files:
                if d.lower().endswith('.mdx'):
                    all_dict.append(root + '/' + d)


    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'ui/mainForm.ui')
        ico_path = os.path.join(os.path.dirname(__file__), 'ui/maple-leaf.png')
        loadUi(ui_path, self)
        self.pushButton.clicked.connect(self.on_search_click)
        self.start_check_dict()
        self.comboBox.currentIndexChanged.connect(self.on_changeWord)
        self.treeWidget.itemClicked.connect(self.treeview_item_on_click)
        self.setWindowIcon(QtGui.QIcon(ico_path))
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyGui()
    # sys.exit(app.exec_())
    app.exec_()
