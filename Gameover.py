from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class GameoverWindow(QLabel):
    def __init__(self, color, parent=None):
        super(GameoverWindow, self).__init__(parent=parent)
        self.setGeometry(0, 0, 500, 400)
        self.setAttribute(Qt.WA_TranslucentBackground)
        font = QFont('Century Gothic', 37)
        self.setFont(font)
        if color == 'b':
            self.move(20, 60)
            self.setText('White won the game')
        else:
            self.move(20, 60)
            self.setText('Black won the game')
        self.show()
