import pandas as pd
from qtpy.QtWidgets import QMainWindow, QSpinBox, QFileDialog, QMenu
from qtpy.QtWidgets import QTableWidgetItem, QComboBox
from qtpy import QtCore, QtGui
from IPython.core.display import display
from IPython.core.display import HTML
import os
import numpy as np
import re
import json
from collections import OrderedDict

from __code._utilities.string import format_html_message
from __code import load_ui
from __code._utilities.status_message import StatusMessageStatus, show_status_message
from __code.group_images_by_cycle_for_grating_experiment.excel_table_handler import ExcelTableHandler as TableHandler
from __code.group_images_by_cycle_for_grating_experiment import list_fit_procedure

ROW_HEIGHT = 40


class ExcelHandler:

    def __init__(self, parent=None):
        self.parent = parent

    def load_excel(self, excel_file=None):
        if excel_file is None:
            return

        self.parent.excel_info_widget.value = f"<b>Loaded excel file</b>: {excel_file}!"

        df = pd.read_excel(excel_file, sheet_name="Tabelle1", header=0)

        # first_last_run_of_each_group_dictionary = Interface.add_output_folder_to_dictionary(
        #         self.parent.first_last_run_of_each_group_dictionary, output_folder=self.parent.output_folder)
        # self.parent.first_last_run_of_each_group_dictionary = first_last_run_of_each_group_dictionary

        nbr_excel_row = len(df)
        nbr_notebook_row = len(self.parent.first_last_run_of_each_group_dictionary.keys())

        if nbr_excel_row != nbr_notebook_row:
            display(HTML("<font color='red'>Number of rows in Excel document selected and number of group <b>DO NOT "
                         "MATCH!</b></font>"))
            display(HTML("<font color='blue'><b>SOLUTION</b>: create a new Excel document!</font>"))

        else:
            data_type_to_populate_with_notebook_data = self.parent.sample_or_ob_radio_buttons.value
            new_df = self._populate_pandas_object(
                    df=df,
                    data_type_to_populate_with_notebook_data=data_type_to_populate_with_notebook_data)

            o_interface = Interface(grand_parent=self.parent,
                                    excel_file=excel_file,
                                    pandas_object=new_df,
                                    data_type_to_populate_with_notebook_data=data_type_to_populate_with_notebook_data,
                                    first_last_run_of_each_group_dictionary=self.parent.first_last_run_of_each_group_dictionary)
            o_interface.show()

    def get_excel_config(self):
        config_file = os.path.join(os.path.dirname(__file__), 'excel_config.json')
        with open(config_file) as json_file:
            return json.load(json_file)

    def _populate_pandas_object(self, df=None, data_type_to_populate_with_notebook_data='sample'):
        output_folder = os.path.abspath(self.parent.output_folder)
        first_last_run_of_each_group_dictionary = self.parent.first_last_run_of_each_group_dictionary
        if data_type_to_populate_with_notebook_data == 'sample':

            for _row_index, _key in enumerate(first_last_run_of_each_group_dictionary.keys()):
                df.iloc[_row_index, 0] = os.path.join(output_folder, first_last_run_of_each_group_dictionary[_key][
                                                          'first'])
                df.iloc[_row_index, 1] = os.path.join(output_folder, first_last_run_of_each_group_dictionary[_key][
                    'last'])

        else:  # ob

            for _row_index, _key in enumerate(first_last_run_of_each_group_dictionary.keys()):
                df.iloc[_row_index, 2] = os.path.join(output_folder, first_last_run_of_each_group_dictionary[_key][
                                                          'first'])
                df.iloc[_row_index, 3] = os.path.join(output_folder, first_last_run_of_each_group_dictionary[_key][
                    'last'])

        return df

    def _create_pandas_object(self, data_type_to_populate_with_notebook_data='sample'):

        # self.parent.output_folder = "/Volumes/G-DRIVE/IPTS/IPTS-28730-gratting-CT"  # REMOVE_ME

        output_folder = os.path.abspath(self.parent.output_folder)
        first_last_run_of_each_group_dictionary = self.parent.first_last_run_of_each_group_dictionary
        excel_config = self.get_excel_config()

        df_dict = OrderedDict()
        if data_type_to_populate_with_notebook_data == 'sample':

            for _row_index, _key in enumerate(first_last_run_of_each_group_dictionary.keys()):

                if _row_index == 0:
                    df_dict["first_data_file"] = [os.path.join(output_folder, first_last_run_of_each_group_dictionary[
                                                                   _key]['first'])]
                    df_dict["last_data_file"] = [os.path.join(output_folder, first_last_run_of_each_group_dictionary[
                                                                  _key]['last'])]
                else:
                    df_dict["first_data_file"].append(os.path.join(output_folder,
                                                                   first_last_run_of_each_group_dictionary[_key][
                                                                       'first']))
                    df_dict["last_data_file"].append(os.path.join(output_folder,
                                                                  first_last_run_of_each_group_dictionary[_key][
                                                                      'last']))

            nbr_row = len(first_last_run_of_each_group_dictionary.keys())
            df_dict["first_ob_file"] = ["None" for _ in np.arange(nbr_row)]
            df_dict["last_ob_file"] = ["None" for _ in np.arange(nbr_row)]

        else:  # ob

            for _row_index, _key in enumerate(first_last_run_of_each_group_dictionary.keys()):

                nbr_row = len(first_last_run_of_each_group_dictionary.keys())
                df_dict["first_sample_file"] = ["None" for _ in np.arange(nbr_row)]
                df_dict["last_sample_file"] = ["None" for _ in np.arange(nbr_row)]

                if _row_index == 0:
                    df_dict["first_ob_file"] = [os.path.join(output_folder, first_last_run_of_each_group_dictionary[
                        _key]['first'])]
                    df_dict["last_ob_file"] = [os.path.join(output_folder, first_last_run_of_each_group_dictionary[
                        _key]['last'])]
                else:
                    df_dict["first_ob_file"].append(os.path.join(output_folder, first_last_run_of_each_group_dictionary[
                                                                     _key]['first']))
                    df_dict["last_ob_file"].append(os.path.join(output_folder, first_last_run_of_each_group_dictionary[
                                                                    _key]['last']))

        df_dict["first_dc_file"] = ["None" for _ in np.arange(nbr_row)]
        df_dict["last_dc_file"] = ["None" for _ in np.arange(nbr_row)]

        list_key = list(excel_config.keys())
        list_key.remove("first_data_file")
        list_key.remove("last_data_file")
        list_key.remove("first_ob_file")
        list_key.remove("last_ob_file")
        for _key in list_key:
            df_dict[_key] = [excel_config[_key] for _ in np.arange(nbr_row)]

        df = pd.DataFrame(data=df_dict)
        return df

    def new_excel(self):
        self.parent.excel_info_widget.value = f"<b>Working with new excel file!"
        data_type_to_populate_with_notebook_data = self.parent.sample_or_ob_radio_buttons.value

        pandas_object = self._create_pandas_object(data_type_to_populate_with_notebook_data=data_type_to_populate_with_notebook_data)

        o_interface = Interface(grand_parent=self.parent,
                                pandas_object=pandas_object,
                                data_type_to_populate_with_notebook_data=data_type_to_populate_with_notebook_data,
                                first_last_run_of_each_group_dictionary=self.parent.first_last_run_of_each_group_dictionary)
        o_interface.show()


class Interface(QMainWindow):
    pandas_object = None  # pandas excel object
    excel_config = None

    def __init__(self, parent=None, grand_parent=None, excel_file=None,
                 first_last_run_of_each_group_dictionary=None,
                 data_type_to_populate_with_notebook_data='sample',
                 pandas_object=None):

        display(format_html_message(pre_message="Check UI that popped up \
                    (maybe hidden behind this browser!)",
                                    spacer=""))
        self.grand_parent = grand_parent
        self.data_type_to_populate_with_notebook_data = data_type_to_populate_with_notebook_data
        self.output_folder = self.grand_parent.output_folder

        self.pandas_object = pandas_object
        super(Interface, self).__init__(parent)
        ui_full_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                    os.path.join('ui',
                                                 'ui_grating_excel_editor.ui'))
        self.ui = load_ui(ui_full_path, baseinstance=self)
        self.setWindowTitle("Excel Editor")
        self.excel_file = excel_file

        # dictionary giving first and last run for each group (row)
        # add output folder to dictionary

        self.init_statusbar_message()

        self.load_config()
        self.set_columns_width()

        self.fill_table()
        self.check_table_content_pushed()

    @staticmethod
    def add_output_folder_to_dictionary(first_last_run_of_each_group_dictionary=None, output_folder=None):
        for _key in first_last_run_of_each_group_dictionary.keys():
            first_last_run_of_each_group_dictionary[_key]['first'] = os.path.join(output_folder,
                                                                                  first_last_run_of_each_group_dictionary[_key]['first'])
            first_last_run_of_each_group_dictionary[_key]['last'] = os.path.join(output_folder,
                                                                                  first_last_run_of_each_group_dictionary[
                                                                                      _key]['last'])
        return first_last_run_of_each_group_dictionary

    def check_table_content_pushed(self):
        """this is where we will check to make sure the format of all the cells is right and they are
        no missing fields"""
        o_table = TableHandler(table_ui=self.ui.tableWidget)
        nbr_rows = o_table.row_count()

        color_error = QtGui.QColor(255, 0, 0)
        color_ok = QtGui.QColor(255, 255, 255)

        self.at_least_one_error_found = False

        def is_string_a_float(string):
            try:
                float(string)
                return True
            except ValueError:
                return False

        def is_string_an_integer(string):
            try:
                int(string)
                return True
            except ValueError:
                return False

        def set_color_for_float_field(string, row, column):
            if is_string_a_float(string):
                color = color_ok
            else:
                color = color_error
                self.at_least_one_error_found = True
            o_table.set_background_color(row, column, color)

        def set_color_for_int_field(string, row, column):
            if is_string_an_integer(string):
                color = color_ok
            else:
                color = color_error
                self.at_least_one_error_found = True
            o_table.set_background_color(row, column, color)

        def is_string_undefined_or_empty(string):
            if string.lower() in ["none", "nan", ""]:
                return True
            return False

        def set_color_for_that_mandatory_field(string, row, column):
            if is_string_undefined_or_empty(string):
                color = color_error
                self.at_least_one_error_found = True
            else:
                color = color_ok
            o_table.set_background_color(row, column, color)

        def is_roi_correct_format(roi):
            """check if roi has the format [##,##,##,##] where ## are integers"""
            roi = roi.strip()
            result = re.search("\[\s*(\d*)\s*,\s*(\d*)\s*,\s*(\d*)\s*,\s*(\d*)\s*\]", roi)
            if len(result.groups()) != 4:
                return False
            try:
                int(result.groups()[0])
                int(result.groups()[1])
                int(result.groups()[2])
                int(result.groups()[3])
            except ValueError:
                return False
            return True

        def set_color_for_roi(roi, row, column):
            if is_roi_correct_format(roi):
                color = color_ok
            else:
                color = color_error
                self.at_least_one_error_found = True
            o_table.set_background_color(row, column, color)

        for _row in np.arange(nbr_rows):
            o_table.define_row_for_getter(row=_row)

            first_data_file = o_table.get_first_data_file()
            set_color_for_that_mandatory_field(first_data_file, _row, 0)

            last_data_file = o_table.get_last_data_file()
            set_color_for_that_mandatory_field(last_data_file, _row, 1)

            first_ob_file = o_table.get_first_ob_file()
            set_color_for_that_mandatory_field(first_ob_file, _row, 2)

            last_ob_file = o_table.get_last_ob_file()
            set_color_for_that_mandatory_field(last_ob_file, _row, 3)

            first_dc_file = o_table.get_first_dc_file()
            set_color_for_that_mandatory_field(first_dc_file, _row, 4)

            last_dc_file = o_table.get_last_dc_file()
            set_color_for_that_mandatory_field(last_dc_file, _row, 5)

            rotation = o_table.get_rotation()
            set_color_for_int_field(rotation, _row, 8)

            roi = o_table.get_roi()
            set_color_for_roi(roi, _row, 10)

            data_threshold_3x3 = o_table.get_data_threshold_3x3()
            set_color_for_int_field(data_threshold_3x3, _row, 12)

            data_threshold_5x5 = o_table.get_data_threshold_5x5()
            set_color_for_int_field(data_threshold_5x5, _row, 13)

            data_threshold_7x7 = o_table.get_data_threshold_7x7()
            set_color_for_int_field(data_threshold_7x7, _row, 14)

            data_sigma_log = o_table.get_data_sigma_log()
            set_color_for_float_field(data_sigma_log, _row, 15)

            dc_threshold_3x3 = o_table.get_dc_threshold_3x3()
            set_color_for_int_field(dc_threshold_3x3, _row, 17)

            dc_threshold_5x5 = o_table.get_dc_threshold_5x5()
            set_color_for_int_field(dc_threshold_5x5, _row, 18)

            dc_threshold_7x7 = o_table.get_dc_threshold_7x7()
            set_color_for_int_field(dc_threshold_7x7, _row, 19)

            dc_sigma_log = o_table.get_dc_log()
            set_color_for_float_field(dc_sigma_log, _row, 20)

            dc_outlier_value = o_table.get_dc_outlier_value()
            set_color_for_float_field(dc_outlier_value, _row, 22)

            result_directory = o_table.get_result_directory()
            set_color_for_that_mandatory_field(result_directory, _row, 23)

            file_id = o_table.get_file_id()
            set_color_for_that_mandatory_field(file_id, _row, 24)

        if self.at_least_one_error_found:
            show_status_message(parent=self,
                                message=f"At least one issue found in table! Angel will not be able to execute this "
                                        f"excel!",
                                status=StatusMessageStatus.error,
                                duration_s=15)

    def load_config(self):
        config_file = os.path.join(os.path.dirname(__file__), 'excel_config.json')
        with open(config_file) as json_file:
            self.excel_config = json.load(json_file)

    def set_columns_width(self):
        columns_width = [int(value) for value in np.ones(28) * 100]

        list_very_wide_columns = [0, 1, 2, 3, 4, 5, 23]
        for index in list_very_wide_columns:
            columns_width[index] = 500

        list_wide_columns = [10, 24]
        for index in list_wide_columns:
            columns_width[index] = 150

        self.columns_width = columns_width

    def init_statusbar_message(self):
        if self.excel_file:
            show_status_message(parent=self,
                                message=f"Loaded excel file {self.excel_file}!",
                                status=StatusMessageStatus.ready,
                                duration_s=10)
        else:
            show_status_message(parent=self,
                                message="Created a new Excel file!",
                                status=StatusMessageStatus.ready,
                                duration_s=10)

    def fill_table(self):
        pandas_object = self.pandas_object
        if pandas_object is None:
            return

        list_columns = pandas_object.columns
        o_table = TableHandler(table_ui=self.ui.tableWidget)

        nbr_columns = len(list_columns)
        for _col_index in np.arange(nbr_columns):
            o_table.insert_column(_col_index)
        o_table.set_column_names(list_columns)

        pandas_entry_for_first_row = pandas_object.iloc[0]

        nbr_rows = len(pandas_object)
        for _row in np.arange(nbr_rows):
            o_table.insert_empty_row(_row)

            pandas_entry_for_this_row = pandas_object.iloc[_row]
            o_table.define_row_for_setter(_row)

            o_table.set_first_data_file(pandas_entry_for_this_row[0])
            o_table.set_last_data_file(pandas_entry_for_this_row[1])
            o_table.set_first_ob_file(pandas_entry_for_this_row[2])
            o_table.set_last_ob_file(pandas_entry_for_this_row[3])
            o_table.set_first_dc_file(pandas_entry_for_this_row[4])
            o_table.set_last_dc_file(pandas_entry_for_this_row[5])
            o_table.set_period(pandas_entry_for_this_row[6])
            o_table.set_images_per_step(pandas_entry_for_this_row[7])
            o_table.set_rotation(pandas_entry_for_this_row[8])
            o_table.set_fit_procedure(pandas_entry_for_this_row[9])
            o_table.set_roi(pandas_entry_for_this_row[10])
            o_table.set_gamma_filter_data_ob(pandas_entry_for_this_row[11])
            o_table.set_data_threshold_3x3(pandas_entry_for_this_row[12])
            o_table.set_data_threshold_5x5(pandas_entry_for_this_row[13])
            o_table.set_data_threshold_7x7(pandas_entry_for_this_row[14])
            o_table.set_data_sigma_log(pandas_entry_for_this_row[15])
            o_table.set_gamma_filter_dc(pandas_entry_for_this_row[16])
            o_table.set_dc_threshold_3x3(pandas_entry_for_this_row[17])
            o_table.set_dc_threshold_5x5(pandas_entry_for_this_row[18])
            o_table.set_dc_threshold_7x7(pandas_entry_for_this_row[19])
            o_table.set_dc_log(pandas_entry_for_this_row[20])
            o_table.set_dc_outlier_removal(pandas_entry_for_this_row[21])
            o_table.set_dc_outlier_value(pandas_entry_for_this_row[22])
            o_table.set_result_directory(pandas_entry_for_this_row[23])
            o_table.set_file_id(pandas_entry_for_this_row[24])

        row_height = [int(value) for value in np.ones(nbr_rows) * ROW_HEIGHT]
        o_table.set_row_height(row_height=row_height)

        o_table.set_column_width(column_width=self.columns_width)

    def cancel_button_pushed(self):
        self.close()

    def save_as_button_pushed(self):
        working_dir = self.grand_parent.working_dir
        folder_selected = self.grand_parent.folder_selected
        base_folder_name = os.path.basename(folder_selected)
        default_file_name = os.path.join(working_dir, base_folder_name + "_angel_excel.xls")
        file_and_extension_name = QFileDialog.getSaveFileName(self,
                                                              "Select or define file name",
                                                              default_file_name,
                                                              "Excel (*.xls)")

        file_name = file_and_extension_name[0]
        if file_name:
            table_dict = self.collect_table_dict()

        df = pd.DataFrame(table_dict)
        writer = pd.ExcelWriter(file_name,
                                engine='xlsxwriter')
        df.to_excel(writer, sheet_name="Tabelle1",
                            index=False)
        writer.save()

    def collect_table_dict(self):
        o_table = TableHandler(table_ui=self.ui.tableWidget)
        nbr_rows = o_table.row_count()

        first_data_file = []
        last_data_file = []
        first_ob_file = []
        last_ob_file = []
        first_dc_file = []
        last_dc_file = []
        period = []
        images_per_step = []
        rotation = []
        fit_procedure = []
        roi = []
        gamma_filter_data_ob = []
        data_threshold_3x3 = []
        data_threshold_5x5 = []
        data_threshold_7x7 = []
        data_sigma_log = []
        gamma_filter_dc = []
        dc_threshold_3x3 = []
        dc_threshold_5x5 = []
        dc_threshold_7x7 = []
        dc_sigma_log = []
        dc_outlier_removal = []
        dc_outlier_value = []
        result_directory = []
        file_id = []
        sample_information = []
        used_environment = []
        osc_pixel = []

        for _row in np.arange(nbr_rows):

            o_table.define_row_for_getter(row=_row)

            first_data_file.append(o_table.get_first_data_file())
            last_data_file.append(o_table.get_last_data_file())
            first_ob_file.append(o_table.get_first_ob_file())
            last_ob_file.append(o_table.get_last_ob_file())
            first_dc_file.append(o_table.get_first_dc_file())
            last_dc_file.append(o_table.get_last_dc_file())
            period.append(o_table.get_period())
            images_per_step.append(o_table.get_images_per_step())
            rotation.append(o_table.get_rotation())
            fit_procedure.append(o_table.get_fit_procedure())
            roi.append(o_table.get_roi())
            gamma_filter_data_ob.append(o_table.get_gamma_filter_data_ob())
            data_threshold_3x3.append(o_table.get_data_threshold_3x3())
            data_threshold_5x5.append(o_table.get_data_threshold_5x5())
            data_threshold_7x7.append(o_table.get_data_threshold_7x7())
            data_sigma_log.append(o_table.get_data_sigma_log())
            gamma_filter_dc.append(o_table.get_gamma_filter_dc())
            dc_threshold_3x3.append(o_table.get_dc_threshold_3x3())
            dc_threshold_5x5.append(o_table.get_dc_threshold_5x5())
            dc_threshold_7x7.append(o_table.get_dc_threshold_7x7())
            dc_sigma_log.append(o_table.get_dc_log())
            dc_outlier_removal.append(o_table.get_dc_outlier_removal())
            dc_outlier_value.append(o_table.get_dc_outlier_value())
            result_directory.append(o_table.get_result_directory())
            file_id.append(o_table.get_file_id())
            sample_information.append("")
            used_environment.append("")
            osc_pixel.append("")

        table_dict = OrderedDict({'first_data_file'     : first_data_file,
                                  'last_data_file'      : last_data_file,
                                  'first_ob_file'       : first_ob_file,
                                  'last_ob_file'        : last_ob_file,
                                  'first_dc_file'       : first_dc_file,
                                  'last_dc_file'        : last_dc_file,
                                  'period'              : period,
                                  'images_per_step'     : images_per_step,
                                  'rotation'            : rotation,
                                  'fit_procedure'       : fit_procedure,
                                  'roi'                 : roi,
                                  'gamma_filter_data/ob': gamma_filter_data_ob,
                                  'data_threshold_3x3'  : data_threshold_3x3,
                                  'data_threshold_5x5'  : data_threshold_5x5,
                                  'data_threshold_7x7'  : data_threshold_7x7,
                                  'data_sigma_log'      : data_sigma_log,
                                  'gamma_filter_dc'     : gamma_filter_dc,
                                  'dc_threshold_3x3'    : dc_threshold_3x3,
                                  'dc_threshold_5x5'    : dc_threshold_5x5,
                                  'dc_threshold_7x7'    : dc_threshold_7x7,
                                  'dc_sigma_log'        : dc_sigma_log,
                                  'dc_outlier_removal'  : dc_outlier_removal,
                                  'dc_outlier_value'    : dc_outlier_value,
                                  'result_directory'    : result_directory,
                                  'file_id'             : file_id,
                                  'sample_information'  : sample_information,
                                  'used_environment'    : used_environment,
                                  'osc_pixel'           : osc_pixel,
                                  })

        return table_dict

    def right_click_table_widget(self, position):
        menu = QMenu(self)

        o_table = TableHandler(table_ui=self.ui.tableWidget)
        column_selected = o_table.get_column_selected()
        row_selected = o_table.get_row_selected()

        show_browse_for_file = False
        show_browse_for_folder = False
        if column_selected in [0, 1, 2, 3, 4, 5]:
            show_browse_for_file = True
        elif column_selected == 23:
            show_browse_for_folder = True

        remove = menu.addAction("Remove selected row")
        duplicate = menu.addAction("Duplicate selected row and move it to bottom")

        if show_browse_for_file:
            menu.addSeparator()
            browse = menu.addAction("Browse for file ...")
        elif show_browse_for_folder:
            menu.addSeparator()
            browse = menu.addAction("Browse for folder ...")
        else:
            browse = None

        action = menu.exec_(QtGui.QCursor.pos())

        if action == remove:
            self.remove_selected_row(row=row_selected)
        elif action == duplicate:
            self.duplicate_row_and_move_it_to_bottom(row=row_selected)
            self.check_table_content_pushed()
        elif action == browse:
            self.browse(show_browse_for_folder=show_browse_for_folder,
                        show_browse_for_file=show_browse_for_file,
                        row_selected=row_selected,
                        column_selected=column_selected)

    def browse(self, show_browse_for_folder=False, show_browse_for_file=True, row_selected=0, column_selected=0):
        folder_selected = self.grand_parent.folder_selected
        if show_browse_for_file:
            file_and_extension_name = QFileDialog.getOpenFileName(self,
                                                                  "Select file ...",
                                                                  folder_selected)

            file_selected = file_and_extension_name[0]
            if file_selected:
                o_table = TableHandler(table_ui=self.ui.tableWidget)
                o_table.set_item_with_str(row=row_selected,
                                          column=column_selected,
                                          cell_str=file_selected)

        elif show_browse_for_folder:
            folder_name = os.path.dirname(folder_selected)
            folder = QFileDialog.getExistingDirectory(self,
                                                      "Select output folder ...",
                                                      folder_name)

            if folder:
                o_table = TableHandler(table_ui=self.ui.tableWidget)
                o_table.set_item_with_str(row=row_selected,
                                          column=column_selected,
                                          cell_str=folder)

        self.check_table_content_pushed()

    def remove_selected_row(self, row=0):
        o_table = TableHandler(table_ui=self.ui.tableWidget)
        o_table.remove_row(row)

    def duplicate_row_and_move_it_to_bottom(self, row=0):
        o_table = TableHandler(table_ui=self.ui.tableWidget)
        nbr_row = o_table.row_count()
        o_table.insert_empty_row(nbr_row)

        o_table.define_row_for_getter(row=row)
        o_table.define_row_for_setter(row=nbr_row)

        o_table.set_first_data_file(o_table.get_first_data_file())
        o_table.set_last_data_file(o_table.get_last_data_file())
        o_table.set_first_ob_file(o_table.get_first_ob_file())
        o_table.set_last_ob_file(o_table.get_last_ob_file())
        o_table.set_first_dc_file(o_table.get_first_dc_file())
        o_table.set_last_dc_file(o_table.get_last_dc_file())
        o_table.set_period(o_table.get_period())
        o_table.set_images_per_step(o_table.get_images_per_step())
        o_table.set_rotation(o_table.get_rotation())
        o_table.set_fit_procedure(o_table.get_fit_procedure())
        o_table.set_roi(o_table.get_roi())
        o_table.set_gamma_filter_data_ob(o_table.get_gamma_filter_data_ob())
        o_table.set_data_threshold_3x3(o_table.get_data_threshold_3x3())
        o_table.set_data_threshold_5x5(o_table.get_data_threshold_5x5())
        o_table.set_data_threshold_7x7(o_table.get_data_threshold_7x7())
        o_table.set_data_sigma_log(o_table.get_data_sigma_log())
        o_table.set_gamma_filter_dc(o_table.get_gamma_filter_dc())
        o_table.set_dc_threshold_3x3(o_table.get_dc_threshold_3x3())
        o_table.set_dc_threshold_5x5(o_table.get_dc_threshold_5x5())
        o_table.set_dc_threshold_7x7(o_table.get_dc_threshold_7x7())
        o_table.set_dc_log(o_table.get_dc_log())
        o_table.set_dc_outlier_removal(o_table.get_dc_outlier_removal())
        o_table.set_dc_outlier_value(o_table.get_dc_outlier_value())
        o_table.set_result_directory(o_table.get_result_directory())
        o_table.set_file_id(o_table.get_file_id())