---
title: VLAN Reference
order: 10
---

# VLAN Reference

Canonical VLAN definitions for WyseChoice network.

| VLAN | Subnet | Purpose |
|-----:|--------|---------|
| 1 | 192.168.1.0/24 | Infrastructure |
| 110 | 192.168.110.0/24 | Trusted |
| 120 | 192.168.120.0/24 | User |
| 130 | 192.168.130.0/24 | IoT |
| 140 | 192.168.140.0/24 | Guest |
| 150 | 192.168.150.0/24 | Management |

## Notes
- DHCP provided by UDM on all VLANs
- Firewall enforces inter-VLAN policy

> Referenced by all network services
