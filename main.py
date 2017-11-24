import sys

from GameOfLife import GameOfLife
from MainWindow import MainWindow
from GolLoop import GolLoop

from PyQt5.QtWidgets import QApplication

qdark_present = True
try:
    import qdarkstyle  # Qt styling package
except ImportError:
    qdark_present = False


if __name__ == '__main__':
    gol = GameOfLife(100, 150, 'random')

    timer = GolLoop()
    timer.timeout.connect(gol.next)

    app = QApplication(sys.argv)
    if qdark_present:
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MainWindow(gol, timer)
    sys.exit(app.exec_())