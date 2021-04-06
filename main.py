# CHESS GAME USING PYQT5
# A PIECE CAN BE MOVED WITH A DRAGGING MOTION FROM IT S LOCATION TO THE LOCATION DESIRED
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Move import pieces, grid, possible_moves, check_and_pins, divide, comprehension, comprehension2
from Gameover import GameoverWindow
import numpy as np
import sys

# KEEPING TRACK OF THE PRESSED PIECE
piece_pressed = None
# KEEPING TRACK OF THE PIECES
pos = []
highlighted_moves = []
check_label = None
white_turn = True
piece_checking = None
valid_pos = []

checks = []
pins = []
inCheck = False

gameover = False


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
        self.setMinimumSize(self.HEIGHT, self.WIDTH)
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
        global piece_pressed, white_turn, gameover, pos, highlighted_moves, piece_checking, check_label, inCheck, pins, checks, valid_pos, king_x, king_y
        if piece_pressed:
            if event.button() == Qt.LeftButton:
                for hm in highlighted_moves:
                    hm.hide()
                highlighted_moves = []

                # GET THE INDEXES OF THE SQUARE WHERE IT HAS TO MOVE INDEXES
                x = event.y() // 60
                y = event.x() // 60

                # MAKE SURE WE DONT ACCIDENTALLY DRAG THE PIECE TO IT S CURRENT POSITION
                if piece_pressed.x == x and piece_pressed.y == y:
                    return

                # CHECK IF THE MOVE YOU WANT TO MAKE WITH THE PRESSED PIECE IS OK AND IF YOU CAPTURE A PIECE AND
                # MUST REMOVE IT FROM THE CHESS GAME
                pair = (x, y)
                if pair in pos:

                    if grid[x][y] != '--':
                        for piece in pieces:
                            if piece.x == x and piece.y == y:
                                piece.hide()
                                pieces.remove(piece)

                    # UPDATE THE GRID ( PLACE AN EMPTY SPOT AT THE PIECE COORDS AND PLACE THE PIECE AT THE NEW COORDS )
                    grid[x][y] = piece_pressed.image
                    grid[piece_pressed.x][piece_pressed.y] = '--'

                    # MOVE THE PIECE AND MAKE THE PRESSED PIECE EQUAL TO NONE
                    self.doAnim(piece_pressed, x, y)

                    # UPDATE PIECE COORDS
                    piece_pressed.x = x
                    piece_pressed.y = y

                    white_turn = not white_turn
                    inCheck, pins, checks = check_and_pins(white_turn)
                    if inCheck:
                        valid_pos = []
                        if white_turn:
                            color = 'w'
                        else:
                            color = 'b'

                        for i in range(0, 8):
                            for j in range(0, 8):
                                if grid[i][j][0] == color and grid[i][j][1] == 'K':
                                    king_x = i
                                    king_y = j
                                    break

                        if len(checks) == 1:
                            direction = (checks[0][2], checks[0][3])
                            if piece_pressed.image[1] == 'N':
                                valid_pos = [(king_x + direction[0], king_y + direction[1])]
                            else:
                                for k in range(1, 8):
                                    x_to = king_x + direction[0] * k
                                    y_to = king_y + direction[1] * k
                                    if 0 <= x_to < 8 and 0 <= y_to < 8:
                                        valid_pos.append((x_to, y_to))
                                        if grid[x_to][y_to] == piece_pressed.image:
                                            break
                        else:
                            pass

                    piece_pressed = None
                    pos = []  # REST POSSIBLE POSITIONS
                #else:
                    #QMessageBox.critical(self, 'Wrong Move', 'You can not make that move!', QMessageBox.Ok)

    def doAnim(self, piece, x_to, y_to):
        self.anim = QPropertyAnimation(piece, b"geometry")
        self.anim.setDuration(500)
        self.anim.setStartValue(QRect(piece.y * 60, piece.x * 60, 60, 60))
        self.anim.setEndValue(QRect(y_to * 60, x_to * 60, 60, 60))
        self.anim.start()


# LABEL FOR EVEY CHESS PIECE TO DISPLAY IMAGE
class ChessLabel(QLabel):

    def __init__(self, x, y, image, parent):
        super(ChessLabel, self).__init__(parent=parent)
        self.x = x
        self.y = y
        self.image = image
        self.parent = parent
        self.setGeometry(y * 60, x * 60, 60, 60)
        # GET THE IMAGE PATH
        self.path = 'images/' + image + '.png'
        # SET THE PIXMAP FOR THE IMAGE
        self.pixmap = QPixmap(self.path)
        self.setPixmap(self.pixmap)
        self.pinned = False
        self.pinned_dir = None

    # GET THE PRESSED PIECE
    def mousePressEvent(self, event):
        global piece_pressed, pos, highlighted_moves, check, inCheck, pins, checks, pos_to_remove, valid_pos, gameover, grid, grid_copy
        if not gameover and (white_turn and self.image[0] == 'w') or (not white_turn and self.image[0] == 'b'):
            if event.button() == Qt.LeftButton:
                piece_pressed = self
                pos = possible_moves(self.x, self.y, self.image[0], self.image[1])
                if inCheck:
                    if len(checks) == 1:

                        if self.image[1] != 'K':
                            pos = comprehension2(pos, valid_pos)
                            print(self.pinned)
                            if self.pinned:
                                pos = []

                        elif self.image[1] == 'K':
                            pos_to_remove = []
                            for p in pos:
                                copy = grid[p[0]][p[1]]
                                grid[p[0]][p[1]] = self.image
                                grid[self.x][self.y] = '--'
                                check, pi, ch = check_and_pins(white_turn)
                                if check:
                                    pos_to_remove.append((p[0], p[1]))
                                grid[self.x][self.y] = self.image
                                grid[p[0]][p[1]] = copy
                            pos = comprehension(pos, pos_to_remove)

                    elif len(checks) == 2:
                        if self.image[1] != 'K':
                            pos = []
                        elif self.image[1] == 'K':
                            pos_to_remove = []
                            for p in pos:
                                copy = grid[p[0]][p[1]]
                                grid[p[0]][p[1]] = self.image
                                grid[self.x][self.y] = '--'
                                check, pi, ch = check_and_pins(white_turn)
                                if check:
                                    pos_to_remove.append((p[0], p[1]))
                                grid[self.x][self.y] = self.image
                                grid[p[0]][p[1]] = copy
                            pos = comprehension(pos, pos_to_remove)

                    for p in pos:
                        highlighted_moves.append(LabelHighlightMove(*p, self.parent))

                elif not inCheck:
                    if self.image[1] != 'K':
                        self.pinned = False
                        for pin in pins:
                            if self.x == pin[0] and self.y == pin[1]:
                                self.pinned = True
                                self.pinned_dir = (pin[2], pin[3])

                        if self.pinned:
                            if self.image[1] == 'N':
                                pos = []
                            else:
                                pos_to_remove = []
                                for p in pos:
                                    x = divide(p[0] - self.x, abs(p[0] - self.x))
                                    y = divide(p[1] - self.y, abs(p[1] - self.y))
                                    if x == self.pinned_dir[0] and y == self.pinned_dir[1] or (
                                            x == -self.pinned_dir[0] and y == -self.pinned_dir[1]):
                                        highlighted_moves.append(LabelHighlightMove(*p, self.parent))
                                    else:
                                        pos_to_remove.append(p)

                                pos = comprehension(pos, pos_to_remove)

                        else:
                            for p in pos:
                                highlighted_moves.append(LabelHighlightMove(*p, self.parent))

                    else:
                        pos_to_remove = []
                        for p in pos:
                            copy = grid[p[0]][p[1]]
                            grid[p[0]][p[1]] = self.image
                            grid[self.x][self.y] = '--'
                            check, pi, ch = check_and_pins(white_turn)
                            if check:
                                pos_to_remove.append((p[0], p[1]))
                            grid[self.x][self.y] = self.image
                            grid[p[0]][p[1]] = copy
                        pos = comprehension(pos, pos_to_remove)

                        for p in pos:
                            highlighted_moves.append(LabelHighlightMove(*p, self.parent))

        super(ChessLabel, self).mousePressEvent(event)


class LabelHighlightMove(QLabel):
    def __init__(self, x, y, parent):
        super(LabelHighlightMove, self).__init__(parent=parent)
        self.setGeometry(y * 60 + 1, x * 60 + 1, 59, 59)
        self.setWindowOpacity(0.5)
        self.setStyleSheet("QLabel{\n"
                           "background-color: rgba(255, 224, 50, 50);\n"
                           "}")
        self.show()


class CheckLabel(QLabel):
    def __init__(self, x, y, piece, parent):
        super(CheckLabel, self).__init__(parent=parent)
        self.setGeometry(y * 60 + 1, x * 60 + 1, 59, 59)
        self.setWindowOpacity(0.5)
        self.stackUnder(piece)
        self.setStyleSheet("QLabel{\n"
                           "background-color: rgba(178, 34, 34, 50);\n"
                           "}")
        self.show()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
