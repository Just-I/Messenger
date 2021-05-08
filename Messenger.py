from PyQt6 import QtWidgets, QtCore
import requests
from datetime import datetime
import client

class Messenger(QtWidgets.QMainWindow, client.Ui_Messenger):
    def __init__(self):

        super().__init__()
        self.setupUi(self)

        self.pushButton.pressed.connect(self.send_message)

        self.after = 0

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)
        

    def send_message(self):
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()

        try:
            response = requests.post(
                'http://127.0.0.1:5000/send',
                json={
                    'name': name,
                    'text': text
                }
            )
        except:
            self.textBrowser.append('Server is unavailable. Please, try later')
            self.textBrowser.append('')
            return

        if response.status_code != 200:
            self.textBrowser.append('Incorrect name or text')
            self.textBrowser.append('')
            return

    def print_message(self, message):
        t = message['time']
        dt = datetime.fromtimestamp(t)
        dt = dt.strftime('%H:%M:%S:')
        self.textBrowser.append(dt + ' ' + message['name'])
        self.textBrowser.append(message['text'])
        self.textBrowser.append('')

    def get_messages(self):
        try:
            response = requests.get(
                'http://127.0.0.1:5000/get',
                params={'after': self.after}
            )
        except:
            return
        
        add = response.json()['messages']

        for message in add:
            self.print_message(message)
            self.after = message['time']

app = QtWidgets.QApplication([])
window = Messenger()
window.show()
app.exec()
