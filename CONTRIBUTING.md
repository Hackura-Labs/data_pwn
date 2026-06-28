# Contributing to Data Pwn

Thank you for helping improve Data Pwn! This guide explains how to contribute effectively to the v2.0 modular codebase.

---

## 📁 Project Structure Overview

Before contributing, familiarise yourself with how the project is organised:

```
data_pawn/
├── data_pwn.py              # Backward-compatible entry point
├── main.py                  # Clean entry point
├── cli.py                   # Argument parsing
├── config.py                # All configuration (edit this, not data_pwn.py)
├── core/
│   ├── base.py              # DataPwn controller (orchestrates phases)
│   ├── scanner.py           # Port scanning & service detection
│   └── reporter.py          # Logger with color-coded output
├── modules/
│   ├── external/
│   │   ├── recon.py         # nmap, DNS, whatweb
│   │   ├── web.py           # SQLi, gobuster, exposed files
│   │   └── services.py      # SSH + database brute force
│   ├── internal/
│   │   ├── discovery.py     # Ping sweep, internal port scan
│   │   ├── pivot.py         # SMB enum, SSH hopping, LDAP/AD
│   │   └── priv_esc.py      # Privilege escalation checks
│   └── extraction/
│       ├── databases.py     # mysqldump, pg_dump, etc.
│       └── files.py         # SSH data mining, config extraction
└── utils/
    ├── helpers.py           # Color class, file & JSON utilities
    ├── network.py           # DNS, port check, local IP helpers
    └── wordlists.py         # Wordlist loading & management
```

---

## 🚀 Quick Contribution Guide

1. **Fork** the repo on GitHub
2. **Clone** your fork: `git clone https://github.com/Hackura-Labs/data_pwn.git && cd data_pwn`
3. **Create** a branch: `git checkout -b feature/my-feature`
4. **Install** dependencies: `pip install -r requirements.txt`
5. **Make** your changes (see guidelines below)
6. **Test** your changes: `python3 data_pwn.py -h`
7. **Commit** with a clear message: `git commit -m "feat: add MongoDB extraction"`
8. **Push** to your fork: `git push origin feature/my-feature`
9. **Open** a Pull Request against `main`

---

## 🔧 Development Guidelines

### Single Responsibility

Each module has one job. Follow this strictly:

- **New attack vector?** → Add to the appropriate `modules/` sub-package.
- **New utility function?** → Add to `utils/helpers.py`, `utils/network.py`, or `utils/wordlists.py`.
- **New config option?** → Add to `config.py` only.
- **Core logic change?** → Modify `core/base.py`, `core/scanner.py`, or `core/reporter.py`.

### Adding a New Module

1. Create your file inside the correct sub-package (e.g., `modules/external/mymodule.py`).
2. Define a class with `__init__(self, target, ..., logger)`.
3. Import and instantiate it in `core/base.py` where needed.
4. Export it from the sub-package `__init__.py` if desired.

Example skeleton for a new external module:

```python
# modules/external/mymodule.py

class MyModule:
    """One-line description of what this module does."""

    def __init__(self, target: str, output_dir: str, logger):
        self.target = target
        self.output_dir = output_dir
        self.logger = logger

    def run(self):
        """Main entry point for this module."""
        self.logger.scan(f"Running MyModule on {self.target}...")
        # ... your logic here ...
        self.logger.success("MyModule completed")
```

### Code Style

- Follow **PEP 8**
- Use **type hints** on function signatures
- Write **docstrings** for every class and public method
- Keep functions **small and focused**
- Use `try/except` with graceful fallback — never crash the whole tool
- Use `self.logger` for all output (never `print()` directly in modules)

### Error Handling

```python
# Good
try:
    result = do_something()
except SomeSpecificException as e:
    self.logger.warning(f"Something failed: {e}")
    return

# Bad
try:
    result = do_something()
except:
    pass
```

### Optional Dependencies

If your module requires an optional library, guard it:

```python
def run_extraction(self):
    try:
        import mysql.connector
    except ImportError:
        self.logger.warning("mysql-connector-python not installed — skipping")
        return
    # ... rest of logic
```

---

## ✅ Pull Request Checklist

- [ ] Code follows PEP 8 and project style
- [ ] All new classes and methods have docstrings
- [ ] Uses `self.logger` (not `print()`) for output
- [ ] Graceful error handling with fallbacks
- [ ] No breaking changes to existing modules
- [ ] `python3 data_pwn.py -h` runs without errors
- [ ] Documentation updated if behaviour changed

---

## 📋 Commit Message Format

Use conventional commits for clarity:

```
feat: add MongoDB extraction module
fix: handle SSH connection reset gracefully
docs: update USER_GUIDE with new entry points
refactor: split scanner into separate class
chore: update requirements.txt
```

---

## 🐛 Reporting Bugs

Open a GitHub Issue and include:

- Python version (`python3 --version`)
- OS and distro
- Full error output
- Steps to reproduce

---

## 💡 Feature Requests

Open a GitHub Issue with:

- What the feature does
- Which module it belongs to (or if it needs a new one)
- Any relevant references or tools

---

## ❓ Questions?

Open an issue or email: lab@hackura.app

**Thank you for contributing!** 🚀