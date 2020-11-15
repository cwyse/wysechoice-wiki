---
title: Network Layout
description: Network diagram, information, and interconnections
published: true
date: 2020-11-15T00:05:17.348Z
tags: level1
editor: markdown
dateCreated: 2020-11-09T01:31:26.503Z
---

# WyseChoice Network

These subpages document the WyseChoice network.  It is a complicated network infrastructure that provides wireless access for users, streaming devices, and IOT devices. There are three access points in the house, each utilize different channels to minimize interference.  Wired access is available in the office and family room, via two switches and a router. 

## Network Diagrams
### Tabs {.tabset}
#### Miscellaneous
#### VLANs
![wysechoicevlans.png](/wysechoicevlans.png)
{.links-list}
## WiFi Access

The network has three separate SSIDs for specific purposes:

1. **WYSECHOICE** - Trusted access for human users
1. **WYSECHOICE_STREAMING** - Untrusted access for streaming devices
1. **WYSECHOICE_IOT** - Untrusted access for IOT devices

### Tabs {.tabset}

#### WYSECHOICE
This access point is for general users of the network.  It provides both 2G and 5G access.  It is a trusted network that can access any of the other internal networks.

TBD - More specific information
#### WYSECHOICE_STREAMING
The access point is intended for untrusted devices that may require high bandwidth support.  This would include devices like security cameras and movie streaming devices.  It is a high speed 5G access point.  As an untrusted access point, devices on this SSID are restricted from accessing the **WYSECHOICE** network.  
The intent of this access point is to group similar devices, to potentially use QoS support with the network to improve performance.

TBD - More specific information
#### WYSECHOICE_IOT
**WYSECHOICE_IOT** is mainly used for IOT devices.  Since the security on IOT devices can vary from vendor to vendor, it's hard to assure that a device's security won't be compromised.  By putting those devices on this isolated network, any unauthorized access to the device would not be able to acces the primary network, **WYSECHOICE**.
he intent is to isolate this network from **WYSECHOICE**, since the actually security on IOT devices can v

TBD - More specific information
{.links-list}

## Wired Access
Wired access is available via the Unifi Dream Machine router ports, a network switch in the office, and another switch in the family room.  All wired access is placed on the **WYSECHOICE_WIRED** VLAN, and has full access to the network.

The network cabling comes in at the office cable modem, then goes to the Unifi Dream Machine router.  Two router ports are utilized to run cabling to the access points in both the living room and family room.  

Ports are available at the router in the office, an 8-port switch in the office, and a 4-port switch in the family room.  One of the ports on the family room switch is utilized for family room access point.

## MACVLans

The network contains two MACVLans, one VLAN hosted on a Raspberry Pi 4 running Docker containers, and another on the router using Podman.  All containers in these MACVLans have their own MAC addresses and appear as if they were physically connected to the network.

> NOTE:  The untrusted networks should not have access to the MACVLans.  This should be updated…
{.is-warning}
