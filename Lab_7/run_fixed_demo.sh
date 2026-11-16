#!/usr/bin/env bash
set -euo pipefail
python -m pip install -r requirements.txt
python solar_panel_estimate_parser.py <<'EOF'
Main Roof
320 kWh
20ft x 15ft
EOF
python -m pytest -q test_solar_panel_estimate_parser.py
