import sudoku

TEST_BOARD = """
6 8 . . . 7 3 . .
. . 1 8 . . . . 2
4 . . . . . . 8 .
. . 9 7 . 1 . 4 3
. . . . 3 . 6 . 7
. . . . . . . 9 .
. . 6 . . . 9 . 4
. . 7 . 5 8 . . .
. 9 . . . . . . .
"""

EVIL_BOARD = """
4 . . . . . . 6 .
. . . . . 8 . . .
. . 1 5 9 . 7 . .
. . 8 . . 7 . . .
. . . . . 2 3 . .
1 . . 8 3 . . . 4
. . . . 2 . . . .
. . 5 3 1 . 9 . .
. 9 . . . . . . 7
"""


def test_board(name, b):
    print()
    print(name)
    b = sudoku.Board() \
        .from_string(b)

    print(b)
    b.solve()
    print('\n' + str(b))
    print()


if __name__ == "__main__":
    test_board("Easier Board", TEST_BOARD)
    test_board("Evil Board", EVIL_BOARD)
