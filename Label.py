from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

piece_pressed = None


class ChessLabel(QLabel):

    def __init__(self, x, y, image, parent):
        super(ChessLabel, self).__init__(parent=parent)
        self.setGeometry(y * 60, x * 60, 60, 60)
        self.path = 'images/' + image + '.png'
        self.pixmap = QPixmap(self.path)
        self.setPixmap(self.pixmap)

    def mousePressEvent(self, event):
        global piece_pressed
        if event.button() == Qt.LeftButton:
            piece_pressed = self

        super(ChessLabel, self).mousePressEvent(event)
