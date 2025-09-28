import unittest

from tetris._beta import TetrisGame

class TetrisGameTest(unittest.TestCase):
    def setUp(self):
        """Setup method to create a TetrisGame instance before each test."""
        self.game = TetrisGame()

    def test_create_grid(self):
        """Test if the grid is created with the correct dimensions."""
        grid = self.game.create_grid()
        self.assertEqual(len(grid), self.game.height)
        self.assertEqual(len(grid[0]), self.game.width)
        for row in grid:
            for cell in row:
                self.assertEqual(cell, " ")

    def test_can_place_empty_grid(self):
        """Test if pieces can be placed in an empty grid."""
        for piece_name in self.game.pieces:
            piece = self.game.pieces[piece_name]
            for column in range(self.game.width - len(piece[0]) + 1):
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
        """Test if a piece is added to the grid correctly."""
        piece = self.game.pieces["T"]
        self.game.add_to_grid(piece, 0, 0)
        self.assertEqual(self.game.grid[0][0], "O")
        self.assertEqual(self.game.grid[0][1], "O")
        self.assertEqual(self.game.grid[0][2], "O")
        self.assertEqual(self.game.grid[1][0], " ")
        self.assertEqual(self.game.grid[1][1], "O")
        self.assertEqual(self.game.grid[1][2], " ")

    def test_clear_lines_no_lines(self):
        """Test clearing lines when there are no full lines."""
        initial_grid = [list(row) for row in self.game.grid]  # Deep copy
        self.game.clear_lines()
        self.assertEqual(self.game.grid, initial_grid)

    def test_clear_lines_one_line(self):
        """Test clearing lines when there is one full line."""
        for i in range(self.game.width):
            self.game.grid[0][i] = "O"
        self.game.clear_lines()
        self.assertEqual(self.game.grid[0], [" " for _ in range(self.game.width)])
        self.assertEqual(self.game.calculate_height(), 0)

    def test_clear_lines_multiple_lines(self):
        """Test clearing lines when there are multiple full lines."""
        for i in range(self.game.width):
            self.game.grid[0][i] = "O"
            self.game.grid[1][i] = "O"
        self.game.clear_lines()
        self.assertEqual(self.game.grid[0], [" " for _ in range(self.game.width)])
        self.assertEqual(self.game.grid[1], [" " for _ in range(self.game.width)])
        self.assertEqual(self.game.calculate_height(), 0)

    def test_calculate_height_empty_grid(self):
        """Test height calculation for an empty grid."""
        self.assertEqual(self.game.calculate_height(), 0)

    def test_calculate_height_with_blocks(self):
        """Test height calculation with blocks on the grid."""
        self.game.place_piece(self.game.pieces["I"], 0)
        self.assertEqual(self.game.calculate_height(), 1)

    def test_process_input_single_piece(self):
        """Test processing a single piece placement."""
        self.game.process_input_line("Q0")
        self.assertEqual(self.game.grid[self.game.height - 2][0], "O")
        self.assertEqual(self.game.grid[self.game.height - 2][1], "O")
        self.assertEqual(self.game.grid[self.game.height - 1][0], "O")
        self.assertEqual(self.game.grid[self.game.height - 1][1], "O")

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
