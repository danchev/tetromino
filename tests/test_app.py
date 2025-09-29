import unittest

from tetris.app import TetrisGame


class TetrisGameTest(unittest.TestCase):
    def setUp(self):
        """Setup method to create a TetrisGame instance before each test."""
        self.game = TetrisGame()

    def test_create_grid(self):
        """Test if the grid is created with the correct dimensions and is empty."""
        grid = self.game.create_grid()
        self.assertEqual(len(grid), self.game.height)
        for row in grid:
            self.assertEqual(row, 0)

    def test_can_place_empty_grid(self):
        """Test if pieces can be placed in an empty grid."""
        for piece_name in self.game.pieces:
            piece = self.game.pieces[piece_name]
            piece_width = piece.width()
            for column in range(self.game.width - piece_width + 1):
                self.assertTrue(self.game.can_place(piece, 0, column))

    def test_can_place_out_of_bounds(self):
        """Test if placement outside the grid boundaries is prevented."""
        piece = self.game.pieces["Q"]
        self.assertFalse(
            self.game.can_place(piece, 0, self.game.width)
        )  # Out of bounds right
        self.assertFalse(
            self.game.can_place(piece, self.game.height, 0)
        )  # Out of bounds bottom

    def test_can_place_overlapping(self):
        """Test if overlapping placement is prevented."""
        self.game.place_piece(self.game.pieces["Q"], 0)  # Place a piece
        self.assertFalse(
            self.game.can_place(self.game.pieces["I"], 99, 1)
        )  # Try to overlap
        self.assertFalse(
            self.game.can_place(self.game.pieces["I"], 98, 0)
        )  # Try to overlap

    def test_add_to_grid(self):
        """Test if a piece is added to the grid correctly (bitfield version)."""
        piece = self.game.pieces["T"]
        self.game.add_to_grid(piece, 0, 0)
        # T piece: [0b111, 0b010] placed at (0,0) on width 10
        # Check first row: bits 7,8,9 should be set (for width 10)
        for i in range(3):
            self.assertTrue((self.game.grid[0] & (1 << (self.game.width - 1 - i))) != 0)
        # Check second row: only bit 8 should be set
        for i in range(self.game.width):
            if i == self.game.width - 2:
                self.assertTrue((self.game.grid[1] & (1 << i)) != 0)
            else:
                self.assertFalse((self.game.grid[1] & (1 << i)) != 0)

    def test_clear_lines_no_lines(self):
        """Test clearing lines when there are no full lines (bitfield version)."""
        initial_grid = list(self.game.grid)  # Deep copy
        self.game.clear_lines()
        self.assertEqual(self.game.grid, initial_grid)

    def test_clear_lines_one_line(self):
        """Test clearing lines when there is one full line (bitfield version)."""
        self.game.grid[0] = (1 << self.game.width) - 1  # All bits set
        self.game.clear_lines()
        self.assertEqual(self.game.grid[0], 0)
        self.assertEqual(self.game.calculate_height(), 0)

    def test_clear_lines_multiple_lines(self):
        """Test clearing lines when there are multiple full lines (bitfield version)."""
        self.game.grid[0] = (1 << self.game.width) - 1
        self.game.grid[1] = (1 << self.game.width) - 1
        self.game.clear_lines()
        self.assertEqual(self.game.grid[0], 0)
        self.assertEqual(self.game.grid[1], 0)
        self.assertEqual(self.game.calculate_height(), 0)

    def test_calculate_height_empty_grid(self):
        """Test height calculation for an empty grid."""
        self.assertEqual(self.game.calculate_height(), 0)

    def test_calculate_height_with_blocks(self):
        """Test height calculation with blocks on the grid."""
        self.game.place_piece(self.game.pieces["I"], 0)
        self.assertEqual(self.game.calculate_height(), 1)

    def test_process_input_single_piece(self):
        """Test processing a single piece placement (bitfield version)."""
        self.game.process_input_line("Q0")
        # Q piece: [0b11, 0b11] placed at column 0, should be at bottom two rows
        for row_idx in [self.game.height - 2, self.game.height - 1]:
            for col in [self.game.width - 2, self.game.width - 1]:
                self.assertTrue((self.game.grid[row_idx] & (1 << col)) != 0)

    def test_process_input_multiple_pieces(self):
        """Test processing multiple piece placements."""
        self.game.process_input_line("Q0,I4")
        self.assertEqual(self.game.calculate_height(), 2)

    def test_process_input_with_line_clear(self):
        """Test processing input that results in clearing a line."""
        test_input = "Q0,I2,I6,I0,I6,I6,Q2,Q4"
        self.game.process_input_line(test_input)
        self.assertEqual(self.game.calculate_height(), 3)


if __name__ == "__main__":
    unittest.main()
