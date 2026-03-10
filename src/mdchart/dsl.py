"""Parsing helpers for mdchart DSL blocks."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

from .errors import DSLParseError

SUPPORTED_CHART_TYPES = {"bar", "line"}
_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_NUMBER_RE = re.compile(r"^-?\d+(?:\.\d+)?$")
_CHART_BLOCK_RE = re.compile(r"```chart[ \t]*\n(.*?)\n```", re.DOTALL)


@dataclass(frozen=True)
class DataPoint:
    label: str
    value: float


@dataclass(frozen=True)
class ChartSpec:
    chart_type: str
    x_field: str
    y_field: str
    data: tuple[DataPoint, ...]


@dataclass(frozen=True)
class ChartBlock:
    start: int
    end: int
    dsl: str


def extract_chart_blocks(markdown: str) -> list[ChartBlock]:
    """Return fenced ```chart blocks with start/end offsets."""
    blocks: list[ChartBlock] = []
    for match in _CHART_BLOCK_RE.finditer(markdown):
        blocks.append(
            ChartBlock(start=match.start(), end=match.end(), dsl=match.group(1).strip())
        )
    return blocks


def parse_chart_dsl(dsl_text: str) -> ChartSpec:
    """Parse one chart DSL block into a typed chart spec."""
    text = _normalize_chart_input(dsl_text)
    assignments = _parse_assignments(text)

    chart_type = assignments["type"].strip().lower()
    x_field = assignments["x"].strip()
    y_field = assignments["y"].strip()

    if chart_type not in SUPPORTED_CHART_TYPES:
        supported = ", ".join(sorted(SUPPORTED_CHART_TYPES))
        raise DSLParseError(f"Unsupported chart type '{chart_type}'. Supported: {supported}")

    _assert_identifier("x", x_field)
    _assert_identifier("y", y_field)

    points = tuple(_parse_data_points(assignments["data"]))
    if not points:
        raise DSLParseError("data must include at least one label:value pair")

    return ChartSpec(chart_type=chart_type, x_field=x_field, y_field=y_field, data=points)


def _normalize_chart_input(dsl_text: str) -> str:
    text = dsl_text.strip()
    if text.startswith("```chart"):
        lines = text.splitlines()
        if len(lines) < 2 or lines[-1].strip() != "```":
            raise DSLParseError("Unclosed chart fence")
        text = "\n".join(lines[1:-1]).strip()
    return text


def _parse_assignments(text: str) -> dict[str, str]:
    assignments: dict[str, str] = {}
    statements = [statement.strip() for statement in text.split(";") if statement.strip()]

    for statement in statements:
        if "=" not in statement:
            raise DSLParseError(f"Invalid statement '{statement}'. Expected key = value;")
        key, value = statement.split("=", 1)
        key = key.strip().lower()
        value = value.strip()

        if key not in {"type", "x", "y", "data"}:
            raise DSLParseError(f"Unknown field '{key}'")
        if key in assignments:
            raise DSLParseError(f"Duplicate field '{key}'")
        if not value:
            raise DSLParseError(f"Field '{key}' cannot be empty")

        assignments[key] = value

    missing = {"type", "x", "y", "data"} - assignments.keys()
    if missing:
        missing_csv = ", ".join(sorted(missing))
        raise DSLParseError(f"Missing required field(s): {missing_csv}")

    return assignments


def _assert_identifier(name: str, value: str) -> None:
    if not _IDENTIFIER_RE.fullmatch(value):
        raise DSLParseError(
            f"{name} must be an identifier matching [A-Za-z_][A-Za-z0-9_]*"
        )


def _parse_data_points(raw_data: str) -> Iterable[DataPoint]:
    stripped = raw_data.strip()
    if not (stripped.startswith("[") and stripped.endswith("]")):
        raise DSLParseError("data must be wrapped in [ ... ]")

    payload = stripped[1:-1].strip()
    if not payload:
        return []

    pairs = [chunk.strip() for chunk in payload.split(",") if chunk.strip()]
    points: list[DataPoint] = []

    for pair in pairs:
        if ":" not in pair:
            raise DSLParseError(f"Invalid data pair '{pair}'. Expected label:value")

        label, raw_value = pair.split(":", 1)
        label = label.strip()
        raw_value = raw_value.strip()

        _assert_identifier("data label", label)
        if not _NUMBER_RE.fullmatch(raw_value):
            raise DSLParseError(f"Invalid numeric value '{raw_value}' in pair '{pair}'")

        points.append(DataPoint(label=label, value=float(raw_value)))

    return points
