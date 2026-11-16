"""Robust parsers for a simple rooftop solar estimate.

Student: Yashwanth Gowda T G
SRN: PES1UG25AM818
"""

import re


def clean_site_name(name):
    """Normalize a site name; return an empty string for invalid input."""
    if not isinstance(name, str):
        return ""
    name = "".join(ch for ch in name if ch.isprintable())
    name = name.replace("#", "").replace("@", "")
    return " ".join(name.split()).title()


def parse_monthly_units(text):
    """Parse a non-negative whole-number kWh reading; invalid input returns 0."""
    if not isinstance(text, str):
        return 0
    candidate = text.strip()
    candidate = re.sub(r"(?i)\s*kwh\s*$", "", candidate).strip()
    if not re.fullmatch(r"\+?\d+", candidate):
        return 0
    try:
        value = int(candidate)
    except (TypeError, ValueError, OverflowError):
        return 0
    return value if value >= 0 else 0


def panels_for_roof(text):
    """Return floor(roof area / 18 sq ft); invalid dimensions return 0."""
    if not isinstance(text, str):
        return 0
    match = re.fullmatch(
        r"\s*(\+?\d+)\s*(?:ft)?\s*[xX×]\s*(\+?\d+)\s*(?:ft)?\s*",
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        return 0
    try:
        length, width = (int(part) for part in match.groups())
    except (TypeError, ValueError, OverflowError):
        return 0
    if length <= 0 or width <= 0:
        return 0
    return (length * width) // 18


def main():
    print("==== Running clean_site_name ====")
    value = input("Enter the installation site name: ")
    print("Site name:", clean_site_name(value))
    print("\n==== Running parse_monthly_units ====")
    value = input("Enter monthly electricity use (e.g. 320 kWh): ")
    print("Monthly units:", parse_monthly_units(value))
    print("\n==== Running panels_for_roof ====")
    value = input("Enter roof size as LENGTHft x WIDTHft (e.g. 20ft x 15ft): ")
    print("Panels that fit:", panels_for_roof(value))


if __name__ == "__main__":
    main()
