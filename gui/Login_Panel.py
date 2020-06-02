import PyQt5
import pyrebase
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLineEdit

from firebase.Configuration import config
from gui.Registration_Panel import Ui_Registration


class Ui_LoginPanel(PyQt5.QtCore.QObject):
    switch_window = QtCore.pyqtSignal()
    login = ""
    password = ""
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()

    def setupUi(self, LoginPanel):
        LoginPanel.setObjectName("LoginPanel")
        LoginPanel.resize(1000, 548)
        self.central_widget = QtWidgets.QWidget(LoginPanel)
        self.central_widget.setObjectName("central_widget")
        self.label = QtWidgets.QLabel(self.central_widget)
        self.label.setGeometry(QtCore.QRect(210, 130, 41, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.central_widget)
        self.label_2.setGeometry(QtCore.QRect(400, 210, 67, 17))
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QTextEdit(self.central_widget)
        self.textEdit.setGeometry(QtCore.QRect(200, 150, 271, 41))
        self.textEdit.setFontPointSize(16)
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QLineEdit(self.central_widget)
        self.textEdit_2.setGeometry(QtCore.QRect(200, 230, 271, 41))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.size()
        self.textEdit_2.setEchoMode(QLineEdit.Password)
        self.textEdit_2.setStyleSheet('lineedit-password-character: 9679')
        self.start_btn = QtWidgets.QPushButton(self.central_widget)
        self.start_btn.setGeometry(QtCore.QRect(560, 370, 251, 81))
        self.start_btn.setObjectName("start_btn")
        self.start_btn.clicked.connect(self.log_in)
        self.register_btn = QtWidgets.QPushButton(self.central_widget)
        self.register_btn.setGeometry(QtCore.QRect(660, 250, 251, 81))
        self.register_btn.setObjectName("register_btn")
        self.register_btn.clicked.connect(self.register)
        LoginPanel.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(LoginPanel)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setObjectName("menubar")
        LoginPanel.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LoginPanel)
        self.statusbar.setObjectName("statusbar")
        LoginPanel.setStatusBar(self.statusbar)
        self.translate_ui(LoginPanel)
        QtCore.QMetaObject.connectSlotsByName(LoginPanel)

    def translate_ui(self, LoginPanel):
        _translate = QtCore.QCoreApplication.translate
        LoginPanel.setWindowTitle(_translate("LoginPanel", "LoginPanel"))
        self.label.setText(_translate("LoginPanel", "Login"))
        self.label_2.setText(_translate("LoginPanel", "Password"))
        self.start_btn.setText(_translate("LoginPanel", "Login"))
        self.register_btn.setText(_translate("LoginPanel", "Register"))

    def log_in(self):
        self.login = self.textEdit.toPlainText()
        self.password = self.textEdit_2.text()
        try:
            self.user = self.auth.sign_in_with_email_and_password(self.login, self.password)
            self.switch_window.emit()
        except:
            error_dial = QtWidgets.QErrorMessage()
            error_dial.showMessage('Wrong data or no login in database')
            error_dial.exec_()

    def register(self):
        self.main_frame = QtWidgets.QMainWindow()
        self.register_ui = Ui_Registration(self.main_frame)
        self.register_ui.setupUi(self.main_frame)
        self.register_ui.translate_ui(self.main_frame)
        self.main_frame.show()
