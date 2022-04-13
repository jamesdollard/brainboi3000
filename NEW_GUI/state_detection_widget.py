
import time
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


class StateDetectionWidget(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.bp_processing = parent.bp_processing

        self.eeg_band_labels = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]
        self.detection_band = self.eeg_band_labels[0]
        self.comparison_options = ["Less than", "Greater than"]
        self.detection_comparison = self.comparison_options[0]
        self.comparison_value = 0
        self.streaming = False

        self.state_length = 0
        self.record_overlap = 0

        # Detection criteria (detect when *band type* is *less than or greater than* *value*)

        detection_criteria_label = QLabel("Detect when ")
        detection_criteria_label.setStyleSheet("""color: #fff; font-size: 15px;""")

        eeg_bands_list = QComboBox()
        eeg_bands_list.addItems(self.eeg_band_labels)
        eeg_bands_list.setCurrentIndex(0)
        eeg_bands_list.setStyleSheet("""background-color: gray; color: #fff; min-width: 50px; max-width: 150px;""")
        eeg_bands_list.currentIndexChanged.connect(self.set_detection_band)

        detection_comparison_list = QComboBox()
        detection_comparison_list.addItems(self.comparison_options)
        detection_comparison_list.setCurrentIndex(0)
        detection_comparison_list.setStyleSheet("""background-color: gray; color: #fff; min-width: 50px; max-width: 150px;""")
        detection_comparison_list.currentIndexChanged.connect(self.set_detection_comparison)

        comparison_value_edit = QLineEdit()
        comparison_value_edit.setPlaceholderText("0")
        comparison_value_edit.setMaxLength(3)
        comparison_value_edit.textChanged.connect(self.set_comparison_value)
        comparison_value_edit.setStyleSheet("""background-color: #fff; color: #000;font: 15px; min-width: 50px;
                                                     margin-bottom: 0px; max-width: 50px; padding: 5px;""")

        detection_criteria = QHBoxLayout()
        detection_criteria.addWidget(detection_criteria_label)
        detection_criteria.addWidget(eeg_bands_list)
        detection_criteria.addWidget(detection_comparison_list)
        detection_criteria.addWidget(comparison_value_edit)

        # Board refresh settings

        state_length_label = QLabel("State length (s): ")
        state_length_label.setStyleSheet("""color: #fff; font-size: 15px;""")
        state_length_edit = QLineEdit()
        state_length_edit.setPlaceholderText("0")
        state_length_edit.setMaxLength(3)
        state_length_edit.textChanged.connect(self.set_state_length)
        state_length_edit.setStyleSheet("""background-color: #fff; color: #000;font: 15px; min-width: 50px;
                                                     margin-bottom: 0px; max-width: 50px; padding: 5px;""")
        state_length = QHBoxLayout()
        state_length.addWidget(state_length_label)
        state_length.addWidget(state_length_edit)

        record_overlap_label = QLabel("Record overlap (s): ")
        record_overlap_label.setStyleSheet("""color: #fff; font-size: 15px;""")
        record_overlap_edit = QLineEdit()
        record_overlap_edit.setPlaceholderText("0")
        record_overlap_edit.setMaxLength(3)
        record_overlap_edit.textChanged.connect(self.set_record_overlap)
        record_overlap_edit.setStyleSheet("""background-color: #fff; color: #000;font: 15px; min-width: 50px;
                                                         margin-bottom: 0px; max-width: 50px; padding: 5px;""")
        record_overlap = QHBoxLayout()
        record_overlap.addWidget(record_overlap_label)
        record_overlap.addWidget(record_overlap_edit)

        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.pressed.connect(self.toggle_stream)
        # self.start_button.released.connect(self.record_a)
        self.start_stop_button.setStyleSheet("""
                border-image: none !important;
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: beige;
                color: #fff;
                font-size: 15px;
            """)

        live_data_settings = QVBoxLayout()
        live_data_settings.addLayout(state_length)
        live_data_settings.addLayout(record_overlap)
        live_data_settings.addWidget(self.start_stop_button)

        # Live graph

        self.graph = Graph(self, self.parent)
        graph_w = QVBoxLayout()
        graph_w.addWidget(self.graph)

        # Detection Status

        self.detection_status = QLabel("Detection Status: Not Detected")
        self.detection_status.setStyleSheet("""color: #fff; font-size: 15px;""")

        # Create Macro layout

        layout = QGridLayout()
        layout.addLayout(live_data_settings, 0, 0)
        layout.addLayout(detection_criteria, 1, 0)
        layout.addLayout(graph_w, 0, 1)
        layout.addWidget(self.detection_status, 1, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)

        self.setLayout(layout)

    def set_detection_band(self, i):
        self.detection_band = self.eeg_band_labels[i]
        print(self.detection_band)

    def set_detection_comparison(self, i):
        self.detection_comparison = self.comparison_options[i]
        print(self.detection_comparison)

    def set_comparison_value(self, val):
        self.comparison_value = float(val)
        print(self.comparison_value)

    def set_state_length(self, val):
        self.state_length = float(val)
        print(self.state_length)

    def set_record_overlap(self, val):
        self.record_overlap = float(val)
        print(self.record_overlap)

    def analyze_state(self):
        s_data = self.parent.board_shim.get_current_board_data(int(self.state_length * self.parent.sampling_rate))

        s_frequencies, s_processed_bp, s_standard_band_values = \
            self.bp_processing.process_state(s_data)
        band_idx = self.eeg_band_labels.index(self.detection_band)
        s_band_value = s_standard_band_values[band_idx]

        if self.detection_comparison == "Less than":
            if s_band_value < self.comparison_value:
                self.detection_status.setText("Detection Status: Detected")
            else:
                self.detection_status.setText("Detection Status: Not Detected")
        else:
            if s_band_value > self.comparison_value:
                self.detection_status.setText("Detection Status: Detected")
            else:
                self.detection_status.setText("Detection Status: Not Detected")

        # Plot frequencies vs bandpowers
        self.graph.clear_plots()
        self.graph.plot_s(s_frequencies, s_processed_bp)

    def toggle_stream(self):
        if not self.streaming:
            self.streaming = True
            self.start_stop_button.setText("Stop")
            self.parent.timer.timeout.connect(self.analyze_state)
            self.parent.timer.start(self.record_overlap * 1000)
        else:
            self.streaming = False
            self.start_stop_button.setText("Start")
            self.parent.timer.stop()


class Graph(pg.GraphicsLayoutWidget):

    def __init__(self, plotSelf, parentSelf):
        self.plotSelf = plotSelf
        self.parentSelf = parentSelf
        super().__init__()
        self.p = self.addPlot(row=0, col=0)
        self.legend = self.p.addLegend()

    def plot_s(self, x, y):
        plot_item = self.p.plot(x, y, pen=pg.mkPen(color=(0, 138, 0)))
        self.legend.addItem(plot_item, "Live State")

    def clear_plots(self):
        self.p.clear()
