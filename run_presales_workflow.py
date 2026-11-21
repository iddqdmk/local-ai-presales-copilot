import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run_step(name, command):
    print(f"\n=== {name} ===", flush=True)

    subprocess.run(
        [sys.executable, *command],
        cwd=ROOT,
        check=True,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Local AI Pre-Sales Engineering Workflow"
    )
    parser.add_argument(
        "--scenario",
        default="scenarios/customer-30-users.json"
    )
    parser.add_argument(
        "--pricing",
        default="tco/customer-30-users-demo-pricing.json"
    )
    parser.add_argument(
        "--output-dir",
        default="demo/results/workflow-30-users"
    )

    args = parser.parse_args()

    scenario = Path(args.scenario).resolve()
    pricing = Path(args.pricing).resolve()
    output_dir = Path(args.output_dir).resolve()

    if not scenario.is_file():
        parser.error(f"Scenario not found: {scenario}")

    if not pricing.is_file():
        parser.error(f"Pricing not found: {pricing}")

    scenario_data = json.loads(
        scenario.read_text(encoding="utf-8")
    )
    pricing_data = json.loads(
        pricing.read_text(encoding="utf-8")
    )

    if scenario_data["scenario_id"] != pricing_data["scenario_id"]:
        parser.error(
            "Scenario and pricing IDs do not match"
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    sizing = output_dir / "sizing.json"
    architecture = output_dir / "architecture-comparison.md"
    tco = output_dir / "tco.json"
    proposal = output_dir / "proposal.md"

    run_step("1. INFRASTRUCTURE SIZING", [
        "sizing/sizing_engine.py",
        "--scenario", str(scenario),
        "--output", str(sizing),
    ])

    run_step("2. ARCHITECTURE COMPARISON", [
        "architecture/compare_architectures.py",
        "--scenario", str(scenario),
        "--sizing", str(sizing),
        "--output", str(architecture),
    ])

    run_step("3. THREE-YEAR TCO", [
        "tco/tco_calculator.py",
        "--pricing", str(pricing),
        "--output", str(tco),
    ])

    run_step("4. PRE-SALES PROPOSAL", [
        "proposals/generate_proposal.py",
        "--scenario", str(scenario),
        "--sizing", str(sizing),
        "--output", str(proposal),
    ])

    tco_data = json.loads(
        tco.read_text(encoding="utf-8")
    )

    # Preserve the original proposal and append
    # the results of the other workflow modules.
    with proposal.open("a", encoding="utf-8") as f:
        f.write("\n---\n\n")
        f.write("## 12. Architecture Alternatives\n\n")
        f.write(
            "Two architectures were assessed: "
            "traditional SAN and HCI.\n\n"
        )
        f.write(
            "See `architecture-comparison.md` "
            "for the technical comparison.\n\n"
        )

        f.write("## 13. Three-Year TCO Comparison\n\n")

        f.write("| Architecture | Three-year TCO |\n")
        f.write("|---|---:|\n")

        for key, option in tco_data["options"].items():
            amount = option["tco_3y"]
            label = (
                f"{amount:,.2f} {tco_data['currency']}"
                if amount is not None
                else "Not available"
            )
            f.write(f"| {key}: {option['name']} | {label} |\n")

        f.write("\n")

        if pricing_data.get("pricing_type") == "illustrative":
            f.write(
                "**Pricing disclaimer:** All cost figures "
                "are synthetic demonstration assumptions, "
                "not vendor quotations.\n\n"
            )

        if not tco_data["comparison"]["available"]:
            f.write(
                "TCO comparison is unavailable because "
                "required pricing inputs are missing.\n\n"
            )

    manifest = {
        "scenario_id": scenario_data["scenario_id"],
        "pricing_type": pricing_data.get(
            "pricing_type", "unspecified"
        ),
        "artifacts": {
            "sizing": sizing.name,
            "architecture_comparison": architecture.name,
            "tco": tco.name,
            "proposal": proposal.name,
        },
        "status": "generated",
        "note": (
            "Outputs are preliminary and require "
            "engineering validation."
        ),
    }

    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8"
    )

    print("\n=== WORKFLOW COMPLETE ===")
    print("Scenario:", scenario_data["scenario_id"])
    print("Output:", output_dir)
    print("Files:")
    for path in sorted(output_dir.iterdir()):
        print(" -", path.name)


if __name__ == "__main__":
    main()
