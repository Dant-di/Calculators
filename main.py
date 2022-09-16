import pandas as pd
import xml.etree.ElementTree as ET
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QFileDialog
from pathlib import Path

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUIinkCoverage()

    def initUIinkCoverage(self):
        loadUi("gui/calculators.ui", self)

        self.w = None


        self.header = self.tableWidget.horizontalHeader()
        self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        self.exit_button.clicked.connect(exit)
        self.open_button.clicked.connect(self.open_file_inks)


        self.calculate_button_inks.clicked.connect(self.calculate_inks)
        self.save_calc_button_inks.clicked.connect(self.save_calculations_inks)

        self.add_td_button.clicked.connect(self.add_td)




    def open_file_inks(self):
    #TODO reset key varaibles for error checking

        home_dir = str(Path().absolute())
        self.fname = QFileDialog.getOpenFileName(self, "Open Ink Coverage file", home_dir)
        self.filename = self.fname[0].split("/")[-1]
        self.load_message.setText(self.filename + ' has been loaded')


    def calculate_inks(self):
        if self.net_area.text() == "" and self.load_message.text() == "":
            message = "Select file first and indicate either TD or TD's net area!"
            self.error_handler_inks(message)
        elif self.net_area.text() == "":
            message = "Indicate either TD or TD's net area!"
            self.error_handler_inks(message)
        elif self.load_message.text() == "":
            message = 'Select file first!'
            self.error_handler_inks(message)
        else:
            df1 = pd.read_xml(self.fname[0], xpath='Inks/Ink',
                              attrs_only=True, parser='etree')
            df2 = pd.read_xml(self.fname[0], xpath='Inks/Ink/Coverage',
                              attrs_only=True, parser='etree')
            df = pd.concat([df1, df2.drop(columns=['Unit'])], axis=1).astype({'Value': float}, errors="raise")
            df['Percentage'] = df['Value'] / float(self.net_area.text())
            self.df_fixed = df.set_axis([x + 1 for x in range(len(df))], axis=0)
            self.df_styled = self.df_fixed.style.format({'Value': "{:.2f}", 'Percentage': "{:.2f}%"})
            print(self.df_styled.data)
        #TODO solve formatting isssue with data from df
        #TODO implement showing the table in the main wndow after calculation


    def save_calculations_inks(self, message):
    #ToDO add erroro catcher and add save dialog
        self.df_styled.to_excel(self.filename.split(".")[0] + '.xlsx')


    def add_td(self, checked):
        if self.w is None:
            self.w = AddTd()
        self.w.show()


    def error_handler_inks(self, message):
        dlg = ErrorWindow(self)
        dlg.error_label_inks.setText(message)

        dlg.exec()




class AddTd(QWidget):
    def __init__(self):
        super(AddTd, self).__init__()
        loadUi("gui/add_td.ui", self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

class ErrorWindow(QDialog):
    def __init__(self, parent = None):
        super(ErrorWindow, self).__init__(parent)
        loadUi("gui/error.ui", self)
        self.ok_button.clicked.connect(lambda: self.close())
        self.setWindowModality(QtCore.Qt.ApplicationModal)






app = QApplication(sys.argv)
mainwindow = MainWindow()
mainwindow.setFixedWidth(1280)
mainwindow.setFixedHeight(960)


mainwindow.show()

try:
    sys.exit(app.exec_())

except:
    print("exiting")










