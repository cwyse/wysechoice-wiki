---
title: Network Service Flow
path: network/architecture/flow
tags: [dhcp, vlan, firewall, udm]
---

# DHCP → VLAN → Firewall Flow

## High-level Flow

```
[ Client Device ]
        |
        | DHCP DISCOVER
        v
[ dnsmasq (UDM DHCP) ]
        |
        | Lease (IP + Subnet)
        v
[ VLAN Assignment ]
        |
        | iptables MARK (mangle table)
        v
[ Firewall Policy Chains ]
        |
        | ACCEPT / DROP / NAT
        v
[ WAN / LAN Routing ]
```

## Cross-links

- [[udm-dhcp]]
- [[vlan-reference]]
- [[udm-firewall]]
