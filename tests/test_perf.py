import time
from tetris.app import TetrisGame

RESOURCE_PATH = "tests/resources/input.txt"


def test_tetris_performance():
    with open(RESOURCE_PATH) as f:
        lines = [line.strip() for line in f if line.strip()]
    game = TetrisGame()
    start = time.perf_counter()
    for line in lines:
        game.process_input_line(line)
    elapsed = time.perf_counter() - start
    print(f"Processed {len(lines)} lines in {elapsed:.6f} seconds.")
    # Assert that it runs in under 1 second (adjust as needed)
    assert elapsed < 1.0, f"Performance test failed: took {elapsed:.6f} seconds"


if __name__ == "__main__":
    test_tetris_performance()
