"""FastAPI application for mdchart playground rendering."""

from __future__ import annotations

from datetime import datetime, timezone
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .dsl import SUPPORTED_CHART_TYPES
from .engine import (
    DEFAULT_MAX_CHARTS,
    DEFAULT_MAX_DSL_CHARS,
    DEFAULT_MAX_MARKDOWN_CHARS,
    ChartArtifact,
    render_dsl,
    render_markdown,
)
from .errors import ChartLimitError, DSLParseError, ValidationError


class DataPointResponse(BaseModel):
    label: str
    value: float


class ChartSpecResponse(BaseModel):
    chart_type: str
    x_field: str
    y_field: str
    data: list[DataPointResponse]


class ChartArtifactResponse(BaseModel):
    chart_id: int
    filename: str
    png_base64: str
    spec: ChartSpecResponse


class RenderDSLRequest(BaseModel):
    dsl: str = Field(..., min_length=1, max_length=DEFAULT_MAX_DSL_CHARS)


class RenderDSLResponse(BaseModel):
    chart: ChartArtifactResponse


class RenderMarkdownRequest(BaseModel):
    markdown: str = Field(..., min_length=1, max_length=DEFAULT_MAX_MARKDOWN_CHARS)
    inline_images: bool = True
    max_charts: int = Field(DEFAULT_MAX_CHARTS, ge=1, le=100)


class RenderMarkdownResponse(BaseModel):
    transformed_markdown: str
    charts: list[ChartArtifactResponse]


class DSLSpecResponse(BaseModel):
    syntax: str
    supported_chart_types: list[str]
    example: str


app = FastAPI(
    title="mdchart API",
    version="1.0.0",
    description="Render mdchart DSL blocks into matplotlib PNG charts.",
)


def _read_allowed_origins() -> list[str]:
    # Comma-separated list, e.g. "https://blog.example.com,http://localhost:3000"
    raw = os.getenv("MDCHART_ALLOWED_ORIGINS", "*")
    origins = [item.strip() for item in raw.split(",") if item.strip()]
    return origins or ["*"]


_allowed_origins = _read_allowed_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "mdchart-api",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/v1/dsl-spec", response_model=DSLSpecResponse)
def dsl_spec() -> DSLSpecResponse:
    return DSLSpecResponse(
        syntax=(
            "type = <bar|line>;\\n"
            "x = <identifier>;\\n"
            "y = <identifier>;\\n"
            "data = [Label1:10, Label2:20];"
        ),
        supported_chart_types=sorted(SUPPORTED_CHART_TYPES),
        example=(
            "type = bar;\\n"
            "x = month;\\n"
            "y = sales;\\n"
            "data = [Jan:100, Feb:120, Mar:90];"
        ),
    )


@app.post("/v1/render-dsl", response_model=RenderDSLResponse)
def render_dsl_endpoint(request: RenderDSLRequest) -> RenderDSLResponse:
    try:
        artifact = render_dsl(request.dsl)
        return RenderDSLResponse(chart=_artifact_response(artifact))
    except (DSLParseError, ValidationError, ChartLimitError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/v1/render-markdown", response_model=RenderMarkdownResponse)
def render_markdown_endpoint(request: RenderMarkdownRequest) -> RenderMarkdownResponse:
    try:
        result = render_markdown(
            request.markdown,
            inline_images=request.inline_images,
            max_charts=request.max_charts,
        )
        return RenderMarkdownResponse(
            transformed_markdown=result.transformed_markdown,
            charts=[_artifact_response(chart) for chart in result.charts],
        )
    except (DSLParseError, ValidationError, ChartLimitError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def _artifact_response(artifact: ChartArtifact) -> ChartArtifactResponse:
    return ChartArtifactResponse(
        chart_id=artifact.chart_id,
        filename=artifact.filename,
        png_base64=artifact.png_base64,
        spec=ChartSpecResponse(
            chart_type=artifact.spec.chart_type,
            x_field=artifact.spec.x_field,
            y_field=artifact.spec.y_field,
            data=[DataPointResponse(label=p.label, value=p.value) for p in artifact.spec.data],
        ),
    )


def run() -> None:
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("mdchart.api:app", host="0.0.0.0", port=port, reload=False)
