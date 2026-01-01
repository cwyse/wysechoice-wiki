---
title: UDM DHCP Service
description: DHCP implementation on the UniFi Dream Machine (UDM), including dnsmasq behavior, lease storage, and CLI inspection.
published: true
tags:
  - network
  - dhcp
  - udm
  - unifi
editor: markdown
---

# UDM DHCP Service

This page documents how DHCP is implemented on the **UniFi Dream Machine (UDM)**, including the underlying dnsmasq service, where lease data is stored, and how to inspect and troubleshoot DHCP behavior from the command line.

The goal is to describe **how DHCP actually works on the UDM**, not just how it is configured via the UniFi UI.

---

## Related Network Documentation

- **[VLAN Architecture](/network/layout)**  
  Defines the VLANs and IPv4 subnets that DHCP serves.

- **[DNS Services](/network/dns)**  
  Describes name resolution behavior for DHCP-assigned clients, including split DNS and Pi-hole integration.

- **[Network Device Inventory](/network/hardware)**  
  Maps DHCP leases to physical and virtual devices on the network.

---

## High-Level Architecture

On the UDM:

- DHCP is provided by **dnsmasq**
- dnsmasq is **managed by UniFi OS**, not user-editable config files
- Configuration is generated dynamically from UniFi Network settings
- Manual edits to dnsmasq config files are **not persistent**

Key characteristics:

- One dnsmasq instance serves **all VLANs**
- DHCP scopes are generated per-network (VLAN)
- Static mappings come from UniFi controller configuration

---

## DHCP Lease Storage

Active DHCP leases are stored in:

```
/data/udapi-config/dnsmasq.lease
```

This file is authoritative for:
- Active IPv4 leases
- Hostnames (when provided)
- MAC ↔ IP mappings
- Lease expiration times (epoch seconds)

### Lease File Format

Example entry:

```
1767203035 80:2a:a8:86:fc:98 192.168.1.31 UAP-AC-Lite-FamilyRoom *
```

Fields:

1. Lease expiration (epoch time)
2. MAC address
3. IPv4 address
4. Hostname (or `*`)
5. Client ID (optional)

---

## Viewing Active DHCP Leases

### Raw lease file

```bash
cat /data/udapi-config/dnsmasq.lease
```

### Human-readable formatting

```bash
awk '{ printf "%-17s  %s  %s\n", $2, $3, $4 }' /data/udapi-config/dnsmasq.lease
```

### Show only currently active (non-expired) leases

```bash
awk -v now=$(date +%s) '$1 > now { printf "%-17s  %s  %s\n", $2, $3, $4 }' \
  /data/udapi-config/dnsmasq.lease
```

This is the most reliable way to see what the UDM believes is currently online.

---

## Static DHCP Mappings

Static DHCP assignments are **not stored directly in dnsmasq config files**.

Instead:
- They are defined in the UniFi Network UI
- Stored internally by UniFi OS
- Rendered dynamically into dnsmasq at runtime

As a result:
- `/run/dnsmasq.conf.d/` is not user-accessible
- Static mappings do not persist if manually injected
- Reboots or provisioning overwrite manual changes

---

## dnsmasq Configuration Files

On the UDM:

- dnsmasq is launched and managed internally
- Traditional locations such as:

```
/etc/dnsmasq.conf
/run/dnsmasq.conf.d/
```

are **not present or not user-editable**

This is intentional and enforced by UniFi OS.

---

## Common Misconceptions

### “dnsmasq logs should be in /var/log”

On the UDM:
- dnsmasq logging is controlled by UniFi OS
- Logs may not appear in `/var/log/messages`
- DHCP behavior should be inspected via the lease file instead

---

### “Pi-hole controls DHCP”

Unless explicitly configured:
- The UDM remains the DHCP server
- Pi-hole only handles DNS
- DHCP lease visibility in Pi-hole depends on conditional forwarding

---

## Operational Notes

- DHCP continues to function even if the UniFi UI is unreachable
- Lease state is preserved across reboots
- UniFi UI may lag behind real-time lease state

For authoritative status, always inspect:

```
/data/udapi-config/dnsmasq.lease
```

---

## Summary

- DHCP on the UDM is provided by **dnsmasq**
- UniFi OS dynamically generates all configuration
- The lease file is the ground truth
- Manual dnsmasq edits are unsupported and non-persistent
- CLI inspection is essential for accurate troubleshooting
