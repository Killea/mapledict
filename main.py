#This is the main script, run from here
from PyQt5 import QtCore, uic,QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,QTreeWidgetItem
import codecs, os
from PyQt5.QtWebEngineWidgets import *
from bs4 import BeautifulSoup
from PyQt5.QtWebChannel import QWebChannel

from readmdict import MDX, MDD
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl,QObject, pyqtSlot
from mdict_query import IndexBuilder
from sys import platform
all_dict =list()


class CallHandler(QObject): 
    @pyqtSlot(str,result=str)
    def myTest(self,test):
        print (test)
        #return test +'来自pyQT'





channel = QWebChannel()
handler = CallHandler()

class MyGui(QMainWindow):

    def start_check_dict(self):
        
        content_folder = os.path.join(os.path.dirname(__file__), "content")
        if not os.path.isdir(content_folder):
            os.mkdir(content_folder)
        temp_folder = os.path.join(os.path.dirname(__file__), "temp")
        if not os.path.isdir(temp_folder):
            os.mkdir(temp_folder)
        
        for root, dirs, files in os.walk(content_folder):   
          print( root,dirs,files)
          for d in files:
              if d.lower().endswith('.mdx'):
                  all_dict.append(root+'/'+d)

        print(all_dict)
    def on_changeWord(self):
        # print(i,self.comboBox.currentText())
        print( os.path.join(os.path.dirname(__file__),  "content/OALD8.mdx"))
        self.treeWidget.clear()
        root = QTreeWidgetItem(self.treeWidget)
        root.setText(0, self.comboBox.currentText())  

        #html_string='<script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>'
        html_string ='''
        <!DOCTYPE html>
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta charset="utf-8" />
            <script type="text/javascript" src="qwebchannel.js"></script>
            <title>QWebChannel测试</title>
            <script>
                window.onload = function () {
                    new QWebChannel(qt.webChannelTransport, function (channel) {
                        window.pyjs = channel.objects.pyjs;   
                    });
                }
            </script>
        </head>
        <body>
        '''

        for d in all_dict:

            builder = IndexBuilder(d)
            #html content
            html_content_list =  builder.mdx_lookup(self.comboBox.currentText())
            

            #print(self.comboBox.currentText(), d , result_list)
             
            # /__playsound.png 
            #print ( 'bytes_list', bytes_list)
            #bytes_list= builder.get_mdd_keys()
            '''
            print('your_file', d )
            with open(d+'your_file.txt', 'w') as f:
              for item in bytes_list:
                f.write("%s\n" % item)
            '''

            sound_list=list()
            pix_list=list()
            if len(html_content_list)>0:
              print(html_content_list[0])
              soup = BeautifulSoup( html_content_list[0],"html.parser"  )
              for link in soup.find_all('a'):
                tmp = link.get('href')
                if tmp.startswith('sound://'):
                    sound_list.append(tmp.replace('sound://',''))


              for link in soup.find_all('img'):
                tmp = link.get('src')
                if tmp.startswith('/'):
                  pix_list.append(tmp.replace('/',''))
                else:
                  pix_list.append(tmp)  

              pix_list =list(set(pix_list))
              
        
              print(pix_list)
              for file in pix_list:
                bytes_list = builder.mdd_lookup('\\'+file)
                if len(bytes_list)>0:
                  with open(os.path.join(os.path.dirname(__file__),  "temp/"+file), "wb") as binary_file:
                    binary_file.write(bytes_list[0])



              
              if html_content_list[0]!='':
                html_string +=html_content_list[0]
                child = QTreeWidgetItem(root)
                child.setText(0, os.path.basename(d))
             
        
        #builder = IndexBuilder( os.path.join(os.path.dirname(__file__), "content/OALD8.mdx"))
        #result_text = builder.mdx_lookup(self.comboBox.currentText())
        #print(result_text)
        # QApplication.processEvents()

        if html_string != '':
            html_string += '''
            <div onclick="qt5test();">测试</div> 
            <script>
            function qt5test() {
            pyjs.myTest('这是测试传参的',function (res) {
            });
            }

             function uptext(msg) {
                 document.getElementById('test').innerHTML=msg;
             }
            </script>
            </body>
            </html>
            '''
            tempFolder = os.path.join(os.path.dirname(__file__), "temp")
            file_path = os.path.abspath(os.path.join(tempFolder, "dict.html"))
            file_path = file_path.replace('\\', '/')
            with codecs.open(file_path, "w", "utf-8-sig") as text_file:
                text_file.write(html_string)
            print(file_path)
            channel.registerObject('pyjs', handler)

            self.widget_2.page().setWebChannel(channel)
     
            self.treeWidget.expandAll()    
            
            
            if platform == "linux" or platform == "linux2":
                self.widget_2.load(QUrl('file://'+file_path))
            elif platform == "darwin":
                self.widget_2.load(QUrl('file://'+file_path))
            elif platform == "win32":
                self.widget_2.load(QUrl(file_path))
            self.treeWidget.expandAll()  
            self.widget_2.show()


            


    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'ui/mainForm.ui')
        ico_path = os.path.join(os.path.dirname(__file__), 'ui/maple-leaf.png')
        loadUi(ui_path, self)  # 请用qt-designer随意编辑ui
        self.start_check_dict()
        # self.pushButton.setObjectName('pushButton')
        # self.pushButton.clicked.connect(self.on_click)
        #self.widget_2.setEnabled(False)
        self.comboBox.currentIndexChanged.connect(self.on_changeWord)
        self.setWindowIcon(QtGui.QIcon(ico_path))
        self.show()
        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = MyGui()
    #sys.exit(app.exec_())

  

    app.exec_()
