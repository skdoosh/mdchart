"""Core mdchart engine used by CLI and API."""

from __future__ import annotations

from dataclasses import dataclass
import base64
from pathlib import Path

from .dsl import ChartSpec, extract_chart_blocks, parse_chart_dsl
from .errors import ChartLimitError, ValidationError
from .renderer import render_chart_png

DEFAULT_MAX_CHARTS = 20
DEFAULT_MAX_MARKDOWN_CHARS = 200_000
DEFAULT_MAX_DSL_CHARS = 10_000


@dataclass(frozen=True)
class ChartArtifact:
    chart_id: int
    filename: str
    png_bytes: bytes
    png_base64: str
    spec: ChartSpec


@dataclass(frozen=True)
class RenderMarkdownResult:
    transformed_markdown: str
    charts: tuple[ChartArtifact, ...]


def render_dsl(dsl: str, *, chart_id: int = 1) -> ChartArtifact:
    """Render one DSL snippet into one chart artifact."""
    if not dsl.strip():
        raise ValidationError("dsl cannot be empty")
    if len(dsl) > DEFAULT_MAX_DSL_CHARS:
        raise ValidationError(f"dsl exceeds {DEFAULT_MAX_DSL_CHARS} characters")

    spec = parse_chart_dsl(dsl)
    png_bytes = render_chart_png(spec)
    filename = f"chart_{chart_id:03d}.png"
    return ChartArtifact(
        chart_id=chart_id,
        filename=filename,
        png_bytes=png_bytes,
        png_base64=_encode_png(png_bytes),
        spec=spec,
    )


def render_markdown(
    markdown: str,
    *,
    inline_images: bool = True,
    max_charts: int = DEFAULT_MAX_CHARTS,
    max_markdown_chars: int = DEFAULT_MAX_MARKDOWN_CHARS,
) -> RenderMarkdownResult:
    """Render all fenced chart blocks from markdown."""
    if len(markdown) > max_markdown_chars:
        raise ValidationError(f"markdown exceeds {max_markdown_chars} characters")

    blocks = extract_chart_blocks(markdown)
    if len(blocks) > max_charts:
        raise ChartLimitError(f"Found {len(blocks)} charts, limit is {max_charts}")

    if not blocks:
        return RenderMarkdownResult(transformed_markdown=markdown, charts=())

    charts: list[ChartArtifact] = []
    parts: list[str] = []
    cursor = 0

    for idx, block in enumerate(blocks, start=1):
        parts.append(markdown[cursor : block.start])

        artifact = render_dsl(block.dsl, chart_id=idx)
        charts.append(artifact)

        if inline_images:
            image_ref = f"data:image/png;base64,{artifact.png_base64}"
        else:
            image_ref = artifact.filename

        parts.append(f"![Chart {idx}]({image_ref} \"Generated Chart\")")
        cursor = block.end

    parts.append(markdown[cursor:])

    return RenderMarkdownResult(
        transformed_markdown="".join(parts),
        charts=tuple(charts),
    )


def write_chart_files(charts: tuple[ChartArtifact, ...], output_dir: str | Path) -> None:
    """Write rendered chart PNG artifacts to disk."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for chart in charts:
        (output_path / chart.filename).write_bytes(chart.png_bytes)


def _encode_png(png_bytes: bytes) -> str:
    return base64.b64encode(png_bytes).decode("ascii")
