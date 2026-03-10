"""CLI entrypoint for mdchart markdown rendering."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .engine import DEFAULT_MAX_CHARTS, render_markdown, write_chart_files
from .errors import MDChartError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mdchart",
        description="Convert fenced mdchart DSL blocks into rendered matplotlib charts.",
    )
    parser.add_argument("input", nargs="?", help="Input markdown file. Uses stdin when omitted.")
    parser.add_argument("-o", "--output", help="Output markdown file. Defaults to stdout.")
    parser.add_argument(
        "--charts-dir",
        default=".",
        help="Directory for chart PNG files when --inline-images is not used.",
    )
    parser.add_argument(
        "--inline-images",
        action="store_true",
        help="Embed rendered PNGs directly as base64 data URLs in markdown output.",
    )
    parser.add_argument(
        "--max-charts",
        type=int,
        default=DEFAULT_MAX_CHARTS,
        help="Maximum chart blocks allowed per document.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        markdown = _read_input(args.input)
        result = render_markdown(
            markdown,
            inline_images=args.inline_images,
            max_charts=args.max_charts,
        )

        if not args.inline_images:
            write_chart_files(result.charts, args.charts_dir)

        _write_output(result.transformed_markdown, args.output)
        return 0
    except MDChartError as exc:
        print(f"mdchart error: {exc}", file=sys.stderr)
        return 1


def _read_input(input_path: str | None) -> str:
    if input_path:
        return Path(input_path).read_text(encoding="utf-8")
    return sys.stdin.read()


def _write_output(markdown: str, output_path: str | None) -> None:
    if output_path:
        Path(output_path).write_text(markdown, encoding="utf-8")
        return
    sys.stdout.write(markdown)


if __name__ == "__main__":
    raise SystemExit(main())
