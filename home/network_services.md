---
title: Network Services
description: Reviews the existing services, their use, setup, and configuration
published: true
date: 2021-02-01T01:53:52.605Z
tags: level1
editor: markdown
dateCreated: 2020-11-09T02:33:13.649Z
---

# Standard Network Services
## Simple Network Management Protocol (SNMP)

## Tabs {.tabset}

### Overview
SNMP allows monitoring of network devices.  The LibreNMS application is configured with the SNMP enabled devices.

### UDM SNMP Configuration
The UDM configuration is not fully integrated with the firmware yet, and requires some manual configuration.  The following commands were found on the Ubiquiti forums:

1. SSH to UDM-Pro
2. Escalate to the Linux shell with :
`unifi-os shell`
3. sudo apt-get -y install snmp snmpd libsnmp-dev vim
4. sudo net-snmp-config --create-snmpv3-user -ro -A password -x password -X AES -A SHA snmpv3
Edit the SNMP configuration :
5. vi /etc/snmp/snmpd.conf
Add the following line:
`agentAddress udp:192.168.1.1:161`
6. systemctl start snmpd

Note that this configuration will probably not survive a firmware update.  In addition to this configuration I enabled SNMP v1, v2c, & v3 in the GUI, and set the user and password to match this configuration (snmpv3/<store securely outside the repository>).

The configuration can be tested by running:
`snmpwalk -v3 -l authPriv -u snmpv3 -a SHA -A <store securely outside the repository> -x AES -X <store securely outside the repository> udp:192.168.1.1:161 .`
from both the UDM and an external host.

SNMP Tutorial: http://www.net-snmp.org/tutorial/tutorial-5/demon/snmpd.html
### QNAP NAS SNMP Configuration
Login to the QNAP NAS, open the ControlPanel, and select 'Network & File Services' on the left hand side.  Next to that, select 'SNMP'.  SNMP should be enabled, v3, user 'admin', use Authentication protocol HMAC-MD5, and password <store securely outside the repository>.

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

The Pi-Hole DNS server currently runs on the Ubiquiti Dream Machine router, in a podman container.  The following steps are required for the initial configuration and setup.

1.  Install the UDM-Boot package
     - The UDM-Boot package is available on GitHub:
     https://raw.githubusercontent.com/boostchicken/udm-utilities/master/on-boot-script/packages/udm-boot_1.0.2_all.deb
     - The source code is available in the on-boot-script dictory of the repository
1.   On your controller, make a Corporate network with no DHCP server and give it a VLAN. For this example we are using VLAN 5.
1.  Install the pi-hole podman container on the UDM
     - Copy 20-dns.conflist to /mnt/data/podman/cni. This will create your podman macvlan network
     - Copy 10-dns.sh to /mnt/data/on_boot.d and update its values to reflect your environment
     - Execute /mnt/data/on_boot.d/10-dns.sh     
1.  Run the pihole docker container, be sure to make the directories for your persistent pihole configuration. They are mounted as volumes in the command below.

    ```
    podman run -d --network dns --restart always \
    --name pihole \
    -e TZ="America/Los Angeles" \
    -v "/mnt/data/etc-pihole/:/etc/pihole/" \
    -v "/mnt/data/pihole/etc-dnsmasq.d/:/etc/dnsmasq.d/" \
    --dns=127.0.0.1 --dns=1.1.1.1 \
    --hostname pi.hole \
    -e VIRTUAL_HOST="pi.hole" \
    -e PROXY_LOCATION="pi.hole" \
    -e ServerIP="10.0.5.3" \
    -e IPv6="False" \
    pihole/pihole:latest
    ```
    The below errors are expected and acceptable:

    ```
    ERRO[0022] unable to get systemd connection to add healthchecks: dial unix /run/systemd/private: connect: no such file or directory
    ERRO[0022] unable to get systemd connection to start healthchecks: dial unix /run/systemd/private: connect: no such file or directory
    ```

1.  Set pihole password
    `podman exec -it pihole pihole -a -p YOURNEWPASSHERE`
    
1.  Update your DNS Servers to 192.168.5.3 (or your custom ip) in all your DHCP configs.    
1.  Configure a cron job to monitor the container and restart if necessary
    - Copy the following script to /usr/local/bin/dns_restart.sh on a host computer
    ```
    #!/usr/bin/env bash

    DNS_SERVER=192.168.5.3
    UDM_ROUTER=192.168.1.1
    PASSWORD="&847&XLXXbxY"

    # If the router is running
    if ping -c 1 ${UDM_ROUTER} > /dev/null 2>&1; then
        # If the DNS server is not working
        if ! nslookup ${UDM_ROUTER} ${DNS_SERVER} > /dev/null 2>&1; then
            sshpass -p ${PASSWORD} ssh -t root@${UDM_ROUTER} "podman stop pihole"
            sshpass -p ${PASSWORD} ssh -t root@${UDM_ROUTER} "podman start pihole"
            # May want to re-load whitelists and blacklists?
        fi
    fi
    ```
    - `chmod 755 /usr/local/bin/dns_restart.sh`
    - `crontab -e` -> `* * * * * /usr/local/bin/dns_restart.sh`

### Maintenance

#### UDM Password Change
The dns_restarts.sh script needs to be updated whenever the UDM root password changes

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
[/mnt/data/on_boot.d/10-dns.sh](/10-dns.sh) - Pi-Hole configuration and startup script
[/mnt/data/podman/cni/20-dns.conflist](/20-dns.conflist) - Configuration of 192.168.5.x MACVLAN for Pi-Hole
[pihole.sh](/pihole.sh) - Create and run container

#### Located on DNS monitoring host
[/usr/local/bin/dns_restart.sh](/dns_restart.sh) - Script to monitor and restart pihole container if necessary

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

## DockerNet.\<subnet>
## Tabs {.tabset}

### Overview
DockerNet is a MACVLAN network for docker containers.  It requires configuration on the Docker host machine to create the network, and additional configuration on the router to access the network remotely.  The configuration allows new docker images to appear on the network as individual devices with their own MAC addresses. 

The intent of is to have an easy way to create a network of Docker containers running on a device.  These containers would have their own MAC addresses and look new devices added to the network.  The current implementation uses a VLAN for each new docker network.

### Initial Setup
The primary reference used for creating this configuration is [Using Docker MACVLAN Networks](https://blog.oddbit.com/post/2018-03-12-using-docker-macvlan-networks/).  The configuration had some issues with the checksum value in the packets being received.  Unfortunately, I didn't document it well, but the solution is to disable the checksum offloading in eth0-shim.  The other unusual required setting is that the host interface needs to be in promiscuous mode.

Creation of the DockerNet MACVLAN requires configuration on the UDM server to support routing to the DockerNet server (192.168.1.2) and additional configuration on the host machine.

#### Required Input parameters:
- Host IP:  This is the address of the host interface, and must be statically assigned.
- Host_GW:  This is the gateway used by the host interface
- HOST_SHIM: Address of the secondary shim interface, and must be statically assigned.
- MAC_ADDR: To prevent address overlap, assign the HOST_SHIM an address using the Docker prefix followed by the assigned IP address.  For example, the Docker prefix is '02:00', and the HOST_SHIM address is 192.168.1.120 (corresponding to 0xC0.0xA8.0x01.0x78).  The MAC_ADDR to use would be '02:00:C0:A8:01:78'.
- HOST_IF:  Name of the host interface (usually eth0)
- IS_WIFI:  Unsupported - set to 0

> NOTE: The script contains some support to bridge across Wifi, but bridging technique is different and more complicated.  It involves additional software as well as configuration changes.  The WiFi support is included in the script for potential future use, but is not used.
{.is-info}


#### Creation Steps:

1. Remove the DockerNet MACVLAN network if it exists
1. Create a virtual interface (eth0-shim) to act as a bridge between the MACVLAN and the host
1. Create /etc/network/interfaced.d/eth0-shim to persist the configuration across boots
1. Dynamically configure eth0-shim on the running system (NOTE: potential bug - address is not set to 192.168.1.3 explicitly)
1. Eth0-shim configuration include bridging all 192.168.40.x/24 containers from 192.168.1.x/24.
1. Creates DockerNet, reserving 192.168.40.1 for the gateway, and 192.168.40.2 for eth0-shim.

Currently, DockerNet is hosted on the Raspberry PI 4 (pi-hole).  It can be created by using the following script function after configuring the routing.  DockerNet is created once, then the network is used by the containers on the Raspberry PI 4. 

The following script function creates the DockerNet on the PI:

```
# 
# create_dockernet:
# 
#   This function creates the 'dockernet' MACVLAN network, using subnet 192.168.40.0/24.
#   This allows each docker container to appear to be connected to the physical network, 
#   with it's own MAC address.
#                                                                                                                       
function create_dockernet()
{
  # Reference:
  # https://blog.oddbit.com/post/2018-03-12-using-docker-macvlan-networks/

  # Routing requirements:
  #    1. Docker assigned addresses should not be used by the router
  #    2. Routes need to be created to access the subnet residing on the docker host
  #    3. Secondary MACVLAN (eth0-shim) used to connect containers to host
  #
  #############################################
  #
  #  The following routes must be configured
  #  on the router to connect to the containers 
  #  in the 192.168.40.0/24 subnet . 
  #
  #############################################
  #  192.168.40.0/24 dev br40 scope link  src 192.168.40.1 
  #  192.168.40.0/31 dev br0  metric 1 
  #  192.168.40.2 via 192.168.1.3 dev br0  metric 1 
  #  192.168.40.4/30 dev br0  metric 1 
  #  192.168.40.8/29 dev br0  metric 1 
  #  192.168.40.16/28 dev br0  metric 1 
  #  192.168.40.32/27 dev br0  metric 1 
  #  192.168.40.64/26 dev br0  metric 1 
  #  192.168.40.128/25 dev br0  metric 1 
  ############################################

  printf "Creating dockernet. "

  # Start from scratch
  if docker network ls | grep  dockernet >/dev/null 2>&1; then
    docker network remove dockernet
  fi

  #
  # Create dockernet corresponding to same definition in router
  #   Uses router DHCP settings which are currently allocating 192.168.40.128 - 192.168.40.255 (192.168.40.128/25)
  #

  # Create eth0-shim MACVLan interface for communication between the host
  #  and the MACVlan network
  sudo rm -f /etc/network/interfaces.d/eth0-shim || true
  SHIM_CFG=$(mktemp)

  # Public MAC addresses use these ranges:
  #   x2-xx-xx-xx-xx-xx
  #   x6-xx-xx-xx-xx-xx
  #   xA-xx-xx-xx-xx-xx
  #   xE-xx-xx-xx-xx-xx
  #
  # The range selected was arbitrary, x2-xx-xx-xx-xx-xx.  The
  # last four segments are mapped to the IP address to prevent
  # internal network conflicts.
  #                                                                                                                     
  MAC_ADDR="02:00:C0:A8:01:03"

  #
  # Make ethtool is installed to provide support to disable
  # checksum offloading.
  #
  echo sudo apt install -y ethtool
  sudo apt install -y ethtool || true

  #
  # Create the MACVlan bridge configuration file for the host,
  # to make the interface persistent across boots.  Also, if the
  # interface is not defined, issue the network commands to create
  # the interface immediately.
  #
  sudo cat <<***REMOVED*** >${SHIM_CFG}
auto eth0-shim
iface eth0-shim inet static
 address 192.168.1.3
 pre-up ip link add eth0-shim link eth0 type macvlan mode bridge
 up ip addr add 192.168.40.2/32 dev eth0-shim                                  
 up ip link set eth0-shim address ${MAC_ADDR} up
 up ip route add 192.168.40.0/31 dev eth0-shim
 up ip route add 192.168.40.3/32 dev eth0-shim
 up ip route add 192.168.40.4/30 dev eth0-shim
 up ip route add 192.168.40.8/29 dev eth0-shim
 up ip route add 192.168.40.16/28 dev eth0-shim
 up ip route add 192.168.40.32/27 dev eth0-shim
 up ip route add 192.168.40.64/26 dev eth0-shim
 up ip route add 192.168.40.128/25 dev eth0-shim
 offload-tso  off
***REMOVED***
 sudo mv ${SHIM_CFG} /etc/network/interfaces.d/eth0-shim

 if ! ip addr show eth0-shim >/dev/null 2>&1; then                                                                     
    # Add a shim ethernet to act as a bridge to the host machine
    sudo ip link add eth0-shim link eth0 type macvlan mode bridge
    sudo ip addr add 192.168.40.2/32 dev eth0-shim
    sudo ip link set eth0-shim address ${MAC_ADDR} up

    # Route all the addresses through the shim
    sudo ip route add 192.168.40.0/31 dev eth0-shim
    sudo ip route add 192.168.40.3/32 dev eth0-shim
    sudo ip route add 192.168.40.4/30 dev eth0-shim
    sudo ip route add 192.168.40.8/29 dev eth0-shim
    sudo ip route add 192.168.40.16/28 dev eth0-shim
    sudo ip route add 192.168.40.32/27 dev eth0-shim
    sudo ip route add 192.168.40.64/26 dev eth0-shim
    sudo ip route add 192.168.40.128/25 dev eth0-shim
  fi
  sudo ethtool -K eth0-shim tso off || true

  #
  # Enable promiscuous mode for eth0                                                                                                                                           
  #   The parent interface (eth0) for the MACVLAN must be
  #   in promiscuous mode to allow multiple VLANs on the interface
  #
  sudo rm -f /etc/network/interfaces.d/eth0 || true
  ETH0_CFG=$(mktemp)
  sudo cat <<***REMOVED*** >${ETH0_CFG}
auto eth0
iface eth0 inet static 
  address 192.168.1.2/24
  gateway 192.168.1.1
  up /sbin/ip -4 link set eth0 promisc on
  down /sbin/ip link set eth0 promisc off
  down /sbin/ip link set eth0 down
***REMOVED***
  sudo mv ${ETH_CFG} /etc/network/interfaces.d/eth0

  sudo ip link set eth0 promisc on

  # Use the MACVLan driver - allowing docker containers to appear as if physically connected to network
  DOCKER_OPTIONS="  -d macvlan"
  # Specify the physical interface to use
  DOCKER_OPTIONS+=" -o parent=eth0"
  # Set the subnet to use for the network.  The router will also define this subnet as a VLAN.
  DOCKER_OPTIONS+=" --subnet 192.168.40.0/24"           
  # Define the external gateway machine.  Ubiquiti provides this virtual gateway in the router.
  DOCKER_OPTIONS+=" --gateway 192.168.40.1"             
  # Define the IP range for containers that don't specify an IP address
  DOCKER_OPTIONS+=" --ip-range 192.168.40.128/25"       
  # Reserve an address to use for the MACVLAN bridge (eth0-shim) communication with host
  DOCKER_OPTIONS+=" --aux-address "'host=192.168.40.2'
  docker network create ${DOCKER_OPTIONS} dockernet
 
  printf "Done.\n"
}
```

### Configuration
In addition to the host configuration, the router must also be configured to allow traffic to get to DockerNet.  The configuration and routing is shown in the following images used to configure the Ubiquiti Dream Machine:
![dockernet.png](/dockernet.png)![rsync.png](/rsync.png)[2019-09-26-raspbian-buster.info](/2019-09-26-raspbian-buster.info)[fwrules.txt](/data/fwrules.txt)
![dockernet.png](/dockernet.png)
![dockernetrouting.png](/dockernetrouting.png)
![dockernetfirewall.png](/dockernetfirewall.png)

### Backup
The website data is continually stored in two places, the postgres database and a git repository.  Both are updated whenever a change is made.

The postgres server runs in a docker image on the same host machine.  The database parameters used for the connection are given below:
- DB Type: postgres
- DB Host: postgres-9.5 (Name of docker container)
- DB Port: 5432
- DB Name: wiki
- DB User: wikijs
- DB Password: wikijsrocks

The postgres data is dumped out every 3 days and stored on the NAS (192.168.1.8).  The backup is performed on from the NAS.  It requires the rsyncd daemon to be running.  It executes the following command on the docker host:
```
docker exec postgres-9.5 pg_dump wiki -U wikijs -F c > ~/wikibackup.dump
```
### Reference
TBD
### Support Files
TBD

## Firewall
## Tabs {.tabset}

### Overview


### Initial Setup
### Configuration


### Backup
TBD
### Reference
TBD
### Support Files
TBD



