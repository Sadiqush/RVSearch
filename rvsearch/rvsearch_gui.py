# -*- coding: utf-8 -*-
import os
import signal
import time
from multiprocessing.pool import ThreadPool

from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd   # Don't remove this

from rvsearch.logger import Logger as logger


class pandasModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        QtCore.QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None


class UiMainWindow:
    def __init__(self):
        self.tp = ThreadPool(processes=2)

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
        self.csvpath_input.setObjectName("csvpath_input")
        self.csvpath = QtWidgets.QLabel(self.centralwidget)
        self.csvpath.setGeometry(QtCore.QRect(70, 40, 71, 20))
        self.csvpath.setObjectName("csvpath")
        self.path_open = QtWidgets.QToolButton(self.centralwidget)
        self.path_open.setGeometry(QtCore.QRect(570, 40, 41, 22))
        self.path_open.setObjectName("path_open")
        self.log = QtWidgets.QTextBrowser(self.centralwidget)
        self.log.setGeometry(QtCore.QRect(20, 160, 641, 141))
        self.log.setObjectName("log")
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(250, 130, 80, 23))
        self.start_button.setObjectName("start_button")
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setGeometry(QtCore.QRect(350, 130, 80, 23))
        self.stop_button.setObjectName("stop_button")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 310, 57, 15))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.csvpath_2 = QtWidgets.QLabel(self.centralwidget)
        self.csvpath_2.setGeometry(QtCore.QRect(80, 70, 51, 20))
        self.csvpath_2.setObjectName("csvpath_2")
        self.csvpath_output = QtWidgets.QLineEdit(self.centralwidget)
        self.csvpath_output.setGeometry(QtCore.QRect(130, 70, 441, 21))
        self.csvpath_output.setText("")
        self.csvpath_output.setObjectName("csvpath_output")
        self.output = QtWidgets.QTableView(self.centralwidget)
        self.output.setGeometry(QtCore.QRect(20, 331, 641, 291))
        self.output.setObjectName("output")
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

        # ==============================================================================
        # Importnant parts
        self.retranslateUi(MainWindow)
        self.path_open.clicked.connect(self.file_opener)  # Open button
        self.actionOpen.triggered.connect(self.file_opener)  # Open in menu
        self.actionExit.triggered.connect(self.exit_program)  # Exit in menu
        self.start_button.clicked.connect(self.thread_start)  # Start button
        self.stop_button.clicked.connect(self.thread_stop)  # Stop button
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.start_button.setEnabled(False)

    def thread_stop(self):
        logger.do_log('Terminating...')
        logger.terminate.value = True
        logger.do_log(f'from my pov ter is: {logger.terminate}')
        return None

    def print_out(self, results):
        if results.any():
            model = pandasModel(results)
            self.output.setModel(model)
        logger.terminate.value = True
        return None

    def thread_start(self):
        logger.terminate.value = False
        time.sleep(0.1)
        t1 = self.tp.apply_async(self.start_log)
        t2 = self.tp.apply_async(self.start, callback=self.print_out)
        return None

    def start(self):
        logger.do_log('Processing...')
        from rvsearch.main import CoreProcess
        in_path = self.csvpath_input.text()  # Path for csv input
        out_path = self.csvpath_output.text()  # Path for csv output
        results = CoreProcess().main([in_path], out_path)
        return results

    def on_csv_input_edit(self, txt):
        self.start_button.setEnabled(bool(txt))

    def start_log(self):
        while not logger.terminate.value:
            if logger.log:
                self.log.append(logger.log)
                logger.log = ''
            time.sleep(0.1)
        time.sleep(0.5)
        self.log.append(logger.log)
        logger.log = ''

    def file_opener(self):
        _translate = QtCore.QCoreApplication.translate
        name, _ = QtWidgets.QFileDialog.getOpenFileName(filter="CSV files (*.csv)")
        if name:
            self.csvpath_input.setText(_translate("MainWindow", name))
            self.log.append(f'File {name} is going to load')
            self.start_button.setEnabled(True)
        return None

    @staticmethod
    def exit_program():
        os.kill(os.getpid(), signal.SIGUSR1)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
