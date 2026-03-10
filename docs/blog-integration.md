# Blog Integration

This backend exposes JSON APIs that return base64 PNG chart data.

## Endpoint choice

- Use `POST /v1/render-dsl` when rendering one chart from one DSL snippet.
- Use `POST /v1/render-markdown` when converting an entire markdown document with multiple chart blocks.

## Browser integration example

```html
<script>
  async function renderChartFromDsl(dsl, imgEl) {
    const API_BASE = "https://<your-service>.onrender.com";

    const res = await fetch(`${API_BASE}/v1/render-dsl`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dsl }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Chart render failed");
    }

    const data = await res.json();
    imgEl.src = `data:image/png;base64,${data.chart.png_base64}`;
    imgEl.alt = `Generated ${data.chart.spec.chart_type} chart`;
  }
</script>
```

## Example DSL input

```text
type = bar;
x = month;
y = sales;
data = [Jan:100, Feb:120, Mar:90];
```

## CORS checklist

- Set `MDCHART_ALLOWED_ORIGINS` to your blog origin(s).
- Redeploy after changing env vars.
- Confirm browser requests include `Origin` and API response includes `Access-Control-Allow-Origin`.
