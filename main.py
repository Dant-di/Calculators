import pandas as pd
import xml.etree.ElementTree as ET
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTabWidget

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui/calculators.ui", self)
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
        pass


    def calculate(self):
        pass

    def save_calculations(self):
        pass

    def add_td(self):
        adding = AddTd()
        widget.addWidget(adding)
        widget.setCurrentIndex(widget.currentIndex()+1)




class AddTd(QTabWidget):
    def __init__(self):
        super(AddTd, self).__init__()
        loadUi("gui/add_td.ui", self)



app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1281)
widget.setFixedHeight(961)
widget.show()

try:
    sys.exit(app.exec_())

except:
    print("exiting")










