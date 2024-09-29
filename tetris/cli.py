import argparse

from tetris import TetrisApp, configure_logging


def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Tetris Game")
    parser.add_argument("--width", type=int, default=10, help="Grid width")
    parser.add_argument("--height", type=int, default=100, help="Grid height")
    parser.add_argument("--log-level", type=int, default=50, help="Log level")
    return parser.parse_args()


def main() -> None:
    """
    Main function to read input and write output.
    """

    kwargs = vars(parse_arguments())
    configure_logging(kwargs.pop("log_level"))
    app = TetrisApp(**kwargs)
    app.run()
