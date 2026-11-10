# Contributing to VeriCode

Thanks for helping make AI-generated code safer! 

## Setup
```bash
python -m pip install -e . pytest pytest-cov ruff
```

## Develop & verify
```bash
ruff check .                 # lint
pytest --cov=vericode        # tests + coverage
vericode . --exclude tests   # dogfood on this repo
```

## Adding a secret rule
Add a `(name, regex, severity)` tuple to `SECRET_PATTERNS` in
`vericode/scanner.py`, then add a unit test in `tests/test_scanner.py`.

## Adding an ecosystem
Extend `parse_dependencies` / `query_osv` in `vericode/deps.py` and cover it
with a test in `tests/test_deps.py`.

## Commit style
Small, atomic commits — one logical change per commit. Keep PRs focused.
