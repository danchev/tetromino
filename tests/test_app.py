import unittest

from tetris.app import TetrisGame, TetrominoType


class TetrisGameTest(unittest.TestCase):
    def setUp(self):
        """Setup method to create a TetrisGame instance before each test."""
        self.game = TetrisGame()

    def test_create_grid(self):
        """Test if the grid is created with the correct dimensions and is empty."""
        grid = self.game.create_grid()
        self.assertEqual(len(grid), self.game.board.height)
        for row in grid:
            self.assertEqual(row, 0)

    def test_clear_lines_no_lines(self):
        """Test clearing lines when there are no full lines (bitfield version)."""
        initial_grid = list(self.game.board.grid)  # Deep copy
        self.game.clear_lines()
        self.assertEqual(self.game.board.grid, initial_grid)

    def test_clear_lines_one_line(self):
        """Test clearing lines when there is one full line (bitfield version)."""
        self.game.board.grid[0] = (1 << self.game.board.width) - 1  # All bits set
        self.game.clear_lines()
        self.assertEqual(self.game.board.grid[0], 0)
        self.assertEqual(self.game.calculate_height(), 0)

    def test_clear_lines_multiple_lines(self):
        """Test clearing lines when there are multiple full lines (bitfield version)."""
        self.game.board.grid[0] = (1 << self.game.board.width) - 1
        self.game.board.grid[1] = (1 << self.game.board.width) - 1
        self.game.clear_lines()
        self.assertEqual(self.game.board.grid[0], 0)
        self.assertEqual(self.game.board.grid[1], 0)
        self.assertEqual(self.game.calculate_height(), 0)

    def test_calculate_height_empty_grid(self):
        """Test height calculation for an empty grid."""
        self.assertEqual(self.game.calculate_height(), 0)

    def test_calculate_height_with_blocks(self):
        """Test height calculation with blocks on the grid."""
        # Use the TetrominoType enum to select the I tetromino.
        self.game.place_tetromino(TetrominoType.I.value, 0)
        self.assertEqual(self.game.calculate_height(), 1)

    def test_process_input_single_piece(self):
        """Test processing a single tetromino placement (bitfield version)."""
        self.game.process_input_line("Q0")
    # Q tetromino: [0b11, 0b11] placed at column 0, should be at bottom two rows
        for row_idx in [self.game.board.height - 2, self.game.board.height - 1]:
            for col in [self.game.board.width - 2, self.game.board.width - 1]:
                self.assertTrue((self.game.board.grid[row_idx] & (1 << col)) != 0)

    def test_process_input_multiple_pieces(self):
        """Test processing multiple tetromino placements."""
        self.game.process_input_line("Q0,I4")
        self.assertEqual(self.game.calculate_height(), 2)

    def test_process_input_with_line_clear(self):
        """Test processing input that results in clearing a line."""
        test_input = "Q0,I2,I6,I0,I6,I6,Q2,Q4"
        self.game.process_input_line(test_input)
        self.assertEqual(self.game.calculate_height(), 3)

    def test_process_input_with_line_clear_alternate_2(self):
        test_input = "T1,Z3,I4"
        self.game.process_input_line(test_input)
        self.assertEqual(self.game.calculate_height(), 4)

    def test_process_input_with_line_clear_alternate(self):
        test_input = "I0,I4,Q8"
        self.game.process_input_line(test_input)
        self.assertEqual(self.game.calculate_height(), 1)

    def test_process_input_without_line_clear(self):
        """Test processing input that does not result in clearing a line."""
        test_input = "Q0,Q1,Q2"
        self.game.process_input_line(test_input)
        self.assertEqual(self.game.calculate_height(), 6)

    def test_process_input_L_tetromino(self):
        """Test processing input with L tetromino."""
        test_input = "L0,L4"
        self.game.process_input_line(test_input)
        self.assertEqual(self.game.calculate_height(), 3)

    def test_process_input_J_tetromino(self):
        """Test processing input with J tetromino."""
        test_input = "J0,J4"
        self.game.process_input_line(test_input)
        self.assertEqual(self.game.calculate_height(), 3)

if __name__ == "__main__":
    unittest.main()
