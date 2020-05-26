import PyQt5
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLineEdit


class Ui_LoginPanel(PyQt5.QtCore.QObject):
    switch_window = QtCore.pyqtSignal()
    login = ""
    password = ""

    def setupUi(self, LoginPanel):
        LoginPanel.setObjectName("LoginPanel")
        LoginPanel.resize(1000, 548)
        self.centralwidget = QtWidgets.QWidget(LoginPanel)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(360, 130, 41, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(550, 210, 67, 17))
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(350, 150, 271, 41))
        self.textEdit.setFontPointSize(16)
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(350, 230, 271, 41))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.size()
        self.textEdit_2.setEchoMode(QLineEdit.Password)
        self.textEdit_2.setStyleSheet('lineedit-password-character: 9679')
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(660, 370, 251, 81))
        self.start_btn.setObjectName("start_btn")
        self.start_btn.clicked.connect(self.log_in)
        LoginPanel.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LoginPanel)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setObjectName("menubar")
        LoginPanel.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LoginPanel)
        self.statusbar.setObjectName("statusbar")
        LoginPanel.setStatusBar(self.statusbar)
        self.retranslateUi(LoginPanel)
        QtCore.QMetaObject.connectSlotsByName(LoginPanel)

    def retranslateUi(self, LoginPanel):
        _translate = QtCore.QCoreApplication.translate
        LoginPanel.setWindowTitle(_translate("LoginPanel", "LoginPanel"))
        self.label.setText(_translate("LoginPanel", "Login"))
        self.label_2.setText(_translate("LoginPanel", "Password"))
        self.start_btn.setText(_translate("LoginPanel", "Login"))

    def log_in(self):
        if self.textEdit.toPlainText() == "" or '@' not in self.textEdit.toPlainText() or self.textEdit_2.text() == "":
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('You need to input e-mail from zalando longue account!')
            error_dialog.exec_()
        else:
            self.login = self.textEdit.toPlainText()
            self.password = self.textEdit_2.text()
            self.switch_window.emit()
