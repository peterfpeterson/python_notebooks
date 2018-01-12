from IPython.core.display import HTML
from IPython.display import display
import numpy as np
from collections import OrderedDict

import pyqtgraph as pg

try:
    from PyQt4.QtGui import QFileDialog
    from PyQt4 import QtCore, QtGui
    from PyQt4.QtGui import QMainWindow
except ImportError:
    from PyQt5.QtWidgets import QFileDialog
    from PyQt5 import QtCore, QtGui
    from PyQt5.QtWidgets import QApplication, QMainWindow

from __code.ui_roi_selection  import Ui_MainWindow as UiMainWindow


class Interface(QMainWindow):

    live_data = []
    o_norm = None
    roi_column_width = 70
    integrated_image = None

    list_roi = {} #  'row": {'x0':None, 'y0': None, 'x1': None, 'y1': None}
    default_roi = {'x0': 0, 'y0': 0, 'x1': 50, 'y1': 50}

    def __init__(self, parent=None, o_norm=None):

        display(HTML('<span style="font-size: 20px; color:blue">Check UI that poped up \
            (maybe hidden behind this browser!)</span>'))

        if o_norm:
            self.o_norm = o_norm

        #self.list_files = self.o_norm.data['sample']['file_name']
        #self.list_data = self.o_norm.data['sample']['data']

        QMainWindow.__init__(self, parent=parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        self.init_statusbar()
        self.setWindowTitle("Background ROI Selection Tool")

        self.ui.image_view = pg.ImageView()
        self.ui.image_view.ui.roiBtn.hide()
        self.ui.image_view.ui.menuBtn.hide()

        top_layout = QtGui.QVBoxLayout()
        top_layout.addWidget(self.ui.image_view)
        self.ui.widget.setLayout(top_layout)
        self.init_widgets()
        self.integrate_images()
        self.display_image()

    def init_widgets(self):
        nbr_columns = self.ui.table_roi.columnCount()
        for _col in range(nbr_columns):
            self.ui.table_roi.setColumnWidth(_col, self.roi_column_width)

    def init_statusbar(self):
        self.eventProgress = QtGui.QProgressBar(self.ui.statusbar)
        self.eventProgress.setMinimumSize(20, 14)
        self.eventProgress.setMaximumSize(540, 100)
        self.eventProgress.setVisible(False)
        self.ui.statusbar.addPermanentWidget(self.eventProgress)

    def apply_clicked(self):
        # do stuff
        self.close()

    def cancel_clicked(self):
        self.close()

    def integrate_images(self):
        self.integrated_image = np.mean(self.o_norm.data['sample']['data'], axis=0)

    def display_image(self):
        self.ui.image_view.setImage(self.integrated_image)

    def remove_row_entry(self, row):
        del self.list_roi[row]

        #rename row
        new_list_roi = {}
        new_row_index = 0
        for _previous_row_index in self.list_roi.keys():
            new_list_roi[new_row_index] = self.list_roi[_previous_row_index]
            new_row_index += 1
        self.list_roi = new_list_roi

    def remove_roi_button_clicked(self):

        self.ui.table_roi.blockSignals(True)

        _selection = self.ui.table_roi.selectedRanges()
        row = _selection[0].topRow()

        # remove entry from list of roi
        self.remove_row_entry(row)

        # update table of rois
        self.update_table_roi_ui()

        self.ui.table_roi.blockSignals(False)

    def clear_table(self):
        nbr_row = self.ui.table_roi.rowCount()
        for _row in np.arange(nbr_row):
            self.ui.table_roi.removeRow(0)

    def update_table_roi_ui(self):
        """Using list_roi as reference, repopulate the table_roi_ui"""
        list_roi = self.list_roi

        self.clear_table()

        _index_row = 0
        for _roi_key in list_roi.keys():
            _roi = list_roi[_roi_key]

            self.ui.table_roi.insertRow(_index_row)

            _item = QtGui.QTableWidgetItem(_roi['x0'])
            self.ui.table_roi.setItem(_index_row, 0, _item)

            _item = QtGui.QTableWidgetItem(_roi['y0'])
            self.ui.table_roi.setItem(_index_row, 1, _item)

            _item = QtGui.QTableWidgetItem(_roi['x1'])
            self.ui.table_roi.setItem(_index_row, 2, _item)

            _item = QtGui.QTableWidgetItem(_roi['y1'])
            self.ui.table_roi.setItem(_index_row, 3, _item)

            _index_row += 1

    def update_table_roi(self, item):
        """Using the table_roi_ui as reference, will update the list_roi dictionary"""
        print("hdfdf")


    def _get_item_value(self, row, column):
        _item = self.ui.table_roi.item(row, column)
        if _item:
            return str(_item.text())
        else:
            return None

    def add_roi_button_clicked(self):
        self.ui.table_roi.blockSignals(True)
        _selection = self.ui.table_roi.selectedRanges()
        if _selection:
            row = _selection[0].topRow()
        else:
            row = 0

        # init new row with default value
        self.ui.table_roi.insertRow(row)
        _default_roi = self.default_roi

        _item = QtGui.QTableWidgetItem(str(_default_roi['x0']))
        self.ui.table_roi.setItem(row, 0, _item)

        _item = QtGui.QTableWidgetItem(str(_default_roi['y0']))
        self.ui.table_roi.setItem(row, 1, _item)

        _item = QtGui.QTableWidgetItem(str(_default_roi['x1']))
        self.ui.table_roi.setItem(row, 2, _item)

        _item = QtGui.QTableWidgetItem(str(_default_roi['y1']))
        self.ui.table_roi.setItem(row, 3, _item)

        # save new list_roi dictionary
        nbr_row = self.ui.table_roi.rowCount()
        list_roi = OrderedDict()
        for _row in np.arange(nbr_row):
            _roi = {}

            _x0 = self._get_item_value(_row, 0)
            _roi['x0'] = _x0

            _y0 = self._get_item_value(_row, 1)
            _roi['y0'] = _y0

            _x1 = self._get_item_value(_row, 2)
            _roi['x1'] = _x1

            _y1 = self._get_item_value(_row, 3)
            _roi['y1'] = _y1

            list_roi[_row] = _roi

        self.list_roi = list_roi

        self.ui.table_roi.blockSignals(False)

    def closeEvent(self, eventhere=None):
        print("Leaving Parameters Selection UI")



