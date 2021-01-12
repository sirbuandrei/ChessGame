# CHECK_MOVE FUNCTION WILL RETURN 2 PARAMETERS: 1st IF THE MOVE CAN BE MADE, 2nd IF WITH THAT MOVE THE PIECE CAPTURES
# ANOTHER PIECE
def check_move(x_from, y_from, x_to, y_to, color, piece, grid):
    # CHECK MOVE FOR PAWN
    # A PAWN CAN MOVE ONLY FORWARD 1 OR 2 BLOCKS AND MOVE DIAGONALLY 1 BLOCK IF IT CNA CAPTURE ANOTHER PIECE
    if piece == 'P':
        # IF THE COLOR IS WHITE THE MOVEMENT CAN BE ONLY ( TOWARDS THE BOTTOM OF THE BOARD )
        if color == 'w':
            if x_to < x_from:
                if x_from - x_to <= 2 and y_to == y_from:
                    if grid[x_to][y_to] == '--':
                        return True, False
                if x_from - x_to == 1 and abs(y_to - y_from) == 1:
                    if grid[x_from - 1][y_from - 1][0] == 'b' or grid[x_from - 1][y_from + 1][0] == 'b':
                        return True, True
        # IF THE COLOR IS BLACK THE MOVEMENT CAN BE ONLY FORWARD ( TOWARDS THE TOP OF THE BOARD )
        elif color == 'b':
            if x_to > x_from:
                if x_from - x_to <= 2 and y_to == y_from:
                    if grid[x_to][y_to] == '--':
                        return True, False
                if x_to - x_from == 1 and abs(y_to - y_from) == 1:
                    if grid[x_from + 1][y_from - 1][0] == 'w' or grid[x_from + 1][y_from + 1][0] == 'w':
                        return True, True

    # CHECK MOVE FOR ROCK
    # A ROCK CAN MOVE FORWARD, BACKWARD AND SIDE TO SIDE
    if piece == 'R':
        ok = False
        # GET THE POSITION WHERE THE ROCK CAN BE MOVED
        positions_rock = []
        for x in range(x_from + 1, 8):
            if 8 - x != 0:
                positions_rock.append((8 - x, 0))
        for x in range(0, x_from + 1):
            if -(x_from - x) != 0:
                positions_rock.append((-(x_from - x), 0))
        for y in range(y_from + 1, 8):
            if 8 - y != 0:
                positions_rock.append((0, 8 - y))
        for y in range(0, y_from + 1):
            if -(y_from - y) != 0:
                positions_rock.append((0, -(y_from - y)))

        for position in positions_rock:
            x, y = position
            if x_from + x == x_to and y_from + y == y_to:
                ok = True

        if ok:
            if x_from == x_to:
                for y in range(min(y_from, y_to) + 1, max(y_from, y_to)):
                    if grid[x_to][y] != '--':
                        return False, False
            elif y_from == y_to:
                for x in range(min(x_from, x_to) + 1, max(x_from, x_to)):
                    if grid[x][y_to] != '--':
                        return False, False

            if grid[x_to][y_to] == '--':
                return True, False
            elif grid[x_to][y_to] != '--' and color == 'w' and grid[x_to][y_to][0] == 'b':
                return True, True
            elif grid[x_to][y_to] != '--' and color == 'b' and grid[x_to][y_to][0] == 'w':
                return True, True

    # CHECK MOVE FOR BISHOP
    # A BISHOP CAN MOVE DIAGONALLY
    if piece == 'B':
        ok = False
        positions_bishop = []
        for k in range(1, 8):
            positions_bishop.append((k, k))
            positions_bishop.append((-k, -k))
            positions_bishop.append((k, -k))
            positions_bishop.append((-k, k))

        for position in positions_bishop:
            x, y = position
            if x_from + x == x_to and y_from + y == y_to:
                ok = True

        if ok:
            for k in range(1, abs(x_to - x_from)):
                print(k)
                if x_to > x_from and y_to > y_from:
                    print('+ +')
                    if grid[x_from + k][y_from + k] != '--':
                        return False, False
                elif x_to > x_from and y_to < y_from:
                    print('+ -')
                    if grid[x_from + k][y_from - k] != '--':
                        return False, False
                elif x_to < x_from and y_to > y_from:
                    print('- +')
                    if grid[x_from - k][y_from + k] != '--':
                        return False, False
                elif x_to < x_from and y_to < y_from:
                    print('- -')
                    if grid[x_from - k][y_from - k] != '--':
                        return False, False
            if grid[x_to][y_to] == '--':
                return True, False
            elif grid[x_to][y_to] != '--' and color == 'w' and grid[x_to][y_to][0] == 'b':
                return True, True
            elif grid[x_to][y_to] != '--' and color == 'b' and grid[x_to][y_to][0] == 'w':
                return True, True

    # CHECK MOVE FOR KING
    # A KING CAN MOVE FORWARD, BACKWARD, SIDE TO SIDE ADN DIAGONALLY ONLY 1 BLOCK
    if piece == 'K':
        ok = False
        positions_king = [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]

        for position in positions_king:
            x, y = position
            if x_from + x == x_to and y_from + y == y_to:
                ok = True

        if ok:
            if grid[x_to][y_to] == '--':
                return True, False
            elif grid[x_to][y_to] != '--' and color == 'w' and grid[x_to][y_to][0] == 'b':
                return True, True
            elif grid[x_to][y_to] != '--' and color == 'b' and grid[x_to][y_to][0] == 'w':
                return True, True

    # CHECK MOVE FOR KNIGHT
    # A KNIGHT CAN MOVE IN 'L' SHAPE
    if piece == 'N':
        ok = False
        # POSITION WHERE THE KNIGHT CAN MOVE FROM IT S CURRENT POSITION
        positions_knight = [(2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]

        for position in positions_knight:
            x, y = position
            if x_from + x == x_to and y_from + y == y_to:
                ok = True

        if ok:
            if grid[x_to][y_to] == '--':
                return True, False
            elif grid[x_to][y_to] != '--' and color == 'w' and grid[x_to][y_to][0] == 'b':
                return True, True
            elif grid[x_to][y_to] != '--' and color == 'b' and grid[x_to][y_to][0] == 'w':
                return True, True

    # CHECK MOVE FOR QUEEN
    # A QUEEN CAN MOVE FORWARD, BACKWARD, SIDE TO SIDE ADN DIAGONALLY ( A ROCKs MOVEMENT COMBINED WITH A
    # BISHOPs MOVEMENT )
    if piece == 'Q':
        ok = False
        position_queen = []
        for k in range(1, 8):
            position_queen.append((k, k))
            position_queen.append((-k, -k))
            position_queen.append((k, -k))
            position_queen.append((-k, k))
        for x in range(x_from + 1, 8):
            if 8 - x != 0:
                position_queen.append((8 - x, 0))
        for x in range(0, x_from + 1):
            if -(x_from - x) != 0:
                position_queen.append((-(x_from - x), 0))
        for y in range(y_from + 1, 8):
            if 8 - y != 0:
                position_queen.append((0, 8 - y))
        for y in range(0, y_from + 1):
            if -(y_from - y) != 0:
                position_queen.append((0, -(y_from - y)))

        for position in position_queen:
            x, y = position
            if x_from + x == x_to and y_from + y == y_to:
                ok = True

        if ok:
            if x_from == x_to:
                for y in range(min(y_from, y_to) + 1, max(y_from, y_to)):
                    if grid[x_to][y] != '--':
                        return False, False
            elif y_from == y_to:
                for x in range(min(x_from, x_to) + 1, max(x_from, x_to)):
                    if grid[x][y_to] != '--':
                        return False, False
            for k in range(1, abs(x_to - x_from)):
                if x_to > x_from and y_to > y_from:
                    if grid[x_from + k][y_from + k] != '--':
                        return False, False
                elif x_to > x_from and y_to < y_from:
                    if grid[x_from + k][y_from - k] != '--':
                        return False, False
                elif x_to < x_from and y_to > y_from:
                    if grid[x_from - k][y_from + k] != '--':
                        return False, False
                elif x_to < x_from and y_to < y_from:
                    if grid[x_from - k][y_from - k] != '--':
                        return False, False
            if grid[x_to][y_to] == '--':
                return True, False
            elif grid[x_to][y_to] != '--' and color == 'w' and grid[x_to][y_to][0] == 'b':
                return True, True
            elif grid[x_to][y_to] != '--' and color == 'b' and grid[x_to][y_to][0] == 'w':
                return True, True

    return False, False
