# Infrastructure Architecture Comparison

**Scenario:** Small Business Infrastructure Modernization
**Users:** 30
**Virtual machines:** 7
**Calculated compute hosts:** 2
**Planned usable storage:** 4449.6 GB
**Status:** Preliminary engineering assessment
**Project:** Fictional portfolio demonstration

## 1. Objective

Compare traditional shared-storage architecture with hyperconverged infrastructure for the same customer workload.

Both options must satisfy the same business requirements before a final selection.

## 2. Option A — Traditional SAN

- Compute: 2 Dell PowerEdge R760 servers.
- Virtualization: VMware vSphere.
- Shared storage: Dell PowerStore 1200T.
- High availability: VMware HA, subject to design.
- Backup: Veeam Backup & Replication.
- Immutable copies: separate hardened repository.

### Logical Architecture A

```text
             Customer LAN
                  |
           Network Fabric
             /       \
            /         \
       ESXi Host 1   ESXi Host 2
       PowerEdge     PowerEdge
          R760          R760
            \            /
             \          /
             Storage Fabric
                   |
            PowerStore 1200T
                   |
              VM Datastores

        Veeam Backup Platform
                   |
       Separate Hardened Repository
```

This is a conceptual diagram. Network paths, redundant switches and storage protocols must be designed separately.

## 3. Option B — Hyperconverged Infrastructure

- Preliminary compute target: 2 nodes.
- Local drives provide distributed storage.
- HCI software and hypervisor: not selected.
- Backup integration: requires validation.
- Witness/quorum: depends on HCI platform.

### Logical Architecture B

```text
             Customer LAN
                  |
           Network Fabric
             /       \
            /         \
       HCI Node 1    HCI Node 2
       Compute +     Compute +
       Local SSD     Local SSD
            \           /
             \         /
          Distributed Storage
                   |
              VM Datastores

          Witness / Quorum
          If platform requires

        Backup Infrastructure
                   |
       Separate Backup Repository
```

The two-node HCI topology is conceptual.
It is not approved until platform-specific quorum, failure tolerance, hardware compatibility and storage overhead are validated.

## 4. Technical Comparison

| Criterion | Option A: SAN | Option B: HCI |
|---|---|---|
| Storage architecture | External shared storage | Distributed local storage |
| Compute scaling | Can scale separately from storage | May be coupled to storage scaling |
| Storage scaling | Storage array expansion | Depends on HCI platform |
| High availability | VMware HA with shared storage | Platform-specific HA and quorum |
| Networking | VM, management and storage networks | VM, management and HCI storage networks |
| Failure domains | Hosts, storage array and network | Nodes, storage replicas and network |
| Licensing | Hypervisor, storage and backup licensing | Hypervisor/HCI and backup licensing |
| Operational complexity | Separate compute and storage management | Potentially unified management |
| CAPEX | Requires vendor quotation | Requires vendor quotation |
| Three-year TCO | Not yet calculated | Not yet calculated |

## 5. Capacity and HA Considerations

The sizing engine estimates 2 compute hosts under its stated N+1 capacity assumptions.

This estimate does not validate storage availability, networking, quorum, hardware compatibility or licensing.

### Option A

- Confirm that the remaining host can run all required VMs after one host failure.
- Validate shared storage availability.
- Design redundant storage connectivity.
- Confirm VMware and Dell compatibility.

### Option B

- Select an actual HCI product and version.
- Validate the minimum supported node count.
- Determine witness or quorum requirements.
- Calculate storage capacity after replication and resilience overhead.
- Validate performance after one node failure.

## 6. Preliminary Commercial Assessment

No reliable CAPEX or TCO comparison is possible without vendor quotations.

Required cost inputs:

- Servers, drives, memory and network adapters.
- Storage hardware or HCI software.
- Hypervisor and backup licensing.
- Network equipment and support.
- Power, cooling and maintenance.

## 7. Risks

**Option A:**

- Potentially excessive storage investment for a small workload.
- Storage network design complexity.
- Additional storage licensing and support.

**Option B:**

- Unsupported two-node configuration risk.
- Storage replication capacity overhead.
- Vendor-specific HCI compatibility.
- Possible compute/storage scaling coupling.

## 8. Preliminary Recommendation

Do not select a final architecture yet.

For a 30-user environment, compare both options using validated hardware designs and three-year commercial quotations.

Option A is the documented reference design.
Option B remains a conceptual alternative until an HCI platform is selected.

The preferred option should be chosen based on workload requirements, availability, supportability and TCO.

## 9. Next Steps

1. Validate actual workload requirements.
2. Confirm RPO, RTO and backup retention.
3. Select an HCI platform for Option B.
4. Validate hardware and software compatibility.
5. Request vendor quotations for both options.
6. Calculate three-year TCO.
7. Prepare a final architecture recommendation.
