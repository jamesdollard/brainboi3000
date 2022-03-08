import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations

# Graphs for bands
class Graph(pg.GraphicsLayoutWidget):
    def __init__(self, plotSelf, parentSelf):
        self.plotSelf = plotSelf
        self.parentSelf = parentSelf
        self.i = 0
        self.increasing = True
        self.update_speed_ms = 250
        self.buffer = []
        super().__init__()

    def start_collection(self):
        p = self.addPlot()
        p.showAxis('left', True)
        p.setMenuEnabled('left', False)
        p.showAxis('bottom', False)
        p.setMenuEnabled('bottom', False)
        p.setTitle('Band Bar Graph')
        p.addLegend()
        self.window_size = 1
        self.time_period = 1
        self.num_points = self.time_period * self.parentSelf.sampling_rate

        self.x = np.arange(1)
        self.y1 = np.array([1])
        self.y2 = np.array([2])
 
        self.bg1 = pg.BarGraphItem(x=self.x, height=0.1, width=0.3, brush='r', name="Delta")
        self.bg2 = pg.BarGraphItem(x=self.x+0.4, height=0.1, width=0.3, brush='g', name="Theta")
        self.bg3 = pg.BarGraphItem(x=self.x+0.8, height=0.1, width=0.3, brush='b', name="Alpha")
        self.bg4 = pg.BarGraphItem(x=self.x+1.2, height=0.1, width=0.3, brush='y', name="Beta")
        #self.bg5 = pg.BarGraphItem(x=self.x+1.6, height=0.1, width=0.3, brush='g')

        p.addItem(self.bg1)
        p.addItem(self.bg2)
        p.addItem(self.bg3)
        p.addItem(self.bg4)
        #p.addItem(self.bg5)

        self.plotSelf.isCollecting = True
        self.plotSelf.isGraphing = True
        self.parentSelf.timer.timeout.connect(self.update)
        self.parentSelf.timer.start(self.update_speed_ms)
        self.plotSelf.feedButton.setText('Pause Feed')
        self.plotSelf.feedButton.setStyleSheet("""
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

    def update(self):
        if self.i < 6 and self.increasing == True:
            self.i = self.i + 1
        else:
            self.i = self.i - 1
            self.increasing == False
        if self.i < 0:
            self.i = 0
            self.increasing = True
    
        
        #collect data here
        #4 differnet bandwidths
        #smooth data based on last few data points 
        data = self.parentSelf.board_shim.get_current_board_data(self.num_points)
        self.sample_rate = self.parentSelf.sampling_rate
        self.eeg_channels = list(range(len(self.parentSelf.exg_channels)))
        #data = self.normalize(data)
        data = self.preformBandPass(data, self.eeg_channels, self.sample_rate, 1, 55, 60)
        data = data[:len(self.eeg_channels)]
        datafft = self.preformFFT(data)
        

        max = len(datafft[0])
        """if max > 60:
            max = 60"""
        max = 31
        dataTrunck = datafft[:max]
        #Delta: 1-4
        delta = self.averageRelativePowerBand(dataTrunck, 0, 4, max)
        #Theta: 4-8
        theta = self.averageRelativePowerBand(dataTrunck, 4, 8, max)
        #Alpha: 8-13
        alpha = self.averageRelativePowerBand(dataTrunck, 8, 13, max)
        #Beta: 13-30
        beta = self.averageRelativePowerBand(dataTrunck, 13, 30, max)
        #Gamma: 30 - 100?
        #gamma = self.averageRelativePowerBand(dataTrunck, 30, max, max)

        self.buffer.append([delta, theta, alpha, beta])

        nowValue = self.rollingFilter(5)

        #print(delta+theta+alpha+beta)
        self.bg1.setOpts(height=nowValue[0])
        self.bg2.setOpts(height=nowValue[1])
        self.bg3.setOpts(height=nowValue[2])
        self.bg4.setOpts(height=nowValue[3])
        #self.bg5.setOpts(height=gamma)

        #self.printAllChannels(datafft)
        #self.bg1.setOpts(height=np.random.randint(10, size=(1)))
        #self.bg2.setOpts(height=np.random.randint(10, size=(1)))



        self.parentSelf.app.processEvents()

    def printAllChannels(self, data):
        df = pd.DataFrame(data)
        for num, channel in enumerate(data):
            plt.figure()
            df[num].plot(subplots=True)
            plt.savefig(f'Fourier_DataCleanUp/indivChannel/{str(num)}.png')
        pass

    def rollingFilter(self, window):
        if len(self.buffer) > window:
            self.buffer.pop(0)
        
        averages = []
        bandwidths = np.transpose(self.buffer)
        for bandwidth in bandwidths:
            averages.append(np.average(bandwidth))
        return averages

    def averageRelativePowerBand(self, data, low, high, maximum):
        #dataFFT = runFFT(data)
        allbandpower = []
        for channel in data:
            allbandpower.append(self.channelRelativePowerBand(channel, low, high, maximum))
        return np.average(allbandpower)


    def channelRelativePowerBand(self, data, low, high, maximum):
        bandpower = np.trapz(data[low:high+1])
        totalband = np.trapz(data[:maximum])
        if totalband != 0.0:
            bandpower /= totalband
        else:
            return 0.0
        return bandpower

    def printSingleChannel(self, data, low, high):
        df = pd.DataFrame(data)
        plt.figure()
        df.plot(subplots=True)
        plt.savefig(f'Fourier_DataCleanUp/singleChannel/{str(low)}_{str(high)}.png')

    def preformFFT(self, data):
        fftData = []
        for channel in range(len(data)):
            allFFT = np.fft.fft(data[channel])
            fftData.append(abs(allFFT[:len(allFFT)//2]))
        fftData = np.array(fftData)
        return fftData

    def normalize(self, data):
        data -= np.mean(data)  # normalize data
        data /= np.std(data)
        print(data.shape)
        return data

    def preformBandPass(self, data, channels, sampling_rate, start, end, cutoff):
        for channel in channels:
            centerFreq = (start + end) / 2.0;
            bandWidth = end - start;
            DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)
            DataFilter.perform_bandpass(data[channel], sampling_rate, centerFreq, bandWidth, 2, FilterTypes.BUTTERWORTH.value, 0.0);
            DataFilter.perform_bandpass(data[channel], sampling_rate, centerFreq, bandWidth, 2, FilterTypes.BUTTERWORTH.value, 0.0);
            DataFilter.perform_bandstop(data[channel], sampling_rate, cutoff, 4.0, 2, FilterTypes.BUTTERWORTH.value, 0.0);
        return data


# Page to show the different frequency bands
class BandGraphWidget(QWidget):
    def __init__(self, parentSelf):
        self.parentSelf = parentSelf
        self.update_speed_ms = 50
        self.isCollecting = False
        self.isGraphing = False
        super().__init__()

        title = QLabel("View your Wave Bands")
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
            color: white;
            font: 14px;
            height: 1em;
            padding: 6px;
            margin: 1em 10em;
        """)

        pageLayout = QVBoxLayout()
        self.title_layout = QHBoxLayout()
        self.dropdown_layout = QHBoxLayout()
        pageLayout.addLayout(self.title_layout)
        pageLayout.addLayout(self.dropdown_layout)
        self.title_layout.addWidget(title)
        self.title_layout.addWidget(self.feedButton)
        self.graph = Graph(self, self.parentSelf)
        pageLayout.addWidget(self.graph)
        self.setLayout(pageLayout)


    # Toggle if graphs are updating or not
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
                    color: white;
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