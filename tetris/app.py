from __future__ import annotations

import logging
import sys

Piece = list[list[str]]


class TetrisGame:
    def __init__(self, width: int = 10, height: int = 100) -> None:
        """Initializes a new Tetris game.

        Args:
            width: The width of the grid.
            height: The height of the grid.
        """
        self.width: int = width
        self.height: int = height
        self.grid: list[list[str]] = self.create_grid()
        self.pieces: dict[str, Piece] = {
            "Q": [
                ["O", "O"],
                ["O", "O"],
            ],
            "Z": [
                ["O", "O", " "],
                [" ", "O", "O"],
            ],
            "S": [
                [" ", "O", "O"],
                ["O", "O", " "],
            ],
            "T": [
                ["O", "O", "O"],
                [" ", "O", " "],
            ],
            "I": [
                ["O", "O", "O", "O"],
            ],
            "L": [
                ["O", " "],
                ["O", " "],
                ["O", " "],
                ["O", "O"],
            ],
            "J": [
                [" ", "O"],
                [" ", "O"],
                [" ", "O"],
                ["O", "O"],
            ],
        }

    def create_grid(self) -> list[list[str]]:
        """Creates a new Tetris grid."""
        return [[" " for _ in range(self.width)] for _ in range(self.height)]

    def print_grid(self) -> None:
        """Prints the current state of the grid."""
        logging.debug("Current grid state:")
        for row in self.grid:
            logging.debug("".join(row))

    def place_piece(self, piece: Piece, column: int) -> None:
        """Places a piece on the grid."""
        for row in range(self.height - 1, -1, -1):
            if self.can_place(piece, row, column):
                self.add_to_grid(piece, row, column)
                logging.debug(f"Placed piece at row {row}, column {column}")
                self.print_grid()
                break

    def can_place(self, piece: Piece, row: int, column: int) -> bool:
        """Checks if a piece can be placed at the given row and column."""
        for row_index, row_ in enumerate(piece):
            for column_index, cell_value in enumerate(row_):
                if cell_value == "O":
                    grid_row = row + row_index
                    grid_col = column + column_index
                    if (
                        grid_row < 0
                        or grid_row >= self.height
                        or grid_col < 0
                        or grid_col >= self.width
                        or self.grid[grid_row][grid_col] == "O"
                    ):
                        return False
        return True

    def add_to_grid(self, piece: Piece, row: int, column: int) -> None:
        """Adds a piece to the grid at the specified position."""
        for row_index, row_ in enumerate(piece):
            for column_index, cell_value in enumerate(row_):
                if cell_value == "O":
                    self.grid[row + row_index][column + column_index] = "O"

    def clear_lines(self) -> None:
        """Clears any full horizontal lines and shifts rows down."""
        full_lines = [
            i for i, row in enumerate(self.grid) if all(cell == "O" for cell in row)
        ]
        for row_index in full_lines:
            del self.grid[row_index]
            self.grid.insert(0, [" " for _ in range(self.width)])
            self.print_grid()

    def calculate_height(self) -> int:
        """Calculates the height of the remaining blocks."""
        for i, row in enumerate(self.grid):
            if any(cell == "O" for cell in row):
                return self.height - i
        return 0

    def process_input_line(self, line: str) -> int:
        """Processes a line of input from the file."""
        for item in line.split(","):
            piece_type = item[0]
            column = int(item[1:])
            self.place_piece(self.pieces[piece_type], column)
            self.clear_lines()
        return self.calculate_height()


class TetrisApp:
    def __init__(self, **kwargs) -> None:
        self.game = TetrisGame(**kwargs)

    def run(self) -> None:
        """Main function to read input and write output."""
        for line in sys.stdin:
            line = line.strip()
            if line:
                height = self.game.process_input_line(line)
                sys.stdout.write(str(height))
