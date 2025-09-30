from __future__ import annotations

import logging
import sys


class Piece:
    __slots__ = ("name", "rows")

    def __init__(self, name: str, rows: tuple[int, ...]):
        self.name = name
        # Always store as tuple of ints (bitfield representation)
        self.rows = rows

    def height(self) -> int:
        return len(self.rows)

    def width(self) -> int:
        # Bitfield: max bits set in any row
        return max((row.bit_length() for row in self.rows), default=0)


class TetrisPieces:
    __slots__ = ("_pieces",)

    def __init__(self):
        self._pieces = {
            "Q": Piece("Q", (0b11, 0b11)),
            "Z": Piece("Z", (0b110, 0b011)),
            "S": Piece("S", (0b011, 0b110)),
            "T": Piece("T", (0b111, 0b010)),
            "I": Piece("I", (0b1111,)),
            "L": Piece("L", (0b10, 0b10, 0b10, 0b11)),
            "J": Piece("J", (0b01, 0b01, 0b01, 0b11)),
        }

    def __getitem__(self, name: str) -> Piece:
        return self._pieces[name]

    def __iter__(self):
        return iter(self._pieces)

    def get(self, name: str) -> Piece:
        return self._pieces[name]

    def names(self):
        return self._pieces.keys()

    def items(self):
        return self._pieces.items()


class TetrisGame:
    __slots__ = ("width", "height", "grid", "pieces")

    def __init__(self, width: int = 10, height: int = 100) -> None:
        """Initializes a new Tetris game.

        Args:
            width: The width of the grid.
            height: The height of the grid.
        """
        self.width = width
        self.height = height
        self.grid = self.create_grid()
        self.pieces = TetrisPieces()

    def create_grid(self) -> list[int]:
        """Creates a new Tetris grid as a list of bitfields (ints)."""
        return [0 for _ in range(self.height)]

    def print_grid(self) -> None:
        """Prints the current state of the grid (bitfield version)."""
        logging.debug("Current grid state:")
        for row in self.grid:
            row_str = "".join(
                "O" if (row & (1 << (self.width - 1 - i))) else " "
                for i in range(self.width)
            )
            logging.debug(row_str)

    def place_piece(self, piece: Piece, column: int) -> None:
        """Places a piece on the grid using bitfields (standard Tetris: lands at lowest possible row)."""
        piece_height = piece.height()
        # Start from the top (row 0) and go down to find the lowest valid position
        # Note that top row has index 0, and bottom row has index height-1.
        last_valid_row = None
        for row in range(0, self.height - piece_height + 1):
            logging.debug(f"Trying to place piece {piece.name} at row {row}, column {column}")
            if self.can_place(piece, row, column):
                last_valid_row = row
            else:
                # Hit an obstacle, can't go any lower
                break
        
        if last_valid_row is not None:
            logging.debug(f"Can place piece {piece.name} at row {last_valid_row}, column {column}")
            self.add_to_grid(piece, last_valid_row, column)
            logging.debug(f"Placed piece at row {last_valid_row}, column {column}")
            self.print_grid()

    def can_place(self, piece: Piece, row: int, column: int) -> bool:
        """Checks if a piece can be placed at the given row and column using bitfields."""
        if column < 0 or column + piece.width() > self.width:
            logging.debug(f"Cannot place: out of bounds col {column} width {piece.width()}")
            return False
        for i in range(piece.height()):
            shift = self.width - (column + piece.width())
            if shift < 0:
                logging.debug(f"Cannot place: negative shift {shift}")
                return False
            piece_row = piece.rows[i] << shift
            grid_row_idx = row + i
            if grid_row_idx < 0 or grid_row_idx >= self.height:
                logging.debug(f"Cannot place: grid_row_idx {grid_row_idx} out of bounds")
                return False
            overlap = (self.grid[grid_row_idx] & piece_row)
            logging.debug(f"Checking row {grid_row_idx}: grid={bin(self.grid[grid_row_idx])} piece_row={bin(piece_row)} overlap={bin(overlap)}")
            if overlap != 0:
                logging.debug(f"Cannot place: overlap at row {grid_row_idx}")
                return False
        return True

    def add_to_grid(self, piece: Piece, row: int, column: int) -> None:
        """Adds a piece to the grid at the specified position using bitfields."""
        piece_width = piece.width()
        for i, piece_row in enumerate(piece.rows):
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
            piece = self.pieces.get(piece_type)
            self.place_piece(piece, column)
            self.clear_lines()
        return self.calculate_height()


class TetrisApp:
    __slots__ = ("game",)

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
