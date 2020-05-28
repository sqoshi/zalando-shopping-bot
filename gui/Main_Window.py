import gc
import multiprocessing
import time
from datetime import datetime

import PyQt5
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QLineEdit

from Bot import ShoppingBot
from gui.Add_Account_Input_Dialog import Login


def remove_item_qlist(given_qlist):
    """
    :param given_qlist:
    :return: removing item from qlist
    """
    listItems = given_qlist.selectedItems()
    if not listItems:
        return
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


def convert_qlist(listWidget):
    """
    Convert qwidgetlist to list
    :param listWidget:
    :return:
    """
    return [str(listWidget.item(i).text()) for i in range(listWidget.count())]


def get_delay(later_time):
    """
    Gets difference between 2 times in different
    object date_times.
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
    def threaded_function(self):
        self.pp.start_bot()

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
        self.stuck_slider.valueChanged[int].connect(self.set_stuck)

    def set_stuck(self, value):
        """
        Set stuck value
        :param value:
        :return:
        """
        self.stucks = value
        self.update_config_progress()

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
        if self.textEdit.toPlainText() == "":
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('You need to input account and pass campaign id ')
            error_dialog.exec_()
        else:
            self.sb = ShoppingBot(convert_qlist(self.accounts_list),convert_qlist(self.categories_list),
                                  convert_qlist(self.sizes_list),
                                  convert_qlist(self.brands_list), self.textEdit.toPlainText(),
                                  self.lcdNumber.intValue(),self.get_stuck,0)
            if self.check_box_date.isChecked():
                delay = get_delay(self.dateTimeEdit.textFromDateTime(self.dateTimeEdit.dateTime()))
            else:
                delay = 0
            time.sleep(delay)
            self.process.start()

    def stop_bot(self):
        """
        Terminating the subprocces of creation, and closes windows.
        :return:
        """
        quiter = multiprocessing.Process(target=self.pp.driver.quit)
        quiter.start()
        self.process.terminate()
        gc.collect()

    def add_size(self):
        """
        Adds size to sizes_qlist
        :return:
        """
        self.sizes_list.addItem(get_text())
        self.update_config_progress()

    def add_brand(self):
        """
        Add new brand to brand_qlist
        :return:
        """
        self.brands_list.addItem(get_text())
        self.update_config_progress()

    def add_category(self):
        """
        Inserting new category to category list.
        :return:
        """
        self.categories_list.addItem(get_text())
        self.update_config_progress()

    def add_account(self):
        """
        Add accounts to widget list and,
        and login,passwords pairs to account list passed
        to shopping bot
        :return:
        """
        self.log = Login()
        self.log.show()
        if self.log.exec_() == QtWidgets.QDialog.Accepted:
            self.accounts_list.addItem(str(self.log.log) + ' ' + str(self.log.pwd))
        self.log.close()
        self.update_config_progress()

    def set_max_price(self):
        """
        Sets max price per item. default - none on
        lcd displayer
        :return:
        """
        self.lcdNumber.display(str(get_integer()))
        self.update_config_progress()

    def del_size(self):
        """
        Removes given size. from size list
        :return:
        """
        remove_item_qlist(self.sizes_list)
        self.update_config_progress()

    def del_brand(self):
        """
        Deletes brand from brand list
        :return:
        """
        remove_item_qlist(self.brands_list)
        self.update_config_progress()

    def del_category(self):
        """
        Remove category from category list
        :return:
        """
        remove_item_qlist(self.categories_list)
        self.update_config_progress()

    def del_account(self):
        """
        Remove zalando account from account list.
        :return:
        """
        if len(self.accounts_list) > 1:
            remove_item_qlist(self.accounts_list)
        else:
            pass
        self.update_config_progress()

    def get_config(self):
        return convert_qlist(self.categories_list), convert_qlist(self.accounts_list), convert_qlist(
            self.sizes_list), convert_qlist(self.brands_list), self.lcdNumber.intValue(), self.textEdit.toPlainText()

    def update_config_progress(self):
        points = 0
        max_p = 6
        l1, l2, l3, l4, lcd, cid = self.get_config()
        if len(l1) > 0:
            points += 1
        if len(l2) > 0:
            points += 1
        if len(l3) > 0:
            points += 1
        if len(l4) > 0:
            points += 1
        if lcd != 0:
            points += 1
        if cid != "":
            points += 1
        if points != 0:
            self.progressBar.setProperty("value", int(100 * points / max_p))

    def reset_config(self):
        """
        Resets current config to default.
        :return:
        """
        self.categories_list.clear()
        self.sizes_list.clear()
        self.brands_list.clear()
        self.accounts_list.clear()
        self.textEdit.clear()
        self.textEdit_3.clear()
        self.stuck_slider.setValue(1)
        self.progressBar.setProperty("value", 0)
        self.progressBar_2.setProperty("value", 0)
        self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.lcdNumber.display('0')
        self.checkBox.setChecked(False)
        self.check_box_date.setChecked(False)

    def __init__(self, MainWindow):
        """
        Initate all components.
        :param MainWindow:
        """
        super(Ui_MainWindow, self).__init__()
        self.process = multiprocessing.Process(target=self.threaded_function)

        MainWindow.setFixedSize(980, 538)
        self.stucks = 1
        self.sb = None
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionInfo = QtWidgets.QAction(MainWindow)
        self.actionReset_preferences = QtWidgets.QAction(MainWindow)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.check_box_date = QtWidgets.QCheckBox(self.central_widget)
        self.del_account_btn = QtWidgets.QPushButton(self.central_widget)
        self.add_account_btn = QtWidgets.QPushButton(self.central_widget)
        self.stuck_slider = QtWidgets.QSlider(self.central_widget)
        self.configure_slider()
        self.label_10 = QtWidgets.QLabel(self.central_widget)
        self.up_range_stuck = QtWidgets.QLabel(self.central_widget)
        self.down_range_stuck = QtWidgets.QLabel(self.central_widget)
        self.accounts_list = QtWidgets.QListWidget(self.central_widget)
        self.set_max_price_btn = QtWidgets.QPushButton(self.central_widget)
        self.del_category_btn = QtWidgets.QPushButton(self.central_widget)
        self.add_category_btn = QtWidgets.QPushButton(self.central_widget)
        self.label_9 = QtWidgets.QLabel(self.central_widget)
        self.categories_list = QtWidgets.QListWidget(self.central_widget)
        self.del_brand_btn = QtWidgets.QPushButton(self.central_widget)
        self.add_brand_btn = QtWidgets.QPushButton(self.central_widget)
        self.del_size_btn = QtWidgets.QPushButton(self.central_widget)
        self.add_size_btn = QtWidgets.QPushButton(self.central_widget)
        self.brands_list = QtWidgets.QListWidget(self.central_widget)
        self.label_8 = QtWidgets.QLabel(self.central_widget)
        self.label_7 = QtWidgets.QLabel(self.central_widget)
        self.label_6 = QtWidgets.QLabel(self.central_widget)
        self.textEdit_3 = QtWidgets.QTextEdit(self.central_widget)
        self.checkBox = QtWidgets.QCheckBox(self.central_widget)
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.central_widget)
        self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.lcdNumber = QtWidgets.QLCDNumber(self.central_widget)
        self.progressBar = QtWidgets.QProgressBar(self.central_widget)
        self.progressBar_2 = QtWidgets.QProgressBar(self.central_widget)
        self.sizes_list = QtWidgets.QListWidget(self.central_widget)
        self.textEdit = QtWidgets.QTextEdit(self.central_widget)
        self.label_4 = QtWidgets.QLabel(self.central_widget)
        self.label_5 = QtWidgets.QLabel(self.central_widget)
        self.start_btn = QtWidgets.QPushButton(self.central_widget)
        self.stop_btn = QtWidgets.QPushButton(self.central_widget)
        self.menuMenu = QtWidgets.QMenu(self.menubar)

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
        self.actionReset_preferences.setObjectName("actionReset_preferences")
        self.actionInfo.setObjectName("actionInfo")
        self.actionSave.setObjectName("actionSave")
        self.actionOpen.setObjectName("actionOpen")

    def connect_buttons(self):
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
        self.actionReset_preferences.triggered.connect(self.reset_config)

    def setup_menu(self):
        """
        setup menu bar and options.
        :return:
        """

        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionReset_preferences)
        self.menuMenu.addAction(self.actionInfo)
        self.menuMenu.addAction(self.actionSave)
        self.menuMenu.addAction(self.actionOpen)
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
        self.connect_buttons()
        self.setup_obj_names()
        self.progressBar.setProperty("value", 0)
        self.progressBar_2.setProperty("value", 0)
        self.accounts_list.addItem(login + ' ' + password)
        MainWindow.setCentralWidget(self.central_widget)
        MainWindow.setStatusBar(self.statusbar)
        MainWindow.setMenuBar(self.menubar)
        self.setup_menu()
        self.translate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def translate_ui(self, MainWindow):
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
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.update_config_progress()
