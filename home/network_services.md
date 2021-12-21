---
title: Network Services
description: Reviews the existing services, their use, setup, and configuration
published: true
date: 2021-12-21T04:44:21.027Z
tags: level1
editor: markdown
dateCreated: 2020-11-09T02:33:13.649Z
---

- Reverse 

# Standard Network Services

## [Network Services List](/home/network_services/service_list)

## Grafana / InfluxDB / UnifiPoller

## Tabs {.tabset}

### Overview
1. docker network create grafana_net
1. Create a local Limited Admin account on the UDM, username unifipoller.  Note the password and use it in the docker run command.
1. docker pull influxdb:1.8.4
1. `docker run -p 8086:8086 --network grafana_net -e INFLUXDB_DB=unifi -e INFLUXDB_ADMIN_USER=unifipoller -e INFLUXDB_ADMIN_PASSWORD=9Yuzebes -v /home/chris/docker/influxdb:/var/lib/influxdb --name influxdb_1.8.4 influxdb:1.8.4`
1. Update the retention policy to prevent disk overruns.
```
root@db084cee31fe:/# influx
Connected to http://localhost:8086 version 1.8.4
InfluxDB shell version: 1.8.4
> CREATE RETENTION POLICY retention_policy ON unifi DURATION 32d REPLICATION 1
> quit
root@db084cee31fe:/# exit
```
5. docker pull grafana/grafana:8.2.6
1. `docker run -p 3000:3000 --network grafana_net  --privileged -v /home/chris/docker/grafana:/var/lib/grafana -e GF_INSTALL_PLUGINS=grafana-clock-panel,natel-discrete-panel,grafana-piechart-panel --name grafana_8.2.6 grafana/grafana:8.2.6`
1. In browser, navigate to 127.0.0.1:3000 (Grafana)
1. Select 'Add your first data source', choose InfluxDB
1. Change the URL to http://influxdb_1.8.4:8086/
1. Enter Database: unifi, User: unifipoller, Password: <influxdb password>, then press Save & Test
1. Import the dashboards be clicking the '+' on the left hand side, and choosing import.  Add the following IDs:
  - 10419
  - 10414
  - 10417
  - 10416
  - 10415
  - 10418
1. Select the InfluxDB data source for each of the dashboards, and create a new ID for each.
1. `docker pull golift/unifi-poller`
1. Copy an example config to ~/docker/unpoller - https://github.com/unpoller/unpoller/blob/master/examples/up.conf.example
1. Rename example config to up.conf
1. Update influxdb url to 'http://influxdb_1.8.4:8086/', user to unifipoller, pass to <password>.
1. `docker run -v /home/chris/docker/unpoller/up.conf:/etc/unifi-poller/up.conf --network grafana_net --name unifi-poller --name unifi-poller golift/unifi-poller`


## Reverse Proxy

## Tabs {.tabset}

### Overview
Reverse-proxy support is available via a Caddy server running on the QNAP NAS.  The Caddyfile is located at /share/CACHEDEV1_DATA/.qpkg/Caddy2.  It needs an entry for each new port mapping required.  

It is currently not running.  It can be tested by executing 'Caddy run' from the NAS command line.  It needs to be configured to start automatically.

The DNS server also needs to be updated to map each desired name to the Caddy server.


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
- `podman pull pihole/pihole:latest`
- Copy a modified 20-dns.conflist to /mnt/data/podman/cni. This will create your podman macvlan network.  The original file was modified to create a subnet so that the unbound container can be added to it.
  
```
  {
     "args": {
        "podman_labels": {
           "dns": ""
        }
     },
     "cniVersion": "0.4.0",
     "name": "dns",
     "plugins": [
        {
           "type": "macvlan",
           "master": "br5",
           "ipam": {
              "type": "host-local",
              "routes": [
                 {
                    "dst": "0.0.0.0/0"
                 }
              ],
              "ranges": [
                 [
                    {
                       "subnet": "192.168.5.0/24",
                       "rangeStart": "192.168.5.1",
                       "rangeEnd": "192.168.5.127",
                       "gateway": "192.168.5.1"
                    }
                 ]
              ]
           }
        }
     ]
  }
```  
  
- Copy a modified _10-dns.sh_ to /mnt/data/on_boot.d and update its values to reflect your environment.
  
```
  #!/bin/sh

  ## configuration variables:
  VLAN=5
  PIHOLE_IP="192.168.5.3"
  UNBOUND_IP="192.168.5.4"
  # This is the IP address of the container. You may want to set it to match
  # your own network structure such as 192.168.5.3 or similar.
  IPV4_GW="192.168.5.1/24"
  # As above, this should match the gateway of the VLAN for the container
  # network as above which is usually the .1/24 range of the IPV4_IP

  # if you want IPv6 support, generate a ULA, select an IP for the dns server
  # and an appropriate gateway address on the same /64 network. Make sure that
  # the 20-dns.conflist is updated appropriately. It will need the IP and GW
  # added along with a ::/0 route. Also make sure that additional --dns options
  # are passed to podman with your IPv6 DNS IPs when deploying the container for
  # the first time. You will also need to configure your VLAN to have a static
  # IPv6 block.

  # IPv6 Also works with Prefix Delegation from your provider. The gateway is the
  # IP of br(VLAN) and you can pick any ip address within that subnet that dhcpv6
  # isn't serving
  IPV6_IP=""
  IPV6_GW=""

  # set this to the interface(s) on which you want DNS TCP/UDP port 53 traffic
  # re-routed through the DNS container. separate interfaces with spaces.
  # e.g. "br0" or "br0 br1" etc.
  FORCED_INTFC="br0 br10 br20 br30 br40 br50"

  # container name; e.g. nextdns, pihole, adguardhome, etc.
  PIHOLE_CONTAINER=pihole
  UNBOUND_CONTAINER=unbound

  if ! test -f /opt/cni/bin/macvlan; then
      echo "Error: CNI plugins not found. You can install it with the following command:" >&2
      echo "       curl -fsSLo /mnt/data/on_boot.d/05-install-cni-plugins.sh https://raw.githubusercontent.com/boostchicken/udm-utilities/master/cni-plugins/05-install-cni-plugins.sh && /bin/sh /mnt/data/on_boot.d/05-install-cni-plugins.sh" >&2
      exit 1
  fi

  CNI_PATH=/mnt/data/podman/cni
  for file in "$CNI_PATH"/*.conflist
  do
      if [ -f "$file" ]; then
          ln -fs "$file" "/etc/cni/net.d/$(basename "$file")"
      fi
  done

  # set VLAN bridge promiscuous
  ip link set br${VLAN} promisc on

  # create macvlan bridge and add IPv4 IP
  ip link add br${VLAN}.mac link br${VLAN} type macvlan mode bridge
  ip addr add ${IPV4_GW} dev br${VLAN}.mac noprefixroute

  # (optional) add IPv6 IP to VLAN bridge macvlan bridge
  if [ -n "${IPV6_GW}" ]; then
    ip -6 addr add ${IPV6_GW} dev br${VLAN}.mac noprefixroute
  fi

  # set macvlan bridge promiscuous and bring it up
  ip link set br${VLAN}.mac promisc on
  ip link set br${VLAN}.mac up

  # add IPv4 route to DNS container
  ip route add ${PIHOLE_IP}/32 dev br${VLAN}.mac
  ip route add ${UNBOUND_IP}/32 dev br${VLAN}.mac

  # (optional) add IPv6 route to DNS container
  if [ -n "${IPV6_IP}" ]; then
    ip -6 route add ${IPV6_IP}/128 dev br${VLAN}.mac
  fi

  # Make DNSMasq listen to the container network for split horizon or conditional forwarding
  if ! grep -qxF interface=br$VLAN.mac /run/dnsmasq.conf.d/custom.conf; then
      echo interface=br$VLAN.mac >> /run/dnsmasq.conf.d/custom.conf
      kill -9 `cat /run/dnsmasq.pid`
  fi

  if podman container exists ${PIHOLE_CONTAINER}; then
    podman start ${PIHOLE_CONTAINER}
  else
    logger -s -t podman-dns -p ERROR Container $PIHOLE_CONTAINER not found, make sure you set the proper name, you can ignore this error if it is your first time setting it up
  fi

  if podman container exists ${UNBOUND_CONTAINER}; then
    podman start ${UNBOUND_CONTAINER}
  else
    logger -s -t podman-dns -p ERROR Container $UNBOUND_CONTAINER not found, make sure you set the proper name, you can ignore this error if it is your first time setting it up
  fi

  # (optional) IPv4 force DNS (TCP/UDP 53) through DNS container
  for intfc in ${FORCED_INTFC}; do
    if [ -d "/sys/class/net/${intfc}" ]; then
      for proto in udp tcp; do
        prerouting_rule="PREROUTING -i ${intfc} -p ${proto} ! -s ${PIHOLE_IP} ! -d ${PIHOLE_IP} --dport 53 -j DNAT --to ${PIHOLE_IP}"
        iptables -t nat -C ${prerouting_rule} || iptables -t nat -A ${prerouting_rule}

        # (optional) IPv6 force DNS (TCP/UDP 53) through DNS container
        if [ -n "${IPV6_IP}" ]; then
          prerouting_rule="PREROUTING -i ${intfc} -p ${proto} ! -s ${IPV6_IP} ! -d ${IPV6_IP} --dport 53 -j DNAT --to ${IPV6_IP}"
          ip6tables -t nat -C ${prerouting_rule} || ip6tables -t nat -A ${prerouting_rule}
        fi
      done
    fi
  done
```  
- Execute /mnt/data/on_boot.d/10-dns.sh     
4.  Run the pihole docker container, be sure to make the directories for your persistent pihole configuration. They are mounted as volumes in the command below.

```
    podman run -d --network dns --restart always \
    --name pihole \
    -e TZ="America/New_York" \
    -v "/mnt/data/etc-pihole/:/etc/pihole/" \
    -v "/mnt/data/pihole/etc-dnsmasq.d/:/etc/dnsmasq.d/" \
    --dns=127.0.0.1 --dns=1.1.1.1 \
    --dns=1.0.0.1 \
    --hostname pi.hole \
    -e VIRTUAL_HOST="pi.hole" \
    -e PROXY_LOCATION="pi.hole" \
    -e ServerIP="192.168.5.3" \
    -e IPv6="False" \
    --cap-add NET_ADMIN \
    --cap-add SYS_NICE \
    --group-add=www-data \
    --ip=192.168.5.3 \
    pihole/pihole:latest
```
  
The below errors are expected and acceptable:

```
    ERRO[0022] unable to get systemd connection to add healthchecks: dial unix /run/systemd/private: connect: no such file or directory
    ERRO[0022] unable to get systemd connection to start healthchecks: dial unix /run/systemd/private: connect: no such file or directory
```

5.  Set pihole password
    `podman exec -it pihole pihole -a -p YOURNEWPASSHERE`
1.  Create docker.io_password.txt in the /mnt/data/scripts directory.  It should contain a single line with the password for the user account used in
the docker login command in upd_unbound.sh
1.  Copy the following script into /mnt/data/scripts/upd_unbound.sh and execute it to create the `unbound` container.
    
```
  #!/bin/sh

  cat /mnt/data/scripts/docker.io_password.txt | docker login --username cwyse --password-stdin

  IMAGE="pedantic/unbound:latest"
  IMAGE_NAME=unbound

  podman pull $IMAGE
  podman stop $IMAGE_NAME
  podman rm $IMAGE_NAME

  curl  https://www.internic.net/domain/named.root > /mnt/data/unbound/root.hints

  cat /mnt/data/scripts/docker.io_password.txt | docker login --username cwyse --password-stdin

  # Podman cgroup is v1 not v2

  podman run -d --name $IMAGE_NAME --network dns \
      -e TZ="America/New_York" \
      --hostname unbound \
      --ip=192.168.5.4 \
      --restart=always \
      -v "/mnt/data/unbound/root.hints:/var/lib/unbound/root.hints" \
      -v "/mnt/data/unbound:/opt/unbound/etc/unbound/" \
      $IMAGE

```  
8. The unbound configuraiton includes support for adding custom A records.  An a-records.conf file can be placed in the unbound directory to allow DNS mapping of local addresses.  For example:
```
  # A Record
	#local-data: "somecomputer.local. A 192.168.1.1"

# PTR Record
	#local-data-ptr: "192.168.1.1 somecomputer.local."
```
SRV records and forward records are also supported.  See the github page for the unbound container:  
  https://github.com/MatthewVance/unbound-docker/tree/master/1.10.0
  
If this support is not needed or implemented yet, the files must still be created:
```
  touch /mnt/data/unbound/a-records.conf
  touch /mnt/data/unbound/forward-records.conf
  touch /mnt/data/unbound/srv-records.conf
```
9. Logon to the pihole admin page, and under settings, TODO: Configure PiHole/Unbound to use each other select the DNS tab.  Unselect all Upstream DNS servers, and then add a custom IPv4 server - 192.168.5.4#53.  Also make sure DNSSEC is turned off. (https://github.com/pi-hole/docs/issues/207)
1.  Run `podman exec -it unbound unbound-control-setup` to create keys for remote control
1.  Set remote control to yes in unbound.conf, and run upd_unbound.conf to activate.
1.  unbound.conf should match this:
```
  server:
      ###########################################################################
      # BASIC SETTINGS
      ###########################################################################
      # Time to live maximum for RRsets and messages in the cache. If the maximum
      # kicks in, responses to clients still get decrementing TTLs based on the
      # original (larger) values. When the internal TTL expires, the cache item
      # has expired. Can be set lower to force the resolver to query for data
      # often, and not trust (very large) TTL values.
      cache-max-ttl: 86400

      # Time to live minimum for RRsets and messages in the cache. If the minimum
      # kicks in, the data is cached for longer than the domain owner intended,
      # and thus less queries are made to look up the data. Zero makes sure the
      # data in the cache is as the domain owner intended, higher values,
      # especially more than an hour or so, can lead to trouble as the data in
      # the cache does not match up with the actual data any more.
      #cache-min-ttl: 300
      cache-min-ttl: 0

      # Set the working directory for the program.
      directory: "/opt/unbound/etc/unbound"

      # RFC 6891. Number  of bytes size to advertise as the EDNS reassembly buffer
      # size. This is the value put into  datagrams over UDP towards peers.
      # The actual buffer size is determined by msg-buffer-size (both for TCP and
      # UDP). Do not set higher than that value.
      # Default  is  1232 which is the DNS Flag Day 2020 recommendation.
      # Setting to 512 bypasses even the most stringent path MTU problems, but
      # is seen as extreme, since the amount of TCP fallback generated is
      # excessive (probably also for this resolver, consider tuning the outgoing
      # tcp number).
      edns-buffer-size: 1232

      # Listen to for queries from clients and answer from this network interface
      # and port.
      interface: 0.0.0.0@53

      # Rotates RRSet order in response (the pseudo-random number is taken from
      # the query ID, for speed and thread safety).
      rrset-roundrobin: yes

      # Drop user  privileges after  binding the port.
      username: "_unbound"

      ###########################################################################
      # LOGGING
      ###########################################################################

      # Do not print log lines to inform about local zone actions
      log-local-actions: no

      # Do not print one line per query to the log
      log-queries: no

      # Do not print one line per reply to the log
      log-replies: no

      # Do not print log lines that say why queries return SERVFAIL to clients
      log-servfail: no

      # Further limit logging
      logfile: /dev/null

      # Only log errors
      verbosity: 0

      ###########################################################################
      # PRIVACY SETTINGS
      ###########################################################################

      # RFC 8198. Use the DNSSEC NSEC chain to synthesize NXDO-MAIN and other
      # denials, using information from previous NXDO-MAINs answers. In other
      # words, use cached NSEC records to generate negative answers within a
      # range and positive answers from wildcards. This increases performance,
      # decreases latency and resource utilization on both authoritative and
      # recursive servers, and increases privacy. Also, it may help increase
      # resilience to certain DoS attacks in some circumstances.
      aggressive-nsec: yes

      # Extra delay for timeouted UDP ports before they are closed, in msec.
      # This prevents very delayed answer packets from the upstream (recursive)
      # servers from bouncing against closed ports and setting off all sort of
      # close-port counters, with eg. 1500 msec. When timeouts happen you need
      # extra sockets, it checks the ID and remote IP of packets, and unwanted
      # packets are added to the unwanted packet counter.
      delay-close: 10000

      # Prevent the unbound server from forking into the background as a daemon
      do-daemonize: no

      # Add localhost to the do-not-query-address list.
      do-not-query-localhost: no

      # Number  of  bytes size of the aggressive negative cache.
      neg-cache-size: 4M

      # Send minimum amount of information to upstream servers to enhance
      # privacy (best privacy).
      qname-minimisation: yes

      ###########################################################################
      # SECURITY SETTINGS
      ###########################################################################
      # Only give access to recursion clients from LAN IPs
      access-control: 127.0.0.1/32 allow
      access-control: 192.168.0.0/16 allow
      access-control: 172.16.0.0/12 allow
      access-control: 10.0.0.0/8 allow
      # access-control: fc00::/7 allow
      # access-control: ::1/128 allow

      # File with trust anchor for  one  zone, which is tracked with RFC5011
      # probes.
      auto-trust-anchor-file: "var/root.key"

      # Enable chroot (i.e, change apparent root directory for the current
      # running process and its children)
      chroot: "/opt/unbound/etc/unbound"

      # Deny queries of type ANY with an empty response.
      deny-any: yes

      # Harden against algorithm downgrade when multiple algorithms are
      # advertised in the DS record.
      harden-algo-downgrade: yes

      # RFC 8020. returns nxdomain to queries for a name below another name that
      # is already known to be nxdomain.
      harden-below-nxdomain: yes

      # Require DNSSEC data for trust-anchored zones, if such data is absent, the
      # zone becomes bogus. If turned off you run the risk of a downgrade attack
      # that disables security for a zone.
      harden-dnssec-stripped: yes

      # Only trust glue if it is within the servers authority.
      harden-glue: yes

      # Ignore very large queries.
      harden-large-queries: yes

      # Perform additional queries for infrastructure data to harden the referral
      # path. Validates the replies if trust anchors are configured and the zones
      # are signed. This enforces DNSSEC validation on nameserver NS sets and the
      # nameserver addresses that are encountered on the referral path to the
      # answer. Experimental option.
      harden-referral-path: no

      # Ignore very small EDNS buffer sizes from queries.
      harden-short-bufsize: yes

      # If enabled the HTTP header User-Agent is not set. Use with caution
      # as some webserver configurations may reject HTTP requests lacking
      # this header. If needed, it is better to explicitly set the
      # the http-user-agent.
      hide-http-user-agent: no

      # Refuse id.server and hostname.bind queries
      hide-identity: yes

      # Refuse version.server and version.bind queries
      hide-version: yes

      # Set the HTTP User-Agent header for outgoing HTTP requests. If
      # set to "", the default, then the package name and version are
      # used.
      http-user-agent: "DNS"

      # Report this identity rather than the hostname of the server.
      identity: "DNS"

      # These private network addresses are not allowed to be returned for public
      # internet names. Any  occurrence of such addresses are removed from DNS
      # answers. Additionally, the DNSSEC validator may mark the  answers  bogus.
      # This  protects  against DNS  Rebinding
      private-address: 10.0.0.0/8
      private-address: 172.16.0.0/12
      private-address: 192.168.0.0/16
      private-address: 169.254.0.0/16
      # private-address: fd00::/8
      # private-address: fe80::/10
      # private-address: ::ffff:0:0/96

      # Enable ratelimiting of queries (per second) sent to nameserver for
      # performing recursion. More queries are turned away with an error
      # (servfail). This stops recursive floods (e.g., random query names), but
      # not spoofed reflection floods. Cached responses are not rate limited by
      # this setting. Experimental option.
      ratelimit: 1000

      # Use this certificate bundle for authenticating connections made to
      # outside peers (e.g., auth-zone urls, DNS over TLS connections).
      tls-cert-bundle: /etc/ssl/certs/ca-certificates.crt

      # Set the total number of unwanted replies to eep track of in every thread.
      # When it reaches the threshold, a defensive action of clearing the rrset
      # and message caches is taken, hopefully flushing away any poison.
      # Unbound suggests a value of 10 million.
      unwanted-reply-threshold: 10000

      # Use 0x20-encoded random bits in the query to foil spoof attempts. This
      # perturbs the lowercase and uppercase of query names sent to authority
      # servers and checks if the reply still has the correct casing.
      # This feature is an experimental implementation of draft dns-0x20.
      # Experimental option.
      use-caps-for-id: yes

      # Help protect users that rely on this validator for authentication from
      # potentially bad data in the additional section. Instruct the validator to
      # remove data from the additional section of secure messages that are not
      # signed properly. Messages that are insecure, bogus, indeterminate or
      # unchecked are not affected.
      val-clean-additional: yes

      ###########################################################################
      # PERFORMANCE SETTINGS
      ###########################################################################
      # https://nlnetlabs.nl/documentation/unbound/howto-optimise/
      # https://nlnetlabs.nl/news/2019/Feb/05/unbound-1.9.0-released/

      # Number of slabs in the infrastructure cache. Slabs reduce lock contention
      # by threads. Must be set to a power of 2.
      infra-cache-slabs: 4

      # Number of incoming TCP buffers to allocate per thread. Default
      # is 10. If set to 0, or if do-tcp is "no", no  TCP  queries  from
      # clients  are  accepted. For larger installations increasing this
      # value is a good idea.
      incoming-num-tcp: 10

      # Number of slabs in the key cache. Slabs reduce lock contention by
      # threads. Must be set to a power of 2. Setting (close) to the number
      # of cpus is a reasonable guess.
      key-cache-slabs: 4

      # Number  of  bytes  size  of  the  message  cache.
      # Unbound recommendation is to Use roughly twice as much rrset cache memory
      # as you use msg cache memory.
      msg-cache-size: 78561280

      # Number of slabs in the message cache. Slabs reduce lock contention by
      # threads. Must be set to a power of 2. Setting (close) to the number of
      # cpus is a reasonable guess.
      msg-cache-slabs: 4

      # The number of queries that every thread will service simultaneously. If
      # more queries arrive that need servicing, and no queries can be jostled
      # out (see jostle-timeout), then the queries are dropped.
      # This is best set at half the number of the outgoing-range.
      # This Unbound instance was compiled with libevent so it can efficiently
      # use more than 1024 file descriptors.
      num-queries-per-thread: 4096

      # The number of threads to create to serve clients.
      # This is set dynamically at run time to effectively use available CPUs
      # resources
      num-threads: 3

      # Number of ports to open. This number of file descriptors can be opened
      # per thread.
      # This Unbound instance was compiled with libevent so it can efficiently
      # use more than 1024 file descriptors.
      outgoing-range: 8192

      # Number of bytes size of the RRset cache.
      # Use roughly twice as much rrset cache memory as msg cache memory
      rrset-cache-size: 157122560

      # Number of slabs in the RRset cache. Slabs reduce lock contention by
      # threads. Must be set to a power of 2.
      rrset-cache-slabs: 4

      # Do no insert authority/additional sections into response messages when
      # those sections are not required. This reduces response size
      # significantly, and may avoid TCP fallback for some responses. This may
      # cause a slight speedup.
      minimal-responses: yes

      # # Fetch the DNSKEYs earlier in the validation process, when a DS record
      # is encountered. This lowers the latency of requests at the expense of
      # little more CPU usage.
      prefetch: yes

      # Fetch the DNSKEYs earlier in the validation process, when a DS record is
      # encountered. This lowers the latency of requests at the expense of little
      # more CPU usage.
      prefetch-key: yes

      # Have unbound attempt to serve old responses from cache with a TTL of 0 in
      # the response without waiting for the actual resolution to finish. The
      # actual resolution answer ends up in the cache later on.
      serve-expired: yes

      # Open dedicated listening sockets for incoming queries for each thread and
      # try to set the SO_REUSEPORT socket option on each socket. May distribute
      # incoming queries to threads more evenly.
      so-reuseport: yes

      ###########################################################################
      # LOCAL ZONE
      ###########################################################################

      # Include file for local-data and local-data-ptr
      include: /opt/unbound/etc/unbound/a-records.conf
      include: /opt/unbound/etc/unbound/srv-records.conf

      ###########################################################################
      # FORWARD ZONE
      ###########################################################################

      include: /opt/unbound/etc/unbound/forward-records.conf


  remote-control:
      control-enable: yes
```
1.  Update /mnt/data/pihole/etc-dnsmasq.d/01-pihole.conf and set the cache-size to 0.
1.  Update your DNS Servers to 192.168.5.3 (or your custom ip) in all your DHCP configs.    
1.  Configure a cron job to monitor the container from a separate host and restart it if necessary
    - Copy the following script to /usr/local/bin/dns_restart.sh on a host computer
    ```
    #!/usr/bin/env bash

    DNS_SERVER=192.168.5.3
    UDM_ROUTER=192.168.1.1
    WYSECHOICE=wysechoice.net
    PASSWORD="&847&XLXXbxY"

    # If the router is running
    if ping -c 1 ${UDM_ROUTER} > /dev/null 2>&1; then
        # If the DNS server is not working
        if ! nslookup ${WYSECHOICE} ${DNS_SERVER} > /dev/null 2>&1; then
            sshpass -p ${PASSWORD} ssh -t root@${UDM_ROUTER} "podman stop pihole"
            sshpass -p ${PASSWORD} ssh -t root@${UDM_ROUTER} "/mnt/data/on_boot.d/10-dns.sh"
        fi
    fi
    ```
    
    - `chmod 755 /usr/local/bin/dns_restart.sh`
    - `crontab -e` -> `* * * * * /usr/local/bin/dns_restart.sh`
    
    - Copy the following script to /usr/local/bin/pihole_whitelist.sh on a host computer.  This will update the whitelist nightly.
    ```
    #!/usr/bin/env bash

    DNS_SERVER=192.168.5.3
    UDM_ROUTER=192.168.1.1
    WYSECHOICE=wysechoice.net
    PASSWORD="&847&XLXXbxY"

    # If the router is running
    if ping -c 1 ${UDM_ROUTER} > /dev/null 2>&1; then
        # If the DNS server is not working
        if ! nslookup ${WYSECHOICE} ${DNS_SERVER} > /dev/null 2>&1; then
            curl -ks https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt >/tmp/whitelist.txt
            sshpass -p ${PASSWORD} scp /tmp/whitelist.txt root@${UDM_ROUTER}:/mnt/data/etc-pihole                                       
	        sshpass -p ${PASSWORD} ssh -t root@${UDM_ROUTER} podman exec -it pihole pihole -g
        fi
    fi
    ```
    
    - `chmod 755 /usr/local/bin/pihole_whitelist.sh`
    - `crontab -e` -> `0 2 * * * /usr/local/bin/pihole_whitelist.sh`

More unbound info: https://www.nlnetlabs.nl/documentation/unbound/howto-setup/
### Maintenance

#### UDM Password Change
The dns_restarts.sh script needs to be updated whenever the UDM root password changes

#### Update Pi-Hole Image

From host machine (UDM/192.168.1.1), in the /mnt/data/scripts directory, run the upd_pihole.sh script:
```
  #!/bin/sh

  # Change to boostchicken/pihole:latest for DoH
  # Change to boostchicken/pihole-dote:latest for DoTE
  IMAGE=pihole/pihole:latest                          

  podman pull $IMAGE
  podman stop pihole
  podman rm pihole  
  podman run -d --network dns --restart always \
  --name pihole \                               
  -e TZ="America/New_York" \
  -v "/mnt/data/etc-pihole/:/etc/pihole/" \
  -v "/mnt/data/pihole/etc-dnsmasq.d/:/etc/dnsmasq.d/" \
  --dns=127.0.0.1 --dns=1.1.1.1 \                       
  --dns=1.0.0.1 \                
  --hostname pi.hole \
  -e VIRTUAL_HOST="pi.hole" \
  -e PROXY_LOCATION="pi.hole" \
  -e ServerIP="192.168.5.3" \  
  -e IPv6="False" \          
  --cap-add NET_ADMIN \
  --cap-add SYS_NICE \ 
  --group-add=www-data \
  --ip=192.168.5.3 \    
  $IMAGE            
```
  
    
  
As an added check to make sure the restart script is working properly, you can stop the container (`podman stop pihole`), then wait a maximum of 1 minute, and the container should restart.  You can check it using `podman container ls`.
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
[pi-hole-pi_hole-teleporter_2021-06-13_13-02-07.tar.gz](/home/network_services/pihole/pi-hole-pi_hole-teleporter_2021-06-13_13-02-07.tar.gz)
[pi-hole-pi_hole-teleporter_2021-06-16_01-20-07.tar.gz](/home/network_services/pihole/pi-hole-pi_hole-teleporter_2021-06-16_01-20-07.tar.gz)

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
[pihole.sh](/pihole.sh) - Create and run container ---  NOTE:  This doesn't match the run command shown above.  Specifically, it has an additional backup DNS (1.0.0.1), and is missing the --cap-add and --group-add parameters.  Not sure why - but needs to be reviewed.

#### Located on DNS monitoring host
[/usr/local/bin/dns_restart.sh](/dns_restart.sh) - Script to monitor and restart pihole container if necessary
## Multicast Domain Name Service (MDNS)

## Tabs {.tabset}
### Overview
The MDNS support provided by the router does not work as expected.  Therefore, it needs to be disabled in the UDM, and replaced with a custom MDNS repeater.

This page provides instructions: 
https://www.brandonmartinez.com/2020/09/02/unifi-and-mdns-with-apple-homekit/

In the UDM, all MDNS and IGMP snooping needs to be disabled.  Then a custom MDNS repeater 
image is downloaded.  This image is used to create three containers to allow MDNS forwarding
from the networks to the internet, while still keeping the VLANs separater from each other.

The commands used to create the containers:
```
# podman run -it -d --restart=always --name="multicast-relay-IOT" --network=host -e OPTS=" --verbose" -e INTERFACES="br0 br20 br30" docker.io/scyto/multicast-relay
# podman run -it -d --restart=always --name="multicast-relay-10" --network=host -e OPTS=" --verbose" -e INTERFACES="br0 br10" docker.io/scyto/multicast-relay
# podman run -it -d --restart=always --name="multicast-relay-Docker" --network=host -e OPTS=" --verbose" -e INTERFACES="br0 br40 br50" docker.io/scyto/multicast-relay
```

Finally, a script needs to be created to start the containers at boot.  Create 
/mnt/data/on_boot.d/01-mulicast-relay.sh, with the following content:
```
#!/bin/sh
#
# https://www.brandonmartinez.com/2020/09/02/unifi-and-mdns-with-apple-homekit/
#
# podman run -it -d --restart=always --name="multicast-relay-IOT" --network=host -e OPTS=" --verbose" -e INTERFACES="br0 br20 br30" docker.io/scyto/multicast-relay
# podman run -it -d --restart=always --name="multicast-relay-10" --network=host -e OPTS=" --verbose" -e INTERFACES="br0 br10" docker.io/scyto/multicast-relay
# podman run -it -d --restart=always --name="multicast-relay-Docker" --network=host -e OPTS=" --verbose" -e INTERFACES="br0 br40 br50" docker.io/scyto/multicast-relay
#

# kill all instances of avahi-daemon (UDM spins an instance up even with mDNS services disabled)
killall avahi-daemon

# start the multicast-relay container image
podman start multicast-relay-IOT
podman start multicast-relay-10
podman start multicast-relay-Docker
```

Make sure to make the file executable:
`chmod 755 01-mulicast-relay.sh`

Then reboot the system and make sure the containers start and the avahi-daemon(s) is not running.

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

> Steps need to be updated & scripts should be cleaned up - script below is current (2/1/21) 
{.is-info}

1. Remove the DockerNet MACVLAN network if it exists
1. Create a virtual interface (eth0-shim) to act as a bridge between the MACVLAN and the host
1. Create /etc/network/interfaced.d/eth0-shim to persist the configuration across boots
1. Dynamically configure eth0-shim on the running system (NOTE: potential bug - address is not set to 192.168.1.3 explicitly)
1. Eth0-shim configuration include bridging all 192.168.40.x/24 containers from 192.168.1.x/24.
1. Creates DockerNet, reserving 192.168.40.1 for the gateway, and 192.168.40.2 for eth0-shim.

Currently, DockerNet is hosted on the Raspberry PI 4 (pi-hole).  It can be created by using the following script function after configuring the routing.  DockerNet is created once, then the network is used by the containers on the Raspberry PI 4. 

The following script function creates the DockerNet on the PI:

```bash
#!/bin/bash
set -e
set -xv


function create_dockernet()
{
  HOST_IP=192.168.1.119
  HOST_GW=192.168.1.1
  HOST_SHIM_IP=192.168.1.120
  MAC_ADDR="02:00:C0:A8:01:78"
  NEW_SUBNET=50
  HOST_IF=eth0
  IS_WIFI=0

  # Reference:
  # https://blog.oddbit.com/post/2018-03-12-using-docker-macvlan-networks/

  # Routing requirements:
  #    1. Docker assigned addresses should not be used by the router
  #    2. Routes need to be created to access the subnet residing on the docker host
  #    3. Secondary MACVLAN (${HOST_IF}-shim) used to connect containers to host
  #
  #############################################
  #
  #  The following routes must be configured
  #  on the router to connect to the containers
  #  in the 192.168.${NEW_SUBNET}.0/24 subnet .
  #
  #############################################
  #  192.168.${NEW_SUBNET}.0/24 dev br40 scope link  src 192.168.${NEW_SUBNET}.1
  #  192.168.${NEW_SUBNET}.0/31 dev br0  metric 1
  #  192.168.${NEW_SUBNET}.2 via ${HOST_SHIM_IP} dev br0  metric 1
  #  192.168.${NEW_SUBNET}.4/30 dev br0  metric 1
  #  192.168.${NEW_SUBNET}.8/29 dev br0  metric 1
  #  192.168.${NEW_SUBNET}.16/28 dev br0  metric 1
  #  192.168.${NEW_SUBNET}.32/27 dev br0  metric 1
  #  192.168.${NEW_SUBNET}.64/26 dev br0  metric 1
  #  192.168.${NEW_SUBNET}.128/25 dev br0  metric 1
  ############################################

  printf "Creating dockernet. "

  # Start from scratch
  if docker network ls | grep  dockernet >/dev/null 2>&1; then
    docker network remove dockernet.${NEW_SUBNET}
  fi

  #
  # Create dockernet corresponding to same definition in router
  #   Uses router DHCP settings which are currently allocating 192.168.${NEW_SUBNET}.128 - 192.168.${NEW_SUBNET}.255 (192.168.${NEW_SUBNET}.128/25)
  #

  # Create ${HOST_IF}-shim MACVLan interface for communication between the host
  #  and the MACVlan network
  sudo rm -f /etc/network/interfaces.d/${HOST_IF}-shim || true
  SHIM_CFG=$(mktemp)

  # Public MAC addresses use these ranges:
  #   x2-xx-xx-xx-xx-xx
  #   x6-xx-xx-xx-xx-xx
  #   xA-xx-xx-xx-xx-xx
  #   xE-xx-xx-xx-xx-xx
  #
  # The range selected was arbitrary, x2-xx-xx-xx-xx-xx.  The
  # last four segments are mapped to the IP address to prevent
  # internal network conflicts.
  #
  #MAC_ADDR="02:00:C0:A8:01:78"

  #
  # Make ethtool is installed to provide support to disable
  # checksum offloading.
  #
  echo sudo apt install -y ethtool
  sudo apt install -y ethtool || true

#  if ! grep 'kernel.dmesg_restrict' /etc/sysctl.conf; then
#    sudo echo 'kernel.dmesg_restrict = 0' >>/etc/sysctl.conf
#  fi

#  sudo service procps restart

  #
  # Create the MACVlan bridge configuration file for the host,
  # to make the interface persistent across boots.  Also, if the
  # interface is not defined, issue the network commands to create
  # the interface immediately.
  #
  sudo cat <<***REMOVED*** >${SHIM_CFG}
auto ${HOST_IF}-shim
iface ${HOST_IF}-shim inet static
 address ${HOST_SHIM_IP}
 pre-up ip link set ${HOST_IF}-shim link ${HOST_IF} type macvlan mode bridge
 up /bin/bash -c "echo ${HOST_IF}-shim up >/dev/kmsg"
 up ip addr replace 192.168.${NEW_SUBNET}.2/32 dev ${HOST_IF}-shim noprefixroute
 up ip link set ${HOST_IF}-shim address ${MAC_ADDR} up
 up ip route add 192.168.${NEW_SUBNET}.0/31 dev ${HOST_IF}-shim
 up ip route add 192.168.${NEW_SUBNET}.3/32 dev ${HOST_IF}-shim
 up ip route add 192.168.${NEW_SUBNET}.4/30 dev ${HOST_IF}-shim
 up ip route add 192.168.${NEW_SUBNET}.8/29 dev ${HOST_IF}-shim
 up ip route add 192.168.${NEW_SUBNET}.16/28 dev ${HOST_IF}-shim
 up ip route add 192.168.${NEW_SUBNET}.32/27 dev ${HOST_IF}-shim
 up ip route add 192.168.${NEW_SUBNET}.64/26 dev ${HOST_IF}-shim
 up ip route add 192.168.${NEW_SUBNET}.128/25 dev ${HOST_IF}-shim
 offload-gso  off
***REMOVED***
 sudo mkdir -p /etc/network/interfaces.d/
 sudo mv ${SHIM_CFG} /etc/network/interfaces.d/${HOST_IF}-shim

 sudo ip link delete ${HOST_IF}-shim || true
 if ! ip addr show ${HOST_IF}-shim >/dev/null 2>&1; then
    # Add a shim ethernet to act as a bridge to the host machine
    sudo ip link add ${HOST_IF}-shim link ${HOST_IF} type macvlan mode bridge
    sudo bash -c "echo ${HOST_IF}-shim up >/dev/kmsg"
    sudo ip addr replace 192.168.${NEW_SUBNET}.2/32 dev ${HOST_IF}-shim noprefixroute
    sudo ip link set ${HOST_IF}-shim address ${MAC_ADDR} up

    # Route all the addresses through the shim
    sudo ip route add 192.168.${NEW_SUBNET}.0/31 dev ${HOST_IF}-shim
    sudo ip route add 192.168.${NEW_SUBNET}.3/32 dev ${HOST_IF}-shim
    sudo ip route add 192.168.${NEW_SUBNET}.4/30 dev ${HOST_IF}-shim
    sudo ip route add 192.168.${NEW_SUBNET}.8/29 dev ${HOST_IF}-shim
    sudo ip route add 192.168.${NEW_SUBNET}.16/28 dev ${HOST_IF}-shim
    sudo ip route add 192.168.${NEW_SUBNET}.32/27 dev ${HOST_IF}-shim
    sudo ip route add 192.168.${NEW_SUBNET}.64/26 dev ${HOST_IF}-shim
    sudo ip route add 192.168.${NEW_SUBNET}.128/25 dev ${HOST_IF}-shim
  fi
  sudo ethtool -K ${HOST_IF}-shim gso off 

  #
  # Enable promiscuous mode for ${HOST_IF}
  #   The parent interface (${HOST_IF}) for the MACVLAN must be
  #   in promiscuous mode to allow multiple VLANs on the interface
  #
  sudo rm -f /etc/network/interfaces.d/${HOST_IF} || true
  ETH0_CFG=$(mktemp)
  sudo cat <<***REMOVED*** >${ETH0_CFG}
auto ${HOST_IF}
iface ${HOST_IF} inet static
  address ${HOST_IP}/24
  gateway ${HOST_GW}
  up /sbin/ip -4 link set ${HOST_IF} promisc on
  down /sbin/ip link set ${HOST_IF} promisc off
  down /sbin/ip link set ${HOST_IF} down
***REMOVED***
  sudo mv ${ETH0_CFG} /etc/network/interfaces.d/${HOST_IF}
  sudo ip link set ${HOST_IF} promisc on

  systemd_setup
  if [ ${IS_WIFI} -eq 1 ]; then
    wifi_support
  fi

  if grep 'CONFIGURE_INTERFACES=' /etc/default/networking; then
    sudo sed -i '/CONFIGURE_INTERFACES=/d' /etc/default/networking
  fi
  sudo bash -c "echo 'CONFIGURE_INTERFACES=yes' >>/etc/default/networking"

  if grep 'VERBOSE=' /etc/default/networking; then
    sudo sed -i '/VERBOSE=/d' /etc/default/networking
  fi
  sudo bash -c "echo 'VERBOSE=no' >>/etc/default/networking"

  if grep 'source-directory' /etc/network/interfaces; then
    sudo sed -i -e 's/source-directory/source/g' /etc/network/interfaces
  fi

  if grep 'DOCKER_OPTS=' /etc/default/docker; then
    sudo sed -i '/DOCKER_OPTS=/d' /etc/default/docker
  fi
  sudo bash -c "echo 'DOCKER_OPTS=\" --dns 192.168.5.3 -dns 1.1.1.1 --dns 8.8.8.8 --dns 8.8.4.4\"' >>/etc/default/docker"

  # Use the MACVLan driver - allowing docker containers to appear as if physically connected to network
  DOCKER_OPTIONS="  -d macvlan"
  # Specify the physical interface to use
  DOCKER_OPTIONS+=" -o parent=${HOST_IF}"
  # Set the subnet to use for the network.  The router will also define this subnet as a VLAN.
  DOCKER_OPTIONS+=" --subnet 192.168.${NEW_SUBNET}.0/24"
  # Define the external gateway machine.  Ubiquiti provides this virtual gateway in the router.
  DOCKER_OPTIONS+=" --gateway 192.168.${NEW_SUBNET}.1"
  # Define the IP range for containers that don't specify an IP address
  DOCKER_OPTIONS+=" --ip-range 192.168.${NEW_SUBNET}.128/25"
  # Reserve an address to use for the MACVLAN bridge (${HOST_IF}-shim) communication with host
  DOCKER_OPTIONS+=" --aux-address host=192.168.${NEW_SUBNET}.2"
  docker network create ${DOCKER_OPTIONS} dockernet.${NEW_SUBNET}

  printf "Done.\n"
}

systemd_setup() {
  sysd_cfg=$(mktemp)
  sudo cat <<***REMOVED*** >${sysd_cfg}
[NetDev]
Name=${HOST_IF}-shim
Kind=macvlan

[MACVLAN]
Mode=bridge
***REMOVED***
  sudo mv -f ${sysd_cfg} /etc/systemd/network/${HOST_IF}-shim.netdev
  sudo chmod 644 /etc/systemd/network/${HOST_IF}-shim.netdev

  sudo cat <<***REMOVED*** >${sysd_cfg}
[Match]
Name=${HOST_IF}-shim

[Network]
IPForward=yes
Address=192.168.${NEW_SUBNET}.2/24
Gateway=192.168.${NEW_SUBNET}.1
***REMOVED***
  sudo mv -f ${sysd_cfg} /etc/systemd/network/${HOST_IF}-shim.network
  sudo chmod 644 /etc/systemd/network/${HOST_IF}-shim.network

  sudo cat <<***REMOVED*** >${sysd_cfg}
[Match]
Name=${HOST_IF}

[Network]
MACVLAN=${HOST_IF}-shim
***REMOVED***
  sudo mv ${sysd_cfg} /etc/systemd/network/${HOST_IF}.network
  sudo chmod 644 /etc/systemd/network/${HOST_IF}.network

  sudo cat <<***REMOVED*** >${sysd_cfg}
[Unit]
After=network.target
Before=network-online.target

[Service]
Type=oneshot
ExecStart=/sbin/ip link set ${HOST_IF} promisc on
RemainAfterExit=yes

[Install]
WantedBy=network-online.target
***REMOVED***
  sudo mv -f ${sysd_cfg} /etc/systemd/system/macvlan.service

sudo systemctl daemon-reload
sudo systemctl enable systemd-networkd
sudo systemctl enable macvlan

}

wifi_support()
{
  # https://www.linux-tips-and-tricks.de/en/raspberry/312-how-to-create-a-wlan-ethernet-bridge-on-debian-raspberry/#arp

  if grep -v 'net.ifnames' /boot/cmdline.txt; then
    sudo bash -c "sed -i -e 's/$/ net.ifnames=0/' /boot/cmdline.txt"
  fi

  if grep 'net.ipv4.ip_forward' /etc/sysctl.conf; then
    sudo sed -i '/net.ipv4.ip_forward/d' /etc/sysctl.conf
  fi
  sudo bash -c "echo 'net.ipv4.ip_forward=1' >>/etc/sysctl.conf"

  sudo apt install -y parprouted dhcp-helper avahi-daemon

  if grep 'DHCPHELPER_OPTS' /etc/default/dhcp-helper; then
    sudo sed -i '/DHCPHELPER_OPTS/d' /etc/default/dhcp-helper
  fi
  sudo bash -c "echo 'DHCPHELPER_OPTS=\"-b wlan0\"' >>/etc/default/dhcp-helper"

  if grep 'enable-reflector' /etc/avahi/avahi-daemon.conf; then
    sudo sed -i '/enable-reflector/d' /etc/avahi/avahi-daemon.conf
  fi
  sudo bash -c "echo 'enable-reflector=yes' >>/etc/avahi/avahi-daemon.conf"


  sudo cat <<***REMOVED*** > /etc/network/interfaces.d/${HOST_IF}-shim
auto ${HOST_IF}-shim
allow-hotplug ${HOST_IF}-shim
iface ${HOST_IF}-shim inet dhcp
  post-down /usr/bin/killall /usr/sbin/parprouted
  # Assign eth0 same IP address as wlan0 so dhcp-proxy will proxy for the same subnet
  post-up /sbin/ip addr add $(ip addr show ${HOST_IF}-shim | grep -Eo "^\s+inet [^ ]+ " | sed -E 's/^\s+//' | cut -f 2 -d ' ' | cut -f 1 -d/ | head -1)/32 dev eth0
  post-up /usr/sbin/service dhcp-helper restart && /usr/sbin/parprouted eth0 ${HOST_IF}-shim
  post-down /sbin/ifdown eth0 
  pre-up ip link set ${HOST_IF}-shim link ${HOST_IF} type macvlan mode bridge
  up /bin/bash -c "echo ${HOST_IF}-shim up >/dev/kmsg"
  up ip addr add 192.168.50.2/32 dev ${HOST_IF}-shim
  up ip link set ${HOST_IF}-shim address 02:00:C0:A8:0A:4D up
 up ip route add 192.168.50.0/31 dev ${HOST_IF}-shim
 up ip route add 192.168.50.3/32 dev ${HOST_IF}-shim
 up ip route add 192.168.50.4/30 dev ${HOST_IF}-shim
 up ip route add 192.168.50.8/29 dev ${HOST_IF}-shim
 up ip route add 192.168.50.16/28 dev ${HOST_IF}-shim
 up ip route add 192.168.50.32/27 dev ${HOST_IF}-shim
 up ip route add 192.168.50.64/26 dev ${HOST_IF}-shim
 up ip route add 192.168.50.128/25 dev ${HOST_IF}-shim
 offload-gso  off
 offload-tx   off
 offload-rx   off
 offload-tso  off
***REMOVED***


}


```

### Configuration
In addition to the host configuration, the router must also be configured to allow traffic to get to DockerNet.  The configuration and routing is shown in the following images used to configure the Ubiquiti Dream Machine:
![dockernet.png](/dockernet.png)
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

The postgres data is dumped out every 3 days (TBD!!) and stored on the NAS (192.168.1.8).  The backup is performed on from the NAS.  It requires the rsyncd daemon to be running.  It executes the following command on the docker host:
```
docker exec postgres-9.5 pg_dump wiki -U wikijs -F c > ~/wikibackup.dump
```

To restore the database backup, stop the wiki docker container:
```
docker stop wiki
```
Then restore the wikibackup.dump file into a new database, first dropping the existing empty DB:
```
docker exec -it postgres-9.5 dropdb -U wikijs wiki
docker exec -it postgres-9.5 createdb -U wikijs wiki
cat ~/wikibackup.dump | docker exec -i postgres-9.5 pg_restore -U wikijs -d wiki
```
We can now restart the wiki container:
```
docker start wiki
```

### Upgrade
Before upgrading the wiki, perform a backup, and make sure the git repository is also backup up the site.  Then stop the wiki:

```
docker stop wiki
```
Pull the latest docker image:
```
docker pull requarks/wiki:2
```
Create and run a new container that includes the date in the name:
```
docker run -d -p 8080:3000 --net=dockernet --name wiki_01_31_21 --restart unless-stopped -e "DB_TYPE=postgres" -e "DB_HOST=postgres-9.5" -e "DB_PORT=5432" -e "DB_USER=wikijs" -e "DB_PASS=wikijsrocks" -e "DB_NAME=wiki" -v /home/pi/docker_vols/wiki_data requarks/wiki:2
```
Test the updated wiki.  If everything is OK, the old container and image can be deleted.

### Support Files
TBD

## Firewall
## Tabs {.tabset}

### Overview
To support better firewall logging, the UDM has been provisioned with some scripts from https://github.com/boostchicken/udm-utilities/blob/master/ipt-enable-logs/scripts/ipt-enable-logs.sh.  The version of the scripts on the UDM do not include the Go scripts.  The scripts are not intended for a UDM, so they will not work without modification.

The changes are to use an enable script (scripts/ipt-enable-logs.sh) written for a Bourne shell, shown in this thread.
https://github.com/opustecnica/public/issues/2
The original notes and instructions on the setup are found here:
https://github.com/opustecnica/public/wiki/UDM-&-UDM-PRO-NOTES
The ipt-enables-logs-launch.sh script is taken from the last web site.
Note that the /data directory on the UDM must be a symbolic link to /mnt/data/unifi-os.
A script for remotely viewing the log files is included at the bottom of the ipt-enable-logs.sh script.

**/mnt/data/scripts/ipt-enable-logs.sh**
```
#!/bin/sh

# [NOTE] Need to find a hook to run this script not only at startup but every time time the firewall is modified.

# Clear existing ipt-save if it exists.

# [NOTE] /data must be a symbolic link to /mnt/data/unifi-os
#   lrwxrwxrwx    1 root     root            18 Dec  7 22:29 /data -> /mnt/data/unifi-os

FILE=/data/ipt-save
if test -f "${FILE}"; then
  rm -f "${FILE}"
fi

# Collect existing iptables configuration into an array.
prev_line=''
iptables-save |
while IFS= read -r line; do
  if [ -n "${prev_line}" ]; then
    ACTION="$(echo "${line}" | sed -E "s/.*-j\s(.*)$/\1/")"
    if echo "${ACTION}" | grep ^RETURN$ >/dev/null; then ACTION='ACCEPT'; fi
    echo -e "${prev_line}" | sed -E "s/^-A\sUBIOS_(\S+)\s.*-j LOG$/& --log-prefix \"[${ACTION}_\1] \"/" >> "${FILE}"
    prev_line=''
  fi

  if echo "${line}" | grep LOG$ >/dev/null
    then
      prev_line="${line}"
    else
      echo -e "${line}" >> "${FILE}"
      prev_line=''
  fi
done

exit

#
# Copy this script to view the follow the UDM firewall log from a remote machine
#

#!/bin/bash

# Set this to the name of the router, and define passwordless login
UDM=udm

logunifijson () 
{ 
    ssh_alias ${UDM} "tail -f /var/log/messages" | rg "kernel:" | sed "s/]IN/] IN/" | jq --unbuffered -R '. | rtrimstr(" ") | split(": ") | {date: (.[0] | split(" ") | .[0:3] | join(" "))} + (.[1] | capture("\\[.+\\] \\[(?<rule>.*)\\].*")) + ((.[1] | capture("\\[.+\\] (?<rest>.*)") | .rest | split(" ") | map(select(startswith("[") == false) | split("=") | {(.[0]): .[1]})) | (reduce .[] as $item ({}; . + $item)))'
}

logunifi () 
{ 
    logunifijson | jq --unbuffered -r '"\(.date) - \(.rule)\tIN=\(.IN)  \t\(.PROTO)\tSRC=\(.SRC)@\(.SPT)\tDST=\(.DST)@\(.DPT)\tLEN=\(.LEN)\t"'
}
```
**/mnt/data/on_boot.d/30-ipt-enable-logs-launch.sh**
```
#!/bin/sh
set -e

/mnt/data/scripts/ipt-enable-logs.sh
iptables-restore -c < /data/ipt-save
```
**/mnt/data/scripts/refresh-iptables.sh**
```
#!/bin/sh

set -e

if [ -f /mnt/data/on_boot.d/10-dns.sh ]; then
  if ! iptables-save | grep -e '\-A PREROUTING.* \--log-prefix "\[' > /dev/null; then
    /mnt/data/on_boot.d/10-dns.sh
  else
    echo "iptables already contains DNAT log prefixes, ignoring."
  fi
fi

/mnt/data/on_boot.d/30-ipt-enable-logs-launch.sh
```
If 30-ipt-enable-logs-launch.sh is present (could be a symbolic link to the scripts directory), the logging will be started at boot up.  If changes are made to the firewall rules, either the UDM must be rebooted, or the refresh-iptables.sh script must be executed.




### Initial Setup
### Configuration


### Backup
TBD
### Reference
TBD
### Support Files
TBD



