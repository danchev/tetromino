from __future__ import annotations

import logging
import sys

Piece = list[int]


class TetrisGame:
    def __init__(self, width: int = 10, height: int = 100) -> None:
        """Initializes a new Tetris game.

        Args:
            width: The width of the grid.
            height: The height of the grid.
        """
        self.width = width
        self.height = height
        self.grid = self.create_grid()
        self.pieces = {
            # Q (O-block): 2x2
            "Q": [0b11, 0b11],
            # Z: 2 rows, 3 cols
            "Z": [0b110, 0b011],
            # S: 2 rows, 3 cols
            "S": [0b011, 0b110],
            # T: 2 rows, 3 cols
            "T": [0b111, 0b010],
            # I: 1 row, 4 cols
            "I": [0b1111],
            # L: 4 rows, 2 cols
            "L": [0b10, 0b10, 0b10, 0b11],
            # J: 4 rows, 2 cols
            "J": [0b01, 0b01, 0b01, 0b11],
        }

    def create_grid(self) -> list[int]:
        """Creates a new Tetris grid as a list of bitfields (ints)."""
        return [0 for _ in range(self.height)]

    def print_grid(self) -> None:
        """Prints the current state of the grid (bitfield version)."""
        logging.debug("Current grid state:")
        for row in self.grid:
            row_str = ''.join('O' if (row & (1 << (self.width - 1 - i))) else ' ' for i in range(self.width))
            logging.debug(row_str)

    def place_piece(self, piece: Piece, column: int) -> None:
        """Places a piece on the grid using bitfields."""
        piece_height = len(piece)
        for row in range(self.height - piece_height, -1, -1):
            if self.can_place(piece, row, column):
                self.add_to_grid(piece, row, column)
                logging.debug(f"Placed piece at row {row}, column {column}")
                self.print_grid()
                break

    def can_place(self, piece: Piece, row: int, column: int) -> bool:
        """Checks if a piece can be placed at the given row and column using bitfields."""
        piece_height = len(piece)
        piece_width = self._piece_width(piece)
        if column < 0 or column + piece_width > self.width:
            return False
        for i in range(piece_height):
            shift = self.width - (column + piece_width)
            if shift < 0:
                return False
            piece_row = piece[i] << shift
            grid_row_idx = row + i
            if grid_row_idx < 0 or grid_row_idx >= self.height:
                return False
            if (self.grid[grid_row_idx] & piece_row) != 0:
                return False
        return True

    def _piece_width(self, piece: Piece) -> int:
        """Returns the width of the piece (max bits set in any row)."""
        return max((row.bit_length() for row in piece), default=0)

    def add_to_grid(self, piece: Piece, row: int, column: int) -> None:
        """Adds a piece to the grid at the specified position using bitfields."""
        piece_width = self._piece_width(piece)
        for i, piece_row in enumerate(piece):
            shifted_piece_row = piece_row << (self.width - (column + piece_width))
            self.grid[row + i] |= shifted_piece_row

    def clear_lines(self) -> None:
        """Clears any full horizontal lines and shifts rows down using bitfields."""
        full_mask = (1 << self.width) - 1
        new_grid = [row for row in self.grid if row != full_mask]
        lines_cleared = self.height - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, 0)
        self.grid = new_grid
        if lines_cleared > 0:
            self.print_grid()

    def calculate_height(self) -> int:
        """Calculates the height of the remaining blocks using bitfields."""
        for i, row in enumerate(self.grid):
            if row != 0:
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
    def __init__(self, use_beta: bool = False, **kwargs) -> None:
        if use_beta:
            from ._beta import TetrisGame as TetrisGameBeta
            self.game = TetrisGameBeta(**kwargs)
        else:
            self.game = TetrisGame(**kwargs)

    def run(self) -> None:
        """Main function to read input and write output."""
        for line in sys.stdin:
            line = line.strip()
            if line:
                height = self.game.process_input_line(line)
                sys.stdout.write(str(height))
