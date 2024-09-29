import argparse

import sys

from tetris import TetrisApp, configure_logging
from typing import Iterable, Optional, TextIO, List


class TetrisCLI:
    """Object-oriented CLI for running the Tetris application.

    This class encapsulates argument parsing, logging configuration
    and application instantiation so it can be instantiated and used
    from tests or other programs.
    """

    def __init__(
        self,
        argv: Optional[Iterable[str]] = None,
        input_stream: TextIO = sys.stdin,
        output_stream: TextIO = sys.stdout,
    ) -> None:
        self.args = self.parse_arguments(list(argv) if argv is not None else None)
        self.input_stream = input_stream
        self.output_stream = output_stream

    @staticmethod
    def parse_arguments(argv: Optional[List[str]] = None) -> argparse.Namespace:
        """Parse and return CLI arguments.

        Accepts an optional argv list for easier testing.
        """
        parser = argparse.ArgumentParser(description="Tetris Game")
        parser.add_argument("--width", type=int, default=10, help="Grid width")
        parser.add_argument("--height", type=int, default=100, help="Grid height")
        parser.add_argument("--log-level", type=int, default=50, help="Log level")
        return parser.parse_args(argv)

    def run(self) -> None:
        """Configure logging, create the app and process input/output streams."""
        kwargs = vars(self.args).copy()
        log_level = kwargs.pop("log_level")
        configure_logging(log_level)
        app = TetrisApp(width=kwargs.get("width", 10), height=kwargs.get("height", 100), input_stream=self.input_stream, output_stream=self.output_stream)
        app.run()


def main() -> None:
    """Entry point for the console script."""
    cli = TetrisCLI()
    cli.run()
