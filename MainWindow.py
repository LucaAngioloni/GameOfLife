import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QSlider, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox,
                             QComboBox, QCheckBox)

from GolViewer import GolViewer

class PatternMenu(QComboBox):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(250)
        self.path_to_patterns = os.path.abspath(os.path.dirname(sys.argv[0])) + "/patterns/"
        self.files = sorted([f for f in os.listdir(self.path_to_patterns) if not f.startswith('.')], key=lambda f: f.lower())
        self.addItem("Empty")
        self.addItem("Random")
        self.addItems(self.files)

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

        self.check_box = QCheckBox("Heatmap(History)")
        self.check_box.stateChanged.connect(self.check_box_slot)

        self.menu_label = QLabel("Known Patterns: ")
        self.menu = PatternMenu()
        self.menu.currentTextChanged.connect(self.change_pattern)

        top_h_box = QHBoxLayout()
        top_h_box.addWidget(self.menu_label)
        top_h_box.addWidget(self.menu)
        top_h_box.addStretch()
        top_h_box.addWidget(self.check_box)

        bottom_h_box = QHBoxLayout()
        bottom_h_box.addWidget(self.play_pause)
        bottom_h_box.addWidget(self.reset)
        bottom_h_box.addStretch()
        bottom_h_box.addWidget(QLabel('Speed '))
        bottom_h_box.addWidget(self.slider)
        bottom_h_box.addStretch()
        bottom_h_box.addWidget(self.load)
        bottom_h_box.addWidget(self.save)

        v_box = QVBoxLayout()
        v_box.addLayout(top_h_box)
        v_box.addWidget(self.viewer)
        v_box.addLayout(bottom_h_box)

        self.setLayout(v_box)

        self.play_pause.clicked.connect(self.play_pause_clicked)
        self.reset.clicked.connect(self.reset_clicked)
        self.slider.valueChanged.connect(self.slider_changed)
        self.load.clicked.connect(self.load_clicked)
        self.save.clicked.connect(self.save_clicked)

        self.setMinimumSize(600, 500)
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

    def check_box_slot(self, code):
        if code == Qt.Checked:
            self.gol.set_do_heatmap(True)
        else:
            self.gol.set_do_heatmap(False)
        self.viewer.updateView()

    def change_pattern(self, text):
        if self.timer.is_going():
            self.timer.play_pause()
            self.play_pause.changeText()
        if text == "Empty":
            self.gol.reinitialize('empty')
        elif text == "Random":
            self.gol.reinitialize('random')
        else:
            if self.gol.load(self.menu.path_to_patterns + text) is False:
                QMessageBox.about(self, "File Error", "File selected is not valid")
        self.viewer.updateView()
