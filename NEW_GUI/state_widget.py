

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
from funcs import *


# Enables user to capture/load a recording session
class StateWidget(QWidget):

    def __init__(self, parent, index):

        # ** CLASS VARIABLE INITIALIZATION ** #

        super().__init__()
        self.parent = parent
        self.index = index

        self.index_label = make_label(str(self.index))
        self.title = "State " + str(self.index)
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("State " + str(self.index))
        self.title_edit.setMaxLength(20)
        self.title_edit.textChanged.connect(self.title_changed)
        self.title_edit.setStyleSheet("""background-color: #fff; color: #000;font: 15px; min-width: 50px;
                                                 margin-bottom: 0px; max-width: 50px; padding: 5px;""")

        self.record_button = make_button("Record (s)")
        self.record_button.pressed.connect(self.record_button_pressed)
        self.record_button.released.connect(self.record_button_released)

        self.record_length = 0  # seconds
        self.record_length_edit = QLineEdit()
        self.record_length_edit.setPlaceholderText("0")
        self.record_length_edit.setMaxLength(2)
        self.record_length_edit.textChanged.connect(self.record_length_changed)
        self.record_length_edit.setStyleSheet("""background-color: #fff; color: #000;font: 15px; min-width: 50px;
                                                     margin-bottom: 0px; max-width: 50px; padding: 5px;""")

        top = QHBoxLayout()
        top.addWidget(self.index_label)
        top.addWidget(self.title_edit)
        top.addWidget(self.delete_button)

        record_section = QHBoxLayout()
        record_section.addWidget(self.record_button)
        record_section.addWidget(self.record_length_edit)

        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addWidget(self.load_button)
        layout.addLayout(record_section)


        a_record_time_label = make_label("State A Record Time (s): ")
        a_record_time_input = QLineEdit()
        a_record_time_input.setPlaceholderText("0")
        a_record_time_input.setMaxLength(2)
        a_record_time_input.textChanged.connect(self.set_a_record_time)

        self.a_record_button = make_button("Record State A")
        self.a_record_button.pressed.connect(self.pressed_record_a)
        # self.a_record_button.released.connect(self.record_a)

        state_a = QHBoxLayout()
        state_a.addWidget(a_record_time_label)
        state_a.addWidget(a_record_time_input)
        state_a.addWidget(self.a_record_button)


        self.setLayout(layout)

    def title_changed(self, title):
        if title == "":
            self.title = "State " + str(self.index)
        else:
            self.title = str(title)

    def record_length_changed(self, s):
        if s == "":
            self.record_length = 0
        else:
            self.record_length = int(s)

    def load_button_pressed(self):
        return

    def load_button_released(self):
        return

    def record_button_pressed(self):
        return

    def record_button_released(self):
        return

    def delete_button_pressed(self):
        return

    def delete_button_released(self):
        return
