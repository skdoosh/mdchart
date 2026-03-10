# mdchart

`mdchart` is a markdown-to-chart toolkit with:
- a Python DSL parser and matplotlib renderer
- a CLI for markdown transformation
- a FastAPI backend for playground-style rendering

## Repository layout

- `src/mdchart/`: core engine, parser, renderer, CLI, API module
- `apps/api/`: API entrypoint for local development
- `src/c/`: legacy C/Flex/Bison implementation
- `docs/`: DSL, API, and architecture documentation
- `tests/`: parser, engine, and API tests
- `examples/`: sample markdown inputs/outputs

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## CLI usage

```bash
# Inline image output (playground-like)
mdchart --inline-images examples/example.md -o /tmp/output-inline.md

# File-based output + PNG files in ./charts
mdchart examples/example.md -o /tmp/output.md --charts-dir ./charts
```

## Run API

```bash
uvicorn apps.api.main:app --reload
```

Interactive docs: `http://127.0.0.1:8000/docs`

## DSL syntax

```text
type = <bar|line>;
x = <identifier>;
y = <identifier>;
data = [Label1:10, Label2:20, Label3:30];
```

See [docs/dsl.md](docs/dsl.md) and [docs/api.md](docs/api.md) for full details.
