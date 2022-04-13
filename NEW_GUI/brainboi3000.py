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
from home_page import HomePage
from ab_bandpower_widget import ABBandpowerWidget
from bandpower_processing import BandpowerProcessing


# Main application window
class MainWindow(QMainWindow):
    def __init__(self, app):

        # Variable initialization

        self.app = app
        self.timer = QtCore.QTimer()
        self.helpWindow = None
        super().__init__()
        self.setWindowTitle("Brainboi 3000")
        self.bp_processing = BandpowerProcessing()

        # Stack
        self.stack_layout = QStackedLayout()
        self.home_page = HomePage(self)
        self.stack_layout.addWidget(self.home_page)
        self.electrode_connectivity = ElectrodeConnectivityWidget(self)
        self.stack_layout.addWidget(self.electrode_connectivity)
        self.ab_bandpower = ABBandpowerWidget(self)
        self.stack_layout.addWidget(self.ab_bandpower)

        # Add layout to main window
        widget = QWidget()
        widget.setLayout(self.stack_layout)
        widget.setStyleSheet("background-color: #103650;")

        self.setCentralWidget(widget)

    def change_page_index(self, i):
        self.stack_layout.setCurrentIndex(i)

    def connect_headset(self):
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

            prepared = self.board_shim.is_prepared()

            if prepared:
                self.board_shim.start_stream(45000, args.streamer_params)
                self.home_page.headset_connection_info.setText("Connected")
                self.home_page.headset_connection_info.setStyleSheet("""
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
            else:
                self.home_page.headset_connection_info.setText("Failed to connect")
                self.home_page.headset_connection_info.setStyleSheet("""
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

        except BaseException:
            self.home_page.headset_connection_info.setText("Failed to connect")
            self.home_page.headset_connection_info.setStyleSheet("""
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
            logging.warning('Exception', exc_info=True)

app = QApplication(sys.argv)
window = MainWindow(app)
window.showMaximized()
app.exec()
