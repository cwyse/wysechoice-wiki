---
title: <SERVICE NAME>
description: <WHAT THIS SERVICE DOES>
published: true
tags: network service <keywords>
editor: markdown
---

# <SERVICE NAME>

## Overview
What the service does, why it exists, and what depends on it.

**Role in network:**  
- Critical / Important / Optional  
- Used by: <devices / users / other services>

---

## Architecture
How this service is deployed.

- Host: <UDM / Raspberry Pi / VM / NAS>
- Runtime: Podman / Docker / Native
- Network: VLAN / MACVLAN / host
- Ports exposed:
- Data paths:

```text
/path/to/config
/path/to/data
```

---

## Prerequisites
What must exist *before* this can be installed.

- OS / firmware version
- Packages required
- Network prerequisites (VLANs, DNS, firewall)
- Credentials or certificates required

---

## Installation / Recreation
**This section must be sufficient to recreate the service from scratch.**

### Image / Package
```bash
# docker / podman pull …
```

### Configuration files
```bash
# mkdir /path
# curl / copy config
```

### Initial start
```bash
# docker run / podman run …
```

### Verify
- URL to check:
- CLI check:
- Expected output:

---

## Configuration
What is customized beyond defaults.

- Key config files
- Non-obvious settings
- Links to upstream docs
- Why these settings were chosen

---

## Backup
**This is non-negotiable.**

### What must be backed up
- Config:
- Data:
- Secrets:

### Backup method
```bash
# rsync / tar / script
```

### Backup location
- Local:
- Off-host:
- Frequency:

---

## Restore
How to recover **on a new system**.

1. Reinstall service (see Installation)
2. Restore files:
   ```bash
   # rsync back
   ```
3. Restart service
4. Verify functionality

---

## Operations
Day-to-day usage.

- Start / stop commands
- Upgrade procedure
- Log locations
- Health checks

---

## Security Notes
Anything security-relevant.

- Credentials stored where?
- Firewall rules
- VLAN isolation
- Known risks

---

## Failure Modes & Troubleshooting
What breaks, how it presents, and how to fix it.

| Symptom | Likely Cause | Fix |
|------|------------|-----|

---

## References
- Upstream docs:
- Git repos:
- Related wiki pages:
