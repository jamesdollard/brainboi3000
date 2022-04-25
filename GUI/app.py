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
)
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter
from brainflow.ml_model import MLModel

from helpWindow import *
from welcomeWidget import *
from bCIIntroWidget import *
from eegIntroWidget import *
from configureHeadsetWidget import *
from electrodeConnectivityWidget import *
from electodeVisualizerWidget import *
from bandGraphIntro import *
from bandGraphWidget import *
from ABBandpowerWidget import *
from bandpowerProcessing import BandpowerProcessing
from stateDetectionWidget import StateDetectionWidget
from visualStimulusWindow import VisualStimulusWindow
# from handPredictionWidget import *
from handPredictionIntroWidget import *


# Main application window
class MainWindow(QMainWindow):
    def __init__(self, app):
        self.app = app
        self.timer = QtCore.QTimer()
        self.helpWindow = None
        super().__init__()
        # Main Window Set Up
        self.setWindowTitle("Brain Boi 2000")
        # Toolbar set up
        toolbar = QToolBar("Brain Boi toolbar")
        self.addToolBar(toolbar)
        self.bp_processing = BandpowerProcessing()

        # Page Widgets are each a layer of the stacked layout
        pageLayout = QVBoxLayout()
        self.headset_status_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()
        pageLayout.addLayout(self.headset_status_layout)
        pageLayout.addLayout(self.stacklayout)
        pageLayout.addLayout(self.button_layout)

        # Add headset status
        self.connectLabel = QLabel("Headset: ")
        self.connectLabel.setAlignment(Qt.AlignHCenter)
        self.connectLabel.setStyleSheet("""
            color: #fff;
        """)
        self.statusLabel = QLabel("Disconnected")
        self.statusLabel.setStyleSheet("color: red;")
        self.connectHeadset = QPushButton("Connect Headset")
        self.connectHeadset.pressed.connect(self.connect_headset)

        # Buttons to toggle between pages
        self.nextButton = QPushButton("Next")
        self.nextButton.pressed.connect(self.next_tab)
        self.nextButton.setStyleSheet("""
            background-color: gray;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            color: white;
            font: 14px;
            height: 1em;
            max-width: 30em;
            padding: 6px;
            margin: 1em 0;
        """)
        self.backButton = QPushButton("Back")
        self.backButton.pressed.connect(self.previous_tab)
        self.backButton.setStyleSheet("""
            background-color: gray;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            color: white;
            font: 14px;
            height: 1em;
            max-width: 30em;
            padding: 6px;
            margin: 1em 0;
        """)

        # Help button - on toolbar
        self.helpButton = QPushButton("Help")
        self.helpButton.pressed.connect(self.show_help_window)
        # self.visualStimulus = QPushButton("Visual Stimulus")
        # self.visualStimulus.pressed.connect(self.show_visual_stimulus_window)
        toolbar.addWidget(self.helpButton)
        # toolbar.addWidget(self.visualStimulus)

        # Visual stimulus - on toolbar


        # Add Pages to stack
        self.stacklayout.addWidget(WelcomeWidget(self))
        self.stacklayout.addWidget(BCIIntroWidget(self))
        self.stacklayout.addWidget(EegIntroWidget(self))
        self.stacklayout.addWidget(ConfigureHeadsetWidget(self))
        self.stacklayout.addWidget(ElectrodeConnectivityWidget(self))
        self.stacklayout.addWidget(ElectodeVisualizerWidget(self))
        self.stacklayout.addWidget(BandGraphIntro(self))
        self.stacklayout.addWidget(BandGraphWidget(self))
        # self.stacklayout.addWidget(ABBandpowerWidget(self))
        # self.stacklayout.addWidget(StateDetectionWidget(self))
        self.stacklayout.addWidget(HandPredictionIntroWidget(self))
        # self.stacklayout.addWidget(HandPredictionWidget(self))
        self.lastIndex = 10

        # Add layout to main window
        widget = QWidget()
        widget.setLayout(pageLayout)
        widget.setStyleSheet("background-color: #0F0F0F;")
        self.setCentralWidget(widget)        


    # Connect to BCI headset
    def connect_headset(self, serialPort):
        self.statusLabel.setText("Attempting to connect...")
        self.statusLabel.setStyleSheet("color: yellow;")
        # Board set up
        BoardShim.enable_dev_board_logger()
        BoardShim.enable_board_logger()
        DataFilter.enable_data_logger()
        MLModel.enable_ml_logger()
        logging.basicConfig(level=logging.DEBUG)

        parser = argparse.ArgumentParser()
        # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
        parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                            default=0)
        parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
        parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                            default=0)
        parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
        parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
        parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
        parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
        parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
        parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
        parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                            required=False, default=BoardIds.SYNTHETIC_BOARD)
        parser.add_argument('--file', type=str, help='file', required=False, default='')
        args = parser.parse_args()

        params = BrainFlowInputParams()
        params.ip_port = args.ip_port
        #params.serial_port = args.serial_port
        params.serial_port = "/dev/cu.usbserial-DM0257XC"
        params.mac_address = args.mac_address
        params.other_info = args.other_info
        params.serial_number = args.serial_number
        params.ip_address = args.ip_address
        params.ip_protocol = args.ip_protocol
        params.timeout = args.timeout
        params.file = args.file

        try:
            #self.board_shim = BoardShim(args.board_id, params)
            self.board_shim = BoardShim(BoardIds.CYTON_BOARD, params)
            self.board_id = self.board_shim.get_board_id()
            self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
            self.exg_channels = BoardShim.get_exg_channels(self.board_id)
            self.eeg_channels = BoardShim.get_eeg_channels(int(self.board_id))
            self.board_shim.prepare_session()

            isBoardReady = self.board_shim.is_prepared()
            self.toggleConnected(isBoardReady, args)
            return isBoardReady
        except BaseException:
            self.toggleConnected(False, args)
            logging.warning('Exception', exc_info=True)
        

    # Change label to notify user that the headset is connected
    def toggleConnected(self, isConnected, args):
        if isConnected == True:
            self.statusLabel.setText("Connected")
            self.statusLabel.setStyleSheet("color: green;")
            self.board_shim.start_stream(45000, args.streamer_params)
        else:
            self.statusLabel.setText("Connection Failed!")
            self.statusLabel.setStyleSheet("color: red;")


    # Toggle to next page in stacked layout
    def next_tab(self):
        self.timer.stop()
        if self.stacklayout.currentIndex() == 1:
            self.button_layout.removeWidget(self.nextButton)
            self.button_layout.addWidget(self.backButton)
            self.button_layout.addWidget(self.nextButton)
        if self.stacklayout.currentIndex() == 2:
            self.headset_status_layout.addWidget(self.connectLabel)
            self.headset_status_layout.addWidget(self.statusLabel)
        if self.stacklayout.currentIndex() != self.lastIndex:
            self.stacklayout.setCurrentIndex(self.stacklayout.currentIndex()+1)


    # Toggle to previous page in stacked layout
    def previous_tab(self):
        self.timer.stop()
        if self.stacklayout.currentIndex() != 1:
            self.stacklayout.setCurrentIndex(self.stacklayout.currentIndex()-1)

    # Show pop up window with help
    def show_help_window(self):
        if self.helpWindow is None:
            self.helpWindow = HelpWindow()
            self.helpWindow.show()
        else:
            self.helpWindow.close()  # Close window.
            self.helpWindow = None

    def show_visual_stimulus_window(self):
        self.w = VisualStimulusWindow()
        self.w.show()


app = QApplication(sys.argv)
window = MainWindow(app)
window.showMaximized()
app.exec()
