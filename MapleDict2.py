# This is the main script, run from here
from PyQt5 import QtCore, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QMenu, QMessageBox
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
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, Qt #,QJsonValue
from mdict_query import IndexBuilder
from sys import platform
from collections import Counter
import re

import json
# https://stackoverflow.com/questions/41695104/importerror-no-module-named-driver-in-pyttsx
import pyttsx3

# from multiprocessing import Process

import threading


from flask import Flask, request
from flask_restful import reqparse, Resource, Api



# Pyqt5 GUI Begin
all_dict = list()
all_html=  list()




win = None  # win = MyGui()
engine = pyttsx3.init()
extract_path = 'maple-front/public/'

html_string =''



def get_mdd_file(file_list, builder):
    for file in file_list:
        bytes_list = builder.mdd_lookup('\\' + file)
        if len(bytes_list) > 0:
            with open(os.path.join(os.path.dirname(__file__), extract_path + file), "wb") as binary_file:
                binary_file.write(bytes_list[0])


def get_single_html(word,mydict,index):

    builder = IndexBuilder(mydict)
    html_content_list = builder.mdx_lookup(word)
    dict_title = builder._title
    sound_list = list()
    pix_list = list()
    if len(html_content_list) > 0:
        soup = BeautifulSoup(html_content_list[0], "html.parser")
        for link in soup.find_all('a'):
            tmp = link.get('href')
            #print(tmp)
            if tmp is not None:
                if tmp.startswith('sound://'):
                    sound_list.append(tmp.replace('sound://', ''))
                    link['sound'] = tmp.replace('sound://', '')
                    link['href'] = "javascript:"
                    link['onclick'] = "javascript:playSound(this);"
                    #print(link['href'])
        for link in soup.find_all('img'):
            tmp = link.get('src')
            if tmp is not None:
                if tmp.startswith('/') and tmp is not None:
                    pix_list.append(tmp.replace('/', ''))
                    link['src'] = tmp.replace('/', '')
                else:
                    pix_list.append(tmp)
        pix_list = list(set(pix_list))
        file_list = sound_list + pix_list



        write_thread = threading.Thread(target=get_mdd_file,args=(file_list,builder,))
        write_thread.start()

        #get_mdd_file(file_list, builder)

        global html_string          
        html_string += str(soup)
        
    '''
    tempFolder = os.path.join(os.path.dirname(__file__), "temp")
    html_filename= "dict"+ str(index)+ ".html"
    
    file_path = os.path.abspath(os.path.join(tempFolder, html_filename))
    file_path = file_path.replace('\\', '/')
    with codecs.open(file_path, "w", "utf-8-sig") as text_file:
        text_file.write(html_string)
    all_html.append (file_path)
    '''

def look_up_word(word):
        # print(i,self.comboBox.currentText())
        # empty_temp()
        all_html =[]
        print('word = ', word)
        global html_string 
        html_string = ''
        for index, mydict in enumerate(all_dict):
            get_single_html(word,mydict,index)
            '''
            write_thread = threading.Thread(target=get_single_html,args=(word,mydict,index,))
            write_thread.start()
            write_thread.join()
            '''
        return html_string


def empty_temp():
    folder = os.path.join(os.path.dirname(__file__), extract_path)
    for the_file in os.listdir(folder):
        print(the_file)
        if the_file =='index.html':
            continue
        if the_file =='favicon.ico':
            continue
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                print('deleting:'+file_path)
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


class CallHandler(QObject):
    @pyqtSlot(str)
    def search(self, myword):
        print(myword)
        return look_up_word(myword)
    
    @pyqtSlot(str)
    def get_all_dict(self,res):
        #print('get_all_dict')
        #print('get_all_dict',all_dict)
        print('get_all_dict_json:',json.dumps(all_dict))
        res = json.dumps(all_dict)
        return   json.dumps(all_dict)
 
    @pyqtSlot(str)
    def speak(self, my_text):
        print('say: ', my_text)
        #engine = pyttsx3.init()
        engine.stop()
        voices = engine.getProperty('voices')
        for voice in voices:
            # print("Voice:")
            #print(" - ID: %s" % voice.id)
            #print(" - Name: %s" % voice.name)
            #print(" - Gender: %s" % voice.gender)
            #print(" - Age: %s" % voice.age)
            if 'Zira' in voice.name:
                engine.setProperty('voice', voice.id)
        engine.say(my_text)
        engine.runAndWait()

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


def speak( result):
    #engine.stop()
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'Zira' in voice.name:
            engine.setProperty('voice', voice.id)
    engine.say(result)
    try:
        engine.runAndWait()
    except:
        print('playing~')
    

class MyGui(QMainWindow):
    def showContextMenu(self, position):

        menu = QMenu()
        search_action = menu.addAction("🔍 Search selected text")
        read_action = menu.addAction("🔊 Read selected text")
        reload_action = menu.addAction("Reload page")
        ac = menu.exec_(self.widget_2.mapToGlobal(position))

        if ac == read_action:
            self.get_select_text()
        if ac == search_action:
            self.search_select_text()
        if ac == reload_action:
            self.widget_2.reload()
        '''
        if ac == remove_action:
                quit_msg = "Are you sure?"
                reply = QMessageBox.question(self.widget_2, 'Delete confirmation', quit_msg,
                                             QMessageBox.Yes, QMessageBox.No)
        '''
    


    def js_callback_speak(self, result):
        print('getSelectionText:', result)
        threading.Thread(target=speak,args=(result,)).start()
        #p = Process(target=speak, args=(result,))
        #p.start()
    def js_callback_pass(self, result):
        pass
       

    def get_select_text(self):
         win.widget_2.page().runJavaScript('getSelectionText();',
                                                self.js_callback_speak)  # PyQt5使用runJavaScript修正
    def search_select_text(self):
         win.widget_2.page().runJavaScript('pyjsSearchSelected()', self.js_callback_pass)  # PyQt5使用runJavaScript修正

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
                    file_path = (root + '/' + d).replace('\\', '/')
                    all_dict.append(file_path)

        print(all_dict)

    def on_changeWord(self):
        self.look_up_word('')

    def look_up_word(self, word):
        # print(i,self.comboBox.currentText())

        self.treeWidget.clear()
        root = QTreeWidgetItem(self.treeWidget)
        root.setText(0, self.comboBox.currentText())
        empty_temp()
        html_string = '''
        <!DOCTYPE html>
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta charset="utf-8" />
            <script type="text/javascript" src="jpemartins-speex.js-a6bbdfd/qwebchannel.js"></script>
            <script type="text/javascript" src="jpemartins-speex.js-a6bbdfd/jquery-3.4.0.min.js"></script>
        '''
        html_string += '<link rel="stylesheet" href="css_js/dict.css">'

        html_string += ''' <title>MapleDict</title>

        </head>
        <body>
        <div ondblclick="qt5test();" >
        '''
        print('word = ', word)
        if word == '':
            word = self.comboBox.currentText()
            print('word = ', word)
        for index, d in enumerate(all_dict):

            builder = IndexBuilder(d)

            # html content

            html_content_list = builder.mdx_lookup(word)
            dict_title = builder._title
            #print('html_content_list', html_content_list)

            # print(self.comboBox.currentText(), d , result_list)

            # print ( 'bytes_list', bytes_list)
            # bytes_list= builder.get_mdd_keys()
            '''
            print('your_file', d )
            with open(d+'your_file.txt', 'w') as f:
              for item in bytes_list:
                f.write("%s\n" % item)
            '''

            sound_list = list()
            pix_list = list()
            if len(html_content_list) > 0:
                # print(html_content_list[0])
                soup = BeautifulSoup(html_content_list[0], "html.parser")

                for link in soup.find_all('a'):
                    tmp = link.get('href')
                    print(tmp)
                    if tmp is not None:
                        if tmp.startswith('sound://'):
                            sound_list.append(tmp.replace('sound://', ''))
                            link['sound'] = tmp.replace('sound://', '')
                            link['href'] = "javascript:"
                            link['onclick'] = "javascript:playSound(this);"
                            print(link['href'])

                for link in soup.find_all('img'):
                    tmp = link.get('src')
                    if tmp is not None:
                        if tmp.startswith('/') and tmp is not None:
                            pix_list.append(tmp.replace('/', ''))
                            link['src'] = tmp.replace('/', '')
                        else:
                            pix_list.append(tmp)

                pix_list = list(set(pix_list))
                file_list = sound_list + pix_list
                for file in file_list:
                    bytes_list = builder.mdd_lookup('\\' + file)
                    if len(bytes_list) > 0:
                        with open(os.path.join(os.path.dirname(__file__), "temp/" + file), "wb") as binary_file:
                            binary_file.write(bytes_list[0])

                # 1st line:  <a href="sound://GB_ld45boot.spx" ><img src="snd_uk.png" style="margin-bottom:-4px" border="0" ></img></a>
                # 2nd line:  <a onclick="javascript:qt5test(this);" href="javascript:" sound = "GB_boo_interjecti0205.spx" ><img src="snd_uk.png" style="margin-bottom:-4px" border="0" ></img></a>
                # modify the 1st to the 2nd line style

                if html_content_list[0] != '':
                    # html_string +=html_content_list[0]
                    html_string += '<fieldset>'
                    html_string += '<a name="part' + str(index) + '"></a>'

                    child = QTreeWidgetItem(root)
                    if dict_title == '':
                        #html_string += '<h2>' + os.path.basename(d) + '</h2>'
                        html_string += '<legend>' + \
                            os.path.basename(d) + '</legend>'
                        child.setText(0, os.path.basename(d))
                    else:
                        #html_string += '<h2>' + dict_title + '</h2>'
                        html_string += '<legend>' + dict_title + '</legend>'
                        child.setText(0, dict_title)
                    html_string += str(soup)
                    html_string += '</fieldset>'

        # builder = IndexBuilder( os.path.join(os.path.dirname(__file__), "content/OALD8.mdx"))
        # result_text = builder.mdx_lookup(self.comboBox.currentText())
        # print(result_text)
        # QApplication.processEvents()

        if html_string != '':
            html_string += '''</div> 
               <script src="jpemartins-speex.js-a6bbdfd/public/js/lib/xaudio.js"></script>
               <script src="jpemartins-speex.js-a6bbdfd/public/js/lib/pcmdata.min.js"></script>
               <script src="jpemartins-speex.js-a6bbdfd/public/js/lib/swfobject.js"></script>
               <script src="jpemartins-speex.js-a6bbdfd/public/js/lib/usertiming.js"></script>
               <script src="jpemartins-speex.js-a6bbdfd/public/js/lib/bitstring.js"></script>
               <script src="jpemartins-speex.js-a6bbdfd/public/js/lib/mediacapture.js"></script>
               <script src="jpemartins-speex.js-a6bbdfd/dist/speex.min.js"></script>
               <script src="jpemartins-speex.js-a6bbdfd/public/js/audio.js"></script>
               <script src="jpemartins-speex.js-a6bbdfd/public/js/application.js"></script>
              <script>
                   function playSound(obj) {
                          pyjs.playSound(obj.getAttribute('sound'))
                           }
               
                           function qt5test() {
                           pyjs.myTest(getSelectionText(),function (res) {
                           });
                           }

              
              function getSelectionText() {
                               var text = "";
                               if (window.getSelection) {
                                   text = window.getSelection().toString();
                               } else if (document.selection && document.selection.type != "Control") {
                                   text = document.selection.createRange().text;
                               }
                               return text;
                           }
               

               
                           var myurl
                           $('a').mouseover(function() {
                           myurl =$(this).attr('href')
                           });
                            $('a').mouseout(function() { myurl = '' });
               
                           function qt5MouseClick() {
                            pyjs.myMouseClick( myurl ,function (res) {  
                           });
                           }       

                           function QTscrollTo(hash) {
                             
                               location.hash = "#" + hash;
                           } 
                   const b64toBlob = (b64Data, contentType='', sliceSize=512) => {
               	const byteCharacters = atob(b64Data);
               	const byteArrays = [];
               	for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
               	  const slice = byteCharacters.slice(offset, offset + sliceSize);
                 
               	  const byteNumbers = new Array(slice.length);
               	  for (let i = 0; i < slice.length; i++) {
               		byteNumbers[i] = slice.charCodeAt(i);
               	  }
               	  const byteArray = new Uint8Array(byteNumbers);
               	  byteArrays.push(byteArray);
               	}
               	const blob = new Blob(byteArrays, {type: contentType});
               	return blob;
                 }
                  function decodeFile(bufSpx) {
                   const bin = b64toBlob(bufSpx, '');
                   console.log(bin)
                   var arrayBuffer;
                 var fileReader = new FileReader();
                 fileReader.onload = function(event) {
                   arrayBuffer = event.target.result;
                   console.log(event.target.result )
                   var stream, samples, st;
               	var ogg, header, err;
                 
                   ogg = new Ogg(arrayBuffer, {file: true});
                   
               	ogg.demux();
               	stream = ogg.bitstream();
                 
               	header = Speex.parseHeader(ogg.frames[0]);
               	console.log(header);
                 
               	comment = new SpeexComment(ogg.frames[1]);
               	console.log(comment.data);
                 
               	st = new Speex({
               	  quality: 8,
               	  mode: header.mode,
               	  rate: header.rate
               	});
                 
               	samples = st.decode(stream, ogg.segments);
                 
               	var waveData = PCMData.encode({
               		sampleRate: header.rate,
               		channelCount: header.nb_channels,
               		bytesPerSample: 2,
               		data: samples
               	  });
                 
               	  Speex.util.play(samples,  header.rate);  
               
               	// array buffer holding audio data in wav codec
               	var bufWav = Speex.util.str2ab(waveData);
               	// convert to a blob object
               	var blob = new Blob([bufWav], {type: "audio/wav"});
               	// return a "blob://" url which can be used as a href anywhere
               	return URL.createObjectURL(blob);
               };
               fileReader.readAsBinaryString(bin);
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
            # channel.registerObject('pyjs', handler)

            self.widget_2.page().setWebChannel(channel)

            # self.widget_2.scroll(0,0)

    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'ui/viewForm.ui')
        ico_path = os.path.join(os.path.dirname(__file__), 'ui/maple-leaf.png')
        loadUi(ui_path, self)
        self.start_check_dict()
        self.setWindowIcon(QtGui.QIcon(ico_path))
        self.show()

        self.widget_2.page().setWebChannel(channel)

        if platform == "linux" or platform == "linux2":
            self.widget_2.load(QUrl('file://'))
        elif platform == "darwin":
            self.widget_2.load(QUrl('http://localhost:8080/'))
        elif platform == "win32":
            self.widget_2.load(QUrl('http://localhost:8080/'))

        self.widget_2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.widget_2.customContextMenuRequested.connect(self.showContextMenu)

# Pyqt5 GUI End

# Mdict Flask Server Begin

class Mdict(Resource):
    def get(self):
      
        return {'Hello': 'This is the server for MapleDict',
                'key_test':'OK'}

    def post(self):
        json_data = request.get_json(force=True)
        func = json_data['data']['func']
        if func == 'get_all_dict':
           return {'all_html': all_html, 'all_dict':all_dict}
        if func == 'look_up_word':
           
           myword = json_data['data']['myword']
           print ('look_up_word:'+myword)
           return look_up_word(myword)

flask_app = Flask(__name__)
api = Api(flask_app)
api.add_resource(Mdict, '/')

# Mdict Flask Server End

if __name__ == "__main__":
    #flask_app.run(port=31410, debug=DEBUG)

    flask_thread= threading.Thread(target=flask_app.run,args=(None,'31410'))
    flask_thread.daemon =True
    flask_thread.start()

    #https://stackoverflow.com/questions/33730771/qtwebengine-not-allowed-to-load-local-resource-for-iframe-how-to-disable-web/35034503
    # This is for (Cross-Origin Read Blocking), we don't need any security here because its our own local server
    sys.argv.append('--disable-web-security')
    app = QApplication(sys.argv)
    #settings = QWebEngineSettings.defaultSettings()
    #settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
    win = MyGui()
    app.exec_()
    

