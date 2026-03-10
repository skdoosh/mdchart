# Architecture

## Request flow

1. User submits DSL or markdown (CLI or API)
2. `mdchart.dsl` parses DSL into `ChartSpec`
3. `mdchart.renderer` renders spec to PNG bytes via matplotlib
4. `mdchart.engine` assembles markdown replacements and chart artifacts
5. API returns transformed markdown + base64 image payloads

## Modules

- `mdchart.dsl`: DSL tokenization/parsing and markdown chart-block extraction
- `mdchart.renderer`: pure rendering concern for `ChartSpec -> PNG`
- `mdchart.engine`: orchestration, limits, markdown replacement logic
- `mdchart.api`: HTTP boundary, validation mapping, response serialization
- `mdchart.cli`: file/stdin I/O and chart file output behavior

## Safety controls

- Input size caps for DSL and markdown
- Max chart count per markdown document
- Strict DSL validation (known fields, known chart types, numeric data)
- No shell execution for rendering path

## Legacy implementation

`src/c/` preserves the original C/Flex/Bison implementation for reference and compatibility experiments. The default production path is now Python engine + FastAPI.
