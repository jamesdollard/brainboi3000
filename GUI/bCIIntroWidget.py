from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)
from PySide6.QtGui import QPixmap

# Intro page to explain BCI's and the headset
class BCIIntroWidget(QWidget):
    def __init__(self, parentSelf):
        self.parentSelf = parentSelf
        super().__init__()

        title = QLabel("What is a Brain Computer Interface?")
        title.setAlignment(Qt.AlignHCenter)
        title.setStyleSheet("""
            color: #fff;
            font-size: 30px;
        """)

        picture = QLabel()
        picture.setPixmap(QPixmap('images/bci.jpeg').scaled(700, 500))

        info = QLabel("""
            A Brain Computer Interface (BCI) is a system that combines hardware and software in order to measure and analyze cognitive and motor functions. BCI’s can be used to improve accessibility for people that are disabled. This can be done through either replacing lost functions, such as speaking or moving, restoring the ability to control the body, such as by stimulating nerves, or improving bodily functions, such as training users to repair damaged pathways required to grasp. 
           
            For our hardware, we are using the OpenBCI Cyton Board and OpenBCI Daisy Module. The CytonDaisy Board can be used to sample up to 8 channels of brain activity (EEG), muscle activity (EMG), and heart activity (ECG). In this lab, our headset is designed specifically for EEG data, which is collected at 125 Hz on each of its 8 channels.
        """)
        info.setStyleSheet("""
            color: white;
            font: 20px;
        """)
        info.setWordWrap(True)

        pageLayout = QVBoxLayout()
        titleLayout = QHBoxLayout()
        infoLayout = QHBoxLayout()
        pageLayout.addLayout(titleLayout)
        pageLayout.addLayout(infoLayout)

        titleLayout.addWidget(title)
        infoLayout.addWidget(info)
        infoLayout.addWidget(picture)
        self.setLayout(pageLayout)