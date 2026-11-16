"""Hypothesis property-based tests for the solar estimate parsers.

Student: Yashwanth Gowda T G
SRN: PES1UG25AM818
"""

from hypothesis import given, settings, strategies as st

from solar_panel_estimate_parser import (
    clean_site_name,
    parse_monthly_units,
    panels_for_roof,
)

FUZZ_INPUTS = st.one_of(
    st.text(), st.none(), st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.booleans(), st.lists(st.integers()),
)


@settings(max_examples=300, deadline=None)
@given(FUZZ_INPUTS)
def test_clean_site_name_no_crash(value):
    result = clean_site_name(value)
    assert isinstance(result, str)
    assert "#" not in result
    assert "@" not in result


@settings(max_examples=300, deadline=None)
@given(FUZZ_INPUTS)
def test_parse_monthly_units_no_crash(value):
    result = parse_monthly_units(value)
    assert isinstance(result, int)
    assert result >= 0


@settings(max_examples=300, deadline=None)
@given(FUZZ_INPUTS)
def test_panels_for_roof_no_crash(value):
    result = panels_for_roof(value)
    assert isinstance(result, int)
    assert result >= 0


@given(st.text())
def test_site_name_removes_markers_and_is_trimmed(value):
    result = clean_site_name(value)
    assert result == result.strip()
    assert "#" not in result and "@" not in result


@given(st.integers(min_value=0, max_value=10**9))
def test_monthly_units_plain_integer_round_trip(value):
    assert parse_monthly_units(str(value)) == value
    assert parse_monthly_units(f"{value} kWh") == value


@given(st.integers(min_value=1, max_value=10**6), st.integers(min_value=1, max_value=10**6))
def test_roof_panel_count_is_floor_area_divided_by_18(length, width):
    expected = (length * width) // 18
    assert panels_for_roof(f"{length}ft x {width}ft") == expected
