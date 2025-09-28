import logging

class TetrisGame:
    def __init__(self, width: int = 10, height: int = 100) -> None:
        """Initializes a new Tetris game (list-of-lists version)."""
        self.width = width
        self.height = height
        self.grid = self.create_grid()
        self.pieces = {
            # Q (O-block): 2x2
            "Q": [[1, 1], [1, 1]],
            # Z: 2 rows, 3 cols
            "Z": [[1, 1, 0], [0, 1, 1]],
            # S: 2 rows, 3 cols
            "S": [[0, 1, 1], [1, 1, 0]],
            # T: 2 rows, 3 cols
            "T": [[1, 1, 1], [0, 1, 0]],
            # I: 1 row, 4 cols
            "I": [[1, 1, 1, 1]],
            # L: 4 rows, 2 cols
            "L": [[1, 0], [1, 0], [1, 0], [1, 1]],
            # J: 4 rows, 2 cols
            "J": [[0, 1], [0, 1], [0, 1], [1, 1]],
        }

    def create_grid(self) -> list[list[str]]:
        """Creates a new Tetris grid as a list of lists (' '/ 'O')."""
        return [[" " for _ in range(self.width)] for _ in range(self.height)]

    def print_grid(self) -> None:
        """Prints the current state of the grid (list version)."""
        logging.debug("Current grid state (beta):")
        for row in self.grid:
            row_str = ''.join(cell for cell in row)
            logging.debug(row_str)

    def place_piece(self, piece: list[list[int]], column: int) -> None:
        piece_height = len(piece)
        for row in range(self.height - piece_height, -1, -1):
            if self.can_place(piece, row, column):
                self.add_to_grid(piece, row, column)
                logging.debug(f"[Beta] Placed piece at row {row}, column {column}")
                self.print_grid()
                break

    def can_place(self, piece: list[list[int]], row: int, column: int) -> bool:
        piece_height = len(piece)
        piece_width = self._piece_width(piece)
        if column < 0 or column + piece_width > self.width:
            return False
        for i in range(piece_height):
            for j in range(piece_width):
                grid_row_idx = row + i
                grid_col_idx = column + j
                if piece[i][j]:
                    if grid_row_idx < 0 or grid_row_idx >= self.height:
                        return False
                    if grid_col_idx < 0 or grid_col_idx >= self.width:
                        return False
                    if self.grid[grid_row_idx][grid_col_idx] == "O":
                        return False
        return True

    def _piece_width(self, piece: list[list[int]]) -> int:
        return max((len(row) for row in piece), default=0)

    def add_to_grid(self, piece: list[list[int]], row: int, column: int) -> None:
        piece_height = len(piece)
        piece_width = self._piece_width(piece)
        for i in range(piece_height):
            for j in range(piece_width):
                if piece[i][j]:
                    self.grid[row + i][column + j] = "O"

    def clear_lines(self) -> None:
        new_grid = [row for row in self.grid if not all(cell == "O" for cell in row)]
        lines_cleared = self.height - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, [" " for _ in range(self.width)])
        self.grid = new_grid
        if lines_cleared > 0:
            self.print_grid()

    def calculate_height(self) -> int:
        for i, row in enumerate(self.grid):
            if any(cell == "O" for cell in row):
                return self.height - i
        return 0

    def process_input_line(self, line: str) -> int:
        for item in line.split(","):
            piece_type = item[0]
            column = int(item[1:])
            self.place_piece(self.pieces[piece_type], column)
            self.clear_lines()
        return self.calculate_height()
