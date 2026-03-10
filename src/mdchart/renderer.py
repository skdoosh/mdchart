"""Matplotlib rendering helpers for mdchart specs."""

from __future__ import annotations

from io import BytesIO
import os
import tempfile

# Ensure matplotlib has a writable cache/config location in restricted environments.
_MPL_CONFIG_DIR = os.path.join(tempfile.gettempdir(), "mdchart-mpl")
os.makedirs(_MPL_CONFIG_DIR, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", _MPL_CONFIG_DIR)
os.environ.setdefault("XDG_CACHE_HOME", tempfile.gettempdir())

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .dsl import ChartSpec


def render_chart_png(
    spec: ChartSpec,
    *,
    width: float = 8.0,
    height: float = 5.0,
    dpi: int = 144,
) -> bytes:
    """Render one chart spec to PNG bytes."""
    labels = [point.label for point in spec.data]
    values = [point.value for point in spec.data]

    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
    if spec.chart_type == "bar":
        ax.bar(labels, values)
    elif spec.chart_type == "line":
        ax.plot(labels, values, marker="o", linewidth=2)
    else:
        raise ValueError(f"Unsupported chart type '{spec.chart_type}'")

    ax.set_xlabel(spec.x_field)
    ax.set_ylabel(spec.y_field)
    ax.set_title(f"{spec.chart_type.capitalize()} Chart")
    ax.grid(True, linestyle="--", alpha=0.35)
    fig.tight_layout()

    output = BytesIO()
    fig.savefig(output, format="png", bbox_inches="tight")
    plt.close(fig)
    return output.getvalue()
