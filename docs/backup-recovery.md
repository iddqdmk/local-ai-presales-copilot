
# Backup & Recovery

## Environment

	- Host: Windows 11 with WSL2 Ubuntu 24.04
	- Container runtime: Docker Engine
	- Orchestration: Docker Compose
	- Automation: Ansible
	- AI inference: Ollama / Qwen3 4B
	- User interface: Open WebUI

## Backup strategy

Cold backup of Docker volumes.

The AI services are stopped before archiving to reduce
the risk of inconsistent application data.

Each backup contains:
- ollama.tar.gz
- webui.tar.gz
- SHA256SUMS

## Automation

Ansible role: ansible/roles/backup

The role performs:
- Preflight checks
- Volume discovery
- Disk space validation
- Application shutdown
- Volume archiving
- Application restart attempt
- Archive and checksum verification

## Recovery test

Recovery was tested using separate Docker volumes
and a dedicated Docker Compose project.

Validation included:
- Archive checksum verification
- Successful extraction of both archives
- Ollama model discovery
- Qwen3 4B inference
- Open WebUI authentication
- Restoration of existing chat history
- Verification that the original stack remained operational

## Limitations

- Single-host environment
- Backup requires temporary service downtime
- No automatic backup schedule yet
- No offsite backup
- No defined production RPO/RTO
- No disaster recovery test on a second physical host

## Next improvements

- Version pinning
- Automated backup schedule
- Retention policy
- Encrypted off-host backup
- Recovery time measurements
- Monitoring and alerting
