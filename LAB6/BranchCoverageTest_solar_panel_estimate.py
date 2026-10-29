"""
Branch Coverage Test Suite for solar_panel_estimate.py
Lab 6: Code and Branch Coverage Analysis

This test suite targets 100% Branch Coverage and 100% Line Coverage
by comprehensively exercising every decision branch (True and False paths),
compound boolean conditions, edge cases, and boundary values across all functions.
"""

import pytest
from solar_panel_estimate import panels_needed, install_cost, payback_years


# ============================================================================
# Branch Coverage Tests for panels_needed()
# Decision Points & Branches:
# 1. if panel_type not in PANEL_WATTS:
#    - True -> raises ValueError("unknown panel type")
#    - False -> proceeds (tested for both 'mono' and 'poly')
# 2. if monthly_units <= 0 or sun_hours <= 0:
#    - monthly_units <= 0 (True) -> raises ValueError("invalid input")
#    - sun_hours <= 0 (True) -> raises ValueError("invalid input")
#    - Both > 0 (False) -> proceeds
# 3. if daily_wh % per_panel_wh:
#    - Remainder != 0 (True) -> panels += 1
#    - Remainder == 0 (False) -> panels remains unchanged
# 4. if panels < 2:
#    - panels < 2 (True) -> clamped to 2
#    - panels >= 2 (False) -> retains calculated count
# ============================================================================

def test_panels_needed_unknown_panel_type():
    """Branch: panel_type not in PANEL_WATTS -> True."""
    with pytest.raises(ValueError, match="unknown panel type"):
        panels_needed(300, "bifacial", 5)


def test_panels_needed_invalid_monthly_units_zero():
    """Branch: monthly_units <= 0 -> True (boundary: 0)."""
    with pytest.raises(ValueError, match="invalid input"):
        panels_needed(0, "mono", 5)


def test_panels_needed_invalid_monthly_units_negative():
    """Branch: monthly_units <= 0 -> True (negative value)."""
    with pytest.raises(ValueError, match="invalid input"):
        panels_needed(-100, "mono", 5)


def test_panels_needed_invalid_sun_hours_zero():
    """Branch: sun_hours <= 0 -> True (boundary: 0)."""
    with pytest.raises(ValueError, match="invalid input"):
        panels_needed(300, "mono", 0)


def test_panels_needed_invalid_sun_hours_negative():
    """Branch: sun_hours <= 0 -> True (negative value)."""
    with pytest.raises(ValueError, match="invalid input"):
        panels_needed(300, "mono", -3)


def test_panels_needed_exact_division_no_remainder():
    """Branch: daily_wh % per_panel_wh == 0 -> False branch of remainder check."""
    # monthly_units=300 -> daily_wh = 10000; mono (400W) * 5 sun_hours = 2000; 10000 % 2000 == 0 -> 5 panels
    assert panels_needed(300, "mono", 5) == 5


def test_panels_needed_with_remainder():
    """Branch: daily_wh % per_panel_wh != 0 -> True branch (panels += 1)."""
    # monthly_units=300 -> daily_wh = 10000; mono (400W) * 4 sun_hours = 1600; 10000 // 1600 = 6, rem = 400 -> 7 panels
    assert panels_needed(300, "mono", 4) == 7


def test_panels_needed_poly_panel_type():
    """Branch: panel_type in PANEL_WATTS using 'poly' (330W)."""
    # monthly_units=330 -> daily_wh = 11000; poly (330W) * 5 = 1650; 11000 // 1650 = 6, rem = 1100 -> 7 panels
    assert panels_needed(330, "poly", 5) == 7


def test_panels_needed_clamp_below_two():
    """Branch: panels < 2 -> True (clamps minimum panels to 2)."""
    # monthly_units=10 -> daily_wh = 333; mono (400W) * 5 = 2000; 333 // 2000 = 0 + 1 = 1 < 2 -> 2 panels
    assert panels_needed(10, "mono", 5) == 2


def test_panels_needed_two_or_more_no_clamp():
    """Branch: panels < 2 -> False (panels >= 2 is preserved)."""
    # monthly_units=120 -> daily_wh = 4000; mono * 5 = 2000; 4000 // 2000 = 2, rem = 0 -> 2 panels
    assert panels_needed(120, "mono", 5) == 2


# ============================================================================
# Branch Coverage Tests for install_cost()
# Decision Points & Branches:
# 1. if panels < 1:
#    - True -> raises ValueError("invalid panel count")
#    - False -> proceeds
# 2. if roof_type == "tin":
#    - True -> cost += 8000
#    - False -> proceeds to next check
# 3. elif roof_type == "tiled":
#    - True -> cost += panels * 2000
#    - False -> proceeds to next check
# 4. elif roof_type != "concrete":
#    - True -> raises ValueError("unknown roof type")
#    - False (i.e. roof_type == "concrete") -> proceeds
# 5. if has_battery:
#    - True -> cost += 60000
#    - False -> cost unchanged
# 6. if panels >= 10:
#    - True -> cost -= cost // 10 (10% discount)
#    - False -> no discount
# ============================================================================

def test_install_cost_invalid_panels_zero():
    """Branch: panels < 1 -> True (boundary: 0)."""
    with pytest.raises(ValueError, match="invalid panel count"):
        install_cost(0, "concrete", False)


def test_install_cost_invalid_panels_negative():
    """Branch: panels < 1 -> True (negative count)."""
    with pytest.raises(ValueError, match="invalid panel count"):
        install_cost(-5, "tin", True)


def test_install_cost_tin_roof_no_battery_under_10():
    """Branches: roof_type == 'tin' (True), has_battery=False, panels < 10 (False)."""
    # 4 panels * 25000 = 100000 + 8000 = 108000
    assert install_cost(4, "tin", False) == 108000


def test_install_cost_tiled_roof_with_battery_under_10():
    """Branches: roof_type == 'tiled' (True), has_battery=True, panels < 10 (False)."""
    # 4 panels * 25000 = 100000 + (4 * 2000 = 8000) + 60000 = 168000
    assert install_cost(4, "tiled", True) == 168000


def test_install_cost_concrete_roof_no_battery_under_10():
    """Branches: roof_type == 'concrete' (False for tin/tiled, False for != concrete), has_battery=False."""
    # 4 panels * 25000 = 100000
    assert install_cost(4, "concrete", False) == 100000


def test_install_cost_unknown_roof_type():
    """Branch: roof_type != 'concrete' -> True (raises ValueError)."""
    with pytest.raises(ValueError, match="unknown roof type"):
        install_cost(4, "slate", False)


def test_install_cost_discount_exactly_10_panels():
    """Branch: panels >= 10 -> True (boundary: exactly 10 panels, with 10% discount)."""
    # 10 panels * 25000 = 250000; concrete -> +0; no battery -> +0; cost -= 250000 // 10 = 25000 -> 225000
    assert install_cost(10, "concrete", False) == 225000


def test_install_cost_discount_with_tin_and_battery_over_10_panels():
    """Branches: tin roof (True), has_battery=True, panels >= 10 (True)."""
    # 12 panels * 25000 = 300000 + 8000 (tin) + 60000 (battery) = 368000; cost -= 36800 = 331200
    assert install_cost(12, "tin", True) == 331200


def test_install_cost_boundary_9_panels_no_discount():
    """Branch: panels >= 10 -> False (boundary: 9 panels, no discount)."""
    # 9 panels * 25000 = 225000; concrete -> +0; no battery -> +0; no discount -> 225000
    assert install_cost(9, "concrete", False) == 225000


# ============================================================================
# Branch Coverage Tests for payback_years()
# Decision Points & Branches:
# 1. if monthly_saving <= 0:
#    - True -> return -1
#    - False -> proceeds
# 2. if subsidy_percent > 40:
#    - True -> capped to 40
#    - False -> remains unchanged
# 3. if net_cost % yearly_saving:
#    - True (remainder != 0) -> years += 1
#    - False (remainder == 0) -> exact years
# ============================================================================

def test_payback_years_saving_zero():
    """Branch: monthly_saving <= 0 -> True (boundary: 0)."""
    assert payback_years(100000, 20, 0) == -1


def test_payback_years_saving_negative():
    """Branch: monthly_saving <= 0 -> True (negative savings)."""
    assert payback_years(100000, 20, -500) == -1


def test_payback_years_subsidy_capped_above_40():
    """Branch: subsidy_percent > 40 -> True (subsidy capped at 40%)."""
    # system_cost=100000, subsidy 60% capped to 40% -> net_cost = 60000; saving = 1000 * 12 = 12000; 60000 // 12000 = 5, rem = 0
    assert payback_years(100000, 60, 1000) == 5


def test_payback_years_subsidy_exactly_40():
    """Branch: subsidy_percent > 40 -> False (boundary: exactly 40%)."""
    # net_cost = 100000 - 40000 = 60000; saving = 12000; 60000 // 12000 = 5, rem = 0
    assert payback_years(100000, 40, 1000) == 5


def test_payback_years_subsidy_below_40():
    """Branch: subsidy_percent > 40 -> False (subsidy = 20%)."""
    # net_cost = 100000 - 20000 = 80000; saving = 12000; 80000 // 12000 = 6, rem = 8000 != 0 -> 7 years
    assert payback_years(100000, 20, 1000) == 7


def test_payback_years_zero_subsidy_exact_division():
    """Branch: net_cost % yearly_saving == 0 -> False (no remainder, exact years)."""
    # net_cost = 120000; yearly_saving = 12000; 120000 % 12000 == 0 -> 10 years
    assert payback_years(120000, 0, 1000) == 10


def test_payback_years_with_remainder_rounds_up():
    """Branch: net_cost % yearly_saving != 0 -> True (years += 1)."""
    # net_cost = 130000; yearly_saving = 12000; 130000 // 12000 = 10, rem = 10000 -> 11 years
    assert payback_years(130000, 0, 1000) == 11
