import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QSlider, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox)

from GolViewer import GolViewer

class PlayPauseButton(QPushButton):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(100)
        self.btn_text = ["  Play  ", "Pause"]
        self.i = 0

        self.setText(self.btn_text[self.i])

        self.clicked.connect(self.changeText)

    def changeText(self):
        self.i += 1
        self.setText(self.btn_text[self.i % 2])

class MainWindow(QWidget):
    def __init__(self, gol, timer):
        super().__init__()

        self.gol = gol
        self.timer = timer
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Game of Life")

        self.viewer = GolViewer()
        # self.viewer = QLabel()
        self.viewer.resize(800, 600)
        self.viewer.set_model(self.gol)

        self.timer.timeout.connect(self.viewer.updateView)

        self.play_pause = PlayPauseButton()

        self.reset = QPushButton()
        self.reset.setText("Reset")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(10)
        self.slider.setMaximum(1000)
        self.slider.setValue(910)
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(QSlider.TicksBelow)

        self.load = QPushButton()
        self.load.setText("Load")

        self.save = QPushButton()
        self.save.setText("Save")

        h_box = QHBoxLayout()
        h_box.addWidget(self.play_pause)
        h_box.addWidget(self.reset)
        h_box.addStretch()
        h_box.addWidget(QLabel('Speed '))
        h_box.addWidget(self.slider)
        h_box.addStretch()
        h_box.addWidget(self.load)
        h_box.addWidget(self.save)

        v_box = QVBoxLayout()
        v_box.addWidget(self.viewer)
        v_box.addLayout(h_box)

        self.setLayout(v_box)

        self.play_pause.clicked.connect(self.play_pause_clicked)
        self.reset.clicked.connect(self.reset_clicked)
        self.slider.valueChanged.connect(self.slider_changed)
        self.load.clicked.connect(self.load_clicked)
        self.save.clicked.connect(self.save_clicked)

        self.setMinimumSize(600, 400)
        self.viewer.updateView()
        self.show()

    def play_pause_clicked(self):
        self.timer.play_pause()

    def reset_clicked(self):
        if self.timer.is_going():
            self.timer.play_pause()
            self.play_pause.changeText()
        self.gol.reset()
        self.viewer.updateView()

    def slider_changed(self):
        speed = 1010 - self.slider.value()
        self.timer.set_speed(speed)

    def load_clicked(self):
        if self.timer.is_going():
            self.timer.play_pause()
            self.play_pause.changeText()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;PNG Save File (*.png);;TXT Save File (*.txt)", options=options)
        if fileName:
            if self.gol.load(fileName) is False:
                QMessageBox.about(self, "File Error", "File selected is not valid")
        else:
            QMessageBox.about(self, "File Name Error", "No file name selected")

        self.viewer.updateView()

    def save_clicked(self):
        if self.timer.is_going():
            self.timer.play_pause()
            self.play_pause.changeText()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "Save File as PNG (*.png)", options=options)
        if fileName:
            self.gol.save(fileName)
        else:
            QMessageBox.about(self, "File Name Error", "No file name selected")

    def resizeEvent(self, ev):
        self.viewer.updateView()
        super().resizeEvent(ev)