# -*- coding: utf-8 -*-
import threading

from PyQt5 import QtCore, QtGui, QtWidgets

from rvsearch.main import MainThread


class UiMainWindow(threading.Thread):
    def __init__(self, qtlog=[]):
        threading.Thread.__init__(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.csvpath_input.setPlaceholderText(_translate("MainWindow", "File"))
        self.csvpath.setText(_translate("MainWindow", "Input file"))
        self.path_open.setText(_translate("MainWindow", "Open"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.stop_button.setText(_translate("MainWindow", "Stop"))
        self.label.setText(_translate("MainWindow", "Output:"))
        self.csvpath_2.setText(_translate("MainWindow", "Save as"))
        self.csvpath_output.setPlaceholderText(_translate("MainWindow", "File"))
        self.menu.setTitle(_translate("MainWindow", "Menu"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(682, 665)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.csvpath_input = QtWidgets.QLineEdit(self.centralwidget)
        self.csvpath_input.setGeometry(QtCore.QRect(130, 40, 441, 21))
        self.csvpath_input.setText("")
        self.csvpath_input.setObjectName("csvpath_edit")
        self.csvpath = QtWidgets.QLabel(self.centralwidget)
        self.csvpath.setGeometry(QtCore.QRect(70, 40, 71, 20))
        self.csvpath.setObjectName("csvpath")
        self.path_open = QtWidgets.QToolButton(self.centralwidget)
        self.path_open.setGeometry(QtCore.QRect(570, 40, 41, 22))
        self.path_open.setObjectName("path_open")
        self.log = QtWidgets.QTextBrowser(self.centralwidget)
        self.log.setGeometry(QtCore.QRect(20, 210, 641, 211))
        self.log.setObjectName("log")
        self.output = QtWidgets.QTextBrowser(self.centralwidget)
        self.output.setGeometry(QtCore.QRect(70, 450, 591, 171))
        self.output.setObjectName("output")
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(240, 180, 80, 23))
        self.start_button.setObjectName("start_button")
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setGeometry(QtCore.QRect(340, 180, 80, 23))
        self.stop_button.setObjectName("stop_button")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 520, 57, 15))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.csvpath_2 = QtWidgets.QLabel(self.centralwidget)
        self.csvpath_2.setGeometry(QtCore.QRect(80, 70, 71, 20))
        self.csvpath_2.setObjectName("csvpath_2")
        self.csvpath_output = QtWidgets.QLineEdit(self.centralwidget)
        self.csvpath_output.setGeometry(QtCore.QRect(130, 70, 441, 21))
        self.csvpath_output.setText("")
        self.csvpath_output.setObjectName("csvpath_edit_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 682, 20))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menu.addAction(self.actionOpen)
        self.menu.addAction(self.actionAbout)
        self.menu.addSeparator()
        self.menu.addAction(self.actionExit)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.path_open.clicked.connect(self.file_opener)
        self.actionExit.triggered.connect(self.exit_program)
        self.actionOpen.triggered.connect(self.file_opener)
        self.start_button.clicked.connect(self.start_main)
        self.stop_button.clicked.connect(self.stop_button.animateClick)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def start_main(self):
        main = MainThread(self.log)
        input = self.csvpath_input.text()
        output = self.csvpath_output.text()
        main.main(input, output)

    def file_opener(self):
        _translate = QtCore.QCoreApplication.translate
        name, _ = QtWidgets.QFileDialog.getOpenFileName()
        if name:
            self.csvpath_input.setText(_translate("MainWindow", name))
        return None

    @staticmethod
    def exit_program():
        exit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
