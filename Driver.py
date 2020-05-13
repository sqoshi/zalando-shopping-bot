import sys

from PyQt5 import QtWidgets, QtGui

from gui.Login_Panel import Ui_LoginPanel
from gui.Main_Window import Ui_MainWindow

""" Switching between frames."""


class Controller:
    def __init__(self):
        pass

    def show_login(self):
        self.LoginPanel = QtWidgets.QMainWindow()
        self.lp = Ui_LoginPanel()
        self.lp.setupUi(self.LoginPanel)
        self.lp.switch_window.connect(self.show_main)
        self.LoginPanel.show()

    def show_main(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.mw = Ui_MainWindow()
        self.mw.setupUi(self.MainWindow)
        self.LoginPanel.close()
        self.MainWindow.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
