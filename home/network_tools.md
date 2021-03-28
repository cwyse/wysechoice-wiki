---
title: Network Tools
description: Network administration tools and utilities
published: true
date: 2021-01-31T23:29:37.411Z
tags: 
editor: undefined
dateCreated: 2020-11-13T04:39:58.551Z
---

# Network Tools

Network administration is supported through various web interfaces.  All passwords and user information is available through LastPass.

Unifi - Router management interface.  Provides DHCP server, firewall, and VLAN management.  Router works in conjunction with two Ubiquiti access points.
pihole - Provides local DNS service with ad blocking support
pgAdmin4 - Started on local host to manage postgres databases.
grafana - Interactive dashboard with ability to collect data from multiple sources.
syslog - TBD -  Service needed to manage server logs
portainer - Started in docker container (currently on local host) to manage both local and remote docker objects
wiki - Documentation web server running Wiki.js.
The table below provides additional information on these servers.


## Tools
### Tabs {.tabset}

#### Administrative Tools
<figure class="table">
  <table>
    <thead>
      <tr>
        <th>Service</th>
        <th>Server</th>
        <th>Server IP</th>
        <th>Port</th>
        <th>VM</th>
        <th>VM Type</th>
        <th>VM Host</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>pihole</td>
        <td>pihole</td>
        <td>192.168.5.3</td>
        <td>80</td>
        <td><span class="text-huge">✓</span></td>
        <td>Podman</td>
        <td>udm</td>
        <td>Ad-aware DNS service</td>
      </tr>
      <tr>
        <td>pgAdmin4</td>
        <td>&nbsp;localhost</td>
        <td>&nbsp;localhost</td>
        <td>32887</td>
        <td><span class="text-huge">✗</span></td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;Database administration</td>
      </tr>
      <tr>
        <td>Unifi</td>
        <td>postgres&nbsp;</td>
        <td>192.168.1.1</td>
        <td>&nbsp;80</td>
        <td><span class="text-huge">✗</span></td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;Router management</td>
      </tr>
      <tr>
        <td>Grafana</td>
        <td>grafana</td>
        <td>192.168.40.40</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>Docker</td>
        <td>rpi4</td>
        <td>Multi-service dashboard</td>
      </tr>
      <tr>
        <td>Syslog</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>Service logging</td>
      </tr>
      <tr>
        <td>portainer</td>
        <td>&nbsp;</td>
        <td>localhost</td>
        <td>9000</td>
        <td><span class="text-huge">✓</span></td>
        <td>Docker</td>
        <td>localhost</td>
        <td>Container management</td>
      </tr>
      <tr>
        <td>Wiki</td>
        <td>wiki</td>
        <td>192.168.40.128</td>
        <td>80</td>
        <td><span class="text-huge">✓</span></td>
        <td>Docker</td>
        <td>rpi4</td>
        <td>WyseChoice documentation</td>
      </tr>
    </tbody>
  </table>
</figure>

#### Network Servers
<figure class="table">
  <table>
    <thead>
      <tr>
        <th>Service</th>
        <th>Web Interfaces</th>
        <th>Server</th>
        <th>Server IP</th>
        <th>Port</th>
        <th>VM</th>
        <th>VM Type</th>
        <th>VM Host</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Wiki</td>
        <td>Wiki.js</td>
        <td>wiki</td>
        <td>192.168.40.128</td>
        <td>80</td>
        <td><span class="text-huge">✓</span></td>
        <td>Docker</td>
        <td>rpi4</td>
        <td>WyseChoice documentation</td>
      </tr>
      <tr>
        <td>Postgres</td>
        <td>&nbsp;</td>
        <td>postgres&nbsp;</td>
        <td>192.168.40.30</td>
        <td>&nbsp;</td>
        <td><span class="text-huge">✓</span></td>
        <td>Docker</td>
        <td>rpi4</td>
        <td>&nbsp;Wiki and ghini clients</td>
      </tr>
      <tr>
        <td>influxdb</td>
        <td>&nbsp;</td>
        <td>localhost</td>
        <td>localhost</td>
        <td>9000</td>
        <td>&nbsp;<span class="text-huge">✓</span></td>
        <td>&nbsp;Docker</td>
        <td>&nbsp;rpi4</td>
        <td>&nbsp;Used by grafana</td>
      </tr>
      <tr>
        <td>&nbsp;qnap</td>
        <td>&nbsp;</td>
        <td>qnap</td>
        <td>192.168.1.8/9</td>
        <td>&nbsp;</td>
        <td>&nbsp;<span class="text-huge">✗</span></td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>File server&nbsp;</td>
      </tr>
    </tbody>
  </table>
</figure>


{.links-list}