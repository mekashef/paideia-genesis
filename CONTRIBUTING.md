# Contributing to Paideia Genesis

Thank you for your interest in contributing to Paideia Genesis! This guide will help you get started.

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone git@github.com:mekashef/paideia-genesis.git
   cd paideia-genesis
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

5. **Run the application**:
   ```bash
   python3 run.py          # Clean workspace (default)
   python3 run.py --seed   # With demo curricula
   ```

6. **Open**: http://localhost:8000

## Running Tests

The test suite runs entirely offline using the mock LLM provider:

```bash
python3 -m unittest discover tests/ -v
```

All 83 tests should pass without any API keys or external services.

## How to Contribute

### Reporting Bugs
- Open a [GitHub Issue](https://github.com/mekashef/paideia-genesis/issues) with:
  - Steps to reproduce
  - Expected vs actual behavior
  - Python version and OS

### Suggesting Features
- Open a GitHub Issue with the `enhancement` label
- Describe the use case and proposed solution

### Submitting Pull Requests

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** with clear, focused commits
4. **Run the test suite**: `python3 -m unittest discover tests/ -v`
5. **Push** to your fork and open a Pull Request against `main`

### Pull Request Guidelines
- Keep PRs focused on a single concern
- Add tests for new functionality
- Update documentation (README, docstrings) as needed
- Ensure all existing tests pass
- Write clear commit messages

## Code Style

- Python code follows standard PEP 8 conventions
- Use type hints where practical
- Add docstrings to public functions and classes
- Keep functions focused and reasonably sized

## Project Structure

- `src/` — Core application source code
- `tests/` — Automated test suite
- `static/` — Frontend HTML, JS, CSS
- `demo_data/` — Starter curriculum manifests and demo lectures

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
