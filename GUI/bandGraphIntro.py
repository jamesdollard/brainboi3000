from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QVBoxLayout,
    QWidget,
)

# Page to introduce frequency bands
class BandGraphIntro(QWidget):
    def __init__(self, parentSelf):
        self.parentSelf = parentSelf
        super().__init__()

        info = QLabel("Next we'll show how you can use a BCI to detect specific signals. By looking at the frequecy bands of your brainwaves, we can gain insights into different mental states. Below are the different frequency bands that we will be analyzing as well and what they each signify:")
        info.setStyleSheet("""
            color: #fff;
            font: 20px;
            margin: 0;
        """)
        info.setAlignment(Qt.AlignHCenter)
        info.setWordWrap(True)

        waveHeader = QLabel("Wave")
        waveHeader.setStyleSheet("""
            color: #fff;
            font: 20px bold;
            margin-left: 20px;
            text-decoration: underline;
        """)
        frequencyHeader = QLabel("Frequency (Hz)")
        frequencyHeader.setStyleSheet("""
            color: #fff;
            font: 20px bold;
            text-decoration: underline;
        """)
        descriptionHeader = QLabel("Description")
        descriptionHeader.setStyleSheet("""
            color: #fff;
            font: 20px bold;
            margin-right: 20px;
            text-decoration: underline;
        """)

        deltaWave = QLabel("Delta")
        deltaWave.setStyleSheet("""
            color: #fff;
            font: 15px;
            margin-bottom: 10px;
            margin-left: 20px;
        """)
        deltaFrequency = QLabel("0-4")
        deltaFrequency.setStyleSheet("""
            color: #fff;
            font: 15px;
            margin-bottom: 10px;
        """)
        deltaDescription = QLabel("Occur during enjoy restorative, deep, dreamless sleep.")
        deltaDescription.setStyleSheet("""
            color: #fff;
            font: 15px;
            margin-bottom: 10px;
            margin-right: 20px;
        """)

        thetaWave = QLabel("Theta")
        thetaWave.setStyleSheet("""
            color: #fff;
            font: 15px;
            margin-bottom: 10px;
            margin-left: 20px;
        """)
        thetaFrequency = QLabel("4-8")
        thetaFrequency.setStyleSheet("""
            color: #fff;
            font: 15px;
            margin-bottom: 10px;
        """)
        thetaDescription = QLabel("Occur during deep relaxation, creativity, insight, & reduced consciousness, such as day dreaming and deep meditation.")
        thetaDescription.setStyleSheet("""
            color: #fff;
            font: 15px;
            margin-bottom: 10px;
            margin-right: 20px;
        """)

        alphaWave = QLabel("Alpha")
        alphaWave.setStyleSheet("""
            color: #fff;
            font: 15px;
            margin-bottom: 10px;
            margin-left: 20px;
        """)
        alphaFrequency = QLabel("8-13")
        alphaFrequency.setStyleSheet("""
            color: #fff;
            font: 15px;
            margin-bottom: 10px;
        """)
        alphaDescription = QLabel("Occur during light physical and mental relaxation, such as when your eyes are closed or you are during yoga. Alpha waves are also associated with inhibition control.")
        alphaDescription.setStyleSheet("""
            color: #fff;
            font: 15px;
            margin-bottom: 10px;
            margin-right: 20px;
        """)

        betaWave = QLabel("Beta")
        betaWave.setStyleSheet("""
            color: #fff;
            font: 15px;
            margin-bottom: 10px;
            margin-left: 20px;
        """)
        betaFrequency = QLabel("13-32")
        betaFrequency.setStyleSheet("""
            color: #fff;
            font: 15px;
            margin-bottom: 10px;
        """)
        betaDescription = QLabel("Occur when one is focusing on work, solving a problem, or learning a new concept. Beta waves signify normal alert consciousness and active thinking.")
        betaDescription.setStyleSheet("""
            color: #fff;
            font: 15px;
            margin-bottom: 10px;
            margin-right: 20px;
        """)

        gammaWave = QLabel("Gamma")
        gammaWave.setStyleSheet("""
            color: #fff;
            font: 15px;
            margin-left: 20px;
        """)
        gammaFrequency = QLabel("32-100")
        gammaFrequency.setStyleSheet("""
            color: #fff;
            font: 15px;
        """)
        gammaDescription = QLabel("Occur when there is simultaneous information processing from multiple parts of the brain. Gamma waves signify heightened perception and alertness.")
        gammaDescription.setStyleSheet("""
            color: #fff;
            font: 15px;
            margin-right: 20px;
        """)

        #hidden label to fix vertical spacing
        tempLabel = QLabel(".")
        tempLabel.setStyleSheet("""
            color: #0F0F0F
        """)

        pageLayout = QVBoxLayout()
        titleLayout = QHBoxLayout()
        tableLayout = QGridLayout()
        tableLayout.addWidget(waveHeader,0,0)
        tableLayout.addWidget(frequencyHeader,0,1)
        tableLayout.addWidget(descriptionHeader,0,2)
        tableLayout.addWidget(deltaWave,1,0)
        tableLayout.addWidget(deltaFrequency,1,1)
        tableLayout.addWidget(deltaDescription,1,2)
        tableLayout.addWidget(thetaWave,2,0)
        tableLayout.addWidget(thetaFrequency,2,1)
        tableLayout.addWidget(thetaDescription,2,2)
        tableLayout.addWidget(alphaWave,3,0)
        tableLayout.addWidget(alphaFrequency,3,1)
        tableLayout.addWidget(alphaDescription,3,2)
        tableLayout.addWidget(betaWave,4,0)
        tableLayout.addWidget(betaFrequency,4,1)
        tableLayout.addWidget(betaDescription,4,2)
        tableLayout.addWidget(gammaWave,5,0)
        tableLayout.addWidget(gammaFrequency,5,1)
        tableLayout.addWidget(gammaDescription,5,2)
        titleLayout.addWidget(info)
        pageLayout.addLayout(titleLayout)
        pageLayout.addLayout(tableLayout)
        pageLayout.addWidget(tempLabel)

        self.setLayout(pageLayout)