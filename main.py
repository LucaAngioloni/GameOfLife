import sys

from PyQt5.QtWidgets import QApplication

from GameOfLife import GameOfLife
from GolLoop import GolLoop
from MainWindow import MainWindow

qdark_present = True
try:
    import qdarkstyle  # Qt styling package
except ImportError:
    qdark_present = False

if __name__ == '__main__':
    gol = GameOfLife()  # The model

    timer = GolLoop()  # The game loop
    timer.timeout.connect(gol.next)

    app = QApplication(sys.argv)
    if qdark_present:
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MainWindow(gol, timer)  # The view controller / view
    sys.exit(app.exec_())
