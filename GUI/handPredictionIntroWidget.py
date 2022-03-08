from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

# Page to introduce Machine Learning model and readiness potential
class HandPredictionIntroWidget(QWidget):
    def __init__(self, parentSelf):
        self.parentSelf = parentSelf
        super().__init__()

        title = QLabel("Do you have free will?")
        title.setAlignment(Qt.AlignHCenter)
        title.setStyleSheet("""
            color: #FFF;
            font: 30px;
        """)

        info = QLabel("""
            When you make a movement, a readiness potential (also known as the Bereitschaftspotential) can be detected 1 - 1 1/2 seconds before you actually make the movement. This brings into question the idea of free will. Did your choice to make a movement cause that readiness potential to occur before you moved, or is that readiness potential presant becuase you were destined to make that movement?
        """)
        info.setStyleSheet("""
            color: #FFF;
            font: 25px;
            margin-bottom: 25px;
            padding: 0 5em;
        """)
        info.setWordWrap(True)

        pageLayout = QVBoxLayout()
        titleLayout = QHBoxLayout()
        infoLayout = QHBoxLayout()
        pageLayout.addLayout(titleLayout)
        pageLayout.addLayout(infoLayout)

        titleLayout.addWidget(title)
        infoLayout.addWidget(info)
        self.setLayout(pageLayout)