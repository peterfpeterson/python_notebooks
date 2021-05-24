from IPython.core.display import HTML
import pandas as pd
import numpy as np
from IPython.core.display import display
import os
from qtpy.QtWidgets import QMainWindow

from __code import load_ui
from __code.ipywe import fileselector
from __code._utilities.file import retrieve_metadata_value_from_ascii_file
from __code.wave_front_dynamics.algorithms import ListAlgorithm
from __code.wave_front_dynamics.initialization import Initialization
from __code.wave_front_dynamics.event_handler import EventHandler
from __code.wave_front_dynamics.display import Display


class WaveFrontDynamics:

    list_of_ascii_files = None
    list_of_original_image_files = None
    list_of_data = None

    def __init__(self, working_dir="~/"):
        self.working_dir = working_dir

    def select_data(self):
        self.list_data_widget = fileselector.FileSelectorPanel(instruction='select list of ascii profile data ...',
                                                               start_dir=self.working_dir,
                                                               next=self.load_data,
                                                               filters={"ASCII": "*.txt"},
                                                               default_filter="ASCII",
                                                               multiple=True)
        self.list_data_widget.show()

    def load_data(self, list_of_ascii_files=None):
        if list_of_ascii_files is None:
            return

        list_of_ascii_files.sort()
        self.list_of_ascii_files = list_of_ascii_files
        list_of_data = []
        list_of_original_image_files = []
        for _file in list_of_ascii_files:
            _data = pd.read_csv(_file,
                                skiprows=5,
                                delimiter=",",
                                names=['pixel', 'mean counts'],
                                dtype=np.float,
                                index_col=0)
            list_of_data.append(_data)
            _original_image_file = retrieve_metadata_value_from_ascii_file(filename=_file,
                                                                           metadata_name="# source image")
            list_of_original_image_files.append(_original_image_file)

        self.list_of_data = list_of_data
        self.list_of_original_image_files = list_of_original_image_files


class WaveFrontDynamicsUI(QMainWindow):

    list_of_ascii_files = None
    list_of_original_image_files = None
    list_of_data = None
    list_of_data_prepared = None
    peak_value_arrays = {ListAlgorithm.sliding_average: None,
                         ListAlgorithm.change_point   : None,
                         ListAlgorithm.error_function : None}

    # matplotlib
    prepare_data_plot = None

    def __init__(self, parent=None, working_dir="./", wave_front_dynamics=None):

        display(HTML('<span style="font-size: 20px; color:blue">Launched UI! '
                     '(maybe hidden behind this browser!)</span>'))

        self.working_dir = working_dir
        self.wave_front_dynamics = wave_front_dynamics

        self.list_of_data = wave_front_dynamics.list_of_data
        self.nbr_files = len(self.list_of_data)

        super(QMainWindow, self).__init__(parent)
        ui_full_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                    os.path.join('ui',
                                                 'ui_wave_front_dynamics.ui'))
        self.ui = load_ui(ui_full_path, baseinstance=self)
        self.setWindowTitle("Define center and sector of profile")

        o_init = Initialization(parent=self)
        o_init.all()

        self.prepare_data_file_index_pressed()
        self.prepare_data_bin_size_pressed()

    # event handler - prepare data tab
    def prepare_data_file_index_pressed(self):
        o_event = EventHandler(parent=self)
        o_event.prepare_data_file_index_slider_changed()
        o_event.update_prepare_data_plot()

    def prepare_data_file_index_moved(self, value):
        o_event = EventHandler(parent=self)
        o_event.prepare_data_file_index_slider_changed()
        o_event.update_prepare_data_plot()

    def prepare_data_bin_size_pressed(self):
        o_event = EventHandler(parent=self)
        o_event.prepare_data_bin_size_changed()
        o_event.update_prepare_data_plot()

    def prepare_data_bin_size_moved(self, value):
        o_event = EventHandler(parent=self)
        o_event.prepare_data_bin_size_changed()
        o_event.update_prepare_data_plot()

    def prepare_data_bin_type_changed(self):
        o_event = EventHandler(parent=self)
        o_event.update_prepare_data_plot()

    def update_prepare_data_plot(self):
        o_event = EventHandler(parent=self)
        o_event.update_prepare_data_plot()

    # event handler - edge calculation tab
    def edge_calculation_calculate_pressed(self):
        o_event = EventHandler(parent=self)
        o_event.prepare_all_data()
        o_event.calculate_edge_position()
        o_display = Display(parent=self)
        o_display.display_current_selected_profile_and_edge_position()
        o_display.display_all_edge_positions()

    def edge_calculation_file_index_slider_pressed(self):
        o_event = EventHandler(parent=self)
        o_event.edge_calculation_file_index_slider_changed()
        o_display = Display(parent=self)
        o_display.display_current_selected_profile_and_edge_position()
        o_display.display_all_edge_positions()

    def edge_calculation_file_index_slider_moved(self, value):
        o_event = EventHandler(parent=self)
        o_event.edge_calculation_file_index_slider_changed(value)
        o_display = Display(parent=self)
        o_display.display_current_selected_profile_and_edge_position()
        o_display.display_all_edge_positions()
