"""Error types for mdchart engine and API."""


class MDChartError(Exception):
    """Base error for mdchart failures."""


class DSLParseError(MDChartError):
    """Raised when chart DSL cannot be parsed."""


class ValidationError(MDChartError):
    """Raised for user input validation failures."""


class ChartLimitError(ValidationError):
    """Raised when chart limits are exceeded."""
