from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

# A pop up window with answers to commonly asked questions
class HelpWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        pageLayout = QVBoxLayout()
        self.title = QLabel("BrainBoi Help Page")
        self.title.setStyleSheet("""
            color: #fff;
            font: 25px bold;
            margin-bottom: 2em;
        """)

        self.connectionQuestionLabel = QLabel("What do I do if I can't connect to my headset?")
        self.connectionQuestionLabel.setStyleSheet("""
            color: #fff;
            font: 20px;
        """)
        self.connectionQuestion = QLabel("First, make sure that you entered the correct serial port. If the problem persists, turn off your headset for about 30 seconds before turning it back on and trying again.")
        self.connectionQuestion.setStyleSheet("""
            color: #fff;
        """)

        self.electrodeQuestionLabel = QLabel("Why do some of my electrodes say that they are 'railed'?")
        self.electrodeQuestionLabel.setStyleSheet("""
            color: #fff;
            font: 20px;
            margin-top: 1.5em;
        """)
        self.electrodeQuestion = QLabel("An electrode is 'railed' when it it not making proper contact with your scalp. To fix this, make sure the headset is properly positioned ontop of your head, then gradually tighen the 'railed' electrodes until a connection is made.")
        self.electrodeQuestion.setStyleSheet("""
            color: #fff;
        """)

        self.interferanceQuestionLabel = QLabel("What do I do if there seems to be interferance with my readings?")
        self.interferanceQuestionLabel.setStyleSheet("""
            color: #fff;
            font: 20px;
            margin-top: 1.5em;
        """)
        self.interferanceQuestion = QLabel("These headsets are sensitive to many different sources of intereferance. To ensure best results, make sure that your computer is not plugged in to a charger and there are no phones nearby.")
        self.interferanceQuestion.setStyleSheet("""
            color: #fff;
        """)

        self.noDataLabel = QLabel("What do I do data isn't streaming?")
        self.noDataLabel.setStyleSheet("""
            color: #fff;
            font: 20px;
            margin-top: 1.5em;
        """)
        self.noDataQuestion = QLabel("Make sure that nothing is covering the bluetooth dongle and ensure headset is properly fitted.")
        self.noDataQuestion.setStyleSheet("""
            color: #fff;
        """)

        pageLayout.addWidget(self.title)
        pageLayout.addWidget(self.connectionQuestionLabel)
        pageLayout.addWidget(self.connectionQuestion)
        pageLayout.addWidget(self.electrodeQuestionLabel)
        pageLayout.addWidget(self.electrodeQuestion)
        pageLayout.addWidget(self.interferanceQuestionLabel)
        pageLayout.addWidget(self.interferanceQuestion)
        self.setLayout(pageLayout)