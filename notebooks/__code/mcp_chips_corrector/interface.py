from qtpy.QtWidgets import QMainWindow
from IPython.core.display import HTML
import os
from IPython.display import display
import pyqtgraph as pg
from qtpy.QtWidgets import QProgressBar, QVBoxLayout

from __code import load_ui


class Interface(QMainWindow):

    # pyqtgraph views and profile
    setup_image_view = None
    corrected_image_view = None
    profile_view = None

    def __init__(self, parent=None, working_dir="", o_corrector=None):
        self.parent = parent
        self.working_dir = working_dir
        self.o_corrector = o_corrector

        display(HTML('<span style="font-size: 20px; color:blue">Check UI that popped up \
            (maybe hidden behind this browser!)</span>'))

        super(Interface, self).__init__(parent)

        ui_full_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                    os.path.join('ui',
                                                 'ui_mcp_chips_corrector.ui'))

        self.ui = load_ui(ui_full_path, baseinstance=self)
        self.setWindowTitle("MCP Chips Corrector")

        o_init = Initialization(parent=self)
        o_init.run_all()

    # Event handler
    def profile_type_changed(self):
        pass

    def chips_index_changed(self, new_index):
        pass


class Initialization:
    """initialization of all the widgets such as pyqtgraph, progressbar..."""

    def __init__(self, parent=None):
        self.parent = parent

    def run_all(self):
        self.pyqtgraph()

    def pyqtgraph(self):
        # setup
        self.parent.setup_image_view = pg.ImageView()
        self.parent.setup_image_view.ui.roiBtn.hide()
        self.parent.setup_image_view.ui.menuBtn.hide()
        setup_layout = QVBoxLayout()
        setup_layout.addWidget(self.parent.setup_image_view)
        self.parent.ui.setup_widget.setLayout(setup_layout)

        # with correction
        self.parent.corrected_image_view = pg.ImageView()
        self.parent.corrected_image_view.ui.roiBtn.hide()
        self.parent.corrected_image_view.ui.menuBtn.hide()
        correction_layout = QVBoxLayout()
        correction_layout.addWidget(self.parent.corrected_image_view)
        self.parent.ui.with_correction_widget.setLayout(correction_layout)

        # profile
        self.parent.profile_view = pg.PlotWidget(title="Profile")
        profile_layout = QVBoxLayout()
        profile_layout.addWidget(self.parent.profile_view)
        self.parent.ui.profile_widget.setLayout(profile_layout)
