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

import sys

from PyQt5.QtWidgets import QApplication  # pip install PyQt5

from GameOfLife import GameOfLife
from GolLoop import GolLoop
from MainWindow import MainWindow

qdark_present = True
try:
    import qdarkstyle  # Qt styling package, pip install qdarkstyle
except ImportError:
    qdark_present = False

if __name__ == '__main__':
    gol = GameOfLife()  # The model

    timer = GolLoop()  # The game loop
    timer.timeout.connect(gol.next)

    app = QApplication(sys.argv)
    if qdark_present:
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MainWindow(gol, timer)  # The view controller / view (GUI)
    sys.exit(app.exec_())
