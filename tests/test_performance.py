

from tetris.app import TetrisGame

RESOURCE_PATH = "tests/resources/input.txt"

def test_tetris_benchmark(benchmark):
    with open(RESOURCE_PATH) as f:
        lines = [line.strip() for line in f if line.strip()]
    def run_game():
        game = TetrisGame()
        for line in lines:
            game.process_input_line(line)
    benchmark(run_game)
