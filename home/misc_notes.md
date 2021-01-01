---
title: Miscellaneous Notes
description: Various bits of information without a home
published: true
date: 2021-01-01T17:15:16.488Z
tags: 
editor: markdown
dateCreated: 2021-01-01T17:15:16.488Z
---

# Miscellaneous Notes
## Canoga / Wysechoice Network Config
The Canoga / Wysechoice network configuration uses both split tunnel VPN networking and split tunnel DNS services.  This means that only traffic designated for canoga.com will be sent over the VPN link.  This includes nameserver lookups, which will be split between two servers, based on the domain name requested.

By default, the VPN takes over the DNS services, preventing access to wysechoice.net.  Resolving that required several changes across multiple files and services.

DNS resolution uses NetworkManager w/ the dnsmasq plugin, the pppd daemon, and openfortigui w/ openfortivpn.  

> The systemd-resolved and resolvconf packages are not used.  Installing and using them will cause conflicts with this configuration.
{.is-warning}

### Network Manager
The resolv.conf file is controlled by network manager.  It will normally be overwritten when the VPN is connected.  Instead, we want to always use the existing resolv.conf, which will be set to point to the localhost.  The dnsmasq plugin for network manager will listen on localhost port 53 and handle all DNS requests.

After all configuration changes are made, NetworkManager must be restarted:
`sudo systemctl restart NetworkManager`

Enable the dnsmasq plugin by setting *dns* to *dnsmasq*.
- /etc/NetworkManager/NetworkManager.conf
```
[main]                                                                                                                                  
dns=dnsmasq
plugins=ifupdown,keyfile

[ifupdown]
managed=true

[device]
wifi.scan-rand-mac-address=no
```
#### dnsmasq plugin
When a DNS request is made, the dnsmasq plugin will receive and process the request.  The configuration defined below tells the plugin to forward requests to the wysechoice.net domain to the internal DNS server (192.168.5.3), and requests to canoga.com to Canoga's DNS server.  

Add a configuration file for each domain, with the following entries:
- /etc/NetworkManager/dnsmasq.d/00-wysechoice.conf
```
# /etc/NetworkManager/dnsmasq.d/00-wysechoice.conf
#
# This file directs dnsmasq to forward any request to resolve
# names under the .wysechoice.net domain to 192.168.5.3, my 
# home DNS server.  Local requests will also use that server.
server=/wysechoice.net/192.168.5.3       
local=/wysechoice.net/
```
- /etc/NetworkManager/dnsmasq.d/01-canoga.conf
```
# https://fedoramagazine.org/using-the-networkmanagers-dnsmasq-plugin/
# /etc/NetworkManager/dnsmasq.d/00-wysechoice.conf
#
# This file directs dnsmasq to forward any request to resolve
# names under the .canoga.com domain to 172.16.1.46/7.
server=/canoga.com/172.16.1.46    
server=/canoga.com/172.16.1.47    
```
The nameservers here are manually specified.  If the IP addresses change, these configuration files will need to be updated.

The dnsmasq plugin also has support for use of the /etc/hosts file.  Internal host addresses are generally maintained in the pi-hole DNS server, but the local /etc/hosts file could be used for symbolic names for addresses that are not network-wide.  Add the following configuration file to enable use of the local /etc/hosts file:
- /etc/NetworkManager/dnsmaasq.d/02-add-hosts.conf
```
# /etc/NetworkManager/dnsmasq.d/02-add-hosts.conf
# By default, the plugin does not read from /etc/hosts.  
# This forces the plugin to slurp in the file.
#
# If you didn't want to write to the /etc/hosts file.  This could
# be pointed to another file.
#
addn-hosts=/etc/hosts
```
### OpenFortiGUI w/ OpenFortiVPN
OpenFortiGUI is a simple user interface to configure and use the OpenFortiVPN software.  It includes its own copy of OpenFortiVPN, so there will not be any *openfortivpn* software process running, just *openfortigui*.

When the VPN connects, it creates a *ppp* network interface.  We have two potential VPN interfaces, one to connect to California, and one for Connecticut.  To avoid confusion, the interfaces will be renamed to ca_vpn0 and ct_vpn0.

### Point to Point Daemon (pppd)
This might not be necessary after dnsmasq changes, but the pppd configuration was modified to add routes to the DNS servers via the appropriate interface.  The *fortivpn* script uses *dig* to obtain the IP address of the DNS servers, then adds a route to make them go through the correct interface.  If interface names change, this file would need to be updated.
- /etc/ppp/ip-up.d
```
#!/bin/bash
# https://rohanrajpal.com/2020/04/25/Selective-network-routing.html
#
# Domains and IPs are separated by a space
#
touch /home/chris/fortivpn                                                                                                              
wysechoice_ips=''
wysechoice_domains='wysechoice.net'

let resolved
for domain in $wysechoice_domains; do
  resolved=`dig +short $domain | tail -n1`
  canoga_ips="$wysechoice_ips $resolved"
done

for ip in $wysechoice_ips; do
  route add $ip dev eno1
done

# Whitelist here all domains that need to go through openfortivpn
canoga_ips=''
canoga_domains='canoga.com'

let resolved
for domain in $canoga_domains; do
  resolved=`dig +short $domain | tail -n1`
  canoga_ips="$canoga_ips $resolved"
done

for ip in $canoga_ips; do
  route add $ip dev vpn_ca0
done
```
