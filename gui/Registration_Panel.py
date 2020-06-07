import pyrebase
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit

from firebase.Configuration import config
from gui.Main_Window import center


class Ui_Registration(QtWidgets.QMainWindow):
    def __init__(self, RegistrationPanel):
        super(Ui_Registration, self).__init__()
        self.statusbar = QtWidgets.QStatusBar(RegistrationPanel)
        self.menubar = QtWidgets.QMenuBar(RegistrationPanel)
        self.central_widget = QtWidgets.QWidget(RegistrationPanel)
        self.start_btn = QtWidgets.QPushButton(self.central_widget)
        self.textEdit_2 = QtWidgets.QLineEdit(self.central_widget)
        self.textEdit = QtWidgets.QTextEdit(self.central_widget)
        self.label_2 = QtWidgets.QLabel(self.central_widget)
        self.label = QtWidgets.QLabel(self.central_widget)

    def setupUi(self, RegistrationPanel):
        self.regr = RegistrationPanel
        RegistrationPanel.setObjectName("RegistrationPanel")
        RegistrationPanel.resize(980, 538)
        center(RegistrationPanel)
        self.central_widget.setObjectName("central_widget")
        self.label.setGeometry(QtCore.QRect(360, 130, 41, 17))
        self.label.setObjectName("label")
        self.label_2.setGeometry(QtCore.QRect(550, 210, 67, 17))
        self.label_2.setObjectName("label_2")
        self.textEdit.setGeometry(QtCore.QRect(350, 150, 271, 41))
        self.textEdit.setFontPointSize(16)
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2.setGeometry(QtCore.QRect(350, 230, 271, 41))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.size()
        self.textEdit_2.setEchoMode(QLineEdit.Password)
        self.textEdit_2.setStyleSheet('lineedit-password-character: 9679')
        self.start_btn.setGeometry(QtCore.QRect(660, 370, 251, 81))
        self.start_btn.setObjectName("start_btn")
        self.start_btn.clicked.connect(self.register)
        RegistrationPanel.setCentralWidget(self.central_widget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setObjectName("menubar")
        RegistrationPanel.setMenuBar(self.menubar)
        self.statusbar.setObjectName("statusbar")
        RegistrationPanel.setStatusBar(self.statusbar)
        self.translate_ui(RegistrationPanel)
        RegistrationPanel.setFixedSize(980, 538)
        QtCore.QMetaObject.connectSlotsByName(RegistrationPanel)

    def translate_ui(self, RegistrationPanel):
        _translate = QtCore.QCoreApplication.translate
        RegistrationPanel.setWindowTitle(_translate("RegistrationPanel", "RegistrationPanel"))
        RegistrationPanel.setStyleSheet(
            "QWidget#RegistrationPanel {border-image: url(back.png) 0 0 0 0 stretch stretch;}")
        self.label.setText(_translate("RegistrationPanel", "Login"))
        self.label.setStyleSheet("QLabel { background-color : red; color : white; }")
        self.label_2.setStyleSheet("QLabel { background-color : red; color : white; }")
        self.label_2.setText(_translate("RegistrationPanel", "Password"))
        self.start_btn.setText(_translate("RegistrationPanel", "Register"))

    def register(self):
        try:
            firebase = pyrebase.initialize_app(config)
            auth = firebase.auth()
            auth.create_user_with_email_and_password(self.textEdit.toPlainText(), self.textEdit_2.text())
            self.regr.close()
        except Exception:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Rules! <br>'
                                     '  1. Login must be an email<br>'
                                     '  2. Password must have at least 6 symbols.<br>'
                                     'If rules are fulfilled, login may already exists in database, try other. <br>')
            error_dialog.exec_()


