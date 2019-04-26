# This is the main script, run from here
from PyQt5 import QtCore, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem
import codecs, os, sys, base64, shutil
from PyQt5.QtWebEngineWidgets import *
from bs4 import BeautifulSoup
from PyQt5.QtWebChannel import QWebChannel
from readmdict import MDX, MDD
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl, QObject, pyqtSlot
from mdict_query import IndexBuilder
from sys import platform

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
        print(test)
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
        <div ondblclick="qt5test();" >
        '''
        print('word = ', word)
        if word == '':
            word = self.comboBox.currentText()
            print('word = ', word)
        for index, d in  enumerate(all_dict) :

            builder = IndexBuilder(d)
            # html content

            html_content_list = builder.mdx_lookup(word)
            #print('html_content_list', html_content_list)

            # print(self.comboBox.currentText(), d , result_list)

            # /__playsound.png 
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
                    html_string += '<a href="#part' + str(index) +'"></a>'
                    html_string += '<h1>' + os.path.basename(d) + '</h1>'

                    html_string += str(soup)
                    child = QTreeWidgetItem(root)
                    child.setText(0, os.path.basename(d))

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

            self.treeWidget.expandAll()

            if platform == "linux" or platform == "linux2":
                self.widget_2.load(QUrl('file://' + file_path))
            elif platform == "darwin":
                self.widget_2.load(QUrl('file://' + file_path))
            elif platform == "win32":
                self.widget_2.load(QUrl(file_path))
            self.treeWidget.expandAll()
            self.widget_2.show()

    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'ui/mainForm.ui')
        ico_path = os.path.join(os.path.dirname(__file__), 'ui/maple-leaf.png')
        loadUi(ui_path, self)
        self.start_check_dict()
        self.comboBox.currentIndexChanged.connect(self.on_changeWord)
        self.setWindowIcon(QtGui.QIcon(ico_path))
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyGui()
    # sys.exit(app.exec_())
    app.exec_()
