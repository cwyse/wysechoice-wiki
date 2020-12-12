---
title: Network Services
description: Reviews the existing services, their use, setup, and configuration
published: true
date: 2020-12-12T03:37:09.551Z
tags: level1
editor: markdown
dateCreated: 2020-11-09T02:33:13.649Z
---

# Standard Network Services
## Domain Name Service (DNS)

## Tabs {.tabset}

### Overview
The network uses a Pi-hole domain name server.  The Pi-hole server provides both DNS lookup and filtering.  It utilizes various lists of known ad web sites to prevent them from being accessed.  

This server runs as podman container on the UDM router.  Although it is hosted on the UDM router (192.168.1.1), it appears on the network with its own MAC address.  The container resides on VLAN 5, which is a MACVLan network using the UDM router as it's network interface.

#### Boot sequence

> <font color=green>UDM Linux steps in green</font>
{.is-info}

> <font color=blue>Unifi-os podman container steps in blue</font>
{.is-info}

> <font color=red>pihole podman container steps in red</font>
{.is-info}

1.  <font color=green>UDM boots Linux</font>
1.  <font color=green>UDM starts **unifi-os** podman container</font>
1.  <font color=blue>Unifi-os container starts re-installing cached deb packages from /data/dpkg-cache (<font color=green>/mnt/data/unifi-os/dpkg-cache</font>)</font>
1.  <font color=blue>Unifi-os container finds udm-boot package and re-installs it</font>
1.  <font color=blue>udm-boot installs on_boot.sh to /usr/share/udm-boot </font>
1.  <font color=blue>udm-boot installs udm-boot.service to /lib/systemd/system</font>
1.  <font color=blue>udm-boot post-install remote copies on_boot.sh to the host at <font color=green>/mnt/data/on_boot.sh</font> and creates <font color=green>/mnt/data/on_boot.d</font> directory if not present</font>
1.  <font color=blue>udm-boot post-install enables and starts udm-boot service</font>
1.  <font color=blue>udm-boot service uses ssh-proxy to execute <font color=green>/mnt/data/on_boot.sh</font></font>
1.  <font color=green>on_boot.sh searches and executes startup scripts found in /mnt/data/on_boot.d</font> 
1.  <font color=green>/mnt/data/on_boot.d/10-dns.sh is executed, creating 192.168.5.x MACVLan (using configuration from /mnt/data/podman/cni/20-dns.conflist), and starts p-hole podman container</font>
1.  <font color=blue>udm-boot service completes</font>
1.  <font color=red>pihole podman container starts DNS & administrative web server</font>

### Initial Setup
### Configuration
#### Provide data to Grafana (needs more clarification)
Get the WEBPASSWORD from /etc/pihole/setupVars.conf in the podman container:

WEBPASSWORD=c3c6db3026a6ddb15d603ddd2fe20521ea5656d3608e387a7637185b2867bb26

curl -ks "http://192.168.5.3/admin/api.php?overTimeData10mins&auth=c3c6db3026a6ddb15d603ddd2fe20521ea5656d3608e387a7637185b2867bb26"

#### Download and install whitelisted DNS names

https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt  => /etc/pihole/whitelist.txt on container.

root@pi:~# wget https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt

root@pi:~# while read -r line; do pihole -w $line; done <whitelist.txt

/pi-hole-pi_hole-teleporter_2020-10-24_14-15-20.tar.gz
### Backup
Backup and restore is currently manual through the pihole administration:
![piholebackup.png](/piholebackup.png)
[pi-hole-pi_hole-teleporter_2020-10-24_14-15-20.tar.gz](/pi-hole-pi_hole-teleporter_2020-10-24_14-15-20.tar.gz)

### Reference
https://github.com/boostchicken/udm-utilities/tree/master/on-boot-script

https://github.com/boostchicken/udm-utilities/tree/master/run-pihole

http://192.168.5.3/admin/queries.php

https://github.com/boostchicken/udm-utilities/blob/master/cni-plugins/20-dns.conflist

https://github.com/boostchicken/udm-utilities/blob/master/dns-common/on_boot.d/10-dns.sh
### Support Files
#### Located on UDM filesystem (not unifi-os container)
[10-dns.sh](/mnt/data/on_boot.d/10-dns.sh) - Pi-Hole configuration and startup script
[20-dns.conflist](/mnt/data/podman/cni/20-dns.conflist) - Configuration of 192.168.5.x MACVLAN for Pi-Hole
[pihole.sh](/pihole.sh) - Create and run container

## Domain Name Service (DNS)

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
10-dns.sh

20-dns.conflist

pihole.sh

## E-Mail
## Tabs {.tabset}

### Overview
Email addresses: chris.wyse@wysechoice.net, doris.wyse@wysechoice.net


### Initial Setup
### Configuration
The following flow diagram describes the Email configuration.  It uses three separate services - Cloudflare, ImproveMX, and Cox.  When an Email is sent from anywhere on the internet, the DNS service on Cloudflare for the wysechoice.net domain recognizes the Email address and forwards it to ImproveMX.  Cloudflare supports forwarding to a single Email address.  ImproveMX provides Email forwarding for multiple Email addresses in a domain.  The Email is forwarded to one of two servers on ImproveMX, which determine the final destination address and server at cox.net.  Changing Email service providers only requires modification of the ImproveMX records to point to the new servers.  The wysechoice.net Email addresses remain unchanged, regardless of provider.

![wysechoiceemail.png](/wysechoiceemail.png)

### Backup
TBD
### Reference
TBD
### Support Files
TBD

## Firewall
### Overview
The network uses a Pi-hole domain name server.  The Pi-hole server provides both DNS lookup and filtering.  It utilizes various lists of known ad web sites to prevent them from being accessed.  

This server runs as podman container on the UDM router.  Although it is hosted on the UDM router (192.168.1.1), it appears on the network with its own MAC address.  The container resides on VLAN 5, which is a MACVLan network using the UDM router as it's network interface.

### Initial Setup
### Configuration
### Backup
### Reference

### Support Files


