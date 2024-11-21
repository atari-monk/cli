# Simple Python CLI App

## Features/Requirements

-   A simple command-line interface (CLI) app with a command loop.
-   Detects and loads available folders with commands.
-   Allows users to set folder context for command execution.

## Usage

To run the script directly, enter the `src` directory and execute the following command:

```bash
cd src
```

Then run the app:

```bash
python -m cli_app.app
```

### Available Commands

-   **help**: Displays a list of available commands.
-   **set_folder <folder_name>**: Sets the context to the specified folder.
-   **exit**: Exits the application.

## Installation

1. Clone or download the repository to your local machine.
2. Ensure you have Python 3.x installed.
3. Install any required dependencies using:

```bash
pip install -r requirements.txt
```

## Configuration

The app uses a logger for tracking operations and settings can be configured in the `cli_app/config.py` file.

## Documentation

[Docs/repo pages](/docs/index.md)
[Docs/github pages](https://atari-monk.github.io/py_cli_app/)

## Add more commands

-   Add folder to src.
-   Add empty **init**.py.
-   Add commands command.py with function run.
-   Use lib folder to store code shared by commands.

```python
def run(args = None):
#...
```

---
