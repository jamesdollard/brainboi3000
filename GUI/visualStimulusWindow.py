
import sys
import argparse
import logging
from PySide6.QtCore import Qt
from pyqtgraph.Qt import QtCore
import PySide6
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
    QLineEdit,
    QFrame
)


class VisualStimulusWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):

        # Variables
        super().__init__()
        self.hz = 0

        self.timer = PySide6.QtCore.QTimer()
        self.timer.setTimerType(PySide6.QtCore.Qt.PreciseTimer)
        self.timer.timeout.connect(self.switch_colors)
        self.current_color = 0

        # Layout

        label = QLabel("Set Frequency (Hz): ")
        # label.setStyleSheet("""color: #fff; font-size: 15px;""")
        hz_parameter = QLineEdit()
        hz_parameter.setPlaceholderText("0")
        hz_parameter.setMaxLength(2)
        hz_parameter.textChanged.connect(self.set_hz)
        hz_parameter.setStyleSheet("""background-color: #fff; color: #000;font: 15px; min-width: 30px;
                                             margin-bottom: 0px; max-width: 30px; padding: 5px;""")
        blinking_parameters = QHBoxLayout()
        blinking_parameters.addWidget(label)
        blinking_parameters.addWidget(hz_parameter)

        self.stimulus = QFrame()
        # stimulus.setStyleSheet("""background-color: #fff; color: #000;font: 15px; min-width: 30px;
        #                                      margin-bottom: 0px; max-width: 30px; padding: 5px;""")

        self.stimulus.setFixedSize(1000,500)
        self.stimulus.setObjectName("stimulus")
        self.stimulus.setStyleSheet("#stimulus {background-color:red;}")

        self.layout = QVBoxLayout()
        self.layout.addLayout(blinking_parameters)
        self.layout.addWidget(self.stimulus)

        self.setLayout(self.layout)

    def set_hz(self, hz_over_two):
        hz_ms = int(1000 / (int(hz_over_two) * 2))
        self.timer.start(hz_ms)

    def switch_colors(self):
        if self.current_color == 0:
            self.stimulus.setStyleSheet("#stimulus {background-color:white;}")
            self.current_color = 1
        else:
            self.stimulus.setStyleSheet("#stimulus {background-color:black;}")
            self.current_color = 0
