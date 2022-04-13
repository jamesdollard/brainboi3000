
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
from PySide6.QtCore import Qt


def make_button(label):
    button = QPushButton(label)
    button.setStyleSheet("""
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
    return button


def make_label(l):
    label = QLabel(l)
    label.setStyleSheet("""
        background-color: light gray;
        border-width: 5px;
        border-color: black;
        color: #e3ebec;
        font: 14px;
        height: 1em;
        max-width: 30em;
        padding: 6px;
        margin: 1em 0;
    """)
    label.setAlignment(Qt.AlignHCenter)
    return label


def make_red_label(l):
    label = QLabel(l)
    label.setStyleSheet("""
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
    label.setAlignment(Qt.AlignHCenter)
    return label
