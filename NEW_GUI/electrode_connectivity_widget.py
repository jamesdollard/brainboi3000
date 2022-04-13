import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)
from PySide6.QtGui import QPixmap
from funcs import *

# Page to ensure the electrodes are making proper contact with the scalp
class ElectrodeConnectivityWidget(QWidget):
    def __init__(self, parent):
        self.parent = parent
        self.update_speed_ms = 1000
        super().__init__()

        title = QLabel("Check electrode contact")
        title.setAlignment(Qt.AlignHCenter)
        title.setStyleSheet("""
            color: #fff;
            font-size: 30px;
        """)

        self.scan_electrodes_button = make_button("Scan electrodes")
        self.scan_electrodes_button.pressed.connect(self.scan_electrodes_pressed)
        self.scan_electrodes_button.released.connect(self.scan_electrodes_released)

        picture = QLabel()
        picture.setPixmap(QPixmap('images/customConfig.png').scaled(500, 500))
        picture.setStyleSheet("""
            margin-right: 3em;
        """)

        electrodeOne = make_label("Electrode #1 (FP1):")
        electrodeOneStatus = make_red_label("Railed")
        electrodeTwo = make_label("Electrode #2 (FP2):")
        electrodeTwoStatus = make_red_label("Railed")
        electrodeThree = make_label("Electrode #3 (C3):")
        electrodeThreeStatus = make_red_label("Railed")
        electrodeFour = make_label("Electrode #4 (C4):")
        electrodeFourStatus = make_red_label("Railed")
        electrodeFive = make_label("Electrode #5 (P7):")
        electrodeFiveStatus = make_red_label("Railed")
        electrodeSix = make_label("Electrode #6 (P8):")
        electrodeSixStatus = make_red_label("Railed")
        electrodeSeven = make_label("Electrode #7 (O1):")
        electrodeSevenStatus = make_red_label("Railed")
        electrodeEight = make_label("Electrode #8 (O2):")
        electrodeEightStatus = make_red_label("Railed")

        electrodeNine = QLabel("Electrode #9 (C3):")
        electrodeNine.setStyleSheet("color: #fff;")
        electrodeNineStatus = QLabel("Railed")
        electrodeNineStatus.setStyleSheet("color: red;")
        electrodeTen = QLabel("Electrode #10 (Cz):")
        electrodeTen.setStyleSheet("color: #fff;")
        electrodeTenStatus = QLabel("Railed")
        electrodeTenStatus.setStyleSheet("color: red;")
        electrodeEleven = QLabel("Electrode #11 (C4):")
        electrodeEleven.setStyleSheet("color: #fff;")
        electrodeElevenStatus = QLabel("Railed")
        electrodeElevenStatus.setStyleSheet("color: red;")
        electrodeTwelve = QLabel("Electrode #12 (T4):")
        electrodeTwelve.setStyleSheet("color: #fff;")
        electrodeTwelveStatus = QLabel("Railed")
        electrodeTwelveStatus.setStyleSheet("color: red;")
        electrodeThirteen = QLabel("Electrode #13 (CP5):")
        electrodeThirteen.setStyleSheet("color: #fff;")
        electrodeThirteenStatus = QLabel("Railed")
        electrodeThirteenStatus.setStyleSheet("color: red;")
        electrodeFourteen = QLabel("Electrode #14 (CP1):")
        electrodeFourteen.setStyleSheet("color: #fff;")
        electrodeFourteenStatus = QLabel("Railed")
        electrodeFourteenStatus.setStyleSheet("color: red;")
        electrodeFifteen = QLabel("Electrode #15 (CP2):")
        electrodeFifteen.setStyleSheet("color: #fff;")
        electrodeFifteenStatus = QLabel("Railed")
        electrodeFifteenStatus.setStyleSheet("color: red;")
        electrodeSixteen = QLabel("Electrode #16 (CP6):")
        electrodeSixteen.setStyleSheet("color: #fff;")
        electrodeSixteenStatus = QLabel("Railed")
        electrodeSixteenStatus.setStyleSheet("color: red;")
        # Dict to map er and erw to electrode statuses
        self.electrodeDict = {
            1: electrodeOneStatus,
            2: electrodeTwoStatus,
            3: electrodeThreeStatus,
            4: electrodeFourStatus,
            5: electrodeFiveStatus,
            6: electrodeSixStatus,
            7: electrodeSevenStatus,
            8: electrodeEightStatus,
            9: electrodeNineStatus,
            10: electrodeTenStatus,
            11: electrodeElevenStatus,
            12: electrodeTwelveStatus,
            13: electrodeThirteenStatus,
            14: electrodeFourteenStatus,
            15: electrodeFifteenStatus,
            16: electrodeSixteenStatus
        }

        self.problemElectrodes = list(range(1,17))
        self.home_button = make_button("Home")
        self.home_button.pressed.connect(self.home_button_pressed)
        self.home_button.released.connect(self.home_button_released)

        titleLayout = QHBoxLayout()
        titleLayout.addWidget(self.home_button)
        titleLayout.addWidget(title)
        titleLayout.addWidget(self.scan_electrodes_button)

        pageLayout = QVBoxLayout()
        bodyLayout = QHBoxLayout()
        leftLayout = QGridLayout()
        pageLayout.addLayout(titleLayout)
        pageLayout.addLayout(bodyLayout)
        bodyLayout.addLayout(leftLayout)
        leftLayout.addWidget(electrodeOne,0,0)
        leftLayout.addWidget(electrodeOneStatus,0,1)
        leftLayout.addWidget(electrodeTwo,1,0)
        leftLayout.addWidget(electrodeTwoStatus,1,1)
        leftLayout.addWidget(electrodeThree,2,0)
        leftLayout.addWidget(electrodeThreeStatus,2,1)
        leftLayout.addWidget(electrodeFour,3,0)
        leftLayout.addWidget(electrodeFourStatus,3,1)
        # leftLayout.addWidget(electrodeFive,4,0)
        # leftLayout.addWidget(electrodeFiveStatus,4,1)
        # leftLayout.addWidget(electrodeSix,5,0)
        # leftLayout.addWidget(electrodeSixStatus,5,1)
        # leftLayout.addWidget(electrodeSeven,6,0)
        # leftLayout.addWidget(electrodeSevenStatus,6,1)
        # leftLayout.addWidget(electrodeEight,7,0)
        # leftLayout.addWidget(electrodeEightStatus,7,1)
        bodyLayout.addWidget(picture)
        rightLayout = QGridLayout()
        bodyLayout.addLayout(rightLayout)
        rightLayout.addWidget(electrodeFive,4,0)
        rightLayout.addWidget(electrodeFiveStatus,4,1)
        rightLayout.addWidget(electrodeSix,5,0)
        rightLayout.addWidget(electrodeSixStatus,5,1)
        rightLayout.addWidget(electrodeSeven,6,0)
        rightLayout.addWidget(electrodeSevenStatus,6,1)
        rightLayout.addWidget(electrodeEight,7,0)
        rightLayout.addWidget(electrodeEightStatus,7,1)

        # rightLayout.addWidget(electrodeNine,0,0)
        # rightLayout.addWidget(electrodeNineStatus,0,1)
        # rightLayout.addWidget(electrodeTen,1,0)
        # rightLayout.addWidget(electrodeTenStatus,1,1)
        # rightLayout.addWidget(electrodeEleven,2,0)
        # rightLayout.addWidget(electrodeElevenStatus,2,1)
        # rightLayout.addWidget(electrodeTwelve,3,0)
        # rightLayout.addWidget(electrodeTwelveStatus,3,1)
        # rightLayout.addWidget(electrodeThirteen,4,0)
        # rightLayout.addWidget(electrodeThirteenStatus,4,1)
        # rightLayout.addWidget(electrodeFourteen,5,0)
        # rightLayout.addWidget(electrodeFourteenStatus,5,1)
        # rightLayout.addWidget(electrodeFifteen,6,0)
        # rightLayout.addWidget(electrodeFifteenStatus,6,1)
        # rightLayout.addWidget(electrodeSixteen,7,0)
        # rightLayout.addWidget(electrodeSixteenStatus,7,1)

        self.setLayout(pageLayout)

    def scan_electrodes_pressed(self):
        self.scan_electrodes_button.setStyleSheet("""
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

    # Scan electrodes every second
    def scan_electrodes_released(self):
        self.time_period = 2
        self.num_points = self.time_period * self.parent.sampling_rate
        self.parent.timer.timeout.connect(self.check_if_railed)
        self.parent.timer.start(self.update_speed_ms)
        self.scan_electrodes_button.setText("Scanning...")
        self.scan_electrodes_button.setStyleSheet("""
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
    
    # Find which electrodes are railed
    def get_railed_electrodes(self, d):
        threshold_railed = 90
        threshold_railed_warn = 75
        # scalar = (4.5 / (pow(2, 23) - 1) / 1.0 * 1000000.)
        scalar = (4.5 / (pow(2, 23) - 1) / 24 * 1000000.)  # 24 is channel gain. This is 'dynamic scalar'
        max_val = scalar * pow(2, 23)
        n_points = self.time_period * 125
        electrode_railed = []
        electrode_railed_warn = []
        for i in range(1, 9):
            channel_data = d[i]
            end_pos = len(channel_data)
            start_pos = np.maximum(0, end_pos - n_points)
            maximum = np.abs(channel_data[start_pos])
            for j in range(end_pos):
                if np.abs(channel_data[j]) > maximum:
                    maximum = np.abs(channel_data[j])
            percentage = (maximum / max_val) * 100.0
            if percentage > threshold_railed:
                electrode_railed.append(i)
            if percentage > threshold_railed_warn:
                electrode_railed_warn.append(i)
        return electrode_railed, electrode_railed_warn

    # Check if electrodes are railed, change labels for railed electrodes
    def check_if_railed(self):
        data = self.parent.board_shim.get_current_board_data(self.num_points)
        er, erw = self.get_railed_electrodes(data)
        for e in range(1,9):
            if e not in erw and e not in er:
                self.electrodeDict[e].setText('Not Railed')
                self.electrodeDict[e].setStyleSheet("color: green;")
                #self.problemElectrodes.pop(e)
        for e in erw:
            if e not in er:
                self.electrodeDict[e].setText('Almost Railed')
                self.electrodeDict[e].setStyleSheet("color: yellow;")
                #self.problemElectrodes.append(e)
        for e in er:
            self.electrodeDict[e].setText('Railed')
            self.electrodeDict[e].setStyleSheet("color: #cc0000;")
            #self.problemElectrodes.append(e)

    def home_button_pressed(self):
            self.home_button.setStyleSheet("""
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

    def home_button_released(self):
        self.home_button.setStyleSheet("""
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
        self.scan_electrodes_button.setText("Scan electrodes")
        for i in range(1,9):
            button = self.electrodeDict[i]
            button.setText('Railed')
            button.setStyleSheet("color: #cc0000;")
        self.parent.change_page_index(0)
        self.parent.timer.stop()
