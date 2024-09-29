import argparse

from tetris.app import TetrisApp


def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Tetris Game")
    return parser.parse_args()


def main() -> None:
    """
    Main function to read input and write output.
    """
    kwargs = vars(parse_arguments())
    app = TetrisApp(**kwargs)
    app.run()
