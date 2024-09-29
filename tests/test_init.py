import logging
import tetris

def test_configure_logging_creates_handlers(tmp_path, monkeypatch):
    # Patch logging.FileHandler to use a temp file
    log_file = tmp_path / "tetris.log"
    # Patch logging.FileHandler to a minimal custom class
    class DummyFileHandler(logging.StreamHandler):
        def __init__(self, filename, *args, **kwargs):
            super().__init__(open(log_file, "a"))
    monkeypatch.setattr(logging, "FileHandler", DummyFileHandler)
    tetris.configure_logging(logging.INFO)
    logger = logging.getLogger()
    # Should have at least one StreamHandler and one FileHandler
    handlers = logger.handlers
    assert any(isinstance(h, logging.StreamHandler) for h in handlers)
    assert any(isinstance(h, DummyFileHandler) for h in handlers)
    # Log something and check file
    logger.info("test message")
    for h in handlers:
        if hasattr(h, 'flush'):
            h.flush()
    with open(log_file, "r") as f:
        content = f.read()
    assert "test message" in content
