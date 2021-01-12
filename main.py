# CHESS GAME USING PYQT5
# A PIECE CAN BE MOVED WITH A DRAGGING MOTION FROM IT S LOCATION TO THE LOCATION DESIRED
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import Move
from Gameover import GameoverWindow
import numpy as np
import sys

# KEEPING TRACK OF THE PRESSED PIECE
piece_pressed = None
# KEEPING TRACK OF THE TURN
white_turn = True
# KEEPING TRACK OF THE PIECES
pieces = []

gameover = False

# THE BRAD IS AN 8x8 GRID AND USING THIS FORMAT I PLACE THE PIECES ON THE BOARD AND MOVE THEM THROUGH OUT THE GAME
grid = [['bR', 'bN', 'bB', 'bK', 'bQ', 'bB', 'bN', 'bR'],
        ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
        ['wR', 'wN', 'wB', 'wK', 'wQ', 'wB', 'wN', 'wR']]


class MainWindow(QMainWindow):
    HEIGHT = 480
    WIDTH = 480

    def __init__(self):
        super(MainWindow, self).__init__()
        self.label = QLabel(self)
        self.setWindowTitle("Chess Game")
        # SET THE HEIGHT, WIDTH AND THE POSITION WHERE THE MAIN WINDOW HAS TO BE RENDERED
        self.setGeometry(300, 300, self.HEIGHT, self.WIDTH)
        # SET THE MAXIM AND MINIMUM SIZE OF THE WINDOW SO I WONT HAVE TO RESIZE PIECES IMAGES LATER IF THE
        # MAIN WINDOW IS RESIZED
        self.setMaximumSize(self.HEIGHT, self.WIDTH)
        self.setMaximumSize(self.HEIGHT, self.WIDTH)
        self.get_pieces()

    # DRAW THE BOARD
    def paintEvent(self, event):
        # SET A QPAINTER TO DRAW INSIDE MAIN WINDOW
        painter = QPainter(self)
        # THE BOARD IS AN 8x8 AND MY DIMENSIONS, A PIECE IS 60x60 SO MY GRID WILL BE (60x8)x(60x8). I WILL PLACE
        # A COLORED RECT ( WHITE OR GRAY ) EVERY 60 PIXELS
        for i in range(0, 8):
            for j in range(0, 8):
                # ALTERNATE BETWEEN WHITE AND GREY
                if (i + j) % 2 == 0:
                    painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
                    painter.drawRect(i * 60, j * 60, (i + 1) * 60, (j + 1) * 60)
                else:
                    painter.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
                    painter.drawRect(i * 60, j * 60, (i + 1) * 60, (j + 1) * 60)

    def get_pieces(self):
        # DRAW THE PIECES FROM THE GRID MATRIX
        for i in range(0, 8):
            for j in range(0, 8):
                if grid[i][j] != '--':
                    pieces.append(ChessLabel(i, j, grid[i][j], self))

    # IF YOU WANT TO MOVE A PIECE, MUST COMPLETE A 'DRAGGING' MOTION SO THE PLACE WHERE YOU RELEASE THE LEFT BUTTON
    # GIVES THE SQUARE WHERE THE PRESSED PIECE HAS TO MOVE
    def mouseReleaseEvent(self, event):
        global piece_pressed, grid, gameover, white_turn
        if piece_pressed:
            if event.button() == Qt.LeftButton:
                # GET THE INDEXES OF THE SQUARE WHERE IT HAS TO MOVE INDEXES
                x = event.y() // 60
                y = event.x() // 60

                # MAKE SURE WE DONT ACCIDENTALLY DRAG THE PIECE TO IT S CURRENT POSITION
                if piece_pressed.x == x and piece_pressed.y == y:
                    return

                # CHECK IF THE MOVE YOU WANT TO MAKE WITH THE PRESSED PIECE IS OK AND IF YOU CAPTURE A PIECE AND
                # MUST REMOVE IT FROM THE CHESS GAME
                ok, remove = Move.check_move(piece_pressed.x, piece_pressed.y, x, y, piece_pressed.image[0],
                                             piece_pressed.image[1], grid)
                if ok:
                    if remove:
                        # REMOVE THE PIECE CAPTURED FROM THE GRID
                        # ITERATE THOUGH THE PIECES AND FIND THE RIGHT ONE CAPTURED
                        for piece in pieces:
                            if piece.x == x and piece.y == y:
                                if piece.image[1] == 'K':
                                    self.label.setGeometry(0, 0, 500, 400)
                                    self.label.setAttribute(Qt.WA_TranslucentBackground)
                                    if piece.image[0] == 'b':
                                        font = QFont('Century Gothic', 37, Qt.red)
                                        self.label.setFont(font)
                                        self.label.move(20, 60)
                                        self.label.setText('White won the game')
                                    else:
                                        font = QFont('Century Gothic', 37, Qt.red)
                                        self.label.setFont(font)
                                        self.label.move(20, 60)
                                        self.label.setText('Black won the game')
                                    self.label.show()
                                    gameover = True
                                piece.hide()
                                pieces.remove(piece)

                    # UPDATE THE GRID ( PLACE AN EMPTY SPOT AT THE PIECE COORDS AND PLACE THE PIECE AT THE NEW COORDS )
                    grid[x][y] = piece_pressed.image
                    grid[piece_pressed.x][piece_pressed.y] = '--'

                    # UPDATE PIECE COORDS
                    piece_pressed.x = x
                    piece_pressed.y = y

                    # MOVE THE PIECE AND MAKE THE PRESSED PIECE EQUAL TO NONE
                    piece_pressed.move(event.x() // 60 * 60, event.y() // 60 * 60)
                    piece_pressed = None

                    white_turn = not white_turn
                else:
                    QMessageBox.critical(self, 'Wrong Move', 'You can not make that move!', QMessageBox.Ok)


# LABEL FOR EVEY CHESS PIECE TO DISPLAY IMAGE
class ChessLabel(QLabel):

    def __init__(self, x, y, image, parent):
        super(ChessLabel, self).__init__(parent=parent)
        self.x = x
        self.y = y
        self.image = image
        self.setGeometry(y * 60, x * 60, 60, 60)
        # GET THE IMAGE PATH
        self.path = 'images/' + image + '.png'
        # SET THE PIXMAP FOR THE IMAGE
        self.pixmap = QPixmap(self.path)
        self.setPixmap(self.pixmap)

    # GET THE PRESSED PIECE
    def mousePressEvent(self, event):
        global piece_pressed
        if (white_turn and self.image[0] == 'w') or (not white_turn and self.image[0] == 'b'):
            if not gameover and event.button() == Qt.LeftButton:
                piece_pressed = self

        super(ChessLabel, self).mousePressEvent(event)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
