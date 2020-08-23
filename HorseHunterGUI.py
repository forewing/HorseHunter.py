import atexit
import os
import random
import sys
import time
from multiprocessing import Process, freeze_support

import pyperclip
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import (QApplication, QButtonGroup, QDesktopWidget,
                             QGridLayout, QLabel, QLineEdit, QPushButton,
                             QRadioButton, QWidget)

from getLines import getLines


def job(lines, interval):
    while True:
        pyperclip.copy(random.choice(lines))
        time.sleep(interval)


def clearClip():
    pyperclip.copy("")


class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.targetList = ["female", "male", "mix"]
        self.levelList = ["max", "min", "mix"]

        self.target = "female"
        self.level = "max"
        self.interval = 0.1

        self.status = False
        self.process = None
        atexit.register(self.killProcess)

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.createElements()

        # self.resize(400, 400)
        self.center()
        self.setWindowTitle('HorseHunter')
        self.show()
        self.setFixedSize(self.size())

    def createElements(self):
        currentRow = 1

        self.targetLabel = QLabel("Target")
        self.grid.addWidget(self.targetLabel, currentRow, 0, 1, 3)
        currentRow += 1
        self.targetGroup = QButtonGroup(self)
        self.targetAudioButtons = [QRadioButton(v) for v in self.targetList]
        for i, b in enumerate(self.targetAudioButtons):
            b.target = self.targetList[i]
            self.targetGroup.addButton(b, i)
            self.grid.addWidget(b, currentRow, i, 1, 1)
        self.targetAudioButtons[0].setChecked(True)
        currentRow += 1

        self.levelLabel = QLabel("Level")
        self.grid.addWidget(self.levelLabel, currentRow, 0, 1, 3)
        currentRow += 1
        self.levelGroup = QButtonGroup(self)
        self.levelAudioButtons = [QRadioButton(v) for v in self.levelList]
        for i, b in enumerate(self.levelAudioButtons):
            b.level = self.levelList[i]
            self.levelGroup.addButton(b, i)
            self.grid.addWidget(b, currentRow, i, 1, 1)
        self.levelAudioButtons[0].setChecked(True)
        currentRow += 1

        self.intervalLabel = QLabel("Interval(s)")
        self.grid.addWidget(self.intervalLabel, currentRow, 0, 1, 1)
        self.intervalInput = QLineEdit(self)
        self.grid.addWidget(self.intervalInput, currentRow, 1, 1, 2)
        self.intervalInput.setText("0.1")
        self.intervalInput.setValidator(QDoubleValidator(0.00, 99.99, 4))
        currentRow += 1

        self.statusLable = QLabel("Terminated")
        self.grid.addWidget(self.statusLable, currentRow, 0, 1, 2)
        self.StartStopButton = QPushButton("Start/Stop")
        self.grid.addWidget(self.StartStopButton, currentRow, 1, 1, 2)
        self.StartStopButton.clicked.connect(self.startStop)
        currentRow += 1

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def killProcess(self):
        clearClip()
        if self.process and self.process.is_alive():
            self.process.terminate()
            self.process = None

    def startStop(self):
        self.killProcess()

        self.status = not self.status
        if self.status:
            lines = getLines({
                "level": self.levelList[self.levelGroup.checkedId()],
                "target": self.targetList[self.targetGroup.checkedId()],
            })
            try:
                interval = float(self.intervalInput.text())
            except:
                interval = 0.1
            self.process = Process(target=job, args=(lines, interval,))
            self.process.start()
            self.statusLable.setText("Running...")
        else:
            self.statusLable.setText("Terminated")


if __name__ == '__main__':
    atexit.register(clearClip)

    freeze_support()
    path = getattr(sys, '_MEIPASS', os.getcwd())
    os.chdir(path)

    app = QApplication(sys.argv)

    main = Main()

    app.aboutToQuit.connect(main.killProcess)

    sys.exit(app.exec_())
