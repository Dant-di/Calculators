import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QFileDialog, QHeaderView
from PyQt5.QtCore import Qt
from pathlib import Path



# class for main window interface
class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUIinkCoverage()


# Initialize and tweak ink coverage tab features
    def initUIinkCoverage(self):
        loadUi("gui/calculators.ui", self)

        self.w = None

        self.exit_button.clicked.connect(exit)
        self.open_button.clicked.connect(self.open_file_inks)

        self.calculate_button_inks.clicked.connect(self.calculate_inks)
        self.save_calc_button_inks.clicked.connect(self.save_calculations_inks)

        self.add_td_button.clicked.connect(self.add_td)


        self.technical_drawing.currentTextChanged.connect(self.display_net_area)
        # TODO elaborate on change value in the field basing on selected TD



    def display_net_area(self):
        self.net_area.setText(self.technical_drawing.currentText())


    def open_file_inks(self):

        #clean up variables for error checking
        self.fname = None
        self.net_area.setText("")
        self.load_message.setText("")
        self.df_fixed = pd.DataFrame(columns=['Name', 'Value', 'Percentage '])
        self.model = TableModel(self.df_fixed)
        self.result_table_inks.setModel(self.model)
        self.calculated_flag = False


        # take the path
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
            df['Value'] = df['Value'].map('{:.2f}'.format)
            df['Percentage'] = df['Percentage'].map('{:.2f}%'.format)

            self.df_fixed = df.set_axis([x + 1 for x in range(len(df))], axis=0)

            print(self.df_fixed)

            self.model = TableModel(self.df_fixed)
            self.result_table_inks.setModel(self.model)
            self.result_table_inks.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.calculated_flag = True
            print(self.result_table_inks)



    def save_calculations_inks(self):

        message = "You need to calculate first before saving!"
        if self.net_area.text() == "" and self.load_message.text() == "":
            self.error_handler_inks(message)
        elif self.net_area.text() == "":
            self.error_handler_inks(message)
        elif self.load_message.text() == "":
            self.error_handler_inks(message)
        elif self.calculated_flag == False:
            self.error_handler_inks(message)
        else:
            home_dir = str(Path().absolute())
            fname = QFileDialog.getSaveFileName(self, "Save calculations", home_dir + '\\' + self.filename.split(".")[0] + '.xlsx', "Excel files (*.xlsx)")
            if fname:
                self.df_fixed.to_excel(fname[0])


    def add_td(self, checked):
        if self.w is None:
            self.w = AddTd()
        self.w.show()
    #TODO add functionality to add TD in the TD database


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



class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):

        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)



    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])




app = QApplication(sys.argv)
mainwindow = MainWindow()
mainwindow.setFixedWidth(1280)
mainwindow.setFixedHeight(960)


mainwindow.show()

try:
    sys.exit(app.exec_())

except:
    print("exiting")










