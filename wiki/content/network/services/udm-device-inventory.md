---
title: UDM Device Inventory
path: network/services/device-inventory
tags: [udm, inventory, dhcp, dnsmasq]
---

# UDM Device Inventory

This service derives an authoritative device inventory directly from the UDM DHCP lease database
(`/data/udapi-config/dnsmasq.lease`). It avoids controller-side drift and reflects **actual active devices**.

## Data Source

- File: `/data/udapi-config/dnsmasq.lease`
- Owner: `root`
- Updated by: `dnsmasq` (UDM internal DHCP service)

Each IPv4 lease line is:

```
<expiry_epoch> <mac> <ip> <hostname> <client-id>
```

IPv6 leases follow after the `duid` marker.

## Canonical Inventory Script

```bash
awk 'NF>=4 && $2 ~ /:/ {
  printf "%-17s %-15s %s\n", $2, $3, $4
}' /data/udapi-config/dnsmasq.lease
```

### Active-only devices

```bash
awk -v now=$(date +%s) '$1 > now && $2 ~ /:/ {
  printf "%-17s %-15s %s\n", $2, $3, $4
}' /data/udapi-config/dnsmasq.lease
```

## Inventory Fields

| Field | Source | Notes |
|---|---|---|
| MAC | dnsmasq | Stable hardware identifier |
| IP | dnsmasq | VLAN-scoped |
| Hostname | dnsmasq | Empty for many IoT devices |
| VLAN | Derived | From subnet mapping |
| Role | Manual | Switch / AP / Client / Server |

## VLAN Derivation

| Subnet | VLAN |
|---|---|
| 192.168.1.0/24 | LAN |
| 192.168.110.0/24 | Mgmt |
| 192.168.120.0/24 | Clients |
| 192.168.130.0/24 | IoT |

## Output Targets

- Markdown table (Wiki.js)
- CSV (external audit)
- Git-tracked snapshot

## Cross-links

- [[udm-dhcp]]
- [[vlan-reference]]
- [[udm-firewall]]
