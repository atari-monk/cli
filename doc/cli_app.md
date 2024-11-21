# Cli app

Notes for py cli app, to aid project.

## Project Organization

### Project structure

```plaintext
cli/                            # Root folder of repository
├── doc/                        # Notes
│   └── cli_app.md              # Project notes
└── src/                        # Source code folder
│   └── cli_app/                # CLI application module
│   │   ├── __init__.py         # Module initializer
│   │   ├── app.py              # Main CLI logic
│   └── example/                # Example project module
│   │   ├── __init__.py         # Module initializer
│   │   ├── lib                 # Code
|   |   |   ├── __init__.py     # Module initializer
|   │   ├──                     # Commands src
|   └── shared/                 # Shared code
|   |   ├── __init__.py         # Module initializer
|   |   ├──                     # Shared src
|   └── tests/                  # Tests
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
├── requirements.txt            # Dependencies list
```

### File name convention

1. For py, md files:
   -lowercase
   -underscores separators

```plaintext
file_system.py
```

### .gitignore

Elements added to .gitignore in project started from scratch. In order of appearance.

```plaintext
__pycache__
.pytest_cache
cli_app.log
```

### init file

```plaintext
__init__.py
```

Marks directory as package, that means file are modules for import.
Should generally be committed to version control.

### Tests

Tests is run form src, as app, so that imports should be ok.
Naming convention:

```plaintexy
 test_*.py.
```

To run tests:

```bash
cd src
```

```bash
pytest tests
```

Use s flag with pytest to disable output capturing.

```bash
pytest -s
```

## Features/Requirements

1. Simple cli app with command loop.
2. Detecting folders with commands.

## Usage

To run script directly, enter src and run:

```bash
cd src
```

```bash
python -m cli_app.app
```
