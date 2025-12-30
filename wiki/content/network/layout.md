---
title: Network Layout
description: Network diagram, information, and interconnections
published: true
date: 2021-01-31T23:29:16.900Z
tags: level1
editor: markdown
dateCreated: 2020-11-09T01:31:26.503Z
---

# WyseChoice Network

These subpages document the WyseChoice network.  It is a complicated network infrastructure that provides wireless access for users, streaming devices, and IOT devices. There are three access points in the house, each utilize different channels to minimize interference.  Wired access is available in the office and family room, via two switches and a router. 

## Network Diagrams
### Tabs {.tabset}
#### VLANs
![wysechoicevlans.png](/wysechoicevlans.png)

#### D-Link DGS-1100-08
D-Link managed switch assigned to 192.168.1.15.
Link Aggregation configurated on ports 7 & 8, connected to QNAP NAS.
SNMP v2c Enabled
Defaults for other settings
Located in office
[DGS-1100 Series EasySmart Switch user Manual B1 v1.0](/dgs-1100-05_05pd_08_08p_revb_manual_v2.21_ww_en.pdf)

#### Ubiquiti USW-Flex-Mini-FamilyRoom
Ubiquiti USW-Flex-Mini switch assigned to 192.168.1.6
Uplink to UDM
Downlinks to Family Room AP & Toshiba TV
Located in Family Room

#### Ubiquiti USW-Flex-Mini-LivingRoom
Ubiquiti USW-Flex-Mini switch assigned to 192.168.1.7
Uplink to UDM
Downlinks to Living Room AP & Fire TV
Located in Living Room

#### Email
![wysechoiceemail.png](/wysechoiceemail.png)
#### Server Addresses
##### UniFi Dream Machine

```Model:       UniFi Dream Machine
Version:     1.5.6.2150
MAC Address: 74:83:c2:d6:c9:1b
IP Address:  68.9.160.37
Hostname:    DreamMachine
Name: dreammachine.wysechoice.net (Planned)
Firmware: v1.5.6
MAC Address:
Local IP Address: 192.168.1.1
```

##### Networks:

###### WYSECHOICE_WIRED (VLAN 1 - Default)

```192.168.1.1/24
DHCP: 192.168.1.6 - 192.168.1.254
DNS: 8.8.4.4, 8.8.8.8, 10.0.0.1
```

###### PI-HOLE (VLAN 5)

```192.168.5.1/24
DHCP: 192.168.5.6 - 192.168.1.254
DNS: 8.8.4.4, 8.8.8.8, 10.0.0.1
```

###### DockerNet (VLAN 40)

```192.168.40.1/24
DHCP: N/A
DNS: N/A
```

##### Wireless Networks:

Wireless Channels: 1 Low (2G), 48 medium VHT40 (5G)
###### WYSECHOICE (VLAN 10)

```192.168.10.1/24
DHCP: 192.168.10.6 - 192.168.10.254
DNS: 192.168.5.3
```

###### WYSECHOICE_IOT (VLAN 20)

```192.168.20.1/24
DHCP: 192.168.20.6 - 192.168.20.254
DNS: 192.168.5.3
```

###### WYSECHOICE_STREAMING (VLAN 30)

```192.168.30.1/24
DHCP: 192.168.30.6-192.168.30.254
DNS: 192.168.5.3
```


##### UniFi AP-AC-Lite (9/12/20)

```Model:       UAP-AC-Lite
Version:     5.35.0.12205
MAC Address: 80:2a:a8:86:fc:98
IP Address:  192.168.1.29
Hostname:    FamilyRoomAP
Wireless Channels: 11 Low (2G), 36 Medium VHT80 (5G)
```

##### Unifi AP-AC-Lite (9/12/20)

```Model:       UAP-AC-Lite
Version:     5.35.0.12205
MAC Address: 80:2a:a8:86:fb:37
IP Address:  192.168.1.69
Hostname:    LivingRoomAP
Wireless Channels: 6 Low (2G), 40 Medium VHT40 (5G)
```

#### PiHole (Old)
![piholediagram.png](/piholediagram.png)
{.links-list}

## WiFi Access

The network has three separate SSIDs for specific purposes:

1. **WYSECHOICE** - Trusted access for human users
1. **WYSECHOICE_STREAMING** - Untrusted access for streaming devices
1. **WYSECHOICE_IOT** - Untrusted access for IOT devices

Each of the SSIDs is on their own VLAN to allow customization of the group's support.  The primary customization is to only allow the **WYSECHOICE** VLAN to have access to the full network.  The other VLANs may be running proprietary software, that could be compromised, so they are prevented from reaching the **WYSECHOICE** VLAN.  The **WYSECHOICE_STREAMING**  VLAN was separated to potentially prioritize traffic for a better streaming experience.   Currently, it is differentiated by only supporting 5G access, and  **WYSECHOICE_IOT**  is limited to 2G.

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
