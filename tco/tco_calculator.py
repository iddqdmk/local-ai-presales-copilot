import argparse
import json
from decimal import Decimal
from pathlib import Path


def money(value):
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError("Boolean is not a valid price")

    amount = Decimal(str(value))

    if not amount.is_finite() or amount < 0:
        raise ValueError(f"Invalid cost: {value}")

    return amount


def calculate_option(option, years):
    capex = option["capex"]
    annual_opex = option["annual_opex"]

    missing = []
    known_capex = Decimal("0")
    known_annual_opex = Decimal("0")

    for category, value in capex.items():
        amount = money(value)

        if amount is None:
            missing.append(f"capex.{category}")
        else:
            known_capex += amount

    for category, value in annual_opex.items():
        amount = money(value)

        if amount is None:
            missing.append(f"annual_opex.{category}")
        else:
            known_annual_opex += amount

    known_total = (
        known_capex + known_annual_opex * years
    )

    complete = len(missing) == 0

    return {
        "name": option["name"],
        "complete": complete,
        "known_capex": float(known_capex),
        "known_annual_opex": float(known_annual_opex),
        "known_total_3y": float(known_total),
        "tco_3y": float(known_total) if complete else None,
        "missing_inputs": missing
    }


def calculate(data):
    years = data["period_years"]

    if not isinstance(years, int) or years <= 0:
        raise ValueError("Invalid calculation period")

    options = {
        key: calculate_option(value, years)
        for key, value in data["options"].items()
    }

    a = options["A"]
    b = options["B"]

    comparison = {
        "available": a["complete"] and b["complete"],
        "difference": None,
        "lower_tco_option": None
    }

    if comparison["available"]:
        difference = a["tco_3y"] - b["tco_3y"]
        comparison["difference"] = difference

        if difference > 0:
            comparison["lower_tco_option"] = "B"
        elif difference < 0:
            comparison["lower_tco_option"] = "A"
        else:
            comparison["lower_tco_option"] = "Equal"

    return {
        "scenario_id": data["scenario_id"],
        "currency": data["currency"],
        "period_years": years,
        "options": options,
        "comparison": comparison
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pricing", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    data = json.loads(
        Path(args.pricing).read_text(encoding="utf-8")
    )

    result = calculate(data)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8"
    )

    print("=== THREE-YEAR TCO ===")
    print("Scenario:", result["scenario_id"])
    print("Currency:", result["currency"])

    for key, option in result["options"].items():
        print(f"\nOption {key}: {option['name']}")
        print("Complete:", option["complete"])
        print("Known CAPEX:", option["known_capex"])
        print("Known annual OPEX:", option["known_annual_opex"])
        print("TCO:", option["tco_3y"])
        print("Missing inputs:", len(option["missing_inputs"]))

    print("\nComparison available:",
          result["comparison"]["available"])
    print("SAVED:", output)


if __name__ == "__main__":
    main()
