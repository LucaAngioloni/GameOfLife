from PyQt5.QtGui import QImage, qRgb, QPixmap, QPainter, QPen
from PyQt5.QtCore import (Qt, QSize, QPoint)
from PyQt5.QtWidgets import (QSlider, QLabel, QWidget, QScrollArea, QSizePolicy)

import numpy as np


class GolViewer(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.drawing = False
        self.V_margin = 0
        self.H_margin = 0
        self.h = 0
        self.w = 0

    def set_model(self, gol):
        self.gol = gol
        self.updateView()

    def updateView(self):
        mat = self.gol.get_state()
        self.h = mat.shape[0]
        self.w = mat.shape[1]
        qim = self.toQImage(mat)
        qpix = QPixmap.fromImage(qim)
        self.setPixmap(qpix.scaled(self.size(), Qt.KeepAspectRatio, Qt.FastTransformation))
        self.V_margin = (self.size().height() - self.pixmap().size().height())/2
        self.H_margin = (self.size().width() - self.pixmap().size().width())/2


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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            i = event.pos().y() - self.V_margin
            j = event.pos().x() - self.H_margin
            if i > 0 and j > 0 and i < self.pixmap().height() and j < self.pixmap().width():
                print("click pos i: " + str(i) + ", j: " + str(j))
                i = int(i * self.h / self.pixmap().height())
                j = int(j * self.w / self.pixmap().width())
                self.gol.set_pixel(i, j)
                self.updateView()


    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            i = event.pos().y() - self.V_margin
            j = event.pos().x() - self.H_margin
            if i > 0 and j > 0 and i < self.pixmap().height() and j < self.pixmap().width():
                print("move pos i: " + str(i) + ", j: " + str(j))
                i = int(i * self.h / self.pixmap().height())
                j = int(j * self.w / self.pixmap().width())
                self.gol.set_pixel(i, j)
                self.updateView()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawing = False