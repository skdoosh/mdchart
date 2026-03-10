# API Reference

Base URL (local): `http://127.0.0.1:8000`

## `GET /healthz`

Health probe endpoint.

## `GET /v1/dsl-spec`

Returns DSL syntax summary and supported chart types.

## `POST /v1/render-dsl`

Render one DSL payload into one chart.

Request:

```json
{
  "dsl": "type = bar; x = month; y = sales; data = [Jan:100, Feb:120];"
}
```

Response includes `png_base64` and parsed `spec`.

## `POST /v1/render-markdown`

Render all fenced ` ```chart ` blocks in markdown.

Request:

```json
{
  "markdown": "# Report\\n\\n```chart\\ntype = line;\\nx = t;\\ny = v;\\ndata = [A:1, B:2];\\n```",
  "inline_images": true,
  "max_charts": 20
}
```

Response:
- `transformed_markdown`
- `charts[]` with `filename`, `png_base64`, and parsed `spec`

## Error handling

Validation and parse errors return HTTP `400` with a detail message.
