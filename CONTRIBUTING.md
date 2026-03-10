# Contributing

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

## Common tasks

```bash
# Run tests
pytest

# Run API
uvicorn apps.api.main:app --reload

# Legacy C build
make legacy-build
```

## Guidelines

- Keep DSL behavior backward compatible unless explicitly versioned.
- Add tests for parser, engine, and API changes.
- Keep `docs/dsl.md` and `docs/api.md` updated with behavior changes.
