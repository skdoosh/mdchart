from __future__ import annotations

import pytest

from mdchart.dsl import parse_chart_dsl
from mdchart.errors import DSLParseError


def test_parse_chart_dsl_valid() -> None:
    dsl = """
    type = bar;
    x = month;
    y = sales;
    data = [Jan:100, Feb:120, Mar:90];
    """

    spec = parse_chart_dsl(dsl)

    assert spec.chart_type == "bar"
    assert spec.x_field == "month"
    assert spec.y_field == "sales"
    assert len(spec.data) == 3
    assert spec.data[0].label == "Jan"
    assert spec.data[0].value == 100.0


def test_parse_chart_dsl_missing_field() -> None:
    dsl = "type = bar; x = month; data = [Jan:10];"

    with pytest.raises(DSLParseError):
        parse_chart_dsl(dsl)


def test_parse_chart_dsl_invalid_data_value() -> None:
    dsl = "type = line; x = month; y = sales; data = [Jan:abc];"

    with pytest.raises(DSLParseError):
        parse_chart_dsl(dsl)
