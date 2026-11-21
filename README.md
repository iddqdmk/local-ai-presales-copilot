# Local AI Pre-Sales Copilot

A local AI-assisted pre-sales engineering project combining technical document retrieval, infrastructure sizing, architecture comparison, three-year TCO calculations, and proposal generation.

The project demonstrates practical skills in enterprise infrastructure, pre-sales engineering, local AI, and automation.

## 1. Project Overview

The project consists of two independent components.

### AI Knowledge Assistant

A local document-based assistant designed to answer technical questions using indexed vendor documentation.

Current capabilities:

- Local LLM inference through Ollama
- BM25 document retrieval
- Vendor-aware query routing
- Technical document indexing
- Source references in generated answers
- VMware, Veeam, and Dell documentation support
- Command-line interface

The assistant uses locally prepared document indexes.

Citation validation verifies that references correspond to retrieved source records. It does not guarantee factual correctness of every generated claim.

### Pre-Sales Engineering Workflow

A Python-based workflow that generates preliminary engineering deliverables from customer requirements.

Current capabilities:

- Infrastructure sizing
- Workload capacity calculations
- Traditional SAN versus HCI comparison
- Three-year TCO calculation
- Preliminary technical proposal generation
- JSON and Markdown reports

This workflow operates independently of the local LLM.

## 2. System Architecture

### Engineering Workflow

```text
Customer Requirements
        |
        v
Infrastructure Sizing
        |
        v
Architecture Comparison
    SAN vs HCI
        |
        v
Three-Year TCO
        |
        v
Proposal Generator
        |
        v
Engineering Deliverables
```

### AI Knowledge Assistant

```text
Technical Documentation
        |
        v
Document Extraction
        |
        v
Document Indexing
        |
        v
BM25 Retrieval
        |
        v
Vendor-Aware Routing
        |
        v
Local Ollama LLM
        |
        v
Answer with Citations
```

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Local LLM runtime | Ollama |
| Local AI interface | Open WebUI |
| Document extraction | PyMuPDF |
| Retrieval | BM25 |
| Infrastructure deployment | Docker Compose |
| Configuration automation | Ansible |
| Data exchange | JSON |
| Engineering reports | Markdown |

## 4. Quick Start

The engineering workflow can run without Ollama, a GPU, or downloaded vendor PDF documents.

### Requirements

- Python 3
- Git
- A local copy of this repository

### Clone the repository

```bash
git clone <REPOSITORY_URL>
cd local-ai-presales-copilot
```

Replace `<REPOSITORY_URL>` with the actual GitHub repository URL.

### Run the engineering workflow

```bash
python run_presales_workflow.py \
  --scenario scenarios/customer-30-users.json \
  --pricing tco/customer-30-users-demo-pricing.json \
  --output-dir demo/results/workflow-30-users
```

### Generated Files

```text
demo/results/workflow-30-users/
├── architecture-comparison.md
├── manifest.json
├── proposal.md
├── sizing.json
└── tco.json
```

## 5. Demonstration Customer Scenario

The project includes a fictional small-business infrastructure modernization scenario.

Customer profile:

- Industry: Professional Services
- Users: 30
- Sites: 1
- Virtual machines: 7
- Deployment: On-premises

Infrastructure requirements:

- Server virtualization
- High availability
- Centralized storage
- Backup
- Immutable backup repository

### Preliminary Sizing

| Metric | Calculated Value |
|---|---:|
| Total virtual machines | 7 |
| Total vCPU | 26 |
| VM memory | 88 GB |
| Required usable primary storage | 4,449.6 GB |
| Preliminary compute hosts | 2 |

These values are produced using demonstration workload profiles.

The calculations are not a substitute for detailed customer discovery, performance assessment, or vendor-validated infrastructure sizing.

## 6. Architecture Comparison

Two conceptual architectures are compared.

### Option A: Traditional SAN

- Two Dell PowerEdge R760 compute hosts
- External Dell PowerStore storage
- VMware vSphere virtualization
- Veeam Backup & Replication
- Separate immutable backup repository

### Option B: Hyperconverged Infrastructure

- Conceptual HCI nodes
- Distributed local storage
- Integrated compute and storage infrastructure
- Backup integration

The HCI platform has not been selected.

Quorum requirements, supported node counts, licensing, storage overhead, and compatibility require further validation.

## 7. Three-Year TCO

The TCO calculator processes:

- Hardware acquisition
- Infrastructure implementation
- Annual licensing
- Hardware support
- Software support
- Electricity
- Other operational costs

### Illustrative Results

| Metric | Traditional SAN | HCI |
|---|---:|---:|
| CAPEX | $80,000 | $62,000 |
| Annual OPEX | $19,000 | $22,000 |
| Three-year TCO | $137,000 | $128,000 |

**Important:** All prices are synthetic demonstration inputs.

They are not vendor quotations, verified market prices, or purchasing recommendations.

Actual TCO depends on the selected hardware, software, licensing, support contracts, power consumption, and deployment requirements.

## 8. Local AI Knowledge Assistant

The local RAG assistant has been tested with technical questions related to:

- VMware vSphere High Availability
- Veeam Backup & Replication
- Dell PowerEdge servers
- Dell PowerStore storage

### Local Requirements

- Docker and Docker Compose
- Ollama
- A compatible local language model
- Locally prepared technical documentation
- Generated document indexes
- Python dependencies from requirements.txt

### Install Python Dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Start Infrastructure Services

```bash
docker compose -f compose/docker-compose.yml up -d
```

The Docker Compose configuration defines:

- Ollama
- Open WebUI

### Example Technical Question

```bash
python run_presales_copilot.py \
  "How does VMware vSphere HA detect a failed ESXi host?" \
  --save
```

This requires the appropriate local document index and a running Ollama service with the configured model.

### Vendor Documentation

Third-party PDF manuals and extracted full-text indexes are intentionally excluded from the public repository.

Users must obtain the documentation from authorized sources and create local indexes.

The RAG setup is not yet fully automated for a fresh clone.

## 9. Infrastructure Automation

The repository contains infrastructure automation components:

- Docker Compose configuration
- Ansible inventory
- Ansible deployment playbooks
- Backup and recovery documentation
- Restore-test configuration

These are designed for a local laboratory environment.

Production deployment would require additional security, monitoring, backup validation, and infrastructure hardening.

## 10. Project Limitations

This project is a functional engineering demonstration, not a production-ready infrastructure design.

Current limitations:

1. Sizing uses predefined workload assumptions.
2. Physical hardware sizing requires vendor validation.
3. Backup repository capacity is not included in primary storage sizing.
4. HCI architecture compatibility and quorum requirements are not finalized.
5. TCO calculations depend on supplied prices and assumptions.
6. RAG citation validation does not guarantee factual accuracy.
7. The RAG assistant and engineering workflow are separate execution paths.
8. Public RAG setup requires additional preparation of local documentation and indexes.

## 11. Project Status

**MVP v1.0 — Portfolio Demonstration**

Implemented:

- Multi-vendor document retrieval
- Local LLM question answering
- Infrastructure sizing
- Architecture comparison
- Three-year TCO calculation
- Technical proposal generation
- Unified engineering workflow

The engineering workflow has been successfully tested with the included 30-user customer scenario.

Public installation and reproducibility checks are being finalized.

## 12. Intended Use

This project demonstrates practical experience in:

- Pre-Sales Engineering
- Solutions Architecture
- Enterprise Infrastructure
- Technical Requirements Analysis
- Infrastructure Sizing
- Customer Proposal Preparation
- Local AI and RAG
- Docker and Ansible Automation

## Disclaimer

All customer scenarios are fictional.

All commercial figures are illustrative.

Vendor names and trademarks belong to their respective owners.

The project is intended for technical education, experimentation, and portfolio demonstration.
