from timeit import default_timer as timer

from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import QImage, qRgb, QPixmap
from PyQt5.QtWidgets import (QLabel, QSizePolicy)


class GolViewer(QLabel):
    """
    Custom Widget to show and edit (with mouse events) the state of GoL.

    Attributes:
        gol         reference to an object of class GameOfLife (the model)
        drawing     bool value to keep track of mouse button long press and movement
        V_margin    dimension of right and left margin in window (widget) coordinates for the image
        H_margin    dimension of top and bottom margin in window (widget) coordinates for the image
        h           board (gol state) height
        w           board (gol state) height
        lastUpdate  time of the last view update
        pixmap      image representing the state of the game (QPixmap object) (self.pixmap())
    """

    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.drawing = False
        self.V_margin = 0
        self.H_margin = 0
        self.h = 0
        self.w = 0
        self.lastUpdate = timer()

    def set_model(self, gol):
        """
        Set the reference to the gol model.

        Args:
            gol     object of class GameOfLife
        """
        self.gol = gol
        self.updateView()  # update the view to show the first frame

    def updateView(self):
        """Update the view converting the current state (np.ndarray) to an image (QPixmap) and showing it on screen"""
        # All this conversion are not beautiful but necessary...
        mat = self.gol.get_state()
        self.h = mat.shape[0]
        self.w = mat.shape[1]
        qim = self.toQImage(mat)  # first convert to QImage
        qpix = QPixmap.fromImage(qim)  # then convert to QPixmap
        # set the pixmap and resize to fit the widget dimension
        self.setPixmap(qpix.scaled(self.size(), Qt.KeepAspectRatio, Qt.FastTransformation))
        # calculate the margins
        self.V_margin = (self.size().height() - self.pixmap().size().height()) / 2
        self.H_margin = (self.size().width() - self.pixmap().size().width()) / 2
        self.lastUpdate = timer()  # update the lastUpdate time

    def toQImage(self, im):
        """
        Utility method to convert a numpy array to a QImage object.

        Args:
            im          numpy array to be converted. It can be a 2D (BW) image or a color image (3 channels + alpha)

        Returns:
            QImage      The image created converting the numpy array
        """
        gray_color_table = [qRgb(i, i, i) for i in range(256)]
        if im is None:
            return QImage()
        if len(im.shape) == 2:  # 1 channel image
            qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
            qim.setColorTable(gray_color_table)
            return qim
        elif len(im.shape) == 3:  # maybe in the future accept color images (for heatmap)
            if im.shape[2] == 3:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888)
                return qim
            elif im.shape[2] == 4:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32)
                return qim

    def mousePressEvent(self, event):
        """Slot for mouse press event (Override)"""
        if event.button() == Qt.LeftButton:  # if left click draw living cells
            self.drawing = True
            i = event.pos().y() - self.V_margin
            j = event.pos().x() - self.H_margin
            # check if mouse is inside the bounds of the board
            if i > 0 and j > 0 and i < self.pixmap().height() and j < self.pixmap().width():
                # convert widget coordinate to state indexes
                i = int(i * self.h / self.pixmap().height())
                j = int(j * self.w / self.pixmap().width())

                self.gol.set_active_cell(i, j)
                self.updateView()

        if event.button() == Qt.RightButton:  # if right click kill cells
            self.drawing = True
            i = event.pos().y() - self.V_margin
            j = event.pos().x() - self.H_margin
            # check if mouse is inside the bounds of the board
            if i > 0 and j > 0 and i < self.pixmap().height() and j < self.pixmap().width():
                # convert widget coordinate to state indexes
                i = int(i * self.h / self.pixmap().height())
                j = int(j * self.w / self.pixmap().width())

                self.gol.set_inactive_cell(i, j)
                self.updateView()

    def mouseMoveEvent(self, event):
        """Slot for mouse move event (Override)"""
        if event.buttons() == Qt.LeftButton and self.drawing:  # if left click and self.drawing, draw living cells
            i = event.pos().y() - self.V_margin
            j = event.pos().x() - self.H_margin
            # check if mouse is inside the bounds of the board
            if i > 0 and j > 0 and i < self.pixmap().height() and j < self.pixmap().width():
                # convert widget coordinate to state indexes
                i = int(i * self.h / self.pixmap().height())
                j = int(j * self.w / self.pixmap().width())

                self.gol.set_active_cell(i, j)
                if (timer() - self.lastUpdate) > 0.04:
                    self.updateView()

        if event.buttons() == Qt.RightButton and self.drawing:  # if right click and self.drawing, kill living cells
            i = event.pos().y() - self.V_margin
            j = event.pos().x() - self.H_margin
            # check if mouse is inside the bounds of the board
            if i > 0 and j > 0 and i < self.pixmap().height() and j < self.pixmap().width():
                # convert widget coordinate to state indexes
                i = int(i * self.h / self.pixmap().height())
                j = int(j * self.w / self.pixmap().width())

                self.gol.set_inactive_cell(i, j)
                if (timer() - self.lastUpdate) > 0.04:
                    self.updateView()

    def mouseReleaseEvent(self, event):
        """Slot for mouse release event (Override)"""
        # release the self.drawing mode
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawing = False
        if event.button() == Qt.RightButton and self.drawing:
            self.drawing = False
