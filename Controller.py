import sys

import pyrebase
from PyQt5 import QtWidgets, QtGui

from gui.Login_Panel import Ui_LoginPanel
from gui.Main_Window import Ui_MainWindow

config = {
    "apiKey": "AIzaSyCnut8SgRAcPz7MQ6B74soTw_Lyqz9fSbw ",
    "authDomain": "shopping-bot-c75af.firebaseapp.com",
    "databaseURL": "https://shopping-bot-c75af.firebaseio.com/users",
    "storageBucket": "shopping-bot-c75af.appspot.com",
    "serviceAccount": "firebase/shopping-bot-c75af-firebase-adminsdk-bawov-21d8c0da9d.json"
}


class Controller:
    """ Switching between frames."""

    def __init__(self):
        self.lp = Ui_LoginPanel()
        self.LoginPanel = QtWidgets.QMainWindow()
        self.MainWin = QtWidgets.QMainWindow()
        self.mw = Ui_MainWindow(self.MainWin)

    def show_login(self):
        self.lp.setupUi(self.LoginPanel)
        self.lp.switch_window.connect(self.show_main)
        self.LoginPanel.show()

    def show_main(self):
        self.mw.setupUi(self.MainWin, self.lp.login, self.lp.password)
        self.LoginPanel.close()
        self.MainWin.show()


def main():
    firebase = pyrebase.initialize_app(config)
    a = firebase.auth()
    db = firebase.database()
    stor = firebase.storage()
    data = {
        "name": "Mortimer 'Morty' Smith"
    }
    # results = db.child("users").push(data)
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('features/icon.png'))
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
