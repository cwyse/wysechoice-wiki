---
title: Unifi Dream Machine Router
description: All aspects of maintenance for the Unifi Dream Machine router configuration
published: true
date: 2023-03-05T21:41:03.367Z
tags: 
editor: markdown
dateCreated: 2023-03-05T19:10:34.928Z
---

# UDM Route Configuration & Maintenance

## UDM Base configuration
### [General](/upd_02_23/udm/udm_general)
General overview of the backup and restore of a UDM configuration.  

### [Backup](/upd_02_23/udm/udm_backup)
Configure and create backups of the Unifi managed configuration data (custom configuration to support running of PiHole and other apps is handled separately).

### [Restore](/upd_02_23/udm/udm_restore)
Restore the configuration if the hard disk has failed.

## UDM Services

### [UDM Boot Script](/upd_02_23/udm/boot)
This service allows all other services to function by running a oot script at router startup.

### [Domain Name Service](/upd_02_23/udm/dns)
All information relating to the domain services used by the system.

### [Multicast Relay](/upd_02_23/udm/multicast)
Support mDNS local name resolution.

### [RSync](/upd_02_23/udm/rsync)
RSync client to backup UDM data.

### [Podman](/upd_02_23/udm/podman)
Install and update podman tool, which is no longer used in recent UDM firmware.

### [Container Common](/upd_02_23/udm/common)
Common configuration that applies to all UDM containers.

### [Container Network Interface](/upd_02_23/udm/cni)
Network configuration information for the Podman containers.

### [SSH](/upd_02_23/udm/ssh)
Add an SSH key to the UDM that persists across reboots.

### [Firewall updates](/upd_02_23/udm/firewall)
Backup the port forwarding used by the UDM.

### [Boot Script](/upd_02_23/udm/bootscript)
Initial boot script support.

### [Reverse Proxy](/upd_02_23/udm/reverseproxy)
Support simple reverse proxy to avoid entering website port numbers.

### [File Server](/upd_02_23/udm/fileserver)
Lightweight broser based file server.  Primarily used to ensure that referenced UDM configuration files are up to date.








