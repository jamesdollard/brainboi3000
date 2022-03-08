from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# Welcome page for the application
class WelcomeWidget(QWidget):
    def __init__(self, parentSelf):
        self.parentSelf = parentSelf
        super().__init__()

        title = QLabel("Welcome to the Brain Computer Interface Lab!")
        title.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        title.setStyleSheet("""
            color: #fff;
            font-size: 45px;
        """)

        startButton = QPushButton("Start Lab")
        startButton.pressed.connect(self.start_lab)
        startButton.setStyleSheet("""
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

        layout = QVBoxLayout()
        layout.addWidget(title)
        self.setStyleSheet("border-image: url(GUI/brain.png) 0 0 0 0;")
        layout.addWidget(startButton)
        self.setLayout(layout)

    # Button trigger to start the lab
    def start_lab(self):
        self.parentSelf.button_layout.addWidget(self.parentSelf.nextButton)
        self.parentSelf.stacklayout.setCurrentIndex(1)