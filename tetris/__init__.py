import logging

from tetris.app import TetrisApp, TetrisGame, Board, Tetromino, TetrominoType


def configure_logging(log_level: int = logging.DEBUG) -> None:
    """Configure logging for the package.

    Adds both a console handler and a file handler so that log messages
    are visible during interactive runs and also collected to a file for
    later inspection.
    """
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Console output
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(ch)

    # File output
    fh = logging.FileHandler("tetris.log")
    fh.setLevel(log_level)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(fh)


__all__ = ["TetrisApp", "TetrisGame", "Board", "Tetromino", "TetrominoType", "configure_logging"]
