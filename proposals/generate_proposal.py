import argparse
import json
from pathlib import Path
from datetime import date


def load_json(path):
    return json.loads(
        Path(path).read_text(encoding="utf-8")
    )


def generate(scenario, sizing):
    customer = scenario["customer"]
    demand = sizing["resource_demand"]
    storage = sizing["storage_sizing"]
    compute = sizing["compute_sizing"]

    hosts = compute["recommended_host_count"]

    lines = [
        "# Preliminary Infrastructure Proposal",
        "",
        f"**Scenario:** {scenario['scenario_name']}",
        f"**Date:** {date.today().isoformat()}",
        "**Status:** Draft — requires customer validation",
        "**Project type:** Fictional portfolio demonstration",
        "",
        "## 1. Executive Summary",
        "",
        f"The customer has {customer['users']} users "
        f"at {customer['sites']} site(s).",
        "",
        "The proposed approach consolidates existing "
        "physical workloads onto a virtualized platform "
        "with centralized storage and backup.",
        "",
        "This proposal is preliminary. Workload sizing "
        "is based on demonstration assumptions, "
        "not measured production utilization.",
        "",
        "## 2. Customer Requirements",
        "",
        f"- Industry: {customer['industry']}",
        f"- Users: {customer['users']}",
        f"- Sites: {customer['sites']}",
        f"- Business objective: {customer['business_goal']}",
        "- On-premises virtualization",
        "- Host-level high availability",
        "- Centralized storage",
        "- Backup with immutability",
        "",
        "## 3. Preliminary Workload Sizing",
        "",
        "| Metric | Calculated demand |",
        "|---|---:|",
        f"| Virtual machines | {sizing['total_vms']} |",
        f"| Total vCPU | {demand['total_vcpu']} |",
        f"| Total VM RAM | {demand['total_ram_gb']} GB |",
        f"| Initial VM storage | {demand['initial_storage_gb']} GB |",
        f"| Planned usable storage | "
        f"{storage['required_usable_capacity_gb']:.1f} GB |",
        f"| Compute hosts | {hosts} |",
        "",
        "### Workload Breakdown",
        "",
        "| Workload | VMs | vCPU/VM | RAM/VM | Storage/VM |",
        "|---|---:|---:|---:|---:|",
    ]

    for w in sizing["workloads"]:
        lines.append(
            f"| {w['workload']} | {w['vm_count']} | "
            f"{w['vcpu']} | {w['ram_gb']} GB | "
            f"{w['storage_gb']} GB |"
        )

    lines += [
        "",
        "## 4. Proposed Logical Architecture",
        "",
        "```text",
        "                Customer LAN",
        "                     |",
        "              Network Switches",
        "                 /       \\",
        "                /         \\",
        "       Dell PowerEdge   Dell PowerEdge",
        "           R760             R760",
        "              \\             /",
        "               \\           /",
        "                VMware vSphere",
        "                      |",
        "             Dell PowerStore 1200T",
        "                      |",
        "               Virtual Machines",
        "",
        "       Veeam Backup & Replication",
        "                      |",
        "       Separate Immutable Repository",
        "```",
        "",
        "Diagram is conceptual. Physical connectivity, "
        "storage protocols, network redundancy, and "
        "backup traffic paths require detailed design.",
        "",
        "## 5. Indicative Bill of Materials",
        "",
        "| Component | Quantity | Purpose |",
        "|---|---:|---|",
        f"| Dell PowerEdge R760 | {hosts} | "
        "Virtualization hosts |",
        "| Dell PowerStore 1200T | 1 | "
        "Shared primary storage |",
        "| VMware vSphere | TBD | "
        "Virtualization platform |",
        "| Veeam Backup & Replication | TBD | "
        "Backup software |",
        "| Backup repository server/storage | TBD | "
        "Immutable backup target |",
        "| Network switches | TBD | "
        "Management, VM and storage connectivity |",
        "",
        "Quantities are indicative. This is not a "
        "vendor-validated configuration or quotation.",
        "",
        "## 6. High Availability Considerations",
        "",
        f"- Preliminary compute design: {hosts} hosts.",
        "- N+1 compute capacity is estimated using "
        "the sizing assumptions.",
        "- VMware HA configuration and compatibility "
        "must be validated.",
        "- Shared storage availability and network "
        "redundancy require separate assessment.",
        "- HA does not replace backup or disaster recovery.",
        "",
        "## 7. Backup and Recovery",
        "",
        "- Veeam Backup & Replication is the candidate "
        "backup platform.",
        "- A separate hardened repository is proposed "
        "for immutable backup copies.",
        "- Repository sizing is pending retention, "
        "change-rate and restore-point requirements.",
        "- Recovery objectives are not yet confirmed.",
        "",
        "## 8. Commercial and TCO Status",
        "",
        "A three-year TCO cannot yet be calculated "
        "reliably because hardware quotations, "
        "licensing, support and electricity tariffs "
        "have not been supplied.",
        "",
        "No prices have been invented.",
        "",
        "## 9. Open Questions",
        "",
        "1. What are the actual CPU, RAM and disk usage "
        "statistics of the current workloads?",
        "2. What are the required RPO and RTO values?",
        "3. What backup retention periods are required?",
        "4. What is the measured peak storage IOPS "
        "and latency requirement?",
        "5. What annual data growth is expected?",
        "6. Are redundant switches and power feeds available?",
        "7. What is the hardware and software budget?",
        "",
        "## 10. Assumptions and Limitations",
        "",
    ]

    for limitation in sizing["limitations"]:
        lines.append(f"- {limitation}")

    lines += [
        "",
        "## 11. Next Steps",
        "",
        "1. Validate customer requirements.",
        "2. Collect workload performance measurements.",
        "3. Confirm RPO, RTO and retention.",
        "4. Validate vendor hardware compatibility.",
        "5. Prepare detailed BoM and vendor quotations.",
        "6. Calculate three-year TCO.",
        "",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--sizing", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    scenario = load_json(args.scenario)
    sizing = load_json(args.sizing)

    if scenario["scenario_id"] != sizing["scenario_id"]:
        raise ValueError("Scenario and sizing IDs do not match")

    proposal = generate(scenario, sizing)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(proposal, encoding="utf-8")

    print("=== PRE-SALES PROPOSAL ===")
    print("Scenario:", scenario["scenario_id"])
    print("Users:", sizing["users"])
    print("Hosts:", sizing["compute_sizing"]["recommended_host_count"])
    print("Sections:", proposal.count("\n## "))
    print("SAVED:", output)


if __name__ == "__main__":
    main()
