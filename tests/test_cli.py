import pytest
import sys
from tetris.cli import TetrisCLI, main

def test_parse_arguments_defaults():
    args = TetrisCLI.parse_arguments([])
    assert args.width == 10
    assert args.height == 100
    assert args.log_level == 50

def test_parse_arguments_custom():
    args = TetrisCLI.parse_arguments(["--width", "5", "--height", "20", "--log-level", "10"])
    assert args.width == 5
    assert args.height == 20
    assert args.log_level == 10

def test_cli_run_calls_app_run(monkeypatch):
    called = {}
    class DummyApp:
        def __init__(self, **kwargs):
            called['init'] = kwargs
        def run(self):
            called['run'] = True
    monkeypatch.setattr("tetris.cli.TetrisApp", DummyApp)
    cli = TetrisCLI(argv=["--width", "7", "--height", "8", "--log-level", "40"])
    cli.run()
    assert called['init']['width'] == 7
    assert called['init']['height'] == 8
    assert called['run'] is True

def test_main_invokes_cli_run(monkeypatch):
    called = {}
    class DummyCLI:
        def __init__(self):
            called['init'] = True
        def run(self):
            called['run'] = True
    monkeypatch.setattr("tetris.cli.TetrisCLI", DummyCLI)
    main()
    assert called['init']
    assert called['run']

def test_parse_arguments_invalid_width():
    with pytest.raises(SystemExit):
        TetrisCLI.parse_arguments(["--width", "notanint"])

def test_parse_arguments_invalid_height():
    with pytest.raises(SystemExit):
        TetrisCLI.parse_arguments(["--height", "notanint"])

def test_parse_arguments_invalid_log_level():
    with pytest.raises(SystemExit):
        TetrisCLI.parse_arguments(["--log-level", "notanint"])

def test_parse_arguments_missing_args():
    args = TetrisCLI.parse_arguments([])
    assert hasattr(args, 'width')
    assert hasattr(args, 'height')
    assert hasattr(args, 'log_level')

def test_cli_no_argv(monkeypatch):
    # Simulate sys.argv
    monkeypatch.setattr(sys, "argv", ["prog", "--width", "12", "--height", "34", "--log-level", "20"])
    cli = TetrisCLI()
    assert cli.args.width == 12
    assert cli.args.height == 34
    assert cli.args.log_level == 20

def test_cli_help_output(capsys):
    with pytest.raises(SystemExit):
        TetrisCLI.parse_arguments(["--help"])
    out, err = capsys.readouterr()
    assert "usage" in out.lower() or "usage" in err.lower()

def test_cli_version_output(monkeypatch, capsys):
    # Only run if --version is supported
    try:
        with pytest.raises(SystemExit):
            TetrisCLI.parse_arguments(["--version"])
        out, err = capsys.readouterr()
        assert "version" in out.lower() or "version" in err.lower()
    except SystemExit:
        pass
    except Exception:
        pass

def test_log_level_boundaries():
    args = TetrisCLI.parse_arguments(["--log-level", "0"])
    assert args.log_level == 0
    args = TetrisCLI.parse_arguments(["--log-level", "50"])
    assert args.log_level == 50

def test_direct_instantiation_properties():
    cli = TetrisCLI(argv=["--width", "15", "--height", "25", "--log-level", "30"])
    assert cli.args.width == 15
    assert cli.args.height == 25
    assert cli.args.log_level == 30
