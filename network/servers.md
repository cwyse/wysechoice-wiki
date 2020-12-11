---
title: Network Servers
description: Physical network servers
published: true
date: 2020-12-11T15:29:09.967Z
tags: 
editor: markdown
dateCreated: 2020-12-11T12:40:15.387Z
---

# Dream Machine

- Dream Machine
  - Base Configuration
  - Extensions
- RPi4
  - Base OS
  - Dockernet
  - Postgres
  - Ghini
  - Wiki.js
- QNAP
  - Base Configuration
  - Apps
- Host
  - Associated Apps
    - Portainer
    - PgAdmin4





# Dream Machine

## Tabs {.tabset}

### Overview
The network uses a Pi-hole domain name server.  The Pi-hole server provides both DNS lookup and filtering.  It utilizes various lists of known ad web sites to prevent them from being accessed.  

This server runs as podman container on the UDM router.  Although it is hosted on the UDM router (192.168.1.1), it appears on the network with its own MAC address.  The container resides on VLAN 5, which is a MACVLan network using the UDM router as it's network interface.

### Initial Setup
### Configuration
### Backup
### Reference
https://github.com/boostchicken/udm-utilities/tree/master/on-boot-script

https://github.com/boostchicken/udm-utilities/tree/master/run-pihole

http://192.168.5.3/admin/queries.php

https://github.com/boostchicken/udm-utilities/blob/master/cni-plugins/20-dns.conflist

https://github.com/boostchicken/udm-utilities/blob/master/dns-common/on_boot.d/10-dns.sh
### Support Files
#### Browse the Unifi REST API
https://github.com/Art-of-WiFi/UniFi-API-browser

https://github.com/Art-of-WiFi/UniFi-API-client

https://community.ui.com/questions/UniFi-API-browser-tool-updates-and-discussion/30927150-dd44-40f7-96c0-9fbbfc673fb3?page=26
#### Download and extract support information
openssl enc -d -in "unifi-20190707-2225.supp" -out "unifi-20190707-2225.supp.tmp" -aes-128-cbc -K 626379616e676b6d6c756f686d617273 -iv 75626e74656e74657270726973656170 -nosalt -nopad
zip -FF "unifi-20190707-2225.supp.tmp" --out supp
Is this a single-disk archive? (y/n): y

Reference: https://community.ui.com/questions/Extracting-logs-from-the-support-file/9cae86af-b73a-4a1c-8d41-4ba4b0ab45ad
