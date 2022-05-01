
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
import pyqtgraph.opengl as gl
from funcs import *


class UnknownPleasuresWidget(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.bp_processing = parent.bp_processing

        self.streaming = False

        self.state_length = 0
        self.record_overlap = 0

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

        # self.start_stop_button = QPushButton("Start")
        self.start_stop_button = make_button("Start")
        self.start_stop_button.pressed.connect(self.toggle_stream)
        # self.start_stop_button.setStyleSheet("""
        #         border-image: none !important;
        #         border-style: outset;
        #         border-width: 2px;
        #         border-radius: 10px;
        #         border-color: beige;
        #         color: #fff;
        #         font-size: 15px;
        #     """)

        self.clear_button = make_button("Clear")
        self.clear_button.pressed.connect(self.clear_button_pressed)
        self.clear_button.released.connect(self.clear_button_released)

        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.start_stop_button)
        self.buttons.addWidget(self.clear_button)

        live_data_settings = QVBoxLayout()
        live_data_settings.addLayout(state_length)
        live_data_settings.addLayout(record_overlap)
        live_data_settings.addLayout(self.buttons)

        # Live graph

        self.graph = Graph(self, self.parent)
        graph_w = QVBoxLayout()
        graph_w.addWidget(self.graph)

        # New graph

        self.view = gl.GLViewWidget()
        self.view.show()

        # create three grids, add each to the view
        xgrid = gl.GLGridItem()
        ygrid = gl.GLGridItem()
        zgrid = gl.GLGridItem()
        self.view.addItem(xgrid)
        self.view.addItem(ygrid)
        self.view.addItem(zgrid)
        xgrid.hide()
        ygrid.hide()
        zgrid.hide()

        # rotate x and y grids to face the correct direction
        xgrid.rotate(90, 0, 1, 0)
        ygrid.rotate(90, 1, 0, 0)

        ## scale each grid differently
        xgrid.scale(1, 1, 1)
        ygrid.scale(1, 1, 1)
        zgrid.scale(1, 1, 1)

        # Create Macro layout

        layout = QGridLayout()
        layout.addLayout(live_data_settings, 1, 0)
        layout.addWidget(self.view, 0, 0)


        self.all_states = []
        self.max_states = 15

        # p = [[0,0,1],[0,0,2],[0,1,0]]
        # p = np.array(p)
        # print(p.shape)
        #
        # self.line = self.create_line_item(p)
        # self.view.addItem(self.line)
        #
        # line_plot = self.create_line_item(p)
        # self.line_plots.append(line_plot)
        # self.line_plots = np.array(self.line_plots)

        self.setLayout(layout)

    def create_line_item(self, p):
        line_item = gl.GLLinePlotItem(
            pos=p,
            # color=pg.glColor((0, 255, 0)),
            width=2,
        )
        return line_item

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

        # # Plot frequencies vs bandpowers
        # self.graph.clear_plots()
        # self.data.append([s_frequencies, s_processed_bp])
        # self.graph.plot_s()
        # self.graph.plot_s(s_frequencies, s_processed_bp)

        # Plot in new graph

        if len(self.all_states) >= self.max_states:
            self.all_states = np.delete(self.all_states, 0, axis=0)
        if len(self.all_states) > 0:
            for row in self.all_states:
                print(row)
                for point in row:
                    point[0] = point[0] + 1

        new_state = []
        for i in range(len(s_frequencies)):
            new_state.append([0, s_frequencies[i], s_processed_bp[i]])
        new_state = np.array(new_state)
        print("New state")
        print(new_state)
        # self.all_states = np.append(self.all_states, new_state, axis=1)
        # self.all_states.append(new_state)
        # self.all_states = np.array(self.all_states)
        new_all_states = []
        for state in self.all_states:
            new_all_states.append(state)
        new_all_states.append(new_state)
        self.all_states = np.array(new_all_states)
        print("All states")
        print(self.all_states)
        self.view.clear()
        for state in self.all_states:
            line_item = self.create_line_item(state)
            self.view.addItem(line_item)

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

    def clear_button_pressed(self):
        self.clear_button.setStyleSheet("""
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

    def clear_button_released(self):
        self.clear_button.setStyleSheet("""
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
        self.view.clear()
        self.all_states = []


class Graph(pg.GraphicsLayoutWidget):

    def __init__(self, plotSelf, parentSelf):
        self.plotSelf = plotSelf
        self.parentSelf = parentSelf
        super().__init__()
        self.p = self.addPlot(row=0, col=0)
        self.legend = self.p.addLegend()

    def plot_s(self, x, y):
        plot_item = self.p.plot(x, y, z, pen=pg.mkPen(color=(0, 138, 0)))
        # self.legend.addItem(plot_item, "Live State")

    def clear_plots(self):
        self.p.clear()
