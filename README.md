# tetris


![GItHub - Version](https://img.shields.io/github/v/release/danchev/tetromino)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fdanchev%2Ftetromino%2Fmaster%2Fpyproject.toml)
![GitHub License](https://img.shields.io/github/license/danchev/tetromino)

A small command-line implementation of the Tetris game engine.

-----

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [License](#license)

## Installation

Local installation (editable/development):
```console
pip install -e .
```

Install normally:
```console
pip install .
```

## Usage

Run the package from the repository (no install required):
```console
python -m tetris < input.txt > output.txt
```

If the package is installed, you can run the console script directly:
```console
tetris < input.txt > output.txt
```

## Testing

Run the test suite with pytest:
```console
uv run pytest
```

## License

`tetris` is distributed under the terms of the [GPL-3.0-or-later](https://spdx.org/licenses/GPL-3.0-or-later.html) license.
