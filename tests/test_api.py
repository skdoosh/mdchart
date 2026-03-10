from __future__ import annotations

from fastapi.testclient import TestClient

from mdchart.api import app


client = TestClient(app)


def test_healthz() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"


def test_render_dsl_endpoint() -> None:
    response = client.post(
        "/v1/render-dsl",
        json={
            "dsl": "type = bar; x = month; y = sales; data = [Jan:100, Feb:120];",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["chart"]["png_base64"]
    assert payload["chart"]["spec"]["chart_type"] == "bar"


def test_render_markdown_endpoint() -> None:
    markdown = """
# Demo

```chart
type = line;
x = month;
y = value;
data = [Jan:10, Feb:15];
```
"""
    response = client.post(
        "/v1/render-markdown",
        json={"markdown": markdown, "inline_images": True, "max_charts": 20},
    )
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["charts"]) == 1
    assert "data:image/png;base64," in payload["transformed_markdown"]
