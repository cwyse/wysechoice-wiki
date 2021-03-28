---
title: Miscellaneous Notes
description: Various bits of information without a home
published: true
date: 2021-03-25T04:08:30.784Z
tags: 
editor: undefined
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

OpenFortiGUI supports VPN profiles to create a PPP connection with a VPN server.  Location of the profiles can be set in the GUI.  The configuration should be set as shown below.  In particular, the *set_dns* option needs to be *false*, and the *pppd_no_peerdns* option needs to be *true*, otherwise the *resolv.conf* file will be overwritten, preventing *dnsmasq* from splitting the DNS accesses.  Also note that the *pppd_ifname* has been updated to *vpn_ca0*.

- ~/.openfortigui/vpnprofiles/CA_VPN.conf
```
[cert]
ca_file=
trusted_cert=5ab07e8fa6d17fd1e204fa3c1d740c841c167c9576d92d649a848751ec337853
user_cert=
user_key=
verify_cert=false

[options]
set_routes=true
set_dns=false
pppd_no_peerdns=true                                                                                                                    
insecure_ssl=false
debug=false
realm=
autostart=false
always_ask_otp=false
otp_prompt=
otp_delay=0
half_internet_routers=false
pppd_log_file=
pppd_plugin_file=
pppd_ifname=vpn_ca0
pppd_ipparam="'device=$DEVICE'"
pppd_call=

[vpn]
gateway_host=sslvpn.canoga.com
gateway_port=18443
name=CA VPN
password="Vf8MS0VmssZByf/O2ZArug=="
username=cwyse
```
The options section of the Connecticut VPN profile is identical.  The other two sections should be updated to use the Connecticut server as shown below:
```
[cert]
ca_file=
trusted_cert=3ef1ed49853e3512ec0c7f4f56d9e235e86d79bb31060f103a8523beefdee4a2
user_cert=
user_key=
verify_cert=false

# Options section ommitted

[vpn]
gateway_host=ct.canoga.com
gateway_port=18443
name=CT VPN
password="Vf8MS0VmssZByf/O2ZArug=="
username=cwyse
```
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
Haircut 3/25/21