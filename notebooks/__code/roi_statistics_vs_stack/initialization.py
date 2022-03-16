import pyqtgraph as pg
from qtpy.QtWidgets import QProgressBar
from qtpy.QtWidgets import QHBoxLayout
import numpy as np
import os

from __code._utilities.table_handler import TableHandler
from __code.roi_statistics_vs_stack import StatisticsColumnIndex


class Initialization:

    def __init__(self, parent=None):
        self.parent = parent

    def all(self):
        self.pyqtgraph()
        self.splitter()
        self.widgets()
        self.statusbar()

    def pyqtgraph(self):
        # image view
        self.parent.ui.image_view = pg.ImageView()
        self.parent.ui.image_view.ui.menuBtn.hide()
        self.parent.ui.image_view.ui.roiBtn.hide()

        # default ROI
        self.parent.ui.roi = pg.ROI(
            [0, 0], [20, 20], pen=(62, 13, 244), scaleSnap=True)  # blue
        self.parent.ui.roi.addScaleHandle([1, 1], [0, 0])
        self.parent.ui.image_view.addItem(self.parent.ui.roi)
        self.parent.ui.roi.sigRegionChanged.connect(self.parent.roi_changed)

        hori_layout = QHBoxLayout()
        hori_layout.addWidget(self.parent.ui.image_view)
        self.parent.ui.widget.setLayout(hori_layout)

    def splitter(self):
        self.parent.ui.splitter.setSizes([500, 500])

    def statusbar(self):
        self.parent.eventProgress = QProgressBar(self.parent.ui.statusbar)
        self.parent.eventProgress.setMinimumSize(540, 14)
        self.parent.eventProgress.setMaximumSize(540, 100)
        self.parent.eventProgress.setVisible(False)
        self.parent.ui.statusbar.addPermanentWidget(self.parent.eventProgress)

    def widgets(self):
        self.parent.ui.horizontalSlider.setMaximum(len(self.parent.list_of_images)-1)

    def table(self):
        o_table = TableHandler(table_ui=self.parent.ui.tableWidget)
        for _row in np.arange(len(self.parent.list_of_images)):
            o_table.insert_empty_row(_row)
            short_file_name = os.path.basename(self.parent.list_of_images[_row])
            o_table.insert_item(row=_row,
                                column=StatisticsColumnIndex.file_name,
                                value=short_file_name,
                                editable=False)
            o_table.insert_item(row=_row,
                                column=StatisticsColumnIndex.time_offset,
                                value=self.parent.data_dict[_row]['time_offset'],
                                format_str="{:.2f}",
                                editable=False)

            list_column_index = [StatisticsColumnIndex.min, StatisticsColumnIndex.max,
                                 StatisticsColumnIndex.mean, StatisticsColumnIndex.median,
                                 StatisticsColumnIndex.std]
            for _col in list_column_index:
                o_table.insert_item(row=_row,
                                    column=_col,
                                    value="N/A",
                                    editable=False)

        o_table.set_column_width(column_width=[350, 100, 70, 70, 70, 70, 70])