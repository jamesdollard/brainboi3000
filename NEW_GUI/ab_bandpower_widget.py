
import time

import PySide6.QtCore
import numpy as np
import pandas as pd
import pyqtgraph as pg
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextDocument
from PySide6.QtWidgets import (
    QLabel,
    QComboBox,
    QCheckBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLineEdit,
    QGridLayout,
    QButtonGroup,
    QRadioButton,
    QScrollArea,
    QPlainTextDocumentLayout,
    QTableWidget,
    QTableWidgetItem
)
from funcs import *
from state_detection_widget import StateDetectionWidget
from unknown_pleasures_widget import UnknownPleasuresWidget



# Enables user to capture and compare the bandpower of two recording sessions
class ABBandpowerWidget(QWidget):

    def __init__(self, parent):

        # ** CLASS VARIABLE INITIALIZATION ** #

        super().__init__()
        self.parent = parent

        # Data gathering variables
        self.a_record_time = 0
        self.b_record_time = 0
        self.c_record_time = 0
        self.d_record_time = 0
        self.a_data = None
        self.b_data = None
        self.c_data = None
        self.d_data = None

        # Plotting info
        self.plot_state = [False, False, False, False]  # a, b, c, d

        # Bandpower processing
        self.bp_processing = parent.bp_processing

        # Processed data variables
        self.a_processed_bp = None
        self.b_processed_bp = None
        self.c_processed_bp = None
        self.d_processed_bp = None
        self.a_frequencies = [0, 0]
        self.b_frequencies = [0, 0]
        self.c_frequencies = [0, 0]
        self.d_frequencies = [0, 0]

        self.a_standard_band_values = [0, 0, 0, 0, 0]
        self.b_standard_band_values = [0, 0, 0, 0, 0]
        self.c_standard_band_values = [0, 0, 0, 0, 0]
        self.d_standard_band_values = [0, 0, 0, 0, 0]

        # Timers
        self.a_timer = PySide6.QtCore.QTimer()
        self.a_timer.setSingleShot(True)
        self.a_timer.timeout.connect(self.record_a)
        self.b_timer = PySide6.QtCore.QTimer()
        self.b_timer.setSingleShot(True)
        self.b_timer.timeout.connect(self.record_b)
        self.c_timer = PySide6.QtCore.QTimer()
        self.c_timer.setSingleShot(True)
        self.c_timer.timeout.connect(self.record_c)
        self.d_timer = PySide6.QtCore.QTimer()
        self.d_timer.setSingleShot(True)
        self.d_timer.timeout.connect(self.record_d)

        # ** WIDGET CONSTRUCTION ** #

        # ############# #
        # Input Section #
        # ############# #

        # State A #

        a_record_time_label = make_label("State A Record Time (s): ")

        a_record_time_input = QLineEdit()
        a_record_time_input.setPlaceholderText("0")
        a_record_time_input.setMaxLength(2)
        a_record_time_input.textChanged.connect(self.set_a_record_time)
        a_record_time_input.setStyleSheet("""background-color: #fff; color: #000;font: 15px; min-width: 50px;
                                             margin-bottom: 0px; max-width: 50px; padding: 5px;""")

        self.a_record_button = make_button("Record State A")
        self.a_record_button.pressed.connect(self.pressed_record_a)
        # self.a_record_button.released.connect(self.record_a)

        state_a = QHBoxLayout()
        state_a.addWidget(a_record_time_label)
        state_a.addWidget(a_record_time_input)
        state_a.addWidget(self.a_record_button)

        # State B #

        b_record_time_label = make_label("State B Record Time (s): ")

        b_record_time_input = QLineEdit()
        b_record_time_input.setPlaceholderText("0")
        b_record_time_input.setMaxLength(2)
        b_record_time_input.textChanged.connect(self.set_b_record_time)
        b_record_time_input.setStyleSheet("""background-color: #fff; color: #000;font: 15px; min-width: 50px;
                                             margin-bottom: 0px; max-width: 50px; padding: 5px;""")

        self.b_record_button = make_button("Record State B")
        self.b_record_button.pressed.connect(self.pressed_record_b)
        # self.b_record_button.released.connect(self.record_b)

        state_b = QHBoxLayout()
        state_b.addWidget(b_record_time_label)
        state_b.addWidget(b_record_time_input)
        state_b.addWidget(self.b_record_button)

        # State C #

        c_record_time_label = make_label("State C Record Time (s): ")

        c_record_time_input = QLineEdit()
        c_record_time_input.setPlaceholderText("0")
        c_record_time_input.setMaxLength(2)
        c_record_time_input.textChanged.connect(self.set_c_record_time)
        c_record_time_input.setStyleSheet("""background-color: #fff; color: #000;font: 15px; min-width: 50px;
                                             margin-bottom: 0px; max-width: 50px; padding: 5px;""")

        self.c_record_button = make_button("Record State C")
        self.c_record_button.pressed.connect(self.pressed_record_c)
        # self.c_record_button.released.connect(self.record_c)

        state_c = QHBoxLayout()
        state_c.addWidget(c_record_time_label)
        state_c.addWidget(c_record_time_input)
        state_c.addWidget(self.c_record_button)

        # State D #

        d_record_time_label = make_label("State D Record Time (s): ")

        d_record_time_input = QLineEdit()
        d_record_time_input.setPlaceholderText("0")
        d_record_time_input.setMaxLength(2)
        d_record_time_input.textChanged.connect(self.set_d_record_time)
        d_record_time_input.setStyleSheet("""background-color: #fff; color: #000;font: 15px; min-width: 50px;
                                             margin-bottom: 0px; max-width: 50px; padding: 5px;""")

        self.d_record_button = make_button("Record State D")
        self.d_record_button.pressed.connect(self.pressed_record_d)
        # self.d_record_button.released.connect(self.record_d)

        state_d = QHBoxLayout()
        state_d.addWidget(d_record_time_label)
        state_d.addWidget(d_record_time_input)
        state_d.addWidget(self.d_record_button)

        # Clear states button #
        self.clear_states_button = make_button("Clear States")
        self.clear_states_button.pressed.connect(self.clear_states_button_pressed)
        self.clear_states_button.released.connect(self.clear_states_button_released)

        # Bandpower Selection #

        bp_label = make_label("Bandpower processing method: ")

        bp_method_list = QComboBox()
        bp_method_list.addItems(self.bp_processing.bp_methods)
        bp_method_list.setStyleSheet("""background-color: gray; color: #fff; min-width: 50px; max-width: 150px;""")
        bp_method_list.setCurrentIndex(0)
        bp_method_list.currentIndexChanged.connect(self.set_bp_method)

        bandpower_selection = QHBoxLayout()
        bandpower_selection.addWidget(bp_label)
        bandpower_selection.addWidget(bp_method_list)

        # Relative Plot Selection #

        relative_plot_checkbox = QCheckBox("Relative plot")
        relative_plot_checkbox.setStyleSheet("""color: #fff; font-size: 15px;""")
        relative_plot_checkbox.stateChanged.connect(self.set_relative_plot)

        # 60 Hz Filter Selection #

        sixty_hz_filter_checkbox = QCheckBox("Filter 60 Hz")
        sixty_hz_filter_checkbox.setStyleSheet("""color: #fff; font-size: 15px;""")
        sixty_hz_filter_checkbox.stateChanged.connect(self.set_sixty_hz_filter)

        # 0-5 Hz Filter Selection #

        zero_to_five_hz_filter_checkbox = QCheckBox("Filter 0-5 Hz")
        zero_to_five_hz_filter_checkbox.setStyleSheet("""color: #fff; font-size: 15px;""")
        zero_to_five_hz_filter_checkbox.stateChanged.connect(self.set_zero_to_five_hz_filter)

        # Frequency Range Selection #

        # Build all frequencies option
        all_frequencies_button = QRadioButton("Include all frequencies")
        all_frequencies_button.setStyleSheet("""color: #fff; font-size: 15px;""")
        all_frequencies_button.setChecked(True)

        # Build custom frequencies option
        custom_frequencies_button = QRadioButton("Custom frequency range")
        custom_frequencies_button.setStyleSheet("""color: #fff; font-size: 15px;""")

        custom_frequencies_low = QLineEdit()
        custom_frequencies_low.setPlaceholderText("0")
        custom_frequencies_low.setMaxLength(3)
        custom_frequencies_low.textChanged.connect(self.set_low_frequency)
        custom_frequencies_low.setStyleSheet("""background-color: #fff; color: #000;font: 15px; min-width: 50px;
                                                 margin-bottom: 0px; max-width: 50px; padding: 5px;""")
        custom_frequencies_high = QLineEdit()
        custom_frequencies_high.setPlaceholderText("120")
        custom_frequencies_high.setMaxLength(3)
        custom_frequencies_high.textChanged.connect(self.set_high_frequency)
        custom_frequencies_high.setStyleSheet("""background-color: #fff; color: #000;font: 15px; min-width: 50px;
                                                     margin-bottom: 0px; max-width: 50px; padding: 5px;""")

        custom_frequencies_option = QHBoxLayout()
        custom_frequencies_option.addWidget(custom_frequencies_button)
        custom_frequencies_option.addWidget(custom_frequencies_low)
        custom_frequencies_option.addWidget(custom_frequencies_high)

        self.frequency_selection = QButtonGroup()
        self.frequency_selection.addButton(all_frequencies_button)
        self.frequency_selection.addButton(custom_frequencies_button)
        self.frequency_selection.setId(all_frequencies_button, 1)
        self.frequency_selection.setId(custom_frequencies_button, 2)
        self.frequency_selection.idPressed.connect(self.toggle_custom_frequency)

        custom_frequencies_label = make_label("Set custom frequency range")

        # Build frequency range selection
        frequency_range_selection = QVBoxLayout()
        frequency_range_selection.addWidget(all_frequencies_button)
        frequency_range_selection.addLayout(custom_frequencies_option)

        # Included Electrode Selection #

        # Build all electrodes option
        all_electrodes_button = QRadioButton("Include all electrodes")
        all_electrodes_button.setStyleSheet("""color: #fff; font-size: 15px;""")
        all_electrodes_button.setChecked(True)

        # Build custom electrodes option
        custom_electrodes_button = QRadioButton("Include custom electrodes")
        custom_electrodes_button.setStyleSheet("""color: #fff; font-size: 15px;""")

        electrode_1_button = QCheckBox("1")
        electrode_2_button = QCheckBox("2")
        electrode_3_button = QCheckBox("3")
        electrode_4_button = QCheckBox("4")
        electrode_5_button = QCheckBox("5")
        electrode_6_button = QCheckBox("6")
        electrode_7_button = QCheckBox("7")
        electrode_8_button = QCheckBox("8")

        self.selected_electrodes_group = QButtonGroup()
        self.selected_electrodes_group.addButton(electrode_1_button)
        self.selected_electrodes_group.addButton(electrode_2_button)
        self.selected_electrodes_group.addButton(electrode_3_button)
        self.selected_electrodes_group.addButton(electrode_4_button)
        self.selected_electrodes_group.addButton(electrode_5_button)
        self.selected_electrodes_group.addButton(electrode_6_button)
        self.selected_electrodes_group.addButton(electrode_7_button)
        self.selected_electrodes_group.addButton(electrode_8_button)
        self.selected_electrodes_group.setId(electrode_1_button, 1)
        self.selected_electrodes_group.setId(electrode_2_button, 2)
        self.selected_electrodes_group.setId(electrode_3_button, 3)
        self.selected_electrodes_group.setId(electrode_4_button, 4)
        self.selected_electrodes_group.setId(electrode_5_button, 5)
        self.selected_electrodes_group.setId(electrode_6_button, 6)
        self.selected_electrodes_group.setId(electrode_7_button, 7)
        self.selected_electrodes_group.setId(electrode_8_button, 8)
        self.selected_electrodes_group.idPressed.connect(self.select_custom_electrode)
        self.selected_electrodes_group.setExclusive(False)

        electrode_1_button.setStyleSheet("""color: #fff;font-size: 15px;""")
        electrode_2_button.setStyleSheet("""color: #fff;font-size: 15px;""")
        electrode_3_button.setStyleSheet("""color: #fff;font-size: 15px;""")
        electrode_4_button.setStyleSheet("""color: #fff;font-size: 15px;""")
        electrode_5_button.setStyleSheet("""color: #fff;font-size: 15px;""")
        electrode_6_button.setStyleSheet("""color: #fff;font-size: 15px;""")
        electrode_7_button.setStyleSheet("""color: #fff;font-size: 15px;""")
        electrode_8_button.setStyleSheet("""color: #fff;font-size: 15px;""")

        custom_electrode_selection = QHBoxLayout()
        custom_electrode_selection.addWidget(electrode_1_button)
        custom_electrode_selection.addWidget(electrode_2_button)
        custom_electrode_selection.addWidget(electrode_3_button)
        custom_electrode_selection.addWidget(electrode_4_button)
        custom_electrode_selection.addWidget(electrode_5_button)
        custom_electrode_selection.addWidget(electrode_6_button)
        custom_electrode_selection.addWidget(electrode_7_button)
        custom_electrode_selection.addWidget(electrode_8_button)

        custom_electrodes_option = QVBoxLayout()
        custom_electrodes_option.addWidget(custom_electrodes_button)
        custom_electrodes_option.addLayout(custom_electrode_selection)

        # Build electrode selection

        self.all_electrodes_toggle = QButtonGroup()
        self.all_electrodes_toggle.addButton(all_electrodes_button)
        self.all_electrodes_toggle.addButton(custom_electrodes_button)
        self.all_electrodes_toggle.setId(all_electrodes_button, 1)
        self.all_electrodes_toggle.setId(custom_electrodes_button, 2)
        self.all_electrodes_toggle.idPressed.connect(self.toggle_all_electrodes)

        electrode_selection = QVBoxLayout()
        electrode_selection.addWidget(all_electrodes_button)
        electrode_selection.addLayout(custom_electrodes_option)

        # Input Section Layout #

        # Titles
        data_recording_title = make_label("Record/Load Data")
        data_processing_title = make_label("Data Processing Options")

        states = QVBoxLayout()
        states.addLayout(state_a)
        states.addLayout(state_b)
        states.addLayout(state_c)
        states.addLayout(state_d)
        states.addWidget(self.clear_states_button)
        states_frame = QFrame()
        states_frame.setLayout(states)
        states_scrollable = QScrollArea()
        states_scrollable.setWidget(states_frame)
        states_scrollable_layout = QHBoxLayout()
        states_scrollable_layout.addWidget(states_scrollable)
        states_box = QFrame()
        states_box.setLayout(states_scrollable_layout)
        states_box.setStyleSheet("""
                background-color: #8d949c;
                border-radius: 10px;
                border-color: pink;
                color: black;
                font: 14px;
                height: 1em;
                max-width: 30em;
            """)

        processing_options = QVBoxLayout()
        processing_options.addLayout(bandpower_selection)
        processing_options.addWidget(relative_plot_checkbox)
        processing_options.addWidget(sixty_hz_filter_checkbox)
        processing_options.addWidget(zero_to_five_hz_filter_checkbox)
        processing_options.addLayout(frequency_range_selection)
        processing_options.addLayout(electrode_selection)

        processing_box = QFrame()
        processing_box.setLayout(processing_options)
        processing_box.setStyleSheet("""
                        background-color: #8d949c;
                        border-radius: 10px;
                        border-color: pink;
                        color: black;
                        font: 14px;
                        height: 1em;
                        max-width: 30em;
                    """)

        input_layout = QGridLayout()
        input_layout.addWidget(data_recording_title, 0, 0)
        input_layout.addWidget(states_box, 1, 0)
        input_layout.addWidget(data_processing_title, 2, 0)
        input_layout.addWidget(processing_box, 3, 0)
        # input_layout.addWidget(relative_plot_checkbox, 4, 0)
        # input_layout.addWidget(sixty_hz_filter_checkbox, 5, 0)
        # input_layout.addWidget(zero_to_five_hz_filter_checkbox, 6, 0)
        # input_layout.addLayout(frequency_range_selection, 7, 0)
        # input_layout.addLayout(electrode_selection, 8, 0)

        # ############## #
        # Output Section #
        # ############## #

        # State A/B Graph #

        self.graph = Graph(self, self.parent)

        # Rescale graph button #

        rescale_graph_button = make_button("Rescale Graph")
        rescale_graph_button.pressed.connect(self.rescale_graph)

        self.graph_w = QVBoxLayout()
        self.graph_w.addWidget(self.graph)
        self.graph_w.addWidget(rescale_graph_button)

        # State A Information #

        self.a_title_w = make_label("State A")
        # self.a_title_w.setStyleSheet("""color: #fff;font-size: 15px;""")

        self.a_frequency_spacing_w = make_label("Frequency Bin Spacing (Hz): N/A")
        self.a_delta_w = make_label("Delta Relative Power: N/A")
        self.a_theta_w = make_label("Theta Relative Power: N/A")
        self.a_alpha_w = make_label("Alpha Relative Power: N/A")
        self.a_beta_w = make_label("Beta Relative Power: N/A")
        self.a_gamma_w = make_label("Gamma Relative Power: N/A")

        a_output_information = QVBoxLayout()
        a_output_information.addWidget(self.a_title_w)
        a_output_information.addWidget(self.a_frequency_spacing_w)
        a_output_information.addWidget(self.a_delta_w)
        a_output_information.addWidget(self.a_theta_w)
        a_output_information.addWidget(self.a_alpha_w)
        a_output_information.addWidget(self.a_beta_w)
        a_output_information.addWidget(self.a_gamma_w)

        # State B Information #

        self.b_title_w = make_label("State B")

        self.b_frequency_spacing_w = make_label("Frequency Bin Spacing (Hz): N/A")

        self.b_delta_w = make_label("Delta Relative Power: N/A")
        self.b_theta_w = make_label("Theta Relative Power: N/A")
        self.b_alpha_w = make_label("Alpha Relative Power: N/A")
        self.b_beta_w = make_label("Beta Relative Power: N/A")
        self.b_gamma_w = make_label("Gamma Relative Power: N/A")

        b_output_information = QVBoxLayout()
        b_output_information.addWidget(self.b_title_w)
        b_output_information.addWidget(self.b_frequency_spacing_w)
        b_output_information.addWidget(self.b_delta_w)
        b_output_information.addWidget(self.b_theta_w)
        b_output_information.addWidget(self.b_alpha_w)
        b_output_information.addWidget(self.b_beta_w)
        b_output_information.addWidget(self.b_gamma_w)

        # Output Section Layout #

        # Bandpower Graph

        self.state_graph_frame = QFrame()
        self.state_graph_frame.setLayout(self.graph_w)

        # Live Bandpowers

        self.unknown_pleasures = UnknownPleasuresWidget(self.parent)
        self.state_detection = StateDetectionWidget(self.parent)
        self.bandpower_stats = make_label("Bandpower stats")
        self.bandpower_stats = QTableWidget(4, 5)
        self.bandpower_stats.setStyleSheet("""
            background-color: #103650;
            border-width: 5px;
            border-color: black;
            color: #e3ebec;
            font: 14px;
        """)
        delta_header = QTableWidgetItem()
        delta_header.setData(Qt.DisplayRole, "Delta (0-4)")
        self.bandpower_stats.setHorizontalHeaderItem(0, delta_header)
        theta_header = QTableWidgetItem()
        theta_header.setData(Qt.DisplayRole, "Theta (4-7)")
        self.bandpower_stats.setHorizontalHeaderItem(1, theta_header)
        alpha_header = QTableWidgetItem()
        alpha_header.setData(Qt.DisplayRole, "Alpha (7-12)")
        self.bandpower_stats.setHorizontalHeaderItem(2, alpha_header)
        beta_header = QTableWidgetItem()
        beta_header.setData(Qt.DisplayRole, "Beta (12-30)")
        self.bandpower_stats.setHorizontalHeaderItem(3, beta_header)
        gamma_header = QTableWidgetItem()
        gamma_header.setData(Qt.DisplayRole, "Gamma (30-50)")
        self.bandpower_stats.setHorizontalHeaderItem(4, gamma_header)
        a_header = QTableWidgetItem()
        a_header.setData(Qt.DisplayRole, "State A")
        self.bandpower_stats.setVerticalHeaderItem(0, a_header)
        b_header = QTableWidgetItem()
        b_header.setData(Qt.DisplayRole, "State B")
        self.bandpower_stats.setVerticalHeaderItem(1, b_header)
        c_header = QTableWidgetItem()
        c_header.setData(Qt.DisplayRole, "State C")
        self.bandpower_stats.setVerticalHeaderItem(2, c_header)
        d_header = QTableWidgetItem()
        d_header.setData(Qt.DisplayRole, "State D")
        self.bandpower_stats.setVerticalHeaderItem(3, d_header)

        for i in range(4):
            for j in range(5):
                table_item = QTableWidgetItem()
                table_item.setData(Qt.DisplayRole, "0")
                self.bandpower_stats.setItem(i, j, table_item)

        self.output_bins_button = make_button("Output frequency bins")
        self.output_bins_button.pressed.connect(self.output_bins_button_pressed)
        self.output_bins_button.released.connect(self.output_bins_button_released)

        self.stats_layout = QVBoxLayout()
        self.stats_layout.addWidget(self.bandpower_stats)
        self.stats_layout.addWidget(self.output_bins_button)
        self.stats_frame = QFrame()
        self.stats_frame.setLayout(self.stats_layout)


        # self.bandpower_stats.setStyleSheet("""
        #     background-color: light gray;
        #     border-width: 5px;
        #     border-color: black;
        #     color: #e3ebec;
        #     font: 14px;
        #     height: 1em;
        #     max-width: 30em;
        #     padding: 6px;
        #     margin: 1em 0;
        # """)
        self.live_timeseries = make_label("Live timeseries")


        self.output_stack = QStackedLayout()
        self.output_stack.addWidget(self.state_graph_frame)
        self.output_stack.addWidget(self.stats_frame)
        self.output_stack.addWidget(self.state_detection)
        self.output_stack.addWidget(self.unknown_pleasures)

        # ############ #
        # Macro Layout #
        # ############ #

        self.output_options = ['Bandpower Graph', 'Bandpower Statistics', 'Live State Detection', 'Live Timeseries']
        self.selected_output_option = self.output_options[0]

        output_options_list = QComboBox()
        output_options_list.addItems(self.output_options)
        output_options_list.setStyleSheet("""background-color: gray; color: #fff; font: 20px;
                                             height: 1em;""")
        output_options_list.setCurrentIndex(0)
        output_options_list.currentIndexChanged.connect(self.set_output_option)

        title = QLabel("Record and Compare Bandpowers")
        title.setStyleSheet("""
            background-color: light gray;
            border-width: 5px;
            border-color: black;
            color: #e3ebec;
            font: 30px;
            height: 1em;
            max-width: 30em;
            padding: 6px;

        """)
        title.setAlignment(Qt.AlignHCenter)
        self.home_button = make_button("Home")
        self.home_button.pressed.connect(self.home_button_pressed)
        self.home_button.released.connect(self.home_button_released)

        # Layout

        layout = QGridLayout()
        layout.addWidget(self.home_button, 0, 0)
        layout.addWidget(output_options_list, 0, 1)
        layout.addLayout(input_layout, 1, 0)
        layout.addLayout(self.output_stack, 1, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)

        self.setLayout(layout)

    def pressed_record_a(self):
        self.a_record_button.setText("Recording...")
        self.a_timer.start(self.a_record_time * 1000)

    def record_a(self):
        num_data_points = self.parent.sampling_rate * self.a_record_time
        print('recording state a')
        self.a_record_button.setText("Record State A")
        self.a_data = self.parent.board_shim.get_current_board_data(num_samples=num_data_points)[1:9]
        self.plot_state[0] = True
        self.process_bp()
        pd.DataFrame(np.transpose(self.a_data)).to_csv('state_raw_data/a_data.csv')

    def pressed_record_b(self):
        self.b_record_button.setText("Recording...")
        self.b_timer.start(self.b_record_time * 1000)

    def record_b(self):
        num_data_points = self.parent.sampling_rate * self.b_record_time
        print('recording state b')
        self.b_record_button.setText("Record State B")
        self.b_data = self.parent.board_shim.get_current_board_data(num_samples=num_data_points)[1:9]
        self.plot_state[1] = True
        self.process_bp()
        pd.DataFrame(np.transpose(self.b_data)).to_csv('state_raw_data/b_data.csv')

    def pressed_record_c(self):
        self.c_record_button.setText("Recording...")
        self.c_timer.start(self.c_record_time * 1000)

    def record_c(self):
        num_data_points = self.parent.sampling_rate * self.c_record_time
        print('recording state c')
        self.c_record_button.setText("Record State C")
        self.c_data = self.parent.board_shim.get_current_board_data(num_samples=num_data_points)[1:9]
        self.plot_state[2] = True
        self.process_bp()
        pd.DataFrame(np.transpose(self.c_data)).to_csv('state_raw_data/c_data.csv')

    def pressed_record_d(self):
        self.d_record_button.setText("Recording...")
        self.d_timer.start(self.d_record_time * 1000)

    def record_d(self):
        num_data_points = self.parent.sampling_rate * self.d_record_time
        print('recording state d')
        self.d_record_button.setText("Record State D")
        self.d_data = self.parent.board_shim.get_current_board_data(num_samples=num_data_points)[1:9]
        self.plot_state[3] = True
        self.process_bp()
        pd.DataFrame(np.transpose(self.d_data)).to_csv('state_raw_data/d_data.csv')

    def set_a_record_time(self, seconds):
        self.a_record_time = int(seconds)
        print(self.a_record_time)

    def set_b_record_time(self, seconds):
        self.b_record_time = int(seconds)
        print(self.b_record_time)

    def set_c_record_time(self, seconds):
        self.c_record_time = int(seconds)
        print(self.c_record_time)

    def set_d_record_time(self, seconds):
        self.d_record_time = int(seconds)
        print(self.d_record_time)

    def set_bp_method(self, i):
        self.bp_processing.selected_bp_method = self.bp_processing.bp_methods[i]
        print(self.bp_processing.selected_bp_method)
        self.process_bp()

    def set_relative_plot(self, i):
        if i == 0:
            self.bp_processing.relative = False
        else:
            self.bp_processing.relative = True
        print(self.bp_processing.relative)
        self.process_bp()
        self.rescale_graph()

    def set_sixty_hz_filter(self, i):
        if i == 0:
            self.bp_processing.filter_sixty_hz = False
        else:
            self.bp_processing.filter_sixty_hz = True
        print(self.bp_processing.filter_sixty_hz)
        self.process_bp()

    def set_zero_to_five_hz_filter(self, i):
        if i == 0:
            self.bp_processing.filter_zero_to_five_hz = False
        else:
            self.bp_processing.filter_zero_to_five_hz = True
        print(self.bp_processing.filter_zero_to_five_hz)
        self.process_bp()

    def toggle_custom_frequency(self, i):
        if int(i) == 1:
            self.bp_processing.include_all_frequencies = True
        else:
            self.bp_processing.include_all_frequencies = False
        print(self.bp_processing.include_all_frequencies)
        self.process_bp()
        self.rescale_graph()

    def set_low_frequency(self, low):
        if low == "":
            self.bp_processing.custom_low_frequency = 0
        else:
            self.bp_processing.custom_low_frequency = int(low)
        print(self.bp_processing.custom_low_frequency)
        self.process_bp()
        if not self.bp_processing.include_all_frequencies:
            self.rescale_graph()

    def set_high_frequency(self, high):
        if high == "":
            self.bp_processing.custom_high_frequency = 120
        else:
            self.bp_processing.custom_high_frequency = int(high)
        print(self.bp_processing.custom_high_frequency)
        self.process_bp()
        if not self.bp_processing.include_all_frequencies:
            self.rescale_graph()

    def toggle_all_electrodes(self, i):
        if i == 1:
            self.bp_processing.include_all_electrodes = True
        else:
            self.bp_processing.include_all_electrodes = False
        print(self.bp_processing.include_all_electrodes)
        self.process_bp()

    def select_custom_electrode(self, electrode_num):
        if electrode_num in self.bp_processing.custom_electrode_selection:
            self.bp_processing.custom_electrode_selection.remove(electrode_num)
        else:
            self.bp_processing.custom_electrode_selection.append(electrode_num)
            self.bp_processing.custom_electrode_selection.sort()
        print(self.bp_processing.custom_electrode_selection)
        self.process_bp()

    def rescale_graph(self):
        self.graph.p.autoRange()

    # Processes the bandpower for states a and b given the current settings, updates gui
    def process_bp(self):

        if self.plot_state[0] is True:
            self.a_frequencies, self.a_processed_bp, self.a_standard_band_values = \
                self.bp_processing.process_state(self.a_data)
        if self.plot_state[1] is True:
            self.b_frequencies, self.b_processed_bp, self.b_standard_band_values = \
                self.bp_processing.process_state(self.b_data)
        if self.plot_state[2] is True:
            self.c_frequencies, self.c_processed_bp, self.c_standard_band_values = \
                self.bp_processing.process_state(self.c_data)
        if self.plot_state[3] is True:
            self.d_frequencies, self.d_processed_bp, self.d_standard_band_values = \
                self.bp_processing.process_state(self.d_data)

        self.graph.clear_plots()

        if self.plot_state[0] is True:
            self.graph.plot_a(self.a_frequencies, self.a_processed_bp)
        if self.plot_state[1] is True:
            self.graph.plot_b(self.b_frequencies, self.b_processed_bp)
        if self.plot_state[2] is True:
            self.graph.plot_c(self.c_frequencies, self.c_processed_bp)
        if self.plot_state[3] is True:
            self.graph.plot_d(self.d_frequencies, self.d_processed_bp)


        # # Get bandpowers
        # self.a_frequencies, self.a_processed_bp, self.a_standard_band_values = \
        #     self.bp_processing.process_state(self.a_data)
        # self.b_frequencies, self.b_processed_bp, self.b_standard_band_values = \
        #     self.bp_processing.process_state(self.b_data)
        #
        # # Plot frequencies vs bandpowers
        # self.graph.clear_plots()
        # self.graph.plot_a(self.a_frequencies, self.a_processed_bp)
        # self.graph.plot_b(self.b_frequencies, self.b_processed_bp)

        # Update output
        self.update_output_information()

    def update_output_information(self):
        # self.a_title_w.setText("State A (Recorded " + str(self.a_record_time) + " seconds of data)")
        # self.a_frequency_spacing_w.setText("Frequency Bin Spacing (Hz): "
        #                                    + str(round(self.a_frequencies[1] - self.a_frequencies[0], 3)))
        # self.a_delta_w.setText("Delta Relative Power: " + str(round(self.a_standard_band_values[0], 3)))
        # self.a_theta_w.setText("Theta Relative Power: " + str(round(self.a_standard_band_values[1], 3)))
        # self.a_alpha_w.setText("Alpha Relative Power: " + str(round(self.a_standard_band_values[2], 3)))
        # self.a_beta_w.setText("Beta Relative Power: " + str(round(self.a_standard_band_values[3], 3)))
        # self.a_gamma_w.setText("Gamma Relative Power: " + str(round(self.a_standard_band_values[4], 3)))
        #
        # self.b_title_w.setText("State B (Recorded " + str(self.b_record_time) + " seconds of data)")
        # self.b_frequency_spacing_w.setText("Frequency Bin Spacing (Hz): "
        #                                    + str(round(self.b_frequencies[1] - self.b_frequencies[0], 3)))
        #
        # self.b_delta_w.setText("Delta Relative Power: " + str(round(self.b_standard_band_values[0], 3)))
        # self.b_theta_w.setText("Theta Relative Power: " + str(round(self.b_standard_band_values[1], 3)))
        # self.b_alpha_w.setText("Alpha Relative Power: " + str(round(self.b_standard_band_values[2], 3)))
        # self.b_beta_w.setText("Beta Relative Power: " + str(round(self.b_standard_band_values[3], 3)))
        # self.b_gamma_w.setText("Gamma Relative Power: " + str(round(self.b_standard_band_values[4], 3)))

        if self.plot_state[0] is True:
            for j in range(5):
                print('adding')
                table_item = QTableWidgetItem()
                table_item.setData(Qt.DisplayRole, str(round(self.a_standard_band_values[j], 3)))
                self.bandpower_stats.setItem(0, j, table_item)
        if self.plot_state[1] is True:
            for j in range(5):
                table_item = QTableWidgetItem()
                table_item.setData(Qt.DisplayRole, str(round(self.b_standard_band_values[j], 3)))
                self.bandpower_stats.setItem(1, j, table_item)
        if self.plot_state[2] is True:
            for j in range(5):
                table_item = QTableWidgetItem()
                table_item.setData(Qt.DisplayRole, str(round(self.c_standard_band_values[j], 3)))
                self.bandpower_stats.setItem(2, j, table_item)
        if self.plot_state[3] is True:
            for j in range(5):
                table_item = QTableWidgetItem()
                table_item.setData(Qt.DisplayRole, str(round(self.d_standard_band_values[j], 3)))
                self.bandpower_stats.setItem(3, j, table_item)

    def home_button_pressed(self):
        self.home_button.setStyleSheet("""
            background-color: #284351;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: #e3ebec;
            color: white;
            font: 14px;
            height: 1em;
            max-width: 30em;
            padding: 6px;
            margin: 1em 0;
        """)

    def home_button_released(self):
        self.home_button.setStyleSheet("""
            background-color: #73787c;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: #e3ebec;
            color: white;
            font: 14px;
            height: 1em;
            max-width: 30em;
            padding: 6px;
            margin: 1em 0;
        """)
        self.parent.change_page_index(0)

    def set_output_option(self, i):
        self.output_stack.setCurrentIndex(i)
        # self.selected_output_option = self.output_options[i]
        # # Need to update output
        # if self.selected_output_option == self.output_options[0]:
        #     self.output_frame.setLayout(self.graph_w)
        #     self.output_stack.setCurrentIndex(0)
        # elif self.selected_output_option == self.output_options[1]:
        #     self.output_frame.setWidget(QLabel("Hello"))
        # elif self.selected_output_option == self.output_options[3]:
        #     self.output_frame.setLayout(self.state_detection_l)

    def clear_states_button_pressed(self):
        self.home_button.setStyleSheet("""
            background-color: #284351;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: #e3ebec;
            color: white;
            font: 14px;
            height: 1em;
            max-width: 30em;
            padding: 6px;
            margin: 1em 0;
        """)

    def clear_states_button_released(self):
        self.home_button.setStyleSheet("""
            background-color: #73787c;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: #e3ebec;
            color: white;
            font: 14px;
            height: 1em;
            max-width: 30em;
            padding: 6px;
            margin: 1em 0;
        """)
        # Plotting info
        self.plot_state = [False, False, False, False]  # a, b, c, d

        # Processed data variables
        self.a_processed_bp = None
        self.b_processed_bp = None
        self.c_processed_bp = None
        self.d_processed_bp = None
        self.a_frequencies = [0, 0]
        self.b_frequencies = [0, 0]
        self.c_frequencies = [0, 0]
        self.d_frequencies = [0, 0]

        self.a_standard_band_values = [0, 0, 0, 0, 0]
        self.b_standard_band_values = [0, 0, 0, 0, 0]
        self.c_standard_band_values = [0, 0, 0, 0, 0]
        self.d_standard_band_values = [0, 0, 0, 0, 0]

        for i in range(4):
            for j in range(5):
                table_item = QTableWidgetItem()
                table_item.setData(Qt.DisplayRole, "0")
                self.bandpower_stats.setItem(i, j, table_item)

        self.graph.clear_plots()

    def output_bins_button_pressed(self):
        self.output_bins_button.setStyleSheet("""
            background-color: #284351;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: #e3ebec;
            color: white;
            font: 14px;
            height: 1em;
            max-width: 30em;
            padding: 6px;
            margin: 1em 0;
        """)

    def output_bins_button_released(self):
        self.output_bins_button.setStyleSheet("""
            background-color: #73787c;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: #e3ebec;
            color: white;
            font: 14px;
            height: 1em;
            max-width: 30em;
            padding: 6px;
            margin: 1em 0;
        """)

        # Build csv

        index = []
        columns = []
        if self.plot_state[0] is True:
            columns = self.a_frequencies
        elif self.plot_state[1] is True:
            columns = self.b_frequencies
        elif self.plot_state[2] is True:
            columns = self.c_frequencies
        elif self.plot_state[3] is True:
            columns = self.d_frequencies

        data = []
        if self.plot_state[0] is True:
            data.append(self.a_processed_bp)
            index.append("State A")
        if self.plot_state[1] is True:
            data.append(self.b_processed_bp)
            index.append("State B")
        if self.plot_state[2] is True:
            data.append(self.c_processed_bp)
            index.append("State C")
        if self.plot_state[3] is True:
            data.append(self.d_processed_bp)
            index.append("State D")

        pd.DataFrame(data=data, index=index, columns=columns).to_csv("Frequency bins.csv")





class Graph(pg.GraphicsLayoutWidget):

    def __init__(self, plotSelf, parentSelf):
        self.plotSelf = plotSelf
        self.parentSelf = parentSelf
        super().__init__()
        self.p = self.addPlot(row=0, col=0)
        self.legend = self.p.addLegend()

    def plot_a(self, x, y):
        plot_item = self.p.plot(x, y, pen=pg.mkPen(color=(45, 201, 55)))
        self.legend.addItem(plot_item, "State A")

    def plot_b(self, x, y):
        plot_item = self.p.plot(x, y, pen=pg.mkPen(color=(231, 180, 22)))
        self.legend.addItem(plot_item, "State B")

    def plot_c(self, x, y):
        plot_item = self.p.plot(x, y, pen=pg.mkPen(color=(219, 123, 43)))
        self.legend.addItem(plot_item, "State C")

    def plot_d(self, x, y):
        plot_item = self.p.plot(x, y, pen=pg.mkPen(color=(204, 50, 50)))
        self.legend.addItem(plot_item, "State D")

    def clear_plots(self):
        self.p.clear()
