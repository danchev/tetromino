import os
import pytest
from tetris.app import TetrisGame
from tetris._beta import TetrisGame as TetrisGameBeta


RESOURCE_PATHS = [
    "tests/resources/input.txt",
    "tests/resources/input_500.txt",
    "tests/resources/input_3000.txt",
]


@pytest.mark.parametrize(
    "resource_path", RESOURCE_PATHS, ids=[os.path.basename(p) for p in RESOURCE_PATHS]
)
@pytest.mark.parametrize(
    "klass", [TetrisGame, TetrisGameBeta], ids=["bitfield", "beta-list"]
)
def test_tetris_benchmark_matrix(benchmark, klass, resource_path):
    with open(resource_path) as f:
        lines = [line.strip() for line in f if line.strip()]

    def run_game():
        game = klass()
        for line in lines:
            game.process_input_line(line)

    benchmark(run_game)
