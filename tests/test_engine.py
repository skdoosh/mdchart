from __future__ import annotations

import pytest

from mdchart.engine import render_markdown
from mdchart.errors import ChartLimitError


def test_render_markdown_inline_images() -> None:
    markdown = """
# Report

```chart
type = bar;
x = month;
y = sales;
data = [Jan:100, Feb:120, Mar:90];
```
"""

    result = render_markdown(markdown, inline_images=True)

    assert "```chart" not in result.transformed_markdown
    assert "data:image/png;base64," in result.transformed_markdown
    assert len(result.charts) == 1
    assert result.charts[0].png_base64


def test_render_markdown_file_links() -> None:
    markdown = """
```chart
type = line;
x = day;
y = value;
data = [Mon:1, Tue:3, Wed:2];
```
"""

    result = render_markdown(markdown, inline_images=False)

    assert "chart_001.png" in result.transformed_markdown
    assert len(result.charts) == 1


def test_render_markdown_chart_limit() -> None:
    markdown = "\n".join(
        [
            "```chart",
            "type = bar;",
            "x = x;",
            "y = y;",
            "data = [A:1];",
            "```",
            "```chart",
            "type = bar;",
            "x = x;",
            "y = y;",
            "data = [B:2];",
            "```",
        ]
    )

    with pytest.raises(ChartLimitError):
        render_markdown(markdown, max_charts=1)
