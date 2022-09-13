import pandas as pd
import xml.etree.ElementTree as ET
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QFileDialog
from pathlib import Path

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):
        loadUi("gui/calculators.ui", self)

        self.w = None


        self.header = self.tableWidget.horizontalHeader()
        self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        self.exit_button.clicked.connect(exit)
        self.open_button.clicked.connect(self.open_file)




        self.calculate_button.clicked.connect(self.calculate)
        self.save_calc_button.clicked.connect(self.save_calculations)

        self.add_td_button.clicked.connect(self.add_td)



    def open_file(self):
        home_dir = str(Path().absolute())
        fname = QFileDialog.getOpenFileName(self, "Open Ink Coverage file", home_dir)
        self.load_message.setText(fname[0] + ' has been loaded')




    def calculate(self):
        pass


        # if self.net_area.text() == "" and self.load_message.text() == "":
        #     message = 'Select file first and indicate either TD or net coverage area'
        #     self.error_handler()
        # elif self.net_area.text() == "":
        #     message = 'Indicate either TD or net coverage area'
        #     self.error_handler()
        # elif self.load_message.text() == "":
        #     message = 'Select file first'
        #     self.error_handler()
        # else:
        #     pass



    def error_handler(self):
        err_message = ErrorHandler()
        err_message.exec()




    def save_calculations(self):
        pass

    def add_td(self, checked):

        if self.w is None:
            self.w = AddTd()
        self.w.show()




class AddTd(QWidget):
    def __init__(self):
        super(AddTd, self).__init__()
        loadUi("gui/add_td.ui", self)


class ErrorHandler(QDialog):
    def __init__(self):
        super(ErrorHandler, self).__init__()
        loadUi("gui/error.ui", self)

        self.ok_button.clicked.connect(lambda: self.close())
        # self.error_label.setText()



app = QApplication(sys.argv)
mainwindow = MainWindow()
mainwindow.setFixedWidth(1281)
mainwindow.setFixedHeight(961)

# widget = QtWidgets.QStackedWidget()
# widget.addWidget(mainwindow)
# widget.setFixedWidth(1281)
# widget.setFixedHeight(961)
mainwindow.show()

try:
    sys.exit(app.exec_())

except:
    print("exiting")










