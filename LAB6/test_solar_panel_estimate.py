import pytest
from solar_panel_estimate import panels_needed, install_cost, payback_years


# ============================================================================
# Tests for panels_needed()
# ============================================================================

def test_mono_exact():
    """Initial starter test: exact division with mono panel."""
    assert panels_needed(300, "mono", 5) == 5


def test_panels_needed_unknown_panel_type():
    """ValueError raised for unsupported panel type."""
    with pytest.raises(ValueError, match="unknown panel type"):
        panels_needed(300, "bifacial", 5)


def test_panels_needed_invalid_monthly_units_zero():
    """ValueError raised when monthly units is 0."""
    with pytest.raises(ValueError, match="invalid input"):
        panels_needed(0, "mono", 5)


def test_panels_needed_invalid_monthly_units_negative():
    """ValueError raised when monthly units is negative."""
    with pytest.raises(ValueError, match="invalid input"):
        panels_needed(-100, "mono", 5)


def test_panels_needed_invalid_sun_hours_zero():
    """ValueError raised when sun hours is 0."""
    with pytest.raises(ValueError, match="invalid input"):
        panels_needed(300, "mono", 0)


def test_panels_needed_invalid_sun_hours_negative():
    """ValueError raised when sun hours is negative."""
    with pytest.raises(ValueError, match="invalid input"):
        panels_needed(300, "mono", -3)


def test_panels_needed_with_remainder():
    """Remainder != 0 triggers panels += 1."""
    assert panels_needed(300, "mono", 4) == 7


def test_panels_needed_poly_panel():
    """Panel type 'poly' with 330W rating."""
    assert panels_needed(330, "poly", 5) == 7


def test_panels_needed_clamp_below_two():
    """Panels count below 2 is clamped to 2."""
    assert panels_needed(10, "mono", 5) == 2


def test_panels_needed_two_or_more_no_clamp():
    """Panels count >= 2 is not clamped."""
    assert panels_needed(120, "mono", 5) == 2


# ============================================================================
# Tests for install_cost()
# ============================================================================

def test_concrete_roof():
    """Initial starter test: concrete roof with 4 panels."""
    assert install_cost(4, "concrete", False) == 100000


def test_install_cost_invalid_panels_zero():
    """ValueError raised when panel count is 0."""
    with pytest.raises(ValueError, match="invalid panel count"):
        install_cost(0, "concrete", False)


def test_install_cost_invalid_panels_negative():
    """ValueError raised when panel count is negative."""
    with pytest.raises(ValueError, match="invalid panel count"):
        install_cost(-5, "tin", True)


def test_install_cost_tin_roof_no_battery():
    """Tin roof adds flat 8000 surcharge."""
    assert install_cost(4, "tin", False) == 108000


def test_install_cost_tiled_roof_with_battery():
    """Tiled roof adds panels * 2000 and battery adds 60000."""
    assert install_cost(4, "tiled", True) == 168000


def test_install_cost_unknown_roof():
    """ValueError raised for unsupported roof type."""
    with pytest.raises(ValueError, match="unknown roof type"):
        install_cost(4, "slate", False)


def test_install_cost_discount_exactly_10_panels():
    """Exactly 10 panels qualifies for 10% discount."""
    assert install_cost(10, "concrete", False) == 225000


def test_install_cost_discount_tin_battery_over_10_panels():
    """12 panels with tin roof and battery qualifies for 10% discount."""
    assert install_cost(12, "tin", True) == 331200


def test_install_cost_boundary_9_panels_no_discount():
    """9 panels does not receive the discount."""
    assert install_cost(9, "concrete", False) == 225000


# ============================================================================
# Tests for payback_years()
# ============================================================================

def test_payback_years_saving_zero():
    """Returns -1 when monthly saving is 0."""
    assert payback_years(100000, 20, 0) == -1


def test_payback_years_saving_negative():
    """Returns -1 when monthly saving is negative."""
    assert payback_years(100000, 20, -500) == -1


def test_payback_years_subsidy_capped_above_40():
    """Subsidy above 40% is capped at 40%."""
    assert payback_years(100000, 60, 1000) == 5


def test_payback_years_subsidy_exactly_40():
    """Subsidy of exactly 40% is applied."""
    assert payback_years(100000, 40, 1000) == 5


def test_payback_years_subsidy_below_40():
    """Subsidy below 40% is applied as given."""
    assert payback_years(100000, 20, 1000) == 7


def test_payback_years_zero_subsidy_exact_division():
    """Net cost cleanly divisible by yearly saving (no remainder)."""
    assert payback_years(120000, 0, 1000) == 10


def test_payback_years_with_remainder_rounds_up():
    """Net cost with remainder rounds up to next full year."""
    assert payback_years(130000, 0, 1000) == 11
