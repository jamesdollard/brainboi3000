import sys
import argparse
import logging
from PySide6.QtCore import Qt
from pyqtgraph.Qt import QtCore
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QFrame,
)
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter
from brainflow.ml_model import MLModel
from funcs import *

from electrode_connectivity_widget import ElectrodeConnectivityWidget


# Home Page
class HomePage(QWidget):
    def __init__(self, parent):

        # Variable initialization

        super().__init__()
        self.parent = parent

        # Widgets/Layout

        lab_label = QLabel("Brainboi 3000")
        lab_label.setStyleSheet("""
            background-color: light gray;
            border-width: 5px;
            border-color: black;
            color: #e3ebec;
            font: 75px;
        """)
        lab_label.setAlignment(Qt.AlignCenter)

        self.guide_to_eeg_button = make_button("Complete Guide to EEG")
        self.hardware_tutorial_button = make_button("Hardware Tutorial")
        self.brainwave_analysis_button = make_button("Brainwave Analysis")

        self.headset_connection_info = make_label("Headset Disconnected")
        self.make_label_red(self.headset_connection_info)
        self.headset_connect_button = make_button("Connect Headset")
        # headset_contact_info = make_label("Electrode Contact Bad")
        self.headset_contact_button = make_button("Check electrode contact")
        # self.make_label_red(headset_contact_info)
        headset_channels_info = make_label("Number of channels: -")
        headset_refresh_info = make_label("Refresh rate: -")

        # Wire buttons
        self.guide_to_eeg_button.pressed.connect(self.guide_to_eeg_pressed)
        self.guide_to_eeg_button.released.connect(self.guide_to_eeg_released)
        self.hardware_tutorial_button.pressed.connect(self.tutorial_pressed)
        self.hardware_tutorial_button.released.connect(self.tutorial_released)
        self.brainwave_analysis_button.pressed.connect(self.brainwave_analysis_pressed)
        self.brainwave_analysis_button.released.connect(self.brainwave_analysis_released)
        self.headset_connect_button.pressed.connect(self.connect_headset_pressed)
        self.headset_connect_button.released.connect(self.connect_headset_released)
        self.headset_contact_button.pressed.connect(self.fix_electrodes_pressed)
        self.headset_contact_button.released.connect(self.fix_electrodes_released)

        # Home Layout
        buttons = QVBoxLayout()
        buttons.addWidget(self.guide_to_eeg_button)
        buttons.addWidget(self.hardware_tutorial_button)
        buttons.addWidget(self.brainwave_analysis_button)

        headset_status = QVBoxLayout()
        headset_status.addWidget(self.headset_connection_info)
        headset_status.addWidget(self.headset_connect_button)
        # headset_status.addWidget(headset_contact_info)
        headset_status.addWidget(self.headset_contact_button)
        headset_status.addWidget(headset_channels_info)
        headset_status.addWidget(headset_refresh_info)
        headset_status.contentsRect()

        box = QFrame()
        box.setLayout(headset_status)
        box.setStyleSheet("""
            background-color: #8d949c;
            border-width: 10px;
            border-radius: 10px;
            border-color: pink;
            color: black;
            font: 14px;
            height: 1em;
            max-width: 30em;
            padding: 6px;
            margin: 1em 0;
        """)

        home_layout = QGridLayout()
        home_layout.addWidget(lab_label, 0, 0, 1, 2)
        home_layout.addLayout(buttons, 1, 0)
        home_layout.addWidget(box, 1, 1)
        home_layout.setColumnStretch(0, 1)
        home_layout.setColumnStretch(1, 1)

        # # Add layout to main window
        # widget = QWidget()
        # widget.setLayout(home_layout)
        # widget.setStyleSheet("background-color: #103650;")

        self.setLayout(home_layout)

    def make_label_red(self, label):
        label.setStyleSheet("""
            background-color: light gray;
            border-width: 5px;
            border-color: black;
            color: #cc0000;
            font: 14px;
            height: 1em;
            max-width: 30em;
            padding: 6px;
            margin: 1em 0;
        """)

    def make_label_green(self, label):
        label.setStyleSheet("""
            background-color: light gray;
            border-width: 5px;
            border-color: black;
            color: green;
            font: 14px;
            height: 1em;
            max-width: 30em;
            padding: 6px;
            margin: 1em 0;
        """)

    def connect_headset_pressed(self):
        self.headset_connect_button.setStyleSheet("""
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
        self.headset_connection_info.setText("Attempting to connect...")
        self.headset_connection_info.setStyleSheet("""
            background-color: light gray;
            border-width: 5px;
            border-color: black;
            color: #e3ebec;
            font: 14px;
            height: 1em;
            max-width: 30em;
            padding: 6px;
            margin: 1em 0;
        """)

    def connect_headset_released(self):
        self.parent.connect_headset()
        self.headset_connect_button.setStyleSheet("""
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

    def guide_to_eeg_pressed(self):
        self.guide_to_eeg_button.setStyleSheet("""
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

    def guide_to_eeg_released(self):
        self.guide_to_eeg_button.setStyleSheet("""
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

    def tutorial_pressed(self):
        self.hardware_tutorial_button.setStyleSheet("""
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

    def tutorial_released(self):
        self.hardware_tutorial_button.setStyleSheet("""
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

    def brainwave_analysis_pressed(self):
        self.brainwave_analysis_button.setStyleSheet("""
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

    def brainwave_analysis_released(self):
        self.parent.change_page_index(2)
        self.brainwave_analysis_button.setStyleSheet("""
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

    def fix_electrodes_pressed(self):
        self.headset_contact_button.setStyleSheet("""
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

    def fix_electrodes_released(self):
        self.headset_contact_button.setStyleSheet("""
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
        self.parent.change_page_index(1)

