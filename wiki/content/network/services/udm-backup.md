---
title: UDM Backup & Restore
path: network/services/backup
tags: [udm, backup, restore, config]
---

# UDM Backup & Restore Service

Backup and restore is treated as a **first-class network service**.

## Backup Sources

| Path | Purpose |
|---|---|
| /data/unifi/data/backup | Controller backups |
| /data/udapi-config | DHCP + system state |
| dnsmasq.lease | Live inventory |

## Example Backup

```bash
rsync -a root@udm:/data/unifi/data/backup udm-backups/
rsync -a root@udm:/data/udapi-config udm-backups/
```

## Cross-links

- [[udm-dhcp]]
- [[udm-device-inventory]]
- [[udm-firewall]]
