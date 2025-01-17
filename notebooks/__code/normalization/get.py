import os
from ipywidgets import widgets
import numpy as np

from __code._utilities.get import Get as TopGet

from __code.normalization import LOG_FILENAME
from __code import file_handler
from . import ROI_BUTTON_DESCRIPTION, ROI_ICON

LIST_METADATA_NOT_INSTRUMENT_RELATED = ['filename', 'time_stamp', 'time_stamp_user_format']


class Get(TopGet):

    def log_file_name(self):
        return TopGet.log_file_name(LOG_FILENAME)

    def active_tabs(self):
        active_acquisition_tab = self.parent.acquisition_tab.selected_index
        config_tab_dict = self.parent.config_tab_dict[active_acquisition_tab]
        active_config_tab = config_tab_dict['config_tab_id'].selected_index
        return [active_acquisition_tab, active_config_tab]

    def active_tab_acquisition_key(self):
        active_acquisition_tab_index = self.parent.acquisition_tab.selected_index
        title = self.parent.acquisition_tab.get_title(active_acquisition_tab_index)
        [_, time_s] = title.split(": ")
        acquisition_key = time_s[:-1]
        return np.float(acquisition_key)

    def active_tab_config_key(self):
        [active_acquisition, _] = self.active_tabs()
        all_config_tab_of_acquisition = self.parent.config_tab_dict[active_acquisition]
        current_config_tab = all_config_tab_of_acquisition['config_tab_id']
        current_config_tab_index = current_config_tab.selected_index
        return current_config_tab.get_title(current_config_tab_index)

    def time_before_and_after_of_this_config(self, current_config=None):
        [time_before_selected_ui, time_after_selected_ui] = \
            self.time_before_and_after_ui_of_this_config(current_config=current_config)
        return [time_before_selected_ui.value, time_after_selected_ui.value]

    def time_before_and_after_ui_of_this_config(self, current_config=None):
        if current_config is None:
            current_config = self.current_config_of_widgets_id()
        return [current_config['time_slider_before_experiment'], current_config['time_slider_after_experiment']]

    def time_before_and_after_message_ui_of_this_config(self):
        current_config = self.current_config_of_widgets_id()
        return current_config['time_slider_before_message']

    def experiment_label_ui_of_this_config(self):
        current_config = self.current_config_of_widgets_id()
        return current_config['experiment_label']

    def current_config_dict(self):
        active_acquisition = self.active_tab_acquisition_key()
        active_config = self.active_tab_config_key()
        final_full_master_dict = self.parent.final_full_master_dict
        current_config = final_full_master_dict[active_acquisition][active_config]
        return current_config

    def current_config_of_widgets_id(self):
        [active_acquisition, active_config] = self.active_tabs()
        all_config_tab_of_acquisition = self.parent.config_tab_dict[active_acquisition]
        current_config_of_widgets_id = all_config_tab_of_acquisition[active_config]
        return current_config_of_widgets_id

    def max_time_elapse_before_experiment(self):
        # this will use the first sample image taken, the first OB image taken and will calculate that
        # difference. If the OB was taken after the first image, time will be 0

        # retrieve acquisition and config values
        acquisition_key = float(self.active_tab_acquisition_key())  # ex: 55.0
        config_key = self.active_tab_config_key()  # ex: 'config0'

        # retrieve list of ob and df for this config for this acquisition
        final_full_master_dict = self.parent.final_full_master_dict
        dict_for_this_config = final_full_master_dict[acquisition_key][config_key]

        # retrieve first and last sample file for this config and for this acquisition
        first_sample_image_time_stamp = dict_for_this_config['first_images']['sample']['time_stamp']
        first_ob = dict_for_this_config['first_images']['ob']['time_stamp']

        if first_ob > first_sample_image_time_stamp:
            return 0
        else:
            return first_sample_image_time_stamp - first_ob

    def max_time_elapse_after_experiment(self):
        # this will use the last sample image taken, the last OB image taken and will calculate that
        # difference. If the last OB was taken before the last image, time will be 0

        # retrieve acquisition and config values
        acquisition_key = float(self.active_tab_acquisition_key())  # ex: 55.0
        config_key = self.active_tab_config_key()  # ex: 'config0'

        # retrieve list of ob and df for this config for this acquisition
        final_full_master_dict = self.parent.final_full_master_dict
        dict_for_this_config = final_full_master_dict[acquisition_key][config_key]

        # retrieve first and last sample file for this config and for this acquisition
        last_sample_images_time_stamp = dict_for_this_config['last_images']['sample']['time_stamp']
        last_ob = dict_for_this_config['last_images']['ob']['time_stamp']

        if last_ob < last_sample_images_time_stamp:
            return 0
        else:
            return last_sample_images_time_stamp - last_ob

    def full_layout_for_this_config(self, dict_config):
        config_widgets_id_dict = {}

        def _make_list_basename_file(list_name='list_sample'):
            return [os.path.basename(_entry['filename']) for _entry in dict_config[list_name]]

        def _make_full_file_name(list_name='list_sample'):
            return [_entry['filename'] for _entry in dict_config[list_name]]

        list_sample = _make_full_file_name(list_name='list_sample')
        list_ob = _make_full_file_name(list_name='list_ob')
        list_df = _make_full_file_name(list_name='list_df')

        # normalize or not this configuration
        use_this_config_widget = widgets.Checkbox(description="Normalize this configuration",
                                                  value=True,
                                                  layout=widgets.Layout(width="100%"))
        use_this_config_widget.observe(self.parent.update_use_this_config_widget, names='value')
        config_widgets_id_dict['use_this_config'] = use_this_config_widget

        # use custom time range check box
        check_box_user_time_range = widgets.Checkbox(description="Use selected OB & DF from custom time range",
                                                     value=False,
                                                     layout=widgets.Layout(width="35%"))
        config_widgets_id_dict['use_custom_time_range_checkbox'] = check_box_user_time_range
        check_box_user_time_range.observe(self.parent.update_config_widgets, names='value')

        [max_time_elapse_before_experiment,
         max_time_elapse_after_experiment] = self.parent.calculate_max_time_before_and_after_exp_for_this_config(
                dict_config)

        hori_layout1 = widgets.HBox([check_box_user_time_range,
                                     widgets.FloatSlider(value=-max_time_elapse_before_experiment - 0.1,
                                                         min=-max_time_elapse_before_experiment - 0.1,
                                                         max=0,
                                                         step=0.1,
                                                         readout=False,
                                                         layout=widgets.Layout(width="30%",
                                                                               visibility='hidden')),
                                     widgets.Label(" <<< EXPERIMENT >>> ",
                                                   layout=widgets.Layout(width="20%",
                                                                         visibility='hidden')),
                                     widgets.FloatSlider(value=max_time_elapse_before_experiment + 0.1,
                                                         min=0,
                                                         max=max_time_elapse_after_experiment + 0.1,
                                                         step=0.1,
                                                         readout=False,
                                                         layout=widgets.Layout(width="30%",
                                                                               visibility='hidden')),
                                     ])
        self.parent.hori_layout1 = hori_layout1
        self.parent.time_before_slider = hori_layout1.children[1]
        self.parent.time_after_slider = hori_layout1.children[3]
        self.parent.experiment_label = hori_layout1.children[2]
        self.parent.time_after_slider.observe(self.parent.update_time_range_event, names='value')
        self.parent.time_before_slider.observe(self.parent.update_time_range_event, names='value')
        config_widgets_id_dict['time_slider_before_experiment'] = hori_layout1.children[1]
        config_widgets_id_dict['time_slider_after_experiment'] = hori_layout1.children[3]
        config_widgets_id_dict['experiment_label'] = hori_layout1.children[2]

        nbr_sample = len(list_sample)
        nbr_ob = len(list_ob)
        nbr_df = len(list_df)

        def get_html_table():
            force_combine = force_ui.value
            how_to_combine = how_to_ui.value

            if force_combine == 'yes':
                description = f"OBs <b>will be combined</b> using <b>{how_to_combine}</b>"
            else:
                description = f"OBs <b>won't be combined</b>! Each sample will use <b>1 OB</b>"

            html_table = f"<table style='width:100%'>" \
                         "<tr>" \
                         "<th style='background-color: cyan'>Nbr of Samples</th>" \
                         "<th style='background-color: cyan'>Nbr of OBs</th>" \
                         "<th style='background-color: cyan'>Nbr of DFs</th>" \
                         "<th style='background-color: cyan; width:60%'>Description of Process</th>" \
                         "</tr>" \
                         "<tr>" \
                         f"<td>{nbr_sample}</td>" \
                         f"<td>{nbr_ob}</td>" \
                         f"<td>{nbr_df}</td>" \
                         f"<td>{description}</td>" \
                         "</tr>" \
                         "</table>"
            return html_table

        # do you want to combine
        if nbr_sample != nbr_ob:
            force_ui_disabled = True
            html_string = "<font color='blue'>INFO</font>: the option to combine or not is disabled as the number of " \
                          "<b>sample</b> " \
                          "and " \
                          "<b>obs</b> do not match. The <b>OBs</b> will be combined!"
        else:
            force_ui_disabled = False
            html_string = ""
        force_ui = widgets.RadioButtons(options=['yes', 'no'],
                                        value='yes',
                                        disabled=force_ui_disabled,
                                        layout=widgets.Layout(width='200px'))
        force_ui.observe(self.parent.do_you_want_to_combine_changed, names='value')
        combine_or_no_ui = widgets.VBox([widgets.HTML("<b>Do you want to combine the OBs?</b>"),
                                         force_ui,
                                         widgets.HTML(html_string)])
        config_widgets_id_dict['force_combine'] = force_ui
        config_widgets_id_dict['force_combine_message'] = combine_or_no_ui.children[2]

        # how to combine widgets
        how_to_ui = widgets.RadioButtons(options=['median', 'mean'],
                                         value='median',
                                         layout=widgets.Layout(width='200px'))
        how_to_ui.observe(self.parent.how_to_combine_changed, names='value')
        how_to_combine_ui = widgets.VBox([widgets.HTML("<b>How to combine the OBs?</b>"),
                                          how_to_ui])
        config_widgets_id_dict['how_to_combine'] = how_to_ui

        # table
        table_title = widgets.HTML("<font color='blue'><center><b>S U M M A R Y</b></center></font>")

        html_table = ""
        table = widgets.HTML(value=html_table)
        table.value = get_html_table()
        config_widgets_id_dict['table'] = table

        # use all OB and DF
        hori_layout2 = widgets.HBox([widgets.Label("    ",
                                                   layout=widgets.Layout(width="20%")),
                                     widgets.HTML("",
                                                  layout=widgets.Layout(width="80%"))])
        self.parent.hori_layout2 = hori_layout2
        self.parent.time_before_and_after_message = hori_layout2.children[1]
        config_widgets_id_dict['time_slider_before_message'] = hori_layout2.children[1]

        # table of metadata
        [metadata_table_label, metadata_table] = self.parent.populate_metadata_table(dict_config)

        select_width = '100%'
        sample_list_of_runs = widgets.VBox([widgets.HTML("<b>List of Sample runs</b> (ALL RUNS listed here will be "
                                                         "used!"),
                                            widgets.Select(options=list_sample,
                                                           layout=widgets.Layout(width=select_width,
                                                                                 height='300px'))],
                                           layout=widgets.Layout(width="100%"))
        # self.list_of_runs_ui = box0.children[1]
        ob_list_of_runs = widgets.VBox([widgets.HTML("<b>List of OBs</b>. Only the selected images will be used!"),
                                        widgets.SelectMultiple(options=list_ob,
                                                               value=list_ob,
                                                               layout=widgets.Layout(width=select_width,
                                                                                     height='300px'))],
                                       layout=widgets.Layout(width="100%"))
        ob_list_of_runs.children[1].observe(self.parent.selection_of_ob_changed, names='value')
        df_list_of_runs = widgets.VBox([widgets.HTML("<b>List of DFs</b>.Only the selected images will be used!"),
                                        widgets.SelectMultiple(options=list_df,
                                                               value=list_df,
                                                               layout=widgets.Layout(width=select_width,
                                                                                     height='300px'))],
                                       layout=widgets.Layout(width="100%"))

        red_hr_line = widgets.HTML("<style>hr {border-top: 1px solid red}</style><hr>")
        black_hr_line = widgets.HTML("<style>hr {border-top: 1px solid black}</style><hr>")

        # select ROI
        select_roi_button = widgets.Button(description=ROI_BUTTON_DESCRIPTION,
                                           button_style='',
                                           layout=widgets.Layout(width="100%"),
                                           icon=ROI_ICON)
        select_roi_button.style.button_color = 'lightgreen'
        select_roi_button.style.font_weight = 'bold'
        select_roi_button.on_click(self.parent.roi_button_clicked)
        config_widgets_id_dict['select_roi_button'] = select_roi_button

        list_runs_layout = widgets.VBox([sample_list_of_runs,
                                         black_hr_line,
                                         ob_list_of_runs,
                                         combine_or_no_ui,
                                         black_hr_line,
                                         how_to_combine_ui,
                                         black_hr_line,
                                         df_list_of_runs,
                                         red_hr_line,
                                         select_roi_button,
                                         red_hr_line,
                                         table_title,
                                         table])
        config_widgets_id_dict['list_of_sample_runs'] = sample_list_of_runs.children[1]
        config_widgets_id_dict['list_of_ob'] = ob_list_of_runs.children[1]
        config_widgets_id_dict['list_of_df'] = df_list_of_runs.children[1]

        verti_layout = widgets.VBox([use_this_config_widget,
                                     hori_layout1,
                                     hori_layout2,
                                     black_hr_line,
                                     metadata_table_label,
                                     metadata_table,
                                     red_hr_line,
                                     list_runs_layout])

        return {'verti_layout': verti_layout, 'config_widgets_id_dict': config_widgets_id_dict}

    @staticmethod
    def list_of_tiff_files(folder=""):
        list_of_tiff_files = file_handler.get_list_of_files(folder=folder,
                                                            extension='tiff')
        return list_of_tiff_files

    @staticmethod
    def get_instrument_metadata_only(metadata_dict):
        _clean_dict = {}
        for _key in metadata_dict.keys():
            if not _key in LIST_METADATA_NOT_INSTRUMENT_RELATED:
                _clean_dict[_key] = metadata_dict[_key]
        return _clean_dict
