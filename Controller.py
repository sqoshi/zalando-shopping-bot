import sys

from PyQt5 import QtWidgets, QtGui

from gui.Login_Panel import Ui_LoginPanel
from gui.Main_Window import Ui_MainWindow


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
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('features/icon.png'))
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
