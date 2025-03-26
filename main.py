import sys
import socket as sk
from datetime import time
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QByteArray, Qt

from PyQt5.QtGui import QPixmap
import threading as td
import pickle as pc

import Database
from clientfinal import Ui_MainWindow
from steno import stenography

host = "192.168.29.227"
port = 8081
alias = ""
send_to = ""
button_list = []
aliases = []
client = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
client.connect((host, port))

Database.destroy_database('my_chat')
Database.create_database('my_chat')
Database.create_user_table('my_chat_table', 'my_chat')

class MySignals(QObject):
    received_data = pyqtSignal(object)

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send_message)
        self.signals = MySignals()
        self.signals.received_data.connect(self.process_received_data)
        self.show()

        self.show_dialog_flag = True
        self.show_dialog()


        receive_thread = td.Thread(target=self.receive)
        receive_thread.start()

    def show_dialog(self):
        global alias
        if self.show_dialog_flag:
            alias, ok_pressed = QInputDialog.getText(self, "Input", "Your Name:")

            if ok_pressed:
                self.label_user_name = QLabel(f"Welcome, {alias}", self.centralwidget)
                self.verticalLayout.addWidget(self.label_user_name)
                self.label_user_name.setStyleSheet("background-color: lightblue;")

                self.label_user_name.setGeometry(10, 10, 300, 30)
                self.label_user_name.show()

            alias_to_send = alias.encode()
            client.send(alias_to_send)
            self.show_dialog_flag = False

    def process_received_data(self, data):
        global aliases
        if len(data) == 1 and isinstance(data, tuple):
            self.show_dialog()
        elif len(data) == 4 and isinstance(data, tuple):
            sender = data[1]
            message = data[0]
            time_received = data[2]
            img = data[3]
            Database.insert_message('my_chat_table', sender, 0, message, time_received, img, 'my_chat')
            if sender == send_to:
                if img != None:
                    byte_array = QByteArray(img)
                    pixmap = QPixmap()
                    pixmap.loadFromData(byte_array)
                    re_pixmap = pixmap.scaled(400, 267)
                    formatted_message = f"{sender} [{time_received}]:"
                    message_label = QLabel(formatted_message, self.verticalWidget_3)
                    pix_label = QLabel(formatted_message, self.verticalWidget_3)
                    pix_label.setPixmap(re_pixmap)
                    self.verticalLayout_3.addWidget(message_label)
                    self.verticalLayout_3.addWidget(pix_label)
                    pix_label.show()
                else:
                    message = stenography.decode_img_data(data[0])
                    formatted_message = f"{sender} [{time_received}]: {message}"
                    message_label = QLabel(formatted_message, self.verticalWidget_3)
                    self.verticalLayout_3.addWidget(message_label)
                    message_label.show()
        elif len(data) == 2 and data[0] == "ALIAS_LIST":
            new_aliases = data[1]
            if len(new_aliases)<len(aliases):
                dis_clients = set(aliases) - set(new_aliases)
                for client in dis_clients:
                    for i in reversed(range(self.verticalLayout_2.count())):
                        item = self.verticalLayout_2.itemAt(i)
                        if isinstance(item.widget(), QPushButton):
                            button = item.widget()
                            if button.text() == client:
                                button.deleteLater()
                                self.verticalLayout_2.removeItem(item)
                            
                             
           
            else:
                new_clients = set(new_aliases) - set(aliases)
                for alias in new_clients:
                    if alias not in button_list:
                        textn = alias
                        new_button = QPushButton(textn, self.verticalWidget_2)
                        self.verticalLayout_2.addWidget(new_button)
                        new_button.clicked.connect(lambda is_pressed, alias=alias: self.on_button_click(is_pressed, alias))
                        button_list.append(alias)
            aliases = new_aliases
        elif type(data) == list:
            for message in data:
                Database.insert_message('my_chat_table', message[0], message[1], message[2], message[3], message[4], 'my_chat')

    def receive(self):
        global alias
        while True:
            message = client.recv(10 * 1024 * 1024)
            data = pc.loads(message)
            self.signals.received_data.emit(data)       

    def send_message(self):
        global alias
        global send_to

        user = send_to
        image_data=None
        message_text = self.message.toPlainText()
        if message_text:
            path = message_text.split("!!**!!")
            if path[0] == "":
                with open(path[1], 'rb') as file:
                    image_data = file.read()

                time_sent = time.strftime("%H:%M", time.localtime())
                data = (None,user, time_sent,image_data)
                Database.insert_message('my_chat_table', user, 1, None, time_sent, image_data, 'my_chat')
                out = pc.dumps(data)
                client.send(out)
                formatted_message = f"{alias} [{time_sent}]: {message_text}"
                message_label = QLabel(formatted_message, self.verticalWidget_3)
                pix_label = QLabel(formatted_message, self.verticalWidget_3)
                original_pixmap = QPixmap(path[1])
                re_pixmap = original_pixmap.scaled(400, 267)
                pix_label.setPixmap(re_pixmap)
                self.verticalLayout_3.addWidget(message_label)
                self.verticalLayout_3.addWidget(pix_label)
            else:
                time_sent = time.strftime("%H:%M", time.localtime())
                formatted_message = f"{alias} [{time_sent}]: {message_text}"
                message_label = QLabel(formatted_message, self.verticalWidget_3)
                self.verticalLayout_3.addWidget(message_label)
                message_text = stenography.encode_img_data(message_text)

                data = (message_text, user, time_sent,None)
                Database.insert_message('my_chat_table', user, 1, message_text, time_sent, None, 'my_chat')
                out = pc.dumps(data)
                client.send(out)


        self.message.clear()
        self.message.setFocus()

    def on_button_click(self, is_pressed, button_text):
        global send_to
        send_to = button_text
        self.clearthat()

        label_friend_name = QLabel(f"Chatting with {send_to}", self.verticalWidget_3)
        label_friend_name.setAlignment(Qt.AlignCenter)
        self.verticalLayout_3.addWidget(label_friend_name)
        message_history = Database.load_data('my_chat_table', 'my_chat')
        if message_history != 0:
            for message_entry in message_history:
                (friend, type1, message, time_sent,img) = message_entry
                if friend == send_to:
                    if img is not None:
                        byte_array = QByteArray(img)
                        pixmap = QPixmap()
                        pixmap.loadFromData(byte_array)
                        formatted_message = f"{friend} [{time_sent}]:"

                        message_label = QLabel(formatted_message, self.verticalWidget_3)
                        pix_label = QLabel(formatted_message, self.verticalWidget_3)
                        pixmap = pixmap.scaled(400, 267)
                        pix_label.setPixmap(pixmap)
                        self.verticalLayout_3.addWidget(message_label)
                        self.verticalLayout_3.addWidget(pix_label)
                        pix_label.show()
                    else:
                        message = stenography.decode_img_data(message)
                        formatted_message = f"{friend} [{time_sent}]: {message}"
                        message_label = QLabel(formatted_message, self.verticalWidget_3)
                        self.verticalLayout_3.addWidget(message_label)
                        message_label.show()

    def clearthat(self):

        layout = self.verticalLayout_3
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    sys.exit(app.exec_())
