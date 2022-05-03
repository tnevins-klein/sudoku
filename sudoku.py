"""
Sudoku Solver
---
A Sudoku Solver using recursive backtracking and stack unwinding
(via exceptions).
"""
import copy


class UnsolvableBoard(Exception):
    pass


class Tile:
    coordinate: (int, int)
    solutions:  set[int]
    score:      int

    def __init__(self, coordinate, solutions):
        self.coordinate = coordinate
        self.solutions = solutions
        self.score = len(self.solutions)

    def __repr__(self):
        return f"Tile({self.coordinate}, {self.solutions})"


class Board:
    _changed: bool

    def __init__(self, board=None):
        if not board:
            board: list[list[int | None]] = [[None for j in range(9)] for i in range(9)]
        self.board = board

    @staticmethod
    def from_string(board_string: str):
        board = Board()
        for i, row in enumerate(board_string.strip('\n').split('\n')):
            for j, column in enumerate(row.split(' ')):
                if column != '.':
                    board.board[i][j] = int(column)
        return board

    def get_subgrid(self, x: int, y: int):
        subgrid_x = (x // 3) * 3
        subgrid_y = (y // 3) * 3

        return set(
            self.board[subgrid_y][subgrid_x:subgrid_x + 3] +
            self.board[subgrid_y + 1][subgrid_x:subgrid_x + 3] +
            self.board[subgrid_y + 2][subgrid_x:subgrid_x + 3]
        )

    def get_row(self, y: int):
        return set(self.board[y])

    def get_column(self, x: int):
        return set([row[x] for row in self.board])

    def used_numbers(self, x: int, y: int):
        return self.get_row(y) \
            .union(self.get_column(x)) \
            .union(self.get_subgrid(x, y))

    def possible_solutions(self, x: int, y: int):
        if self.board[y][x] is not None:
            return {self.board[y][x]}
        return set(range(1, 10)) \
            .difference(self.used_numbers(x, y))

    def get_tile_information(self, x, y):
        return Tile((x, y), self.possible_solutions(x, y))

    def min_poss(self) -> Tile:
        min_tile: Tile | None = None
        for y, row in enumerate(self.board):
            for x, column in enumerate(row):
                current_tile = self.get_tile_information(y, x)

                if column is not None:
                    continue

                if len(current_tile.solutions) == 0:
                    raise UnsolvableBoard(f"Cell at {current_tile.coordinate} has 0 solutions")
                elif min_tile is None or len(min_tile.solutions) < len(current_tile.solutions):
                    min_tile = current_tile

        return min_tile

    def reduce_one_possibility(self):
        for y, row in enumerate(self.board):
            for x, column in enumerate(row):
                if column is not None:
                    continue

                possibilities = self.possible_solutions(x, y)

                if len(possibilities) == 1:
                    self.board[y][x] = list(possibilities)[0]
                    self._changed = True

    def reduce_row_and_col_possibilities(self):
        for i in range(9):
            # A list of sets of possible solutions for a given row
            row_poss = [self.possible_solutions(i, j) for j in range(9)]

            # A list of sets of possible solutions for a given column
            col_poss = [self.possible_solutions(j, i) for j in range(9)]

            for digit in range(1, 10):
                possible_cells_row = [k for k, cell in enumerate(row_poss) if digit in cell]
                if len(possible_cells_row) == 1 and self.board[possible_cells_row[0]][i] is None:
                    self.board[possible_cells_row[0]][i] = digit
                    self._changed = True

            for digit in range(1, 10):
                possible_cells_col = [k for k, cell in enumerate(col_poss) if digit in cell]
                if len(possible_cells_col) == 1 and self.board[i][possible_cells_col[0]] is None:
                    self.board[i][possible_cells_col[0]] = digit
                    self._changed = True

    def solve(self):
        while True:
            self._changed = False
            self.reduce_one_possibility()
            self.reduce_row_and_col_possibilities()

            if not self._changed:
                break

        min_tile = self.min_poss()

        if not min_tile:
            return True

        progress = False

        for solution in min_tile.solutions:
            trial_board = copy.deepcopy(self)
            trial_board[min_tile.coordinate[0]][min_tile.coordinate[1]] = solution
            try:
                trial_board.solve()
            except UnsolvableBoard:
                continue

            self.board = trial_board.board
            progress = True
            return True

        if not progress:
            return UnsolvableBoard(f"No possibilities for tile {min_tile}")

    def __getitem__(self, item):
        return self.board.__getitem__(item)

    def __setitem__(self, key, value):
        return self.board.__setitem__(key, value)

    def __repr__(self):
        return '\n'.join([' '.join([str(x) if x else "." for x in row]) for row in self.board])


