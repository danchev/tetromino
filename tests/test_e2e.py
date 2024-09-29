
import unittest
import subprocess
import sys

class TetrisGameE2ETest(unittest.TestCase):
    def run_tetris_cli(self, input_line: str) -> str:
        """
        Run the Tetris CLI as a subprocess, passing input_line to stdin.
        Returns the stdout output as a string.
        """
        result = subprocess.run(
            [sys.executable, '-m', 'tetris'],
            input=input_line + '\n',
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()

    def test_process_input_line_i0_i4_q8(self):
        """E2E: process input 'I0,I4,Q8' and check output height."""
        output = self.run_tetris_cli("I0,I4,Q8")
        self.assertIn("1", output)

    def test_process_input_line_q0_q1(self):
        """E2E: process input 'Q0,Q1' and check output height."""
        output = self.run_tetris_cli("Q0,Q1")
        self.assertIn("4", output)

    def test_process_input_line_q0_q2_q4_q6_q8(self):
        """E2E: process input 'Q0,Q2,Q4,Q6,Q8' and check output height."""
        output = self.run_tetris_cli("Q0,Q2,Q4,Q6,Q8")
        self.assertIn("0", output)

    def test_process_input_line_q0_q2_q4_q6_q8_q1(self):
        """E2E: process input 'Q0,Q2,Q4,Q6,Q8,Q1' and check output height."""
        output = self.run_tetris_cli("Q0,Q2,Q4,Q6,Q8,Q1")
        self.assertIn("2", output)

    def test_manual_placement_and_clear_i0_i4_q8(self):
        """E2E: process input 'I0,I4,Q8' and check output height."""
        output = self.run_tetris_cli("I0,I4,Q8")
        self.assertIn("1", output)


if __name__ == "__main__":
    unittest.main()
