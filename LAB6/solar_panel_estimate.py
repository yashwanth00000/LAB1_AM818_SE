PANEL_WATTS = {"mono": 400, "poly": 330}


def panels_needed(monthly_units, panel_type, sun_hours):
    if panel_type not in PANEL_WATTS:
        raise ValueError("unknown panel type")
    if monthly_units <= 0 or sun_hours <= 0:
        raise ValueError("invalid input")
    daily_wh = monthly_units * 1000 // 30
    per_panel_wh = PANEL_WATTS[panel_type] * sun_hours
    panels = daily_wh // per_panel_wh
    if daily_wh % per_panel_wh:
        panels += 1
    if panels < 2:
        panels = 2
    return panels


def install_cost(panels, roof_type, has_battery):
    if panels < 1:
        raise ValueError("invalid panel count")
    cost = panels * 25000
    if roof_type == "tin":
        cost += 8000
    elif roof_type == "tiled":
        cost += panels * 2000
    elif roof_type != "concrete":
        raise ValueError("unknown roof type")
    if has_battery:
        cost += 60000
    if panels >= 10:
        cost -= cost // 10
    return cost


def payback_years(system_cost, subsidy_percent, monthly_saving):
    if monthly_saving <= 0:
        return -1
    if subsidy_percent > 40:
        subsidy_percent = 40
    net_cost = system_cost - system_cost * subsidy_percent // 100
    yearly_saving = monthly_saving * 12
    years = net_cost // yearly_saving
    if net_cost % yearly_saving:
        years += 1
    return years
