from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)
from PySide6.QtGui import QPixmap

# Page to explain how EEG's work.
class EegIntroWidget(QWidget):
    def __init__(self, parentSelf):
        self.parentSelf = parentSelf
        super().__init__()

        title = QLabel("What is Electroencephalography?")
        title.setAlignment(Qt.AlignHCenter)
        title.setStyleSheet("""
            color: #fff;
            font-size: 30px;
        """)

        picture = QLabel()
        picture.setPixmap(QPixmap('images/electrodes.jpeg').scaled(700, 500))

        info = QLabel("""
            Your brain functions through sequences for firing neurons to communicate information. When a neuron fires, tiny electrical impulses known as the postsynaptic potential can be detected.
            Electroencephalography (EEG) uses electrodes to detect these tiny electrical charges that result from the activity of your brain cells. EEG’s measure voltage fluctuations resulting from ionic current within the neurons of the brain. 
            Alternatives to EEGs include MRI (which shows the structure of the brain) and fMRI (which shows brain activity based on blood flow), however neither of these are as cost effective, nor do they provide the same precision in brain acivity.
            Our headset uses dry tip electrodes which provide greater comfort and easier application while sacrificing connectivity. To circumvent connectivity issues, our electrodes are spring loaded and are able to be individually tightened. As you configure your headset, if you notice an electrode is “railed” (not connected), simply tighten it to increase contact against your scalp.
        """)
        info.setStyleSheet("""
            color: #fff;
            font: 20px;
            padding: 0 5em;
        """)
        info.setWordWrap(True)

        pageLayout = QVBoxLayout()
        titleLayout = QHBoxLayout()
        infoLayout = QHBoxLayout()
        pageLayout.addLayout(titleLayout)
        pageLayout.addLayout(infoLayout)

        titleLayout.addWidget(title)
        infoLayout.addWidget(picture)
        infoLayout.addWidget(info)
        self.setLayout(pageLayout)