from datetime import datetime
from skillbot import SkillBot

import requests
from PyQt5 import QtWidgets, QtCore
import clientui


# File with messenger logic


class ExampleApp(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.bot = SkillBot(url)  # Appending bot to messenger
        self.setupUi(self)

        self.pushButton.pressed.connect(self.send_message)

        # Creating timer for checking new messages
        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)

    # Function witch get messages from server
    def get_messages(self):

        try:
            response = requests.get(
                self.url + 'get_messages',
                params={'after': self.after}

            )
        except:
            return

        if response.status_code == 200:
            messages = response.json()['messages']

            # Appending messages to UI
            for message in messages:
                self.after = message['time']
                ftime = datetime.fromtimestamp(message['time']).strftime('%Y/%m/%d %H:%M:%S')
                self.textBrowser.append(ftime + ' ' + message['author'])
                self.textBrowser.append(message['text'])
                self.textBrowser.append('')

    # Sending message from user to server
    def send_message(self):
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()
        try:
            response = requests.post(
                self.url + 'send_message',
                json={'text': text, 'author': name}
            )
        except:
            self.textBrowser.append('Сервер недоступен')
            self.textBrowser.append('')
            self.textBrowser.repaint()
            return

        self.bot.validateMessage({'text': text, 'author': name})

        if response.status_code != 200:
            self.textBrowser.append('Ошибка валидации')
            self.textBrowser.append('')
            self.textBrowser.repaint()
            return

        self.textEdit.clear()
        self.textEdit.repaint()


app = QtWidgets.QApplication([])
window = ExampleApp(' http://127.0.0.1:5000/')
window.show()
app.exec_()
