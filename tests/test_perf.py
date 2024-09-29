import os
import pytest
from tetris.app import TetrisGame
import glob

RESOURCE_PATHS = sorted(glob.glob("./tests/resources/input*.txt")) or [
    "tests/resources/input.txt"
]


@pytest.mark.slow
@pytest.mark.benchmark
@pytest.mark.parametrize(
    "resource_path", RESOURCE_PATHS, ids=[os.path.basename(p) for p in RESOURCE_PATHS]
)
@pytest.mark.parametrize("klass", [TetrisGame], ids=["bitfield"])
def test_tetris_benchmark_matrix(benchmark, klass, resource_path):
    with open(resource_path) as f:
        lines = [line.strip() for line in f if line.strip()]

    def run_game():
        game = klass(width=10, height=1000)
        for line in lines:
            game.process_input_line(line)
            game.reset()

    benchmark(run_game)


if __name__ == "__main__":
    pytest.main()
