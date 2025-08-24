# Agent Guidelines for Quiver

This document outlines the commands and code style guidelines for agents operating within the Quiver repository.

## Build, Lint, and Test Commands

- **Build:**
  - `python setup.py build` (if applicable)
  - `docker-compose build`

- **Linting:**
  - `ruff check .`
  - `mypy .`

- **Testing:**
  - `pytest` (to run all tests)
  - `pytest path/to/test_file.py` (to run a single test file)
  - `pytest path/to/test_file.py::test_function` (to run a single test function)

## Code Style Guidelines

- **Language:** Python 3.10+
- **Formatting:** PEP 8 compliant. Use `ruff format` for auto-formatting.
- **Imports:** Group imports (standard library, third-party, local). Use absolute imports.
- **Naming:** Use `snake_case` for variables and functions, `PascalCase` for classes.
- **Error Handling:** Use standard Python exceptions. Include clear error messages.
- **Type Hinting:** Use type hints extensively (PEP 484). Use `mypy` for type checking.
- **Docstrings:** Follow PEP 257 for docstrings. Explain the purpose, arguments, and return values.
- **Dependencies:** Manage dependencies in `requirements.txt`.
- **Containerization:** Use `Dockerfile` and `docker-compose.yml` for environment setup.
