import logging

from tetris.app import TetrisApp


def configure_logging(log_level: int = logging.DEBUG) -> None:
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("tetris.log")],
    )


__all__ = ["TetrisApp"]
