from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

# Page to connect EEG headset to application
# User's need to input the serial port for their headset
class ConfigureHeadsetWidget(QWidget):
    def __init__(self, parentSelf):
        self.parentSelf = parentSelf
        self.serialPort = ''
        super().__init__()

        title = QLabel("Let's connect to your headset!")
        title.setAlignment(Qt.AlignHCenter)
        title.setStyleSheet("""
            color: #fff;
            font-size: 45px;
        """)

        self.connectionStatus = QLabel()
        self.connectionStatus.setAlignment(Qt.AlignHCenter)
        self.connectionStatus.setStyleSheet("""
            color: #0F0F0F;
            font-size: 20px;
        """)

        serialPortInput = QLineEdit()
        serialPortInput.setPlaceholderText("Enter your serial port")
        serialPortInput.textChanged.connect(self.text_changed)
        serialPortInput.setStyleSheet("""
            background-color: #fff;
            color: #000;
            font: 23px;
            min-width: 250px;
            margin-bottom: 10px;
            max-width: 250px;
            padding: 5px;
        """)

        self.connectButton = QPushButton("Connect")
        self.connectButton.pressed.connect(self.connect)
        self.connectButton.setEnabled(True)
        self.connectButton.setStyleSheet("""
            background-color: green;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            color: white;
            font: 14px;
            height: 1em;
            padding: 6px;
            margin-bottom: 3em;
            min-width: 250px;
            max-width: 250px;
        """)

        pageLayout = QVBoxLayout()
        gridLayout = QGridLayout()
        pageLayout.addWidget(title)
        gridLayout.addWidget(serialPortInput, 0, 1)
        gridLayout.addWidget(self.connectButton, 1, 1)
        pageLayout.addLayout(gridLayout)
        pageLayout.addWidget(self.connectionStatus)
        self.setLayout(pageLayout)

    def text_changed(self, p):
        self.serialPort = p

    # Button trigger to connect headset
    def connect(self):
        # self.parentSelf.connect_headset(self.serialPort)
        self.isConnected = self.parentSelf.connect_headset("/dev/cu.usbserial-DM0257WW")
        self.updateStatus()

    # Updates text with the connection status of the headset
    def updateStatus(self):
        self.connectionStatus.setStyleSheet("""
            color: #fff;
            font-size: 20px;
        """)
        if self.isConnected:
            self.connectionStatus.setText("Headset Connected! Press 'Next' to start the lab.")
            self.connectButton.setEnabled(False)
        else:
            self.connectButton.setText('Retry')
            self.connectionStatus.setText("""
                Headset Connection Failed! 
                Please retry connection by verifying serial port input then press 'Retry'. 
                If problem persists, restart headset and try again.
            """)
            self.connectionStatus.setWordWrap(True)
