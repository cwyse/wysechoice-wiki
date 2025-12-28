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
