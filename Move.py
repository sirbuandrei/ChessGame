pieces = []

grid = [['bR', 'bN', 'bB', 'bK', 'bQ', 'bB', 'bN', 'bR'],
        ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
        ['wR', 'wN', 'wB', 'wK', 'wQ', 'wB', 'wN', 'wR']]


def check_and_pins(white_turn):
    global x_from, y_from
    pins = []
    check = []
    inCheck = False
    if white_turn:
        enemyColor = 'b'
        allayColor = 'w'
    else:
        enemyColor = 'w'
        allayColor = 'b'

    # GET THE KING LOCATION
    for i in range(0, 8):
        for j in range(0, 8):
            if grid[i][j][0] == allayColor and grid[i][j][1] == 'K':
                x_from = i
                y_from = j
                break

    # POSSIBLE POSITION WHERE THE ATTACK MIGHT COME FROM RELATIVE TO KING POSITION
    positions_from_king = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]

    for pos in positions_from_king:
        possiblePin = ()  # RESET POSSIBLE PINS
        for k in range(1, 8):
            x_to = x_from + pos[0] * k
            y_to = y_from + pos[1] * k
            if 0 <= x_to < 8 and 0 <= y_to < 8:
                if grid[x_to][y_to][0] == allayColor and grid[x_to][y_to][0] != 'K':
                    if possiblePin == ():
                        possiblePin = (x_to, y_to, pos[0], pos[1])
                    else:  # IF ANOTHER ALLIED PIECE IS ON THE SAME DIR CAN BE A PIN WE DON T HAVE TO BOTHER,
                        # NO CHECK CAN COME FROM THAT DIR
                        break
                elif grid[x_to][y_to][0] == enemyColor:
                    piece = grid[x_to][y_to][1]
                    index = positions_from_king.index(pos)
                    if (0 <= index <= 3 and piece == 'R') or \
                            (4 <= index <= 7 and piece == 'B') or \
                            (piece == 'Q') or \
                            (k == 1 and piece == 'P') and ((enemyColor == 'w' and 6 <= index <= 7) or (enemyColor == 'b') and 4 <= index <= 5) or \
                            (k == 1 and piece == 'K'):
                        if possiblePin == ():
                            inCheck = True
                            check.append((x_to, y_to, pos[0], pos[1]))
                            break
                        else:
                            pins.append(possiblePin)
                            break
                    else:
                        break
            else:
                break

    positions_knight = [(2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]

    for pos in positions_knight:
        x_to = x_from + pos[0]
        y_to = y_from + pos[1]
        if 0 <= x_to < 8 and 0 <= y_to < 8:
            piece = grid[x_to][y_to]
            if piece[0] == enemyColor and piece[1] == 'N':
                inCheck = True
                check.append((x_to, y_to, pos[0], pos[1]))

    return inCheck, pins, check


def all_valid_moves():
    moves = []
    for i in range(0, 8):
        for j in range(0, 8):
            if grid[i][j] != '--':
                moves.append(possible_moves(i, j, grid[i][j][0], grid[i][j][1]))

    return moves


def possible_moves(x_from, y_from, color, piece):
    highlight = []

    if piece == 'P':
        positions_wp = [(-1, 0), (-2, 0), (-1, -1), (-1, 1)]
        positions_bp = [(1, 0), (2, 0), (1, 1), (1, -1)]

        if color == 'b':
            for position in positions_bp:
                x, y = position
                if 0 <= x_from + x < 8 and 0 <= y_from + y < 8:
                    if y == 0:
                        if x == 2:
                            if grid[x_from + x][y_from + y] == '--' and grid[x_from + 1][y_from] == '--':
                                highlight.append((x_from + x, y_from + y))
                        elif grid[x_from + x][y_from + y] == '--':
                            highlight.append((x_from + x, y_from + y))
                    elif grid[x_from + x][y_from + y][0] == 'w':
                        highlight.append((x_from + x, y_from + y))
        elif color == 'w':
            for position in positions_wp:
                x, y = position
                if 0 <= x_from + x < 8 and 0 <= y_from + y < 8:
                    if y == 0:
                        if x == -2:
                            if grid[x_from + x][y_from + y] == '--' and grid[x_from - 1][y_from] == '--':
                                highlight.append((x_from + x, y_from + y))
                        elif grid[x_from + x][y_from + y] == '--':
                            highlight.append((x_from + x, y_from + y))
                    else:
                        if grid[x_from + x][y_from + y][0] == 'b':
                            highlight.append((x_from + x, y_from + y))

    elif piece == 'R':
        rock_positions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for pos in rock_positions:
            for k in range(1, 8):
                x = pos[0] * k
                y = pos[1] * k
                if 0 <= x_from + x < 8 and 0 <= y_from + y < 8:
                    if grid[x_from + x][y_from + y][0] == color:
                        break
                    elif grid[x_from + x][y_from + y] == '--':
                        highlight.append((x_from + x, y_from + y))
                    else:
                        highlight.append((x_from + x, y_from + y))
                        break

    elif piece == 'B':
        bishop_positions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        for pos in bishop_positions:
            for k in range(1, 8):
                x = pos[0] * k
                y = pos[1] * k
                if 0 <= x_from + x < 8 and 0 <= y_from + y < 8:
                    if grid[x_from + x][y_from + y][0] == color:
                        break
                    elif grid[x_from + x][y_from + y] == '--':
                        highlight.append((x_from + x, y_from + y))
                    else:
                        highlight.append((x_from + x, y_from + y))
                        break

    elif piece == 'K':
        positions_king = [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]

        for position in positions_king:
            x, y = position
            if 0 <= x_from + x < 8 and 0 <= y_from + y < 8:
                if grid[x_from + x][y_from + y] == '--' or grid[x_from + x][y_from + y][0] != color:
                    highlight.append((x_from + x, y_from + y))

    elif piece == 'N':
        positions_knight = [(2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]

        for position in positions_knight:
            x, y = position
            if 0 <= x_from + x < 8 and 0 <= y_from + y < 8:
                if grid[x_from + x][y_from + y] == '--' or grid[x_from + x][y_from + y][0] != color:
                    highlight.append((x_from + x, y_from + y))

    elif piece == 'Q':
        queen_positions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]

        for pos in queen_positions:
            for k in range(1, 8):
                x = pos[0] * k
                y = pos[1] * k
                if 0 <= x_from + x < 8 and 0 <= y_from + y < 8:
                    if grid[x_from + x][y_from + y][0] == color:
                        break
                    elif grid[x_from + x][y_from + y] == '--':
                        highlight.append((x_from + x, y_from + y))
                    else:
                        highlight.append((x_from + x, y_from + y))
                        break

    return highlight


def divide(x, y):
    try:
        return x/y
    except ZeroDivisionError:
        return 0


def comprehension(a, b):
    return [x for x in a if x not in b]


def comprehension2(a, b):
    return [x for x in a if x in b]