"""
Code Coverage Test Suite for solar_panel_estimate.py
Lab 6: Code and Branch Coverage Analysis

This test suite targets line (statement) coverage >= 90% (achieving 100% line coverage)
by executing every statement in solar_panel_estimate.py at least once.
"""

import pytest
from solar_panel_estimate import panels_needed, install_cost, payback_years


# ============================================================================
# Tests for panels_needed() - Line Coverage
# ============================================================================

def test_panels_needed_unknown_panel_type():
    """Executes lines 5-6: ValueError for unsupported panel type."""
    with pytest.raises(ValueError, match="unknown panel type"):
        panels_needed(300, "thin_film", 5)


def test_panels_needed_invalid_monthly_units():
    """Executes lines 7-8: ValueError when monthly units <= 0."""
    with pytest.raises(ValueError, match="invalid input"):
        panels_needed(0, "mono", 5)


def test_panels_needed_with_remainder():
    """Executes lines 9-13: daily_wh % per_panel_wh != 0 triggers panels += 1."""
    # monthly_units=300 -> daily_wh = 10000; mono (400W) * 4 sun_hours = 1600; 10000 // 1600 = 6, rem 400 != 0 -> 7 panels
    assert panels_needed(300, "mono", 4) == 7


def test_panels_needed_minimum_panel_clamp():
    """Executes lines 14-16: panels < 2 triggers panels = 2."""
    # monthly_units=10 -> daily_wh = 333; per_panel_wh = 2000; panels = 0 + 1 = 1 < 2 -> 2 panels
    assert panels_needed(10, "mono", 5) == 2


# ============================================================================
# Tests for install_cost() - Line Coverage
# ============================================================================

def test_install_cost_invalid_panels():
    """Executes lines 20-21: ValueError when panels < 1."""
    with pytest.raises(ValueError, match="invalid panel count"):
        install_cost(0, "tin", False)


def test_install_cost_tin_roof():
    """Executes lines 23-24: adds 8000 for tin roof."""
    # 4 panels * 25000 = 100000 + 8000 = 108000
    assert install_cost(4, "tin", False) == 108000


def test_install_cost_tiled_roof():
    """Executes lines 25-26: adds panels * 2000 for tiled roof."""
    # 4 panels * 25000 = 100000 + (4 * 2000) = 108000
    assert install_cost(4, "tiled", False) == 108000


def test_install_cost_unknown_roof():
    """Executes lines 27-28: ValueError when roof_type is unknown."""
    with pytest.raises(ValueError, match="unknown roof type"):
        install_cost(4, "wood", False)


def test_install_cost_concrete_with_battery():
    """Executes line 30: adds 60000 when has_battery is True on concrete roof."""
    # 4 panels * 25000 = 100000 + 60000 = 160000
    assert install_cost(4, "concrete", True) == 160000


def test_install_cost_bulk_discount():
    """Executes lines 31-33: 10% discount when panels >= 10."""
    # 10 panels * 25000 = 250000; discount = 25000 -> 225000
    assert install_cost(10, "concrete", False) == 225000


# ============================================================================
# Tests for payback_years() - Line Coverage
# ============================================================================

def test_payback_years_non_positive_saving():
    """Executes lines 37-38: returns -1 when monthly saving <= 0."""
    assert payback_years(100000, 20, 0) == -1


def test_payback_years_high_subsidy_capped():
    """Executes lines 39-40: caps subsidy at 40% when subsidy_percent > 40."""
    # system_cost=100000, subsidy capped at 40 -> net_cost = 60000; saving = 1000 * 12 = 12000; 60000 // 12000 = 5
    assert payback_years(100000, 50, 1000) == 5


def test_payback_years_with_remainder():
    """Executes lines 41-46: net_cost % yearly_saving != 0 triggers years += 1."""
    # system_cost=100000, subsidy 20% -> net_cost = 80000; saving = 1000 * 12 = 12000; 80000 // 12000 = 6, rem 8000 != 0 -> 7
    assert payback_years(100000, 20, 1000) == 7
