---
title: UDM DNS
order: 30
---

# UDM DNS Service

This page documents DNS behavior as implemented on the UniFi Dream Machine (UDM).

## Role
- Local DNS resolver for all VLANs
- Forwards upstream queries to ISP or configured external resolvers
- Integrates with DHCP for hostname registration

## Implementation
- Backed by **dnsmasq**
- Configuration generated dynamically by UniFi OS
- Not intended for manual modification

## Key Paths
- Leases: `/data/udapi-config/dnsmasq.lease`
- Runtime config: `/run/dnsmasq.conf` (generated)

## Notes
- Pi-hole documentation retained for future external DNS deployment
- Conditional forwarding handled internally by UDM

## Cross-links
- [UDM DHCP](./udm-dhcp.md)
- [Firewall](./udm-firewall.md)
- [VLAN Layout](../layout.md)
- [Device Inventory](../hardware/servers.md)

> Back to: [Network Services Overview](./overview.md)
