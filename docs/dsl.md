# DSL Reference

## Block format

Use fenced markdown blocks:

```markdown
```chart
type = bar;
x = month;
y = sales;
data = [Jan:100, Feb:120, Mar:90];
```
```

## Fields

- `type`: chart type. Supported values: `bar`, `line`
- `x`: x-axis label identifier (`[A-Za-z_][A-Za-z0-9_]*`)
- `y`: y-axis label identifier (`[A-Za-z_][A-Za-z0-9_]*`)
- `data`: one or more comma-separated `label:value` pairs in brackets

## Data rules

- Labels must be identifiers (`Jan`, `Q1`, `north_region`)
- Values must be numeric (integer or decimal)
- At least one data pair is required

## Errors

Typical parse errors:
- missing required fields
- duplicate fields
- unsupported chart types
- malformed `data` payloads
