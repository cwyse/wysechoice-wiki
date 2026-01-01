---
title: Network Services Overview
order: 10
---

# Network Services

This page provides a unified view of all **network-level services** running in the WyseChoice infrastructure.
Each service has a single canonical name, a dedicated documentation page, and a clear source of truth
(UI, CLI, or config-backed).

## Core Network Services

| Service | Provider | Role | Status | Where Configured | Documentation |
|-------|----------|------|--------|------------------|---------------|
| UDM DHCP | UniFi Dream Machine | DHCP for all VLANs | Active | UniFi Network (UI + dnsmasq) | [udm-dhcp](./udm-dhcp.md) |
| UDM DNS | UniFi Dream Machine | Default DNS + forwarding | Active | UniFi Network (UI) | [udm-dns](./udm-dns.md) |
| UDM Firewall | UniFi Dream Machine | Stateful firewall, VLAN isolation | Active | UniFi Network (UI) | [udm-firewall](./udm-firewall.md) |
| VLAN Routing | UniFi Dream Machine | Inter-VLAN routing | Active | UniFi Network (UI) | [vlans](../vlans.md) |

## Device & Inventory Services

| Service | Provider | Role | Status | Where Configured | Documentation |
|-------|----------|------|--------|------------------|---------------|
| Device Inventory | UniFi Network | Client + device tracking | Active | UniFi Network (UI) | [device-inventory](../device-inventory.md) |

## Optional / Deferred Services

| Service | Provider | Role | Status | Notes | Documentation |
|-------|----------|------|--------|-------|---------------|
| Pi-hole DNS | Pi-hole | Network-wide ad blocking | Disabled | To be rehomed off UDM | [pihole](./pihole.md) |
| ntopng | ntopng | Traffic analysis | Planned | External server required | [ntopng](./ntopng.md) |

## Conventions

- **Canonical naming:** service pages use lowercase kebab-case (e.g. `udm-dhcp.md`)
- **One service = one page**
- **Bidirectional links:** every service page links back here
- **Order is explicit** using front matter (`order:`)

