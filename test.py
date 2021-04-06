positions_from_king = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]

if __name__ == "__main__":
    for pos in positions_from_king:
        print(positions_from_king.index(pos))