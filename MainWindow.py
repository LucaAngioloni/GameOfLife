##
## MIT License
## 
## Copyright (c) 2017 Luca Angioloni
## 
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
## 
## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.
## 
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.
##

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QSlider, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox,
                             QCheckBox)

from GolViewer import GolViewer
from MyWidgets import PatternMenu, PlayPauseButton


class MainWindow(QWidget):
    """
    Main window controller

    Attributes:
        gol         reference to an object of class GameOfLife (the model)
        loop        reference to an object of class GolLoop (the main loop of the game)
        viewer      custom widget to show the Game of Life model
        ...some graphical elements
    """

    def __init__(self, gol, loop):
        super().__init__()

        self.gol = gol
        self.loop = loop
        self.init_ui()

    def init_ui(self):
        """Method to initialize the UI: layouts and components"""
        self.setWindowTitle("Game of Life")

        self.viewer = GolViewer()
        self.viewer.resize(800, 600)
        self.viewer.set_model(self.gol)

        self.loop.timeout.connect(self.viewer.updateView)

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

        self.check_box = QCheckBox("Heatmap (History)")
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
        """Slot for the play/pause button click event. It starts or pauses the loop"""
        self.loop.play_pause()

    def reset_clicked(self):
        """Slot for the reset button click event. Resets the model, pauses the loop and updates the view"""
        if self.loop.is_going():
            self.loop.play_pause()
            self.play_pause.changeText()
        self.gol.reset()
        self.viewer.updateView()

    def slider_changed(self):
        """Slot for the speed slider value changed signal. Changes the loop timeout time based on the speed"""
        speed = 1010 - self.slider.value()
        self.loop.set_speed(speed)

    def load_clicked(self):
        """Slot for the Load button click event. Opens a dialog to choose a file then signals the model to load it"""
        if self.loop.is_going():
            self.loop.play_pause()
            self.play_pause.changeText()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;PNG Save File (*.png);;TXT Save File (*.txt)",
                                                  options=options)
        if fileName:
            if self.gol.load(fileName) is False:
                QMessageBox.about(self, "File Error", "File selected is not valid")
            else:
                self.menu.addItem("- Custom pattern -")
                self.menu.setCurrentText("- Custom pattern -")
        else:
            QMessageBox.about(self, "File Name Error", "No file name selected")
        self.viewer.updateView()

    def save_clicked(self):
        """Slot for the Save button click event. Opens a dialog to choose a file then signals the model to save to it"""
        if self.loop.is_going():
            self.loop.play_pause()
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
        """Slot for window resize event (Override)"""
        self.viewer.updateView()
        super().resizeEvent(ev)

    def check_box_slot(self, code):
        """Slot for the Heatmap checkbox changed state signal. Checks the state and updates the model accordingly"""
        if code == Qt.Checked:
            self.gol.set_do_heatmap(True)
        else:
            self.gol.set_do_heatmap(False)
        self.viewer.updateView()

    def change_pattern(self, text):
        """Slot for the ComboBox changed state signal. Loads the selected known pattern"""
        if self.loop.is_going():
            self.loop.play_pause()
            self.play_pause.changeText()
        if text == "Empty":
            self.gol.reinitialize('empty')
        elif text == "Random":
            self.gol.reinitialize('random')
        elif text != "- Custom pattern -":
            last = self.menu.count() - 1
            if self.menu.itemText(last) == "- Custom pattern -":
                self.menu.removeItem(last)
            elif self.gol.load(self.menu.path_to_patterns + text) is False:
                QMessageBox.about(self, "File Error", "File selected is not valid")
        self.viewer.updateView()
