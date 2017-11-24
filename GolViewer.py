from PyQt5.QtGui import QImage, qRgb, QPixmap, QPainter, QPen
from PyQt5.QtCore import (Qt, QSize, QPoint)
from PyQt5.QtWidgets import (QSlider, QLabel, QWidget, QScrollArea, QSizePolicy)


class GolViewer(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
