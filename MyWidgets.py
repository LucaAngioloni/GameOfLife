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

import os
import sys

from PyQt5.QtWidgets import QComboBox, QPushButton

class PatternMenu(QComboBox):
    """
    Custom combo box widget that auto populates its items with patterns found in the default directory

    Attributes:
        path_to_patterns    default directory for patterns
        files               string list of the file names of the files in path_to_patterns
    """

    def __init__(self):
        super().__init__()
        self.path_to_patterns = os.path.abspath(os.path.dirname(sys.argv[0])) + "/patterns/"
        self.files = sorted([f for f in os.listdir(self.path_to_patterns) if not f.startswith('.')],
                            key=lambda f: f.lower())
        self.addItem("Empty")
        self.addItem("Random")
        self.addItems(self.files)


class PlayPauseButton(QPushButton):
    """
        Custom push button that toggles automatically Play and Pause texts

        Attributes:
            btn_text    list of the 2 strings ["Play", "Pause"]
        """
    def __init__(self):
        super().__init__()

        self.setFixedWidth(100)
        self.btn_text = ["Play", "Pause"]
        self.i = 0

        self.setText(self.btn_text[self.i])

        self.clicked.connect(self.changeText)

    def changeText(self):
        """Slot for the clicked event; automatically changes the button text"""
        self.i += 1
        self.setText(self.btn_text[self.i % 2])