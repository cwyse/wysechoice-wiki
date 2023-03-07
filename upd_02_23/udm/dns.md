---
title: UDM Domain Name Service
description: Description of container providing domain name service.
published: true
date: 2023-03-07T05:34:41.206Z
tags: 
editor: markdown
dateCreated: 2023-03-07T05:34:41.205Z
---



# Domain Name Service (DNS)

## Overview
The network uses a Pi-hole domain name server.  The Pi-hole server provides both DNS lookup and filtering.  It utilizes various lists of known ad web sites to prevent them from being accessed.  

This server runs as podman container on the UDM router.  Although it is hosted on the UDM router (192.168.1.1), it appears on the network with its own MAC address.  The container resides on VLAN 5, which is a MACVLan network using the UDM router as it's network interface.

### Boot sequence

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

## Initial Setup

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
1.  This command will display stats with remote control enabled:
  `podman exec -it unbound unbound-control stats`
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
## Maintenance

### UDM Password Change
The dns_restarts.sh script needs to be updated whenever the UDM root password changes

### Update Pi-Hole Image

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

## Reference
https://github.com/boostchicken/udm-utilities/tree/master/on-boot-script

https://github.com/boostchicken/udm-utilities/tree/master/run-pihole

http://192.168.5.3/admin/queries.php

https://github.com/boostchicken/udm-utilities/blob/master/cni-plugins/20-dns.conflist

https://github.com/boostchicken/udm-utilities/blob/master/dns-common/on_boot.d/10-dns.sh
## Support Files
### Located on UDM filesystem (not unifi-os container)
[/mnt/data/on_boot.d/10-dns.sh](/10-dns.sh) - Pi-Hole configuration and startup script
[/mnt/data/podman/cni/20-dns.conflist](/20-dns.conflist) - Configuration of 192.168.5.x MACVLAN for Pi-Hole
[pihole.sh](/pihole.sh) - Create and run container ---  NOTE:  This doesn''t match the run command shown above.  Specifically, it has an additional backup DNS (1.0.0.1), and is missing the --cap-add and --group-add parameters.  Not sure why - but needs to be reviewed.

### Located on DNS monitoring host
[/usr/local/bin/dns_restart.sh](/dns_restart.sh) - Script to monitor and restart pihole container if necessary
