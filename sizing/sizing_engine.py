import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

WORKLOAD_PROFILES = {
    "Active Directory and DNS": {
        "vcpu": 2, "ram_gb": 4, "storage_gb": 80
    },
    "File Server": {
        "vcpu": 4, "ram_gb": 8, "storage_gb": 1000
    },
    "Application Server": {
        "vcpu": 4, "ram_gb": 16, "storage_gb": 150
    },
    "Database Server": {
        "vcpu": 8, "ram_gb": 32, "storage_gb": 500
    },
    "Monitoring and Management": {
        "vcpu": 2, "ram_gb": 8, "storage_gb": 100
    },
}

ASSUMPTIONS = {
    "annual_growth_percent": 20,
    "planning_years": 3,
    "storage_free_capacity_percent": 20,
    "cpu_overcommit_ratio": 2.0,
    "host_ram_gb": 256,
    "host_physical_cores": 32,
    "host_reserved_ram_gb": 24,
    "target_cpu_utilization": 0.70,
    "target_ram_utilization": 0.80,
    "ha_host_failures": 1,
    "minimum_ha_hosts": 2,
}


def calculate(scenario):
    total_vcpu = 0
    total_ram = 0
    total_storage = 0
    details = []

    for workload in scenario["workloads"]:
        profile = WORKLOAD_PROFILES.get(workload["name"])

        if profile is None:
            raise ValueError(
                f"Unknown workload: {workload['name']}"
            )

        count = workload["vm_count"]

        total_vcpu += count * profile["vcpu"]
        total_ram += count * profile["ram_gb"]
        total_storage += count * profile["storage_gb"]

        details.append({
            "workload": workload["name"],
            "vm_count": count,
            **profile,
        })

    growth_factor = (
        1 + ASSUMPTIONS["annual_growth_percent"] / 100
    ) ** ASSUMPTIONS["planning_years"]

    projected_storage = total_storage * growth_factor

    usable_storage_required = (
        projected_storage /
        (1 - ASSUMPTIONS["storage_free_capacity_percent"] / 100)
    )

    cpu_capacity_per_host = (
        ASSUMPTIONS["host_physical_cores"]
        * ASSUMPTIONS["cpu_overcommit_ratio"]
        * ASSUMPTIONS["target_cpu_utilization"]
    )

    ram_capacity_per_host = (
        ASSUMPTIONS["host_ram_gb"]
        - ASSUMPTIONS["host_reserved_ram_gb"]
    ) * ASSUMPTIONS["target_ram_utilization"]

    hosts_for_cpu = math.ceil(
        total_vcpu / cpu_capacity_per_host
    )

    hosts_for_ram = math.ceil(
        total_ram / ram_capacity_per_host
    )

    required_surviving_hosts = max(
        hosts_for_cpu,
        hosts_for_ram,
        1,
    )

    host_count = max(
        ASSUMPTIONS["minimum_ha_hosts"],
        required_surviving_hosts
        + ASSUMPTIONS["ha_host_failures"],
    )

    return {
        "scenario_id": scenario["scenario_id"],
        "users": scenario["customer"]["users"],
        "total_vms": sum(
            w["vm_count"] for w in scenario["workloads"]
        ),
        "workloads": details,
        "resource_demand": {
            "total_vcpu": total_vcpu,
            "total_ram_gb": total_ram,
            "initial_storage_gb": total_storage,
        },
        "storage_sizing": {
            "projected_data_gb": round(projected_storage, 2),
            "required_usable_capacity_gb": round(
                usable_storage_required, 2
            ),
        },
        "compute_sizing": {
            "cpu_capacity_per_host_vcpu": round(
                cpu_capacity_per_host, 2
            ),
            "ram_capacity_per_host_gb": round(
                ram_capacity_per_host, 2
            ),
            "required_surviving_hosts": required_surviving_hosts,
            "recommended_host_count": host_count,
            "ha_model": "N+1 host capacity",
        },
        "assumptions": ASSUMPTIONS,
        "limitations": [
            "All VM profiles are demonstration assumptions.",
            "CPU sizing uses an assumed vCPU-to-core ratio.",
            "No measured utilization or peak IOPS are available.",
            "Storage is logical capacity before RAID, metadata, "
            "snapshots and data reduction.",
            "Backup repository capacity is not included.",
            "Host count is a capacity estimate, not a validated "
            "Dell hardware configuration.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    scenario = json.loads(
        Path(args.scenario).read_text(encoding="utf-8")
    )

    result = calculate(scenario)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("=== INFRASTRUCTURE SIZING ===")
    print("Scenario:", result["scenario_id"])
    print("Users:", result["users"])
    print("VMs:", result["total_vms"])
    print("vCPU:", result["resource_demand"]["total_vcpu"])
    print("RAM GB:", result["resource_demand"]["total_ram_gb"])
    print(
        "Required usable storage GB:",
        result["storage_sizing"]["required_usable_capacity_gb"]
    )
    print(
        "Recommended hosts:",
        result["compute_sizing"]["recommended_host_count"]
    )
    print("SAVED:", output)


if __name__ == "__main__":
    main()
