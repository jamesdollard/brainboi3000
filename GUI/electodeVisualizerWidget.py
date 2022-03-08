import pyqtgraph as pg
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations

# Graph section for page
class Graph(pg.GraphicsLayoutWidget):
    def __init__(self, plotSelf, parentSelf):
        self.plotSelf = plotSelf
        self.parentSelf = parentSelf
        super().__init__()


    # Start Initial Connection
    def start_collection(self):
        self.window_size = 4
        self.num_points = self.window_size * self.parentSelf.sampling_rate
        self.plotSelf.isCollecting = True
        self.plotSelf.isGraphing = True
        self._init_timeseries()
        self.parentSelf.timer.timeout.connect(self.update)
        self.parentSelf.timer.start(self.plotSelf.update_speed_ms)
        self.plotSelf.feedButton.setText('Pause Feed')
        self.plotSelf.feedButton.setStyleSheet("""
            background-color: orange;
            border-image: none !important;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            color: #fff;
            font: 14px;
            height: 1em;
            padding: 6px;
            margin: 1em 10em;
        """)

    # Create plots for graphs
    def _init_timeseries(self):
        self.plots = list()
        self.curves = list()
        colors = [
            (0, 138, 0),
            (0, 171, 169),
            (27, 161, 226),
            (0, 80, 239),
            (106, 0, 255),
            (170, 0, 255),
            (244, 114, 208),
            (216, 0, 115),
            (162, 0, 37),
            (229, 20, 0),
            (250, 104, 0),
            (227, 200, 0),
            (130, 90, 44),
            (109, 135, 100),
            (100, 118, 135),
            (118, 96, 138)
        ]
        rowNumber = 1
        inRow = 0
        for i in range(len(self.parentSelf.exg_channels)):
            if inRow == 2:
                rowNumber = rowNumber + 1
                inRow = 0
            p = self.addPlot(row=rowNumber, col=inRow*5)
            p.showAxis('left', True)
            p.setMenuEnabled('left', False)
            p.showAxis('bottom', False)
            p.setMenuEnabled('bottom', False)
            pen = pg.mkPen(color=colors[i])
            self.plots.append(p)
            curve = p.plot(pen=pen)
            self.curves.append(curve)
            inRow = inRow + 1

    # Get current board data and add to graphs
    def update(self):
        data = self.parentSelf.board_shim.get_current_board_data(self.num_points)
        for count, channel in enumerate(self.parentSelf.exg_channels):
            # plot timeseries
            DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)
            DataFilter.perform_bandpass(data[channel], self.parentSelf.sampling_rate, 51.0, 100.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_bandpass(data[channel], self.parentSelf.sampling_rate, 51.0, 100.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_bandstop(data[channel], self.parentSelf.sampling_rate, 50.0, 4.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_bandstop(data[channel], self.parentSelf.sampling_rate, 60.0, 4.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            self.curves[count].setData(data[channel].tolist())

        self.parentSelf.app.processEvents()


# Page to show live feeds from all electrodes
class ElectodeVisualizerWidget(QWidget):
    def __init__(self, parentSelf):
        self.parentSelf = parentSelf
        self.update_speed_ms = 50
        self.isCollecting = False
        self.isGraphing = False
        super().__init__()

        title = QLabel("View your Brainwaves")
        title.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        title.setStyleSheet("""
            color: #fff;
            font-size: 30px;
        """)

        self.feedButton = QPushButton("Start Live Feed")
        self.feedButton.pressed.connect(self.controlFeed)
        self.feedButton.setStyleSheet("""
            background-color: green;
            border-image: none !important;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            color: #fff;
            font: 14px;
            height: 1em;
            padding: 6px;
            margin: 1em 10em;
        """)

        graphLabel = QLabel("Electrophysiological Signal TimeSeries Plot (µV)")
        graphLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        graphLabel.setStyleSheet("""
            color: #fff;
        """)
        timeList = QComboBox()
        timeList.setPlaceholderText("Window Speed (ms)")
        timeList.addItems(["1", "10", "50", "100", "500", "1000"])
        timeList.setStyleSheet("""
            background-color: gray;
            color: #fff;
        """)
        timeList.currentIndexChanged.connect(self.time_index_changed)

        pageLayout = QVBoxLayout()
        self.title_layout = QHBoxLayout()
        self.dropdown_layout = QHBoxLayout()
        pageLayout.addLayout(self.title_layout)
        pageLayout.addLayout(self.dropdown_layout)
        self.title_layout.addWidget(title)
        self.title_layout.addWidget(self.feedButton)
        self.dropdown_layout.addWidget(graphLabel)
        self.dropdown_layout.addWidget(timeList)
        self.graph = Graph(self, self.parentSelf)
        pageLayout.addWidget(self.graph)
        self.setLayout(pageLayout)


    # Toggle if graph is running or not
    def controlFeed(self):
        if self.isCollecting:
            if self.isGraphing:
                self.parentSelf.timer.stop()
                self.isGraphing = False
                self.feedButton.setText('Resume Feed')
                self.feedButton.setStyleSheet("""
                    background-color: green;
                    border-image: none !important;
                    border-style: outset;
                    border-width: 2px;
                    border-radius: 10px;
                    border-color: beige;
                    color: #fff;
                    font: 14px;
                    height: 1em;
                    padding: 6px;
                    margin: 1em 10em;
                """)
            else:
                self.parentSelf.timer.start(self.update_speed_ms)
                self.isGraphing = True
                self.feedButton.setText('Pause Feed')
                self.feedButton.setStyleSheet("""
                    background-color: orange;
                    border-image: none !important;
                    border-style: outset;
                    border-width: 2px;
                    border-radius: 10px;
                    border-color: beige;
                    color: white;
                    font: 14px;
                    height: 1em;
                    padding: 6px;
                    margin: 1em 10em;
                """)
        else:
            self.graph.start_collection()

    # Change how quickly graph updates
    def time_index_changed(self, i):
        times = [1, 10, 50, 100, 500, 1000]
        self.parentSelf.timer.setInterval( times[i] )