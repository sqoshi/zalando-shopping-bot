from PyQt5 import QtWidgets


class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        self.pwd, self.log = "", ""
        super(Login, self).__init__(parent)
        self.textName = QtWidgets.QLineEdit(self)
        self.setWindowTitle('Account adder')
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Add Acount', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        self.log = self.textName.text()
        self.pwd = self.textPass.text()
        if self.textName.text() == "" or '@' not in self.textName.text() or self.textName.text() == "" or self.textPass.text() == "":
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('You need to input e-mail and password from zalando longue account!')
            error_dialog.exec_()
        else:
            self.accept()
