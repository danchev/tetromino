"""Tetris bitfield game implementation.

This module implements a compact Tetris representation where each board row
is stored as an integer bitfield. It contains a small game engine used by
the test-suite and a minimal CLI-friendly application coordinator.

The public API is intentionally small and testable: create a
``TetrisGame`` or ``TetrisApp`` and drive it with placement strings or IO
streams. The underlying board stores rows as integers to enable fast bit
operations for collision detection and line clearing.
"""

from __future__ import annotations

from typing import Optional, TextIO, Iterator
from dataclasses import dataclass, field
from enum import Enum
import logging
import sys

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Tetromino:
    """Immutable tetromino shape stored as rows of bitfields.

    Each row is a small integer where the least-significant bit maps to the
    right-most cell. Callers may provide any iterable of integers; rows are
    stored as a tuple for immutability. The instance caches ``height`` and
    ``width`` for efficient reuse.

    Attributes
    ----------
    rows: tuple[int, ...]
        Row bitfields from top to bottom.
    height: int
        Number of rows in the tetromino.
    width: int
        Number of columns required to represent the tetromino.
    """

    rows: tuple[int, ...]
    _height: int = field(init=False, repr=False)
    _width: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Normalize and cache derived dimensions.

        Converts the supplied rows iterable to a tuple and computes the
        cached ``_height`` and ``_width`` values used by the public
        ``height`` and ``width`` properties.
        """
        if not self.rows:
            raise ValueError("Tetromino cannot be empty")
        object.__setattr__(self, "rows", tuple(self.rows))
        object.__setattr__(self, "_height", len(self.rows))
        object.__setattr__(
            self,
            "_width",
            max(row.bit_length() for row in self.rows),
        )

    @property
    def height(self) -> int:
        """Return number of rows (cached)."""
        return self._height

    @property
    def width(self) -> int:
        """Return number of columns (cached)."""
        return self._width

    def __iter__(self) -> Iterator[int]:
        """Yield row bitfields from top to bottom.

        Returns an iterator of integers suitable for bitwise operations.
        """
        return iter(self.rows)

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"Tetromino(rows={self.rows!r})"


class TetrominoType(Enum):
    """Enumeration of Tetris tetromino types.

    Each enum value is a Tetromino instance (rather than a raw tuple)
    which makes shape-related behaviour OOP friendly while keeping a
    compact representation.
    """

    Q = Tetromino((0b11, 0b11))  # 2x2 square
    Z = Tetromino((0b110, 0b011))  # Z-shaped
    S = Tetromino((0b011, 0b110))  # S-shaped
    T = Tetromino((0b111, 0b010))  # T-shaped
    I = Tetromino((0b1111,))  # 4x1 line  # noqa: E741
    L = Tetromino((0b10, 0b10, 0b11))  # L-shaped
    J = Tetromino((0b01, 0b01, 0b11))  # J-shaped



_BITS_TO_CHARS = str.maketrans("10", "O ")


@dataclass
class Board:
    """Encapsulates the Tetris board state and operations.

    This class centralises grid manipulation, collision detection,
    placement and line clearing logic so the game class can remain a
    thin coordinator.
    """

    width: int = 10
    height: int = 100
    _full_row_mask: int = field(init=False)
    grid: list[int] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Width and height must be positive integers")
        self._full_row_mask = (1 << self.width) - 1
        self.grid = self.create_grid()

    def create_grid(self) -> list[int]:
        """Return a freshly zeroed grid.

        Returns a list of integer rows initialised to ``0`` with length
        equal to ``self.height``.
        """
        return [0] * self.height

    def reset(self) -> None:
        """Reset the board grid to an empty state.

        This replaces ``self.grid`` with a newly created zeroed grid.
        """
        self.grid = self.create_grid()

    def print_grid(self) -> None:
        """Log a human-readable representation of the grid at DEBUG level.

        Only emits output when the module logger is configured for the
        DEBUG level. A precomputed translation table maps bits to
        characters to avoid per-call allocations in tight tests.
        """
        if not logger.isEnabledFor(logging.DEBUG):
            return
        logger.debug("Current grid state:")
        for row in self.grid:
            bits = format(row, f"0{self.width}b")
            logger.debug(bits.translate(_BITS_TO_CHARS))

    def _check_collision(self, tetromino: Tetromino, start_row: int, shift: int) -> bool:
        """Determine whether placing a tetromino would collide.

        Parameters
        ----------
        tetromino: Tetromino
            The tetromino shape to test.
        start_row: int
            Index of the board row that should align with the tetromino's
            top row.
        shift: int
            Number of columns to shift the tetromino to the left from the
            right-most board column.

        Returns
        -------
        bool
            True if any tetromino cell would be out of bounds or overlap an
            occupied board cell; False otherwise.
        """
        for i, tetromino_row in enumerate(tetromino):
            board_row_idx = start_row + i
            if board_row_idx >= self.height:
                return True
            if self.grid[board_row_idx] & (tetromino_row << shift):
                return True
        return False

    def place_tetromino(self, tetromino: Tetromino, column: int) -> None:
        """Place a tetromino on the board at the given column.

        Parameters
        ----------
        tetromino: Tetromino
            The tetromino shape to place.
        column: int
            Column offset from the right-most board column (0 aligns the
            tetromino to the right edge).

        Raises
        ------
        ValueError
            If the tetromino does not fit horizontally at the requested
            column or there is no vertical space to place it.
        """
        tetromino_height, tetromino_width = tetromino.height, tetromino.width

        shift = self.width - tetromino_width - column
        if shift < 0:
            raise ValueError(
                "Tetromino of width %d does not fit at column %d in grid of "
                "width %d" % (tetromino_width, column, self.width)
            )
        max_start_row = self.height - tetromino_height

        # Find first row that would collide; landing row is the previous one.
        for row in range(0, max_start_row + 1):
            if self._check_collision(tetromino, row, shift):
                break
        else:
            # No collision until beyond the last possible start row.
            row = max_start_row + 1

        landing_row = row - 1
        if landing_row < 0:
            logger.debug("Cannot place new tetromino: no space")
            raise ValueError("No space to place tetromino")

        for i, tetromino_row in enumerate(tetromino):
            self.grid[landing_row + i] |= tetromino_row << shift

        self.print_grid()


    def clear_lines(self) -> int:
        """Remove any full rows from the board and return the count.

        Full rows are removed and an equivalent number of empty rows are
        prepended to preserve the board height.
        """
        mask = self._full_row_mask
        cleared = sum(1 for row in self.grid if row == mask)
        if cleared == 0:
            return 0
        # Prepend empty rows and keep the existing non-full ones; this mirrors
        # the original behaviour while being explicit about the transformation.
        self.grid = [0] * cleared + [row for row in self.grid if row != mask]
        return cleared

    def calculate_height(self) -> int:
        """Compute the height of the stacked blocks.

        The height is the number of non-empty rows measured from the bottom
        of the board. Returns ``0`` when the board is empty.
        """
        return next((self.height - i for i, row in enumerate(self.grid) if row), 0)


class TetrisGame:
    """A Tetris game implementation using bitfield representation."""

    def __init__(self, width: int = 10, height: int = 100) -> None:
        """Initialise a TetrisGame with a backing Board.

        Parameters
        ----------
        width: int
            Number of columns of the board.
        height: int
            Number of rows of the board.
        """
        self.board = Board(width=width, height=height)


    def create_grid(self) -> list[int]:
        """Return a freshly zeroed grid matching the board height.

        This is a thin delegate to :meth:`Board.create_grid` kept for
        compatibility with tests that access the game directly.
        """
        return self.board.create_grid()

    @property
    def width(self) -> int:
        """The board width (number of columns)."""
        return self.board.width

    @property
    def height(self) -> int:
        """The board height (number of rows)."""
        return self.board.height

    @property
    def grid(self) -> list[int]:
        """The underlying board grid (read-only view)."""
        return self.board.grid

    @property
    def full_row_mask(self) -> int:
        """Mask representing a full row for the current board width."""
        return self.board._full_row_mask

    def reset(self) -> None:
        """Reset the game grid to an empty state.

        Resets the underlying board state.
        """
        self.board.reset()

    def print_grid(self) -> None:
        """Delegate pretty-printing to the underlying board."""
        self.board.print_grid()

    def _check_collision(self, tetromino: Tetromino, start_row: int, shift: int) -> bool:
        """Delegate collision checking to the underlying board.

        See :meth:`Board._check_collision` for parameter semantics and
        return behaviour.
        """
        return self.board._check_collision(tetromino, start_row, shift)

    def place_tetromino(self, tetromino: Tetromino, column: int) -> None:
        """Place a tetromino on the board at the specified column.

        This method delegates to :meth:`Board.place_tetromino`. Column
        semantics count from the right-hand side (0 aligns to the right
        edge) consistent with the bitfield representation.
        """
        self.board.place_tetromino(tetromino, column)

    def clear_lines(self) -> int:
        """Clear full lines and return the number of rows removed.

        Delegates to the underlying board implementation.
        """
        return self.board.clear_lines()

    def calculate_height(self) -> int:
        """Return the current stacked blocks height.

        Delegates to :meth:`Board.calculate_height`.
        """
        return self.board.calculate_height()

    def place_tetromino_by_type(self, shape: str, column: int) -> None:
        """Place a tetromino specified by its single-letter shape name.

        TetrisGame owns input parsing responsibilities and therefore
        exposes a helper that accepts the shape identifier directly.
        """
        try:
            tetromino = TetrominoType[shape].value
        except KeyError:
            raise ValueError("Unknown tetromino type: %s" % shape)

        self.place_tetromino(tetromino, column)

    def _parse_placement(self, item: str, idx: int) -> tuple[Tetromino, int]:
        """Parse a single placement token and return (Tetromino, column).

        Token format is ``'<shape><column>'`` where ``<shape>`` is a single
        letter (e.g. ``T``) and ``<column>`` is an integer. ``idx`` is the
        1-based placement index used to construct helpful error messages.
        """
        if len(item) < 2:
            raise ValueError("Invalid placement '%s' at step %d" % (item, idx))

        shape, col_text = item[0], item[1:]
        try:
            column = int(col_text)
        except ValueError as exc:
            raise ValueError("Invalid column in placement '%s' at step %d" % (item, idx)) from exc

        try:
            tetromino = TetrominoType[shape].value
        except KeyError:
            raise ValueError("Unknown tetromino type: %s" % shape)

        return tetromino, column

    def process_input_line(self, line: str) -> int:
        """Process a comma-separated placement line and return board height.

        The line is split on commas. Each non-empty token is parsed as a
        placement and applied sequentially. After all placements are
        applied any full lines are cleared and the resulting board height
        (number of occupied rows from the bottom) is returned.
        """
        for idx, item in enumerate(filter(None, map(str.strip, line.split(","))), 1):
            tetromino, column = self._parse_placement(item, idx)
            logger.debug("Step %d: place %s at %d", idx, item[0], column)
            self.place_tetromino(tetromino, column)

        cleared = self.clear_lines()
        logger.debug("Cleared rows: %d", cleared)
        return self.calculate_height()


class TetrisApp:
    """Application coordinator for running Tetris via streams.

    This class improves testability by allowing the caller to inject
    input and output streams and a custom TetrisGame. The constructor
    keeps the familiar width/height parameters for simple CLI usage.
    """

    __slots__ = ("game", "input_stream", "output_stream")

    def __init__(
        self,
        width: int = 10,
        height: int = 100,
        *,
        game: Optional[TetrisGame] = None,
        input_stream: TextIO = sys.stdin,
        output_stream: TextIO = sys.stdout,
    ) -> None:
        # Maintain CLI-friendly signature while preferring an injected
        # TetrisGame when provided.
        self.game = game or TetrisGame(width=width, height=height)
        self.input_stream = input_stream
        self.output_stream = output_stream

    def process_line(self, line: str) -> int:
        """Reset the game and process a single placement line.

        Returns the board height after processing the placements.
        """
        self.game.reset()
        return self.game.process_input_line(line)

    def process_stream(self, reader: Optional[TextIO] = None, writer: Optional[TextIO] = None) -> None:
        """Process lines from ``reader`` and write results to ``writer``.

        Blank lines are ignored. For each non-empty input line the game is
        reset, the placements processed and the resulting height is written
        to the output followed by a newline.
        """
        reader = reader or self.input_stream
        writer = writer or self.output_stream

        for line in reader:
            line = line.strip()
            if not line:
                continue
            height = self.process_line(line)
            writer.write(f"{height}\n")

    def run(self) -> None:
        """Run the application using the configured input and output.

        This is equivalent to calling :meth:`process_stream` with the
        injected streams provided at construction time.
        """
        self.process_stream()
