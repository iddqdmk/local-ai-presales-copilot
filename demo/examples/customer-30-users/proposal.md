# Preliminary Infrastructure Proposal

**Scenario:** Small Business Infrastructure Modernization
**Date:** 2026-11-22
**Status:** Draft — requires customer validation
**Project type:** Fictional portfolio demonstration

## 1. Executive Summary

The customer has 30 users at 1 site(s).

The proposed approach consolidates existing physical workloads onto a virtualized platform with centralized storage and backup.

This proposal is preliminary. Workload sizing is based on demonstration assumptions, not measured production utilization.

## 2. Customer Requirements

- Industry: Professional Services
- Users: 30
- Sites: 1
- Business objective: Consolidate workloads onto a virtualized infrastructure
- On-premises virtualization
- Host-level high availability
- Centralized storage
- Backup with immutability

## 3. Preliminary Workload Sizing

| Metric | Calculated demand |
|---|---:|
| Virtual machines | 7 |
| Total vCPU | 26 |
| Total VM RAM | 88 GB |
| Initial VM storage | 2060 GB |
| Planned usable storage | 4449.6 GB |
| Compute hosts | 2 |

### Workload Breakdown

| Workload | VMs | vCPU/VM | RAM/VM | Storage/VM |
|---|---:|---:|---:|---:|
| Active Directory and DNS | 2 | 2 | 4 GB | 80 GB |
| File Server | 1 | 4 | 8 GB | 1000 GB |
| Application Server | 2 | 4 | 16 GB | 150 GB |
| Database Server | 1 | 8 | 32 GB | 500 GB |
| Monitoring and Management | 1 | 2 | 8 GB | 100 GB |

## 4. Proposed Logical Architecture

```text
                Customer LAN
                     |
              Network Switches
                 /       \
                /         \
       Dell PowerEdge   Dell PowerEdge
           R760             R760
              \             /
               \           /
                VMware vSphere
                      |
             Dell PowerStore 1200T
                      |
               Virtual Machines

       Veeam Backup & Replication
                      |
       Separate Immutable Repository
```

Diagram is conceptual. Physical connectivity, storage protocols, network redundancy, and backup traffic paths require detailed design.

## 5. Indicative Bill of Materials

| Component | Quantity | Purpose |
|---|---:|---|
| Dell PowerEdge R760 | 2 | Virtualization hosts |
| Dell PowerStore 1200T | 1 | Shared primary storage |
| VMware vSphere | TBD | Virtualization platform |
| Veeam Backup & Replication | TBD | Backup software |
| Backup repository server/storage | TBD | Immutable backup target |
| Network switches | TBD | Management, VM and storage connectivity |

Quantities are indicative. This is not a vendor-validated configuration or quotation.

## 6. High Availability Considerations

- Preliminary compute design: 2 hosts.
- N+1 compute capacity is estimated using the sizing assumptions.
- VMware HA configuration and compatibility must be validated.
- Shared storage availability and network redundancy require separate assessment.
- HA does not replace backup or disaster recovery.

## 7. Backup and Recovery

- Veeam Backup & Replication is the candidate backup platform.
- A separate hardened repository is proposed for immutable backup copies.
- Repository sizing is pending retention, change-rate and restore-point requirements.
- Recovery objectives are not yet confirmed.

## 8. Commercial and TCO Status

A validated commercial three-year TCO is not yet available because vendor quotations, licensing costs, support prices and electricity tariffs have not been confirmed.

An illustrative three-year TCO has been calculated using synthetic demonstration prices. These figures are intended to demonstrate the calculation process and must not be used for procurement or investment decisions.

No prices have been invented.

## 9. Open Questions

1. What are the actual CPU, RAM and disk usage statistics of the current workloads?
2. What are the required RPO and RTO values?
3. What backup retention periods are required?
4. What is the measured peak storage IOPS and latency requirement?
5. What annual data growth is expected?
6. Are redundant switches and power feeds available?
7. What is the hardware and software budget?

## 10. Assumptions and Limitations

- All VM profiles are demonstration assumptions.
- CPU sizing uses an assumed vCPU-to-core ratio.
- No measured utilization or peak IOPS are available.
- Storage is logical capacity before RAID, metadata, snapshots and data reduction.
- Backup repository capacity is not included.
- Host count is a capacity estimate, not a validated Dell hardware configuration.

## 11. Next Steps

1. Validate customer requirements.
2. Collect workload performance measurements.
3. Confirm RPO, RTO and retention.
4. Validate vendor hardware compatibility.
5. Prepare detailed BoM and vendor quotations.
6. Recalculate three-year TCO using validated vendor quotations and confirmed operating costs.

---

## 12. Architecture Alternatives

Two architectures were assessed: traditional SAN and HCI.

See `architecture-comparison.md` for the technical comparison.

## 13. Three-Year TCO Comparison

| Architecture | Three-year TCO |
|---|---:|
| A: Traditional SAN | 137,000.00 USD |
| B: Hyperconverged Infrastructure | 128,000.00 USD |

**Pricing disclaimer:** All cost figures are synthetic demonstration assumptions, not vendor quotations.

