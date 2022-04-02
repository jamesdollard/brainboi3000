
import time

import PySide6.QtCore
import numpy as np
import pandas as pd
import pyqtgraph as pg
from PySide6.QtCore import Qt
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
    QRadioButton
)


# Enables user to capture and compare the bandpower of two recording sessions
class ABBandpowerWidget(QWidget):

    def __init__(self, parent):

        # ** CLASS VARIABLE INITIALIZATION ** #

        super().__init__()
        self.parent = parent

        # Data gathering variables
        self.a_record_time = 0
        self.b_record_time = 0
        self.a_data = None
        self.b_data = None

        # Bandpower processing
        self.bp_processing = parent.bp_processing

        # Processed data variables
        self.a_processed_bp = None
        self.b_processed_bp = None
        self.a_frequencies = [0, 0]
        self.b_frequencies = [0, 0]

        self.a_standard_band_values = [0, 0, 0, 0, 0]
        self.b_standard_band_values = [0, 0, 0, 0, 0]

        # Timers
        self.a_timer = PySide6.QtCore.QTimer()
        self.a_timer.setSingleShot(True)
        self.a_timer.timeout.connect(self.record_a)
        self.b_timer = PySide6.QtCore.QTimer()
        self.b_timer.setSingleShot(True)
        self.b_timer.timeout.connect(self.record_b)

        # ** WIDGET CONSTRUCTION ** #

        # ############# #
        # Input Section #
        # ############# #

        # State A #

        a_record_time_label = QLabel("State A Record Time (s): ")
        a_record_time_label.setStyleSheet("""color: #fff; font-size: 15px;""")

        a_record_time_input = QLineEdit()
        a_record_time_input.setPlaceholderText("0")
        a_record_time_input.setMaxLength(2)
        a_record_time_input.textChanged.connect(self.set_a_record_time)
        a_record_time_input.setStyleSheet("""background-color: #fff; color: #000;font: 15px; min-width: 30px;
                                             margin-bottom: 0px;  padding: 5px; max-width: 30px;""")

        self.a_record_button = QPushButton("Record State A")
        self.a_record_button.pressed.connect(self.pressed_record_a)
        # self.a_record_button.released.connect(self.record_a)
        self.a_record_button.setStyleSheet("""
            border-image: none !important;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            color: #fff;
            font-size: 15px;
        """)

        state_a = QHBoxLayout()
        state_a.addWidget(a_record_time_label)
        state_a.addWidget(a_record_time_input)
        state_a.addWidget(self.a_record_button)

        # State B #

        b_record_time_label = QLabel("State B Record Time (s): ")
        b_record_time_label.setStyleSheet("""color: #fff; font-size: 15px;""")

        b_record_time_input = QLineEdit()
        b_record_time_input.setPlaceholderText("0")
        b_record_time_input.setMaxLength(2)
        b_record_time_input.textChanged.connect(self.set_b_record_time)
        b_record_time_input.setStyleSheet("""background-color: #fff; color: #000;font: 15px; min-width: 30px;
                                             margin-bottom: 0px; max-width: 30px; padding: 5px;""")

        self.b_record_button = QPushButton("Record State B")
        self.b_record_button.pressed.connect(self.record_b_pressed)
        # self.b_record_button.released.connect(self.record_b)
        self.b_record_button.setStyleSheet("""
            border-image: none !important;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            color: #fff;
            font-size: 15px;
        """)

        state_b = QHBoxLayout()
        state_b.addWidget(b_record_time_label)
        state_b.addWidget(b_record_time_input)
        state_b.addWidget(self.b_record_button)

        # Bandpower Selection #

        bp_label = QLabel("Bandpower processing method: ")
        bp_label.setStyleSheet("""color: #fff; font-size: 15px;""")

        bp_method_list = QComboBox()
        bp_method_list.addItems(self.bp_processing.bp_methods)
        bp_method_list.setCurrentIndex(0)
        bp_method_list.setStyleSheet("""background-color: gray; color: #fff; min-width: 50px; max-width: 150px;""")
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
        custom_frequencies_high.setPlaceholderText("125")
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

        custom_frequencies_label = QLabel("Set custom frequency range")
        custom_frequencies_label.setStyleSheet("""color: #fff; font-size: 15px;""")

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
        data_recording_title = QLabel("Record Data")
        data_recording_title.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        data_recording_title.setStyleSheet("""color: #fff;font-size: 15px;""")
        data_processing_title = QLabel("Data Processing Options")
        data_processing_title.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        data_processing_title.setStyleSheet("""color: #fff;font-size: 15px;""")

        input_layout = QGridLayout()
        input_layout.addWidget(data_recording_title, 0, 0)
        input_layout.addLayout(state_a, 1, 0)
        input_layout.addLayout(state_b, 2, 0)
        input_layout.addWidget(data_processing_title, 3, 0)
        input_layout.addLayout(bandpower_selection, 4, 0)
        input_layout.addWidget(relative_plot_checkbox, 5, 0)
        input_layout.addWidget(sixty_hz_filter_checkbox, 6, 0)
        input_layout.addWidget(zero_to_five_hz_filter_checkbox, 7, 0)
        input_layout.addLayout(frequency_range_selection, 8, 0)
        input_layout.addLayout(electrode_selection, 9, 0)

        # ############## #
        # Output Section #
        # ############## #

        # State A/B Graph #

        self.graph = Graph(self, self.parent)

        # Rescale graph button #

        rescale_graph_button = QPushButton("Rescale Graph")
        rescale_graph_button.pressed.connect(self.rescale_graph)
        rescale_graph_button.setStyleSheet("""
            border-image: none !important;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            color: #fff;
            font-size: 15px;
        """)

        graph_w = QVBoxLayout()
        graph_w.addWidget(self.graph)
        graph_w.addWidget(rescale_graph_button)

        # State A Information #

        self.a_title_w = QLabel("State A")
        self.a_title_w.setStyleSheet("""color: #fff;font-size: 15px;""")

        self.a_frequency_spacing_w = QLabel("Frequency Bin Spacing (Hz): N/A")
        self.a_frequency_spacing_w.setStyleSheet("""color: #fff;font-size: 15px;""")

        self.a_delta_w = QLabel("Delta Relative Power: N/A")
        self.a_delta_w.setStyleSheet("""color: #fff;font-size: 15px;""")
        self.a_theta_w = QLabel("Theta Relative Power: N/A")
        self.a_theta_w.setStyleSheet("""color: #fff;font-size: 15px;""")
        self.a_alpha_w = QLabel("Alpha Relative Power: N/A")
        self.a_alpha_w.setStyleSheet("""color: #fff;font-size: 15px;""")
        self.a_beta_w = QLabel("Beta Relative Power: N/A")
        self.a_beta_w.setStyleSheet("""color: #fff;font-size: 15px;""")
        self.a_gamma_w = QLabel("Gamma Relative Power: N/A")
        self.a_gamma_w.setStyleSheet("""color: #fff;font-size: 15px;""")

        a_output_information = QVBoxLayout()
        a_output_information.addWidget(self.a_title_w)
        a_output_information.addWidget(self.a_frequency_spacing_w)
        a_output_information.addWidget(self.a_delta_w)
        a_output_information.addWidget(self.a_theta_w)
        a_output_information.addWidget(self.a_alpha_w)
        a_output_information.addWidget(self.a_beta_w)
        a_output_information.addWidget(self.a_gamma_w)

        # State B Information #

        self.b_title_w = QLabel("State B")
        self.b_title_w.setStyleSheet("""color: #fff;font-size: 15px;""")

        self.b_frequency_spacing_w = QLabel("Frequency Bin Spacing (Hz): N/A")
        self.b_frequency_spacing_w.setStyleSheet("""color: #fff;font-size: 15px;""")

        self.b_delta_w = QLabel("Delta Relative Power: N/A")
        self.b_delta_w.setStyleSheet("""color: #fff;font-size: 15px;""")
        self.b_theta_w = QLabel("Theta Relative Power: N/A")
        self.b_theta_w.setStyleSheet("""color: #fff;font-size: 15px;""")
        self.b_alpha_w = QLabel("Alpha Relative Power: N/A")
        self.b_alpha_w.setStyleSheet("""color: #fff;font-size: 15px;""")
        self.b_beta_w = QLabel("Beta Relative Power: N/A")
        self.b_beta_w.setStyleSheet("""color: #fff;font-size: 15px;""")
        self.b_gamma_w = QLabel("Gamma Relative Power: N/A")
        self.b_gamma_w.setStyleSheet("""color: #fff;font-size: 15px;""")

        b_output_information = QVBoxLayout()
        b_output_information.addWidget(self.b_title_w)
        b_output_information.addWidget(self.b_frequency_spacing_w)
        b_output_information.addWidget(self.b_delta_w)
        b_output_information.addWidget(self.b_theta_w)
        b_output_information.addWidget(self.b_alpha_w)
        b_output_information.addWidget(self.b_beta_w)
        b_output_information.addWidget(self.b_gamma_w)

        # Output Section Layout #

        output_information = QGridLayout()
        output_information.addLayout(a_output_information, 0, 0)
        output_information.addLayout(b_output_information, 1, 0)

        output_layout = QGridLayout()
        output_layout.addLayout(graph_w, 0, 0)
        output_layout.addLayout(output_information, 0, 1)

        output_layout.setColumnStretch(0, 3)
        output_layout.setColumnStretch(1, 1)

        # ############ #
        # Macro Layout #
        # ############ #

        title = QLabel("Record and Compare Bandpowers in Two States")
        title.setAlignment(Qt.AlignHCenter)
        title.setStyleSheet("""color: #fff; font-size: 15px;""")

        # Layout

        layout = QGridLayout()
        layout.addLayout(input_layout, 0, 0)
        layout.addLayout(output_layout, 0, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)

        self.setLayout(layout)

    def pressed_record_a(self):
        self.a_record_button.setText("Recording...")
        # self.parent.timer.start(self.a_record_time * 1000)
        self.a_timer.start(self.a_record_time * 1000)

    def record_a(self):
        self.parent.timer.stop()
        num_data_points = self.parent.sampling_rate * self.a_record_time
        print('recording state a')
        self.a_record_button.setText("Record State A")
        self.a_data = self.parent.board_shim.get_current_board_data(num_samples=num_data_points)[1:9]
        if self.a_data is not None and self.b_data is not None:
            self.process_bp()
        pd.DataFrame(np.transpose(self.a_data)).to_csv('state_raw_data/a_data.csv')

    def record_b_pressed(self):
        self.b_record_button.setText("Recording...")
        self.parent.timer.timeout.connect(self.record_b)
        self.parent.timer.start(self.b_record_time * 1000)

    def record_b(self):
        self.parent.timer.stop()
        num_data_points = self.parent.sampling_rate * self.b_record_time
        print('recording state b')
        self.b_record_button.setText("Record State B")
        self.b_data = self.parent.board_shim.get_current_board_data(num_samples=num_data_points)[1:9]
        if self.a_data is not None and self.b_data is not None:
            self.process_bp()
        pd.DataFrame(np.transpose(self.b_data)).to_csv('state_raw_data/b_data.csv')

    def set_a_record_time(self, seconds):
        self.a_record_time = int(seconds)
        print(self.a_record_time)

    def set_b_record_time(self, seconds):
        self.b_record_time = int(seconds)
        print(self.b_record_time)

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
            self.bp_processing.custom_high_frequency = 125
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
        # Get bandpowers
        self.a_frequencies, self.a_processed_bp, self.a_standard_band_values = \
            self.bp_processing.process_state(self.a_data)
        self.b_frequencies, self.b_processed_bp, self.b_standard_band_values = \
            self.bp_processing.process_state(self.b_data)

        # Plot frequencies vs bandpowers
        self.graph.clear_plots()
        self.graph.plot_a(self.a_frequencies, self.a_processed_bp)
        self.graph.plot_b(self.b_frequencies, self.b_processed_bp)

        # Update output
        self.update_output_information()

    def update_output_information(self):
        self.a_title_w.setText("State A (Recorded " + str(self.a_record_time) + " seconds of data)")
        self.a_frequency_spacing_w.setText("Frequency Bin Spacing (Hz): "
                                           + str(round(self.a_frequencies[1] - self.a_frequencies[0], 3)))
        self.a_delta_w.setText("Delta Relative Power: " + str(round(self.a_standard_band_values[0], 3)))
        self.a_theta_w.setText("Theta Relative Power: " + str(round(self.a_standard_band_values[1], 3)))
        self.a_alpha_w.setText("Alpha Relative Power: " + str(round(self.a_standard_band_values[2], 3)))
        self.a_beta_w.setText("Beta Relative Power: " + str(round(self.a_standard_band_values[3], 3)))
        self.a_gamma_w.setText("Gamma Relative Power: " + str(round(self.a_standard_band_values[4], 3)))

        self.b_title_w.setText("State B (Recorded " + str(self.b_record_time) + " seconds of data)")
        self.b_frequency_spacing_w.setText("Frequency Bin Spacing (Hz): "
                                           + str(round(self.b_frequencies[1] - self.b_frequencies[0], 3)))

        self.b_delta_w.setText("Delta Relative Power: " + str(round(self.b_standard_band_values[0], 3)))
        self.b_theta_w.setText("Theta Relative Power: " + str(round(self.b_standard_band_values[1], 3)))
        self.b_alpha_w.setText("Alpha Relative Power: " + str(round(self.b_standard_band_values[2], 3)))
        self.b_beta_w.setText("Beta Relative Power: " + str(round(self.b_standard_band_values[3], 3)))
        self.b_gamma_w.setText("Gamma Relative Power: " + str(round(self.b_standard_band_values[4], 3)))


class Graph(pg.GraphicsLayoutWidget):

    def __init__(self, plotSelf, parentSelf):
        self.plotSelf = plotSelf
        self.parentSelf = parentSelf
        super().__init__()
        self.p = self.addPlot(row=0, col=0)
        self.legend = self.p.addLegend()

    def plot_a(self, x, y):
        plot_item = self.p.plot(x, y, pen=pg.mkPen(color=(0, 138, 0)))
        self.legend.addItem(plot_item, "State A")

    def plot_b(self, x, y):
        plot_item = self.p.plot(x, y, pen=pg.mkPen(color=(200, 138, 0)))
        self.legend.addItem(plot_item, "State B")

    def clear_plots(self):
        self.p.clear()
