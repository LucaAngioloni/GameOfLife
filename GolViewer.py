from PyQt5.QtGui import QImage, qRgb, QPixmap, QPainter, QPen
from PyQt5.QtCore import (Qt, QSize, QPoint)
from PyQt5.QtWidgets import (QSlider, QLabel, QWidget, QScrollArea, QSizePolicy)

import numpy as np


class GolViewer(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)


    def set_model(self, gol):
        self.gol = gol

    def updateView(self):
        mat = self.gol.get_state()
        mat = np.require(mat, np.uint8, 'C')
        qim = self.toQImage(mat)
        qpix = QPixmap.fromImage(qim)
        self.setPixmap(qpix.scaled(self.size(), Qt.KeepAspectRatio, Qt.FastTransformation))

    def toQImage(self, im, copy=False):
        gray_color_table = [qRgb(i, i, i) for i in range(256)]
        if im is None:
            return QImage()
        if len(im.shape) == 2:
            qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
            qim.setColorTable(gray_color_table)
            return qim.copy() if copy else qim
        elif len(im.shape) == 3:  # maybe in the future accept color images
            if im.shape[2] == 3:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888);
                return qim.copy() if copy else qim
            elif im.shape[2] == 4:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32);
                return qim.copy() if copy else qim

