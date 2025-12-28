# WyseChoice Wiki

This repository contains the WyseChoice wiki plus infrastructure and reference materials.

## Layout
- `wiki/` – wiki application and content.
- `network/` – UniFi network exports, Pi-hole backups, diagrams, and helper scripts for DNS/network management.
  - `configs/` – UniFi configuration exports (HTML), Pi-hole teleporter/backup artifacts, and CNI/DNS configuration snippets.
  - `diagrams/` – network topology, VLAN, and email routing diagrams.
  - `scripts/` – DNS/Pi-hole helper scripts.
- `assets/`, `data/` – additional documents, images, and data used by the wiki.
- `backupall.sh`, `upgrade_wiki.sh`, etc. – legacy operational scripts (to be moved into `scripts/` in future cleanups).

The goal is to keep operational network artifacts together while we continue organizing the rest of the repository.
