# Agentic Issues - Directory Structure

This document provides an overview of the directory structure and file organization of the Agentic Issues project.

## Project Root

```
agentic-issues/
├── .venv/                 # Virtual environment (not in version control)
├── src/                   # Source code
├── tests/                 # Test files
├── docs/                  # Documentation
├── scripts/               # Utility scripts
├── .gitignore             # Git ignore file
├── README.md              # Project overview
├── LICENSE                # License file
└── pyproject.toml         # Project configuration
```

## Source Code (`src/`)

The `src/` directory contains the main source code for the Agentic Issues system:

```
src/
└── agentic_issues/        # Main package
    ├── __init__.py        # Package initialization
    ├── ag_issues.py       # Entry point for the `ag issues` command
    ├── cli.py             # Command-line interface
    ├── models.py          # Data models
    └── storage.py         # Storage layer
```

### File Descriptions

- **`__init__.py`**: Package initialization file that exports the public API.
- **`ag_issues.py`**: Entry point for the `ag issues` command, integrates with the Agentic framework.
- **`cli.py`**: Command-line interface that parses arguments and dispatches to appropriate handlers.
- **`models.py`**: Data models for issues, comments, and related entities.
- **`storage.py`**: Storage layer for persisting issues and comments.

## Tests (`tests/`)

The `tests/` directory contains test files for the Agentic Issues system:

```
tests/
├── __init__.py            # Test package initialization
├── test_cli.py            # Tests for the CLI module
├── test_models.py         # Tests for the models module
├── test_storage.py        # Tests for the storage module
└── test_data/             # Test data directory
```

## Documentation (`docs/`)

The `docs/` directory contains documentation for the Agentic Issues system:

```
docs/
├── README.md              # Documentation overview
├── DESIGN.md              # Technical design and architecture
├── MANUAL.md              # User manual
├── PLAN.md                # Development plan
└── DIRECTORY_STRUCTURE.md # This file
```

## Scripts (`scripts/`)

The `scripts/` directory contains utility scripts for the Agentic Issues system:

```
scripts/
├── install_ag_issues.py   # Installation script
└── create_test_issue.py   # Script to create a test issue
```

## Configuration Files

- **`.gitignore`**: Specifies files and directories to be ignored by Git.
- **`pyproject.toml`**: Project configuration file for Python packaging.
- **`LICENSE`**: License file for the project.
- **`README.md`**: Project overview and basic usage instructions.

## Data Storage

The Agentic Issues system stores data in the Agentic shared directory:

```
~/Agentic/shared/agentic-issues/
└── issues/                # Issue data
    ├── project-1.json     # Issues for project-1
    ├── project-2.json     # Issues for project-2
    └── ...
```

Each project has its own JSON file containing all issues for that project.

## Integration with Agentic Framework

The Agentic Issues system integrates with the Agentic framework through:

```
~/Agentic/agentic/
├── ag                     # Main Agentic CLI script (modified to include issues command)
└── scripts/
    └── issues_command.py  # Script that handles the `ag issues` command
```

The `install_ag_issues.py` script creates the `issues_command.py` file and updates the `ag` script to include the issues command.

## Development Environment

The development environment for the Agentic Issues system includes:

- Python 3.8 or higher
- Virtual environment (`.venv/`)
- uv package manager (recommended) or pip
- Git for version control

## Best Practices

When working with the Agentic Issues codebase, follow these best practices:

1. **Keep modules focused**: Each module should have a single responsibility.
2. **Write tests**: All code should be covered by tests.
3. **Document code**: Use docstrings and comments to explain code.
4. **Follow PEP 8**: Adhere to Python style guidelines.
5. **Use type hints**: Add type hints to function signatures.
6. **Keep dependencies minimal**: Avoid unnecessary dependencies.
7. **Maintain backward compatibility**: Avoid breaking changes.
