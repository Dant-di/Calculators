import re
import pandas as pd
import xml.etree.ElementTree as ET
import json
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


        with open('resource/td.json') as td:
            self.td_db = json.load(td)

        self.td_list = list(self.td_db.keys())

        for option in self.td_list:
            self.technical_drawing.addItem(option)


        # self.technical_drawing.currentTextChanged.connect(self.display_net_area)
        self.technical_drawing.currentIndexChanged.connect(self.display_net_area)




    def display_net_area(self):
        area = self.td_db.get(self.technical_drawing.currentText())
        self.net_area.setText(str(area.get("Area")))


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
        self.error_label.setText("")
        if self.net_area.text() == "" and self.load_message.text() == "":
            message = "Select file first and indicate either TD or TD's net area!"
            self.error_label_display(message)
        elif self.net_area.text() == "":
            message = "Indicate either TD or TD's net area!"
            self.error_label_display(message)
        elif self.load_message.text() == "":
            message = 'Select file first!'
            self.error_label_display(message)
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
        self.error_label.setText("")

        message = "You need to calculate first before saving!"
        if self.net_area.text() == "" and self.load_message.text() == "":
            self.error_label_display(message)
        elif self.net_area.text() == "":
            self.error_label_display(message)
        elif self.load_message.text() == "":
            self.error_label_display(message)
        elif self.calculated_flag == False:
            self.error_label_display(message)
        else:
            home_dir = str(Path().absolute())
            fname = QFileDialog.getSaveFileName(self, "Save calculations", home_dir + '\\' + self.filename.split(".")[0] + '.xlsx', "Excel files (*.xlsx)")
            if fname:
                try:
                    self.df_fixed.to_excel(fname[0])
                except:
                    self.error_handler_inks("File hasn't been saved")


    def add_td(self, checked):
        if self.w is None:
            self.w = AddTd()
        self.w.show()


    #TODO add functionality to add TD in the TD database


    def error_label_display(self, message):
        self.error_label.setText(message)

    def error_handler_inks(self, message):
        dlg = ErrorWindow(self)
        dlg.error_label_inks.setText(message)

        dlg.exec()


class AddTd(QWidget):
    def __init__(self):
        super(AddTd, self).__init__()
        loadUi("gui/add_td.ui", self)
        # self.add_td_button.clicked.connect(lambda: self.close()) #TODO move into function to close window after saving data
        self.add_td_button.clicked.connect(self.add_td_data)
        self.area_input.editingFinished.connect(self.add_net_area_value)
        self.setWindowModality(QtCore.Qt.ApplicationModal)



    def add_net_area_value(self):
        net_area = float(self.area_input.text()) * 100
        self.net_area_input.setText(str(net_area))

    def add_td_data(self):

        self.mandatory_fields.setText("")
        with open('resource/td.json') as td:
            self.td_db = json.load(td)

        self.td_list = list(self.td_db.keys())

        mandatory_fields_list = [self.td_name_input.text(), self.height_input.text(), self.width_input.text(), self.area_input.text()]

        r = re.compile('TD-[A-Z][A-Z]+[0-9][0-9][0-9][0-9]+-+[0-9][0-9]')

        if self.td_name_input.text() in self.td_list:
            self.mandatory_fields.setText("TD name already exists")

        elif "" in mandatory_fields_list:
            self.mandatory_fields.setText("Mandatory fields cannot be blank")

        elif r.match(self.td_name_input.text()) is None:
            self.mandatory_fields.setText("Incorrect TD name format")
            print(self.td_name_input.text())

        else:
            pass





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










