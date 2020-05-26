import time
from datetime import datetime

import PyQt5
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QLineEdit

from Bot import ShoppingBot


def remove_item_qlist(given_qlist):
    """
    :param given_qlist:
    :return: removing item from qlist
    """
    listItems = given_qlist.selectedItems()
    if not listItems: return
    for item in listItems:
        given_qlist.takeItem(given_qlist.row(item))


def seconds_interval(start, end):
    """
    :param start:
    :param end:
    :return: time interval between 2 datetime bojects
    """
    diff = end - start
    millis = diff.days * 24 * 60 * 60
    millis += diff.seconds
    millis += diff.microseconds
    return millis


def qlist_to_list(listWidget):
    """
    Convert qwidgetlist to list
    :param listWidget:
    :return:
    """
    return [str(listWidget.item(i).text()) for i in range(listWidget.count())]


def get_delay(later_time):
    """
    Gets difference between 2 times in different
    object datetimes.
    :param later_time:
    :return:
    """
    first_time = datetime.now()
    f_a = str(first_time)[:19].replace("-", " ").replace(":", " ").split()
    l_a = [str(x) for x in later_time.replace(".", " ").replace(":", " ").split()] + ['00']
    f_a[0], f_a[2] = f_a[2], f_a[0]
    f_a[2], l_a[2] = f_a[2][:2], l_a[2][:2]
    l_str = l_a[0] + '/' + l_a[1] + '/' + l_a[2] + " " + l_a[3] + ":" + l_a[4] + ":" + l_a[5]
    f_str = f_a[0] + '/' + f_a[1] + '/' + f_a[2] + " " + f_a[3] + ":" + f_a[4] + ":" + f_a[5]
    later = datetime.strptime(str(l_str), '%d/%m/%y %H:%M:%S')
    first = datetime.strptime(f_str, '%d/%m/%y %H:%M:%S')
    return seconds_interval(first, later)


def get_text():
    """
    QDialog for text needs
    :return:
    """
    text, okPressed = QInputDialog.getText(QInputDialog(), "Get text", "Size:", QLineEdit.Normal, "")
    if okPressed and text != '':
        return text


def get_integer():
    """
    QDialog for int needs.
    :return:
    """
    i, okPressed = QInputDialog.getInt(QInputDialog(), "Get integer", "Price:")
    if okPressed:
        return i


class Ui_MainWindow(PyQt5.QtCore.QObject):
    def configure_slider(self):
        """
        Configures slider
        :return:
        """
        self.stuck_slider.setTickInterval(1)
        self.stuck_slider.setSingleStep(1)
        self.stuck_slider.setRange(1, 5)
        self.stuck_slider.senderSignalIndex()
        self.stuck_slider.setOrientation(QtCore.Qt.Vertical)
        self.stuck_slider.setMinimum(1)
        self.stuck_slider.setMaximum(5)

    def __init__(self, MainWindow):
        """
        Initate all components.
        :param MainWindow:
        """
        super(Ui_MainWindow, self).__init__()
        MainWindow.setFixedSize(980, 538)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.actionDonate = QtWidgets.QAction(MainWindow)
        self.actionInfo = QtWidgets.QAction(MainWindow)
        self.actionReset_preferences = QtWidgets.QAction(MainWindow)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.check_box_date = QtWidgets.QCheckBox(self.centralwidget)
        self.del_account_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_account_btn = QtWidgets.QPushButton(self.centralwidget)
        self.stuck_slider = QtWidgets.QSlider(self.centralwidget)
        self.configure_slider()
        self.stuck_slider.valueChanged[int].connect(self.set_stuck)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.up_range_stuck = QtWidgets.QLabel(self.centralwidget)
        self.down_range_stuck = QtWidgets.QLabel(self.centralwidget)
        self.accounts_list = QtWidgets.QListWidget(self.centralwidget)
        self.set_max_price_btn = QtWidgets.QPushButton(self.centralwidget)
        self.del_category_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_category_btn = QtWidgets.QPushButton(self.centralwidget)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.categories_list = QtWidgets.QListWidget(self.centralwidget)
        self.del_brand_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_brand_btn = QtWidgets.QPushButton(self.centralwidget)
        self.del_size_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_size_btn = QtWidgets.QPushButton(self.centralwidget)
        self.brands_list = QtWidgets.QListWidget(self.centralwidget)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_2 = QtWidgets.QProgressBar(self.centralwidget)
        self.sizes_list = QtWidgets.QListWidget(self.centralwidget)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.stop_btn = QtWidgets.QPushButton(self.centralwidget)
        self.menuMenu = QtWidgets.QMenu(self.menubar)

    def set_stuck(self, value):
        """
        Set stuck value
        :param value:
        :return:
        """
        self.value = value

    def get_stuck(self):
        """
        :return: stuck value (per item)
        """
        if self.value:
            return self.value

    def start_bot(self):
        """
        Creates bot object and passes arguments.
        :return:
        """
        print('Creating Bot object start ')
        if self.check_box_date.isChecked():
            delay = get_delay(self.dateTimeEdit.textFromDateTime(self.dateTimeEdit.dateTime()))
        else:
            delay = 0
        time.sleep(delay)
        ShoppingBot("piotrpopisgames@gmail.com", 'testertest', qlist_to_list(self.categories_list),
                    qlist_to_list(self.sizes_list),
                    qlist_to_list(self.brands_list), self.textEdit.toPlainText(), self.lcdNumber.intValue())

    def stop_bot(self):
        # TODO : IMPLEMENT
        print('Stopping bot')

    def add_size(self):
        """
        Adds size to sizes_qlist
        :return:
        """
        self.sizes_list.addItem(get_text())

    def add_brand(self):
        """
        Add new brand to brand_qlist
        :return:
        """
        self.brands_list.addItem(get_text())

    def add_category(self):
        """
        Inserting new category to category list.
        :return:
        """
        self.categories_list.addItem(get_text())

    # TODO IMPLEMENT
    def add_account(self):
        print('Adding account')

    def set_max_price(self):
        """
        Sets max price per item. default - none on
        lcd displayer
        :return:
        """
        self.lcdNumber.display(str(get_integer()))

    def del_size(self):
        """
        Removes given size. from size list
        :return:
        """
        remove_item_qlist(self.sizes_list)

    def del_brand(self):
        """
        Deletes brand from brand list
        :return:
        """
        remove_item_qlist(self.brands_list)

    def del_category(self):
        """
        Remove category from category list
        :return:
        """
        remove_item_qlist(self.categories_list)

    def del_account(self):
        """
        Remove zalando account from account list.
        :return:
        """
        if len(self.accounts_list) > 1:
            remove_item_qlist(self.accounts_list)
        else:
            pass

    def setup_labels(self):
        """
        Creates all labels
        :return:
        """
        self.label_4.setGeometry(QtCore.QRect(450, 190, 101, 17))
        self.label_4.setObjectName("label_4")
        self.label_5.setGeometry(QtCore.QRect(660, 190, 141, 17))
        self.label_5.setObjectName("label_5")
        self.label_6.setGeometry(QtCore.QRect(450, 250, 101, 17))
        self.label_6.setObjectName("label_6")
        self.label_7.setGeometry(QtCore.QRect(30, 60, 121, 17))
        self.label_7.setObjectName("label_7")
        self.label_8.setGeometry(QtCore.QRect(30, 190, 121, 17))
        self.label_8.setObjectName("label_8")
        self.label_9.setGeometry(QtCore.QRect(30, 320, 121, 17))
        self.label_9.setObjectName("label_9")
        self.label_10.setGeometry(QtCore.QRect(450, 60, 121, 17))
        self.label_10.setObjectName("label_10")

    def setup_geometry(self):
        """
        setup geometry for all components
        :return:
        """
        self.start_btn.setGeometry(QtCore.QRect(630, 400, 141, 41))
        self.stop_btn.setGeometry(QtCore.QRect(800, 400, 141, 41))
        self.dateTimeEdit.setGeometry(QtCore.QRect(440, 340, 171, 26))
        self.lcdNumber.setGeometry(QtCore.QRect(650, 210, 101, 31))
        self.progressBar.setGeometry(QtCore.QRect(30, 470, 921, 21))
        self.progressBar_2.setGeometry(QtCore.QRect(20, 10, 921, 21))
        self.sizes_list.setGeometry(QtCore.QRect(20, 80, 241, 91))
        self.stuck_slider.setGeometry(QtCore.QRect(880, 80, 41, 161))
        self.up_range_stuck.setGeometry(QtCore.QRect(875, 80, 11, 21))
        self.down_range_stuck.setGeometry(QtCore.QRect(875, 221, 11, 21))
        self.textEdit.setGeometry(QtCore.QRect(440, 210, 171, 31))
        self.checkBox.setGeometry(QtCore.QRect(620, 270, 91, 31))
        self.textEdit_3.setGeometry(QtCore.QRect(440, 270, 171, 31))
        self.brands_list.setGeometry(QtCore.QRect(20, 210, 241, 91))
        self.add_size_btn.setGeometry(QtCore.QRect(270, 80, 141, 41))
        self.del_size_btn.setGeometry(QtCore.QRect(270, 130, 141, 41))
        self.add_brand_btn.setGeometry(QtCore.QRect(270, 210, 141, 41))
        self.del_brand_btn.setGeometry(QtCore.QRect(270, 260, 141, 41))
        self.categories_list.setGeometry(QtCore.QRect(20, 340, 241, 91))
        self.add_category_btn.setGeometry(QtCore.QRect(270, 340, 141, 41))
        self.del_category_btn.setGeometry(QtCore.QRect(270, 390, 141, 41))
        self.set_max_price_btn.setGeometry(QtCore.QRect(760, 210, 71, 31))
        self.accounts_list.setGeometry(QtCore.QRect(440, 80, 241, 91))
        self.add_account_btn.setGeometry(QtCore.QRect(690, 80, 141, 41))
        self.del_account_btn.setGeometry(QtCore.QRect(690, 130, 141, 41))
        self.check_box_date.setGeometry(QtCore.QRect(620, 340, 91, 31))
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))

    def setup_obj_names(self):
        """
        names components (readability)
        :return:
        """
        self.start_btn.setObjectName("start_btn")
        self.stop_btn.setObjectName("stop_btn")
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.lcdNumber.setObjectName("lcdNumber")
        self.progressBar.setObjectName("progressBar")
        self.progressBar_2.setObjectName("progressBar_2")
        self.sizes_list.setObjectName("sizes_list")
        self.stuck_slider.setObjectName("stuck_slider")
        self.up_range_stuck.setObjectName("up_range_stuck")
        self.down_range_stuck.setObjectName("down_range_stuck")
        self.textEdit.setObjectName("textEdit")
        self.checkBox.setObjectName("checkBox")
        self.textEdit_3.setObjectName("textEdit_3")
        self.brands_list.setObjectName("brands_list")
        self.add_size_btn.setObjectName("add_size_btn")
        self.del_size_btn.setObjectName("del_size_btn")
        self.add_brand_btn.setObjectName("add_brand_btn")
        self.del_brand_btn.setObjectName("del_brand_btn")
        self.categories_list.setObjectName("categories_list")
        self.add_category_btn.setObjectName("add_category_btn")
        self.del_category_btn.setObjectName("del_category_btn")
        self.set_max_price_btn.setObjectName("set_max_price_btn")
        self.accounts_list.setObjectName("accounts_list")
        self.add_account_btn.setObjectName("add_account_btn")
        self.del_account_btn.setObjectName("del_account_btn")
        self.check_box_date.setObjectName("check_box_date")
        self.statusbar.setObjectName("statusbar")
        self.menubar.setObjectName("menubar")
        self.menuMenu.setObjectName("menuMenu")

    def connect_btns(self):
        """
        connect buttons to functionalities
        :return:
        """
        self.start_btn.clicked.connect(self.start_bot)
        self.stop_btn.clicked.connect(self.stop_bot)
        self.add_size_btn.clicked.connect(self.add_size)
        self.del_size_btn.clicked.connect(self.del_size)
        self.add_brand_btn.clicked.connect(self.add_brand)
        self.add_category_btn.clicked.connect(self.add_category)
        self.set_max_price_btn.clicked.connect(self.set_max_price)
        self.add_account_btn.clicked.connect(self.add_account)

    def setup_menu(self):
        """
        setup menu bar and options.
        :return:
        """
        self.actionReset_preferences.setObjectName("actionReset_preferences")
        self.actionInfo.setObjectName("actionInfo")
        self.actionDonate.setObjectName("actionDonate")
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionReset_preferences)
        self.menuMenu.addAction(self.actionInfo)
        self.menuMenu.addAction(self.actionDonate)
        self.menubar.addAction(self.menuMenu.menuAction())

    def setupUi(self, MainWindow, login, password):
        """
        main function to operate over setups
        :param MainWindow:
        :param login:
        :param password:
        :return:
        """
        MainWindow.setObjectName("MainWindow")
        self.setup_labels()
        self.setup_geometry()
        self.connect_btns()
        self.setup_obj_names()
        self.progressBar.setProperty("value", 24)
        self.progressBar_2.setProperty("value", 24)
        self.accounts_list.addItem(login)
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setStatusBar(self.statusbar)
        MainWindow.setMenuBar(self.menubar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        Assign correct words to automatically named
        objects. Readability improvement.+
        :param MainWindow:
        :return:
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_btn.setText(_translate("MainWindow", "Start"))
        self.stop_btn.setText(_translate("MainWindow", "Stop"))
        self.label_4.setText(_translate("MainWindow", "Campaign ID"))
        self.label_5.setText(_translate("MainWindow", "Max Price( Per Item)"))
        self.stuck_slider.setObjectName("Quantity")
        self.checkBox.setText(_translate("MainWindow", "Send Mail"))
        self.label_6.setText(_translate("MainWindow", "Email"))
        self.label_7.setText(_translate("MainWindow", "Sizes"))
        self.label_8.setText(_translate("MainWindow", "Brands"))
        self.up_range_stuck.setText(_translate("MainWindow", "5 - "))
        self.down_range_stuck.setText(_translate("MainWindow", "1 - "))
        self.add_size_btn.setText(_translate("MainWindow", "Add"))
        self.del_size_btn.setText(_translate("MainWindow", "Delete"))
        self.add_brand_btn.setText(_translate("MainWindow", "Add"))
        self.del_brand_btn.setText(_translate("MainWindow", "Delete"))
        self.label_9.setText(_translate("MainWindow", "Categories"))
        self.add_category_btn.setText(_translate("MainWindow", "Add"))
        self.del_category_btn.setText(_translate("MainWindow", "Delete"))
        self.set_max_price_btn.setText(_translate("MainWindow", "Set"))
        self.label_10.setText(_translate("MainWindow", "Accounts"))
        self.add_account_btn.setText(_translate("MainWindow", "Add"))
        self.del_account_btn.setText(_translate("MainWindow", "Delete"))
        self.check_box_date.setText(_translate("MainWindow", "Date"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionReset_preferences.setText(_translate("MainWindow", "Reset preferences"))
        self.actionInfo.setText(_translate("MainWindow", "Info"))
        self.actionDonate.setText(_translate("MainWindow", "Donate"))
