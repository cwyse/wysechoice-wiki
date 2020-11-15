---
title: Network Devices
description: Network device information
published: true
date: 2020-11-15T09:41:06.367Z
tags: 
editor: markdown
dateCreated: 2020-11-13T03:04:49.791Z
---

# Primary Device Information

The following tables list information on the primary devices on the network that other devices are dependent on.

<br>

### Tabs {.tabset}

#### Routers & APs
The routers provide both wired and wireless internet access.  Each access point provides the same set of SSIDs - WYSECHOICE, WYSECHOICE_IOT, andWYSECHOICE_STREAMING.  Only the WYSECHOICE access point is permitted to access the others access point VLANs.  WYSECHOICE is intended for devices used by people that will be aware of security breaches.  Unmonitored devices are purposely separated to prevent unauthorized access.
<br>
<figure class="table">
  <table style="background-color:rgb(255, 255, 255);">
    <thead>
      <tr>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Name</th>
        <th>Hostname</th>
        <th>Device Type</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Address</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">MAC Address</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Ports</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Dream Machine</td>
        <td>udm</td>
        <td>UniFi Dream Machine</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.1.1</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">74:83:c2:d6:c9:1b</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">443, 22</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Unifi Dream Machine</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Family Room AP</td>
        <td>&nbsp;</td>
        <td>UniFi AP-AC-Lite</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.1.29</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">80:2A:A8:86:FC:98</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">22</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Unifi AP-AC-Lite</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Living Room AP</td>
        <td>&nbsp;</td>
        <td>UniFi AP-AC-Lite</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.1.69</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">80:2A:A8:86:FB:37</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">22</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Unifi AP-AC-Lite</td>
      </tr>
    </tbody>
  </table>
</figure>

#### Servers
The servers on the network will be monitored using the network administration tools.  These are intended to be online all the time.
<br>

<figure class="table">
  <table style="background-color:rgb(255, 255, 255);">
    <thead>
      <tr>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">&nbsp;</th>
        <th>Hostname</th>
        <th>Device Type</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Address</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Host Machine</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">MAC Address</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Ports</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">rpi4</td>
        <td>&nbsp;</td>
        <td>Raspberry Pi 4 Model B Rev 1.1</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.1.2</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">-</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">DC:A6:32:24:E4:C3</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">22</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Raspberry PI 4, DockerNet, Postgres &amp; Caddy Server</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">qnap</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.1.8/9</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">-</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">24:5E:BE:13:00:FD/FE</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">8084</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">NAS File Server</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">pi-hole</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.5.3</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">DreamMachine</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">6A:EB:06:85:A5:B5</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">53,80</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Pi-Hole DNS Server, running in MACVLAN podman container on Dream Machine</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">wiki</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.40.128</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">rpi4</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">02:42:c0:a8:28:80</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">3000</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Wiki.js server</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">postgres</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.40.30</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">rpi4</td>
        <td colspan="2" style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">02:42:C0:A8:28:1E</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Postgres database server (wiki, ghini)</td>
      </tr>
    </tbody>
  </table>
</figure>

#### Container Based Servers
<figure class="table">
  <table style="background-color:rgb(255, 255, 255);">
    <thead>
      <tr>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Name</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">VM Type</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Host Machine</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Image</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Container</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Volumes</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Notes</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">pi-hole</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">podman</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">DreamMachine</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;"><a class="is-external-link" href="http://docker.io/pihole/pihole:latest">docker.io/pihole/pihole:latest</a></td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">pihole</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">/mnt/data/etc-pihole:/etc/pihole</td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">&nbsp;</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">&nbsp;</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">&nbsp;</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">&nbsp;</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">&nbsp;</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">/mnt/data/pihole/etc-dnsmasq.d:/etc/dnsmasq.d</td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">wiki</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">docker</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">rpi4</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">requarks/wiki:2</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">wiki</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">/home/pi/docker_vols/wiki_data:/wiki/data/content</td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">postgres</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">docker</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">rpi4</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">postgres:9.5</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">postgres-9.5</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">/home/pi/docker_vols/postgres:/var/lib/postgresql/data</td>
        <td>&nbsp;</td>
      </tr>
    </tbody>
  </table>
</figure>

{.links-list}

#  Devices as of 11/11/20
The devices on the network are subdivided into VLANs. A snapshot of the devices present on 11/12/20 are shown below, grouped by VLAN.
<br>
### Tabs {.tabset}

#### WYSECHOICE_WIRED<br>VLAN 1
<figure class="table">
  <table style="background-color:rgb(255, 255, 255);">
    <thead>
      <tr>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Name</th>
        <th>Hostname</th>
        <th>Device Type</th>
        <th>Vendor</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">IP Address</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">MAC Address</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Dream Machine</td>
        <td>udm</td>
        <td>UDM</td>
        <td>Ubiquiti Networks</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.1.1</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">76:83:C2:D6:C9:1C</td>
      </tr>
      <tr>
        <td>rpi4</td>
        <td>rpi4</td>
        <td>Raspberry Pi 4 Model B Rev 1.1</td>
        <td>Raspberry Pi</td>
        <td>192.168.1.2</td>
        <td>DC:A6:32:24:E4:C3</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">dockernet-shim</td>
        <td>dockernet-shim</td>
        <td>Raspberry Pi 4 Model B Rev 1.1</td>
        <td>Raspberry Pi</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.1.3</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">DC:A6:32:24:E4:C3</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Family Room AP</td>
        <td>&nbsp;familyroomap</td>
        <td>UAP-AC-Lite</td>
        <td>Ubiquiti Networks</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.1.4</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">80:2A:A8:86:FC:98</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Living Room AP</td>
        <td>livingroomap</td>
        <td>UAP-AC-Lite</td>
        <td>Ubiquiti Networks</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.1.5</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">80:2A:A8:86:FB:37</td>
      </tr>
      <tr>
        <td>nas1300fd-1</td>
        <td>NAS1300FD</td>
        <td>QNAP T-251A</td>
        <td>QNAP Systems</td>
        <td>192.168.1.8</td>
        <td>24:5E:BE:13:00:FD</td>
      </tr>
      <tr>
        <td>nas1300fd-2</td>
        <td>&nbsp;NAS1300FD</td>
        <td>QNAP T-251A</td>
        <td>QNAP Systems</td>
        <td>192.168.1.9</td>
        <td>24:5E:BE:13:00:FE</td>
      </tr>
      <tr>
        <td>tsx-100</td>
        <td>tsx-100</td>
        <td>tsx-100</td>
        <td>congatec AG</td>
        <td>192.168.1.240</td>
        <td>00:13:95:37:40:6E</td>
      </tr>
    </tbody>
  </table>
</figure>

#### PiHole<br>VLAN 5
<figure class="table">
  <table style="background-color:rgb(255, 255, 255);">
    <thead>
      <tr>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Name</th>
        <th>Hostname</th>
        <th>Device Type</th>
        <th>Vendor</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">IP Address</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">MAC Address</th>
        <th>Host Machine</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>gateway</td>
        <td>--</td>
        <td>Podman gateway</td>
        <td>Ubiquiti Networks</td>
        <td>192.168.5.1</td>
        <td>5E:42:A3:20:FA:B9</td>
        <td>udm</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">pi.hole</td>
        <td>pi.hole</td>
        <td>Podman container</td>
        <td>Ubiquiti Networks</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.5.3</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">C6:1F:55:1A:E9:76</td>
        <td>udm</td>
      </tr>
    </tbody>
  </table>
</figure>

#### WYSECHOICE<br>VLAN 10
<figure class="table">
  <table style="background-color:rgb(255, 255, 255);">
    <thead>
      <tr>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Name</th>
        <th>Hostname</th>
        <th>Device Type</th>
        <th>Vendor</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">IP Address</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">MAC Address</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">gateway</td>
        <td>--</td>
        <td>UDM</td>
        <td>Ubiquiti Networks</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.10.1</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">76:83:C2:96:C9:20</td>
      </tr>
      <tr>
        <td>wyse-ehs-ipad</td>
        <td>wyse-ehs-ipad</td>
        <td>iPad</td>
        <td>Apple, Inc</td>
        <td>192.168.10.113</td>
        <td>26:ED:33:16:A6:05</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">EHS-Home-iPad</td>
        <td>EHS-Home-iPad</td>
        <td>iPad</td>
        <td>Apple, Inc</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.10.126</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">80:2A:A8:86:FC:98</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">doris-iphone</td>
        <td>doris-iphone</td>
        <td>Smartphone</td>
        <td>Apple, Inc</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.10.174</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">96:41:46:0A:1B:5A</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Chris-iPhone</td>
        <td>Chris-iPhone</td>
        <td>Smartphone</td>
        <td>Apple, Inc</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.10.184</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">DC:A6:32:24:E4:C3</td>
      </tr>
    </tbody>
  </table>
</figure>

#### WYSECHOICE_IOT<br>VLAN 20
<figure class="table">
  <table style="background-color:rgb(255, 255, 255);">
    <thead>
      <tr>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Name</th>
        <th>Hostname</th>
        <th>Device Type</th>
        <th>Vendor</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">IP Address</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">MAC Address</th>
        <th>Notes</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">gateway</td>
        <td>--</td>
        <td>UDM</td>
        <td>Ubiquiti Networks</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.20.1</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">74:83:c2:d6:c9:20</td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td>deck</td>
        <td>deck</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.6</td>
        <td>d4:81:ca:5a:79:b2</td>
        <td>00343258</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">basementstairs</td>
        <td>basementstairs</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.20.11</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">d4:81:ca:5a:78:92</td>
        <td>00343114</td>
      </tr>
      <tr>
        <td>basementmain</td>
        <td>basementmain</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.20</td>
        <td>d4:81:ca:5a:72:44</td>
        <td>00342307</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">toolroom</td>
        <td>toolroom</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.20.40</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">d4:81:ca:5a:72:64</td>
        <td>00342323</td>
      </tr>
      <tr>
        <td>Couch 2</td>
        <td>couch2</td>
        <td>Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.43</td>
        <td>d4:81:ca:57:72:9a</td>
        <td>00244046</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">diningroom</td>
        <td>diningroom</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.20.47</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">d4:81:ca:5b:b2:e2</td>
        <td>00383346</td>
      </tr>
      <tr>
        <td>entry</td>
        <td>entry</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.58</td>
        <td>d4:81:ca:5a:78:c2</td>
        <td>00343138</td>
      </tr>
      <tr>
        <td>MyQ Garage Hub</td>
        <td>MyQ-158</td>
        <td>Smart Device</td>
        <td>Chamberlain</td>
        <td>192.168.20.62</td>
        <td>64:52:99:bc:ed:4a</td>
        <td>2300 1C9 158</td>
      </tr>
      <tr>
        <td>kitchenfan</td>
        <td>kitchenfan</td>
        <td>Wall-Switch (3-way)</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.66</td>
        <td>d4:81:ca:5a:71:ee</td>
        <td>00342264</td>
      </tr>
      <tr>
        <td>Master Fan</td>
        <td>masterfan</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.69</td>
        <td>d4:81:ca:5a:74:9a</td>
        <td>00342606</td>
      </tr>
      <tr>
        <td>bathroom</td>
        <td>bathroom</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.70</td>
        <td>d4:81:ca:5a:7a:e6</td>
        <td>00343412</td>
      </tr>
      <tr>
        <td>bedroom</td>
        <td>bedroom</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.82</td>
        <td>d4:81:ca:5a:73:1e</td>
        <td>00342416</td>
      </tr>
      <tr>
        <td>filter</td>
        <td>filter</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.105</td>
        <td>d4:81:ca:5a:75:4e</td>
        <td>00342696</td>
      </tr>
      <tr>
        <td>porch</td>
        <td>porch</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.119</td>
        <td>d4:81:ca:5a:6b:d8</td>
        <td>00341485</td>
      </tr>
      <tr>
        <td>upstairsbathroom</td>
        <td>upstairsbathroom</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.126</td>
        <td>d4:81:ca:5a:76:ec</td>
        <td>00342903</td>
      </tr>
      <tr>
        <td>livingroom</td>
        <td>livingroom</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.146</td>
        <td>d4:81:ca:5b:bf:72</td>
        <td>00384954</td>
      </tr>
      <tr>
        <td>bench</td>
        <td>bench</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.159</td>
        <td>d4:81:ca:5a:74:f4</td>
        <td>00342651</td>
      </tr>
      <tr>
        <td>office</td>
        <td>office</td>
        <td>Instinct</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.177</td>
        <td>d4:81:ca:70:24:d8</td>
        <td>700690</td>
      </tr>
      <tr>
        <td>upstairsfan</td>
        <td>upstairsfan</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.183</td>
        <td>d4:81:ca:5a:76:2c</td>
        <td>00342807</td>
      </tr>
      <tr>
        <td>family</td>
        <td>family</td>
        <td>Wall-Switch (3-way)</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.192 / 3</td>
        <td>d4:81:ca:5a:7a:68</td>
        <td>00343349</td>
      </tr>
      <tr>
        <td>kitchen</td>
        <td>kitchen</td>
        <td>Wall-Dimmer</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.196</td>
        <td>d4:81:ca:5b:d0:fc</td>
        <td>00387199</td>
      </tr>
      <tr>
        <td>masterbathroom</td>
        <td>masterbathroom</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.203</td>
        <td>d4:81:ca:5a:69:1a</td>
        <td>00341134</td>
      </tr>
      <tr>
        <td>garage</td>
        <td>garage</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.204</td>
        <td>d4:81:ca:5a:77:ca</td>
        <td>00343014</td>
      </tr>
      <tr>
        <td>stairs</td>
        <td>stairs</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.208</td>
        <td>d4:81:ca:5a:77:ce</td>
        <td>00343016</td>
      </tr>
      <tr>
        <td>fishtank</td>
        <td>fishtank</td>
        <td>Switch (4-way)</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.223</td>
        <td>d4:81:ca:51:09:f4</td>
        <td>00034043</td>
      </tr>
      <tr>
        <td>driveway</td>
        <td>driveway</td>
        <td>Wall-Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.237</td>
        <td>d4:81:ca:5a:7b:24</td>
        <td>00343443</td>
      </tr>
      <tr>
        <td>couch</td>
        <td>couch</td>
        <td>Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.252</td>
        <td>d4:81:ca:54:97:06</td>
        <td>00150404</td>
      </tr>
      <tr>
        <td>readinglight</td>
        <td>readinglight</td>
        <td>Switch</td>
        <td>iDevices, Inc</td>
        <td>192.168.20.253</td>
        <td>d4:81:ca:57:08:1e</td>
        <td>00230416</td>
      </tr>
    </tbody>
  </table>
</figure>

#### WYSECHOICE_STREAMING<br>VLAN 30
<figure class="table">
  <table style="background-color:rgb(255, 255, 255);">
    <thead>
      <tr>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Name</th>
        <th>Hostname</th>
        <th>Device Type</th>
        <th>Vendor</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">IP Address</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">MAC Address</th>
        <th>Notes</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">gateway</td>
        <td>--</td>
        <td>UDM</td>
        <td>Ubiquiti Networks</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.30.1</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">76:83:c2:a6:c9:20</td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Kitchen Dot</td>
        <td>kitchendot</td>
        <td>Amazon Echo Show 8</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Amazon</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.30.16</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">14:0a:c5:6d:7c:0e</td>
        <td>e541728f1</td>
      </tr>
      <tr>
        <td>Family Room Fire</td>
        <td>familyroomfire</td>
        <td>SmartTV</td>
        <td>Amazon</td>
        <td>192.168.30.20</td>
        <td>1c:12:b0:dd:66:ff</td>
        <td>415a672cb</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Living Room Dot</td>
        <td>livingroomdot</td>
        <td>Amazon Echo Dot (3rd Gen)</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Amazon</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.30.26</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">4c:17:44:5a:9a:cd</td>
        <td>5d0b27878</td>
      </tr>
      <tr>
        <td>Toshiba</td>
        <td>toshiba</td>
        <td>Smart TV &amp; Set-top box</td>
        <td>Amazon</td>
        <td>192.168.30.44</td>
        <td>9c:5a:44:a0:fc:79</td>
        <td>3ac1fb7a0</td>
      </tr>
      <tr>
        <td>Fire TV Recast</td>
        <td>firetvrecast</td>
        <td>Smart TV &amp; Set-top box</td>
        <td>Amazon</td>
        <td>192.168.30.68</td>
        <td>24:4c:e3:4b:df:83</td>
        <td>7907c9970</td>
      </tr>
      <tr>
        <td>Bedroom Dot</td>
        <td>bedroomdot</td>
        <td>Amazon Show</td>
        <td>Amazon</td>
        <td>192.168.30.94</td>
        <td>08:12:a5:92:98:95</td>
        <td>0adf70edd</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Office Dot</td>
        <td>officedot</td>
        <td>Amazon Echo Dot (2nd Gen)</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Amazon</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.10.132</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">38:f7:3d:0c:58:c9</td>
        <td>2b1587f28</td>
      </tr>
      <tr>
        <td>Porch Dot</td>
        <td>&nbsp;porchdot</td>
        <td>Amazon Echo (2nd Gen)</td>
        <td>Amazon</td>
        <td>192.168.30.151</td>
        <td>50:f5:da:10:3c:20</td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td>Back Camera</td>
        <td>backcamera</td>
        <td>IP Network Camera</td>
        <td>WYZE</td>
        <td>192.168.30.153</td>
        <td>2c:aa:8e:02:23:25</td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Family Room Dot</td>
        <td>&nbsp;familyroomdot</td>
        <td>Amazon Echo Dot (3rd Gen)</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">Amazon</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">192.168.10.163</td>
        <td style="border-bottom:1px solid rgb(238, 238, 238);padding:0.75rem;">1c:4d:66:45:12:8c</td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td>Basement Dot</td>
        <td>basementdot</td>
        <td>Amazon Echo Dot (3rd Gen)</td>
        <td>Amazon</td>
        <td>192.168.30.219</td>
        <td>4c:17:44:5f:eb:7a</td>
        <td>f7bba70c3</td>
      </tr>
    </tbody>
  </table>
</figure>

#### Dockernet<br>VLAN 40
<figure class="table">
  <table style="background-color:rgb(255, 255, 255);">
    <thead>
      <tr>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">Name</th>
        <th>Hostname</th>
        <th>Device Type</th>
        <th>Vendor</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">IP Address</th>
        <th style="border-bottom:2px solid rgb(158, 158, 158);padding:0.75rem;">MAC Address</th>
        <th>Host Machine</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>gateway</td>
        <td>--</td>
        <td>Docker gateway</td>
        <td>Raspberry Pi</td>
        <td>192.168.40.1</td>
        <td>&nbsp;</td>
        <td>rpi4</td>
      </tr>
      <tr>
        <td>eth0-shim</td>
        <td>--</td>
        <td>Docker shim</td>
        <td>Raspberry Pi</td>
        <td>192.168.40.2</td>
        <td>&nbsp;</td>
        <td>rpi4</td>
      </tr>
      <tr>
        <td>postgres</td>
        <td>postgres</td>
        <td>Docker container</td>
        <td>Raspberry Pi</td>
        <td>192.168.40.30</td>
        <td>&nbsp;02:42:c0:a8:28:1e</td>
        <td>rpi4</td>
      </tr>
      <tr>
        <td>wiki</td>
        <td>wiki</td>
        <td>Docker container</td>
        <td>Raspberry Pi</td>
        <td>192.168.40.128</td>
        <td>02:42:c0:a8:28:80</td>
        <td>rpi4</td>
      </tr>
    </tbody>
  </table>
</figure>

{.links-list}