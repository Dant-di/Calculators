import re
import pandas as pd
import openpyxl
import xml.etree.ElementTree as ET
import json
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QFileDialog, QHeaderView, QMainWindow
from PyQt5.QtCore import Qt, pyqtSignal
from pathlib import Path


# class for main window interface
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui/v2/main_window.ui", self)

        self.initUIinkCoverage()
        self.initUILayout()
        self.calculated_flag = False


    # Initialize and tweak ink coverage tab features
    def initUIinkCoverage(self):

        self.button_exit_inks.clicked.connect(exit)
        self.button_new_calc_inks.clicked.connect(self.new_calc_inks)
        self.button_view_calc_inks.clicked.connect(self.display_calc_inks)
        self.button_export_calc_inks.clicked.connect(self.export_calc_inks)
        self.label_error_inks.setText("")

    # Initialize and tweak layout tab features
    def initUILayout(self):
        self.button_exit_layout.clicked.connect(exit)
        self.button_new_calc_layout.clicked.connect(self.new_calc_layout)
        self.button_view_calc_layout.clicked.connect(self.display_calc_layout)
        self.button_export_calc_layout.clicked.connect(self.export_calc_layout)
        self.label_error_layout.setText("")

    def new_calc_inks(self):
        pass

    def display_calc_inks(self):
        pass

    def export_calc_inks(self):
        pass



    # # Initialize and tweak ink coverage tab features
    # def initUIinkCoverage(self):
    #
    #     self.exit_button_inks.clicked.connect(exit)
    #     self.open_button.clicked.connect(self.open_file_inks)
    #
    #     self.calculate_button_inks.clicked.connect(self.calculate_inks)
    #     self.save_calc_button_inks.clicked.connect(self.save_calculations_inks)
    #
    #     self.add_td_button.clicked.connect(self.add_td)
    #
    #     self.get_td_values(self.technical_drawing)
    #
    #     self.technical_drawing.currentIndexChanged.connect(self.display_net_area)

    # Initialize and tweak layout tab features



    def new_calc_layout(self):
        pass

    def display_calc_layout(self):
        pass

    def export_calc_layout(self):
        pass




    # Initialize and tweak layout tab features
    # def initUILayout(self):
    #
    #     self.exit_button_layout.clicked.connect(exit)
    #
    #     self.calculate_button_layout.clicked.connect(self.calculate_layout)
    #     self.save_calc_button_layout.clicked.connect(self.save_calculations_layout)
    #
    #     self.add_td_button_layout.clicked.connect(self.add_td)
    #
    #     self.get_td_values(self.technical_drawing_layout)
    #
    #     self.technical_drawing_layout.currentIndexChanged.connect(self.display_layout_data)

    # get TD values from JSON file
    def get_td_values(self, target_field):
        target_field.clear()
        target_field.addItem("")

        with open('resource/td.json', 'r') as td:
            self.td_db = json.load(td)

        self.td_list = list(self.td_db.keys())

        for key in self.td_list:
            target_field.addItem(key)

    # display net area for selected TD
    def display_net_area(self):
        area = self.td_db.get(self.technical_drawing.currentText())
        if area is None:
            self.net_area.setText("")
        else:
            self.net_area.setText(str(area.get("Area")))

    # display parameters of selected TD for layout tab
    def display_layout_data(self):
        current_td = self.td_db.get(self.technical_drawing_layout.currentText())
        if current_td is None:
            self.blank_width_input.setText("")
            self.blank_height_input.setText("")
            self.nesting_size_input.setText("")

        else:
            self.blank_width_input.setText(str(current_td.get("Width")))
            self.blank_height_input.setText(str(current_td.get("Height")))
            self.nesting_size_input.setText(str(current_td.get("Nesting")))

    # open file buttin inks covergae tab
    def open_file_inks(self):

        # clean up variables for error checking
        self.fname = None
        self.net_area.setText("")
        self.load_message.setText("")
        self.df_fixed = pd.DataFrame(columns=['Name', 'Value', 'Percentage '])
        self.model = TableModel(self.df_fixed)
        self.result_table_inks.setModel(self.model)

        # take the path
        home_dir = str(Path().absolute())
        self.fname = QFileDialog.getOpenFileName(self, "Open Ink Coverage file", home_dir)
        self.filename = self.fname[0].split("/")[-1]
        self.load_message.setText(self.filename + ' has been loaded')

    # calculates ink covergae basing on the xml file
    def calculate_inks(self):
        self.error_label.setText("")
        self.calculated_flag = False  # better than 7 lines of if's
        # perfoem checks for all requred inputs
        if self.net_area.text() == "" and self.load_message.text() == "":
            message = "Select file first and either select TD from the list or provide TD's net area!"
            self.error_label_display(message, self.error_label)
        elif self.net_area.text() == "":
            message = "Either select TD from the list or provide TD's net area!"
            self.error_label_display(message, self.error_label)
        elif self.load_message.text() == "":
            message = 'Select file first!'
            self.error_label_display(message, self.error_label)
        # do calculation if all fields are fiiled in
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

            self.model = TableModel(self.df_fixed)
            self.result_table_inks.setModel(self.model)
            self.result_table_inks.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.calculated_flag = True

    # save calculated ink coverage
    def save_calculations_inks(self):
        self.error_label.setText("")

        message = "You need to calculate first before saving!"

        if self.calculated_flag == False:

            # if self.net_area.text() == "" and self.load_message.text() == "":
            #     self.error_label_display(message, self.error_label)
            # elif self.net_area.text() == "":
            #     self.error_label_display(message, self.error_label)
            # elif self.load_message.text() == "":
            #     self.error_label_display(message, self.error_label)
            # elif self.calculated_flag == False:
            self.error_label_display(message, self.error_label)
        else:
            home_dir = str(Path().absolute())
            fname = QFileDialog.getSaveFileName(self, "Save calculations",
                                                home_dir + '\\' + self.filename.split(".")[0] + '.xlsx',
                                                "Excel files (*.xlsx)")
            if fname:
                try:
                    self.df_fixed.to_excel(fname[0])
                except:
                    self.error_handler_inks("File hasn't been saved")

    # function for button to add TD
    def add_td(self):

        add_td = AddTd()
        add_td.exec()

        # re get data from JSON
        self.get_td_values(self.technical_drawing)
        self.get_td_values(self.technical_drawing_layout)

    # calcuate layout
    def calculate_layout(self):
        self.error_label_layout.setText("")
        self.calculated_flag = False

        # define variables for calcualtion and re-define default data types
        b_width = float(self.blank_width_input.text())
        b_height = float(self.blank_height_input.text())
        if self.nesting_size_input.text() == 'None':
            self.nesting_size_input.setText('0')
        nest = float(self.nesting_size_input.text())
        l_waste = float(self.left_waste_input.text())
        r_waste = float(self.right_waste_input.text())
        b_waste = float(self.back_waste_input.text())
        f_waste = float(self.front_waste_input.text())
        inc_across = float(self.incuts_across_input.text())
        inc_around = float(self.incuts_around_input.text())
        ups_across = int(self.ups_across_input.text())
        ups_around = int(self.ups_around_input.text())

        # list with parameters
        params = [b_width, b_height, nest, l_waste, r_waste, b_waste, f_waste, inc_across, inc_around, ups_across,
                  ups_around]

        # check for missing input
        if any(i == "" for i in params):
            message = "Please fill in all the fields."
            self.error_label_display(message, self.error_label_layout)
        else:
            ups_amount = ups_across * ups_around
            nested = b_height - nest

            # Inline short grain
            if self.rb_layout_inline.isChecked() and self.rb_short_grain.isChecked():
                board_width = l_waste + r_waste + b_height + nested * (ups_across - 1) + (inc_across * (ups_across - 1))
                circumference = b_width * ups_around + f_waste + (inc_around * (ups_around - 1))
                net_length = circumference - f_waste

            # Inline long grain
            elif self.rb_layout_inline.isChecked():
                board_width = l_waste + r_waste + (b_width * ups_across) + (inc_across * (ups_across - 1))
                circumference = nested * ups_around + f_waste + (inc_around * (ups_around - 1))
                net_length = nested * ups_around + nest

            # Offline short grain
            elif self.rb_layout_offline.isChecked() and self.rb_short_grain.isChecked():
                board_width = l_waste + r_waste + b_height + nested * (ups_across - 1) + (inc_across * (ups_across - 1))
                circumference = b_width * ups_around + (inc_around * (ups_around - 1)) + f_waste + b_waste

                net_length = circumference - f_waste - b_waste

            # Offline long grain
            else:
                board_width = l_waste + r_waste + (b_width * ups_across) + (inc_across * (ups_across - 1))
                circumference = b_height + (nested * (ups_around - 1)) + (
                            inc_around * (ups_around - 1)) + f_waste + b_waste

                net_length = circumference - f_waste - b_waste

        net_width = board_width - r_waste - l_waste
        diameter = circumference / 3.14159

        # get rid of float zero part
        if board_width % 1 == 0:
            board_width = int(board_width)

        if diameter % 1 == 0:
            diameter = int(diameter)

        if circumference % 1 == 0:
            circumference = int(circumference)

        if net_width % 1 == 0:
            net_width = int(net_width)

        if net_length % 1 == 0:
            net_length = int(net_length)

        # dispaly calculation results in the window
        self.ups_output.setText(str(ups_amount))
        self.board_width_output.setText(str(round(board_width, 2)))
        self.cylinder_diam_output.setText(str(round(diameter, 2)))
        self.cylinder_circ_output.setText(str(round(circumference, 2)))
        self.net_width_output.setText(str(round(net_width, 2)))
        self.net_length_output.setText(str(round(net_length, 2)))

        # create dictionary with final data for further processing and export
        final_data = {
            self.blank_width_label.text(): b_width,
            self.blank_height_label.text(): b_height,
            self.nesting_size_label.text(): nest,
            self.left_waste_label.text(): l_waste,
            self.right_waste_label.text(): r_waste,
            self.back_waste_label.text(): b_waste,
            self.front_waste_label.text(): f_waste,
            self.incuts_across_label.text(): inc_across,
            self.incuts_around_label.text(): inc_around,
            self.ups_across_label.text(): ups_across,
            self.ups_around_label.text(): ups_around,
            self.ups_label.text(): self.ups_output.text(),
            self.board_width_label.text(): self.board_width_output.text(),
            self.cylinder_diam_label.text(): self.cylinder_diam_output.text(),
            self.cylinder_circ_label.text(): self.cylinder_circ_output.text(),
            self.net_width_label.text(): self.net_width_output.text(),
            self.net_length_label.text(): self.net_length_output.text()

        }

        col = [""]

        self.layout_df = pd.DataFrame.from_dict(final_data, orient='index', columns=col)

        self.calculated_flag = True

    # export calculation as excel file
    def save_calculations_layout(self):
        self.error_label_layout.setText("")
        message = "You need to calculate first before saving!"

        if self.calculated_flag == False:
            self.error_label_display(message, self.error_label)
        else:
            home_dir = str(Path().absolute())
            fname = QFileDialog.getSaveFileName(self, "Save calculations",
                                                home_dir + '\\' + 'Layout calculation.xlsx',
                                                "Excel files (*.xlsx)")
            if fname:
                try:
                    self.layout_df.to_excel(fname[0])
                except:
                    self.error_handler_inks("File hasn't been saved")

    # function to display error message in various error fileds
    def error_label_display(self, message, label):
        label.setText(message)

    # erorr message window
    def error_handler_inks(self, message):
        dlg = ErrorWindow(self)
        dlg.error_label_inks.setText(message)

        dlg.exec()






class Inks_Calculation(QDialog):
    def __init__(self):
        super(Inks_Calculation, self).__init__()
        loadUi("gui/v2/inks.ui", self)









# window with TD adding dialog
class AddTd(QDialog):
    # class AddTd(QWidget):
    def __init__(self):
        super(AddTd, self).__init__()
        loadUi("gui/add_td_v2.ui", self)

        self.add_td_button.clicked.connect(self.add_td_data)
        self.cancel_button.clicked.connect(self.cancelation)
        self.area_input.editingFinished.connect(self.add_net_area_value)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

    def add_net_area_value(self):
        net_area = float(self.area_input.text()) * 100
        self.net_area_input.setText(str(net_area))

    def add_td_data(self):

        self.mandatory_fields.setText("")
        with open('resource/td.json', 'r') as td:
            self.td_db = json.load(td)

        self.td_list = list(self.td_db.keys())

        mandatory_fields_list = [self.td_name_input.text(), self.height_input.text(), self.width_input.text(),
                                 self.area_input.text()]

        # predefine allowed format
        r = re.compile('TD-[A-Z][A-Z]+[0-9][0-9][0-9][0-9]+-+[0-9][0-9]')

        # chekc if TD already exists
        if self.td_name_input.text() in self.td_list:
            self.mandatory_fields.setText("TD name already exists")

        # check for empty fields
        # ToDo rewrite code so that missing fileds are indicated or illuminated
        elif "" in mandatory_fields_list:
            self.mandatory_fields.setText("Mandatory fields cannot be blank")

        # check if entered TD matches pattern
        elif r.match(self.td_name_input.text()) is None:
            self.mandatory_fields.setText("Incorrect TD name format. Please follow: 'TD-XX1234-56'")
            print(self.td_name_input.text())

        # creates dictionary with TD parameter and adds it to JSON file
        else:
            self.td_db[self.td_name_input.text()] = {"Description": self.description_input.text(),
                                                     "Lifecycle Phase": "", "Height": self.height_input.text(),
                                                     "Width": self.width_input.text(),
                                                     "Length 3D": self.length_3d_input.text(),
                                                     "Width 3D": self.width_3d_input.text(),
                                                     "Height 3D": self.height_3d_input.text(),
                                                     "Area [cm2]": self.area_input.text(),
                                                     "Cigarette Length Category": self.cig_length_cat_input.text(),
                                                     "Cigarette Length [mm]": self.cig_length_input.text(),
                                                     "Cigarettes per Item": self.cig_per_item_input.text(),
                                                     "Pack Type": self.pack_type_input.text(),
                                                     "Thickness Category": self.thick_cat_input.text(),
                                                     "Nesting": self.nesting_input.text(),
                                                     "Area": self.net_area_input.text()}
            with open('resource/td.json', 'w') as td_file_write:
                json.dump(self.td_db, td_file_write, sort_keys=True)

            self.close()

    def cancelation(self):
        dlg = ErrorWindow(self)
        dlg.error_label_inks.setText("TD entry was not saved")
        dlg.exec()
        self.close()


class ErrorWindow(QDialog):
    def __init__(self, parent=None):
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

