# Cli app

Notes for py cli app, to aid project.

## Project Assumptions

### Project structure

```plaintext
cli/                            # Root folder of repository
├── doc/                        # Notes
│   └── cli_app.md              # Project notes
└── src/                        # Source code folder
│   └── cli_app/                # CLI application module
│   │   ├── __init__.py         # Module initializer
│   │   ├── app.py              # Main CLI logic
│   └── log_project/            # Log project module
│   │   ├── __init__.py         # Module initializer
│   │   ├── lib                 # Code
|   |   |   ├── __init__.py     # Module initializer
|   │   ├──                     # Commands src
|   └── shared/                 # Shared code
|       ├── __init__.py         # Module initializer
|       ├──                     # Shared src
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

In tests folders. Using pytest.
Naming convention:

```plaintexy
 test_*.py.
```

To test shared files i used this assumptions.
I cd to shared folder.
Run command

```bash
pytest tests
```

This will work when relative import, from folder above tests, to tested file, is correct.  
Init file is needed in tests folder as relative import is used.
For example:

```python
#test file in tests, testing ..logger.py from shared
#__init__.py file in tests
import pytest
import logging
from ..logger import setup_logger
```

Files from shared import each other with .

```python
#file from shared imports other file form shared
from .logger import log_message
```

Use s flag with pytest to disable output capturing. You will see test oputput if needed.

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
