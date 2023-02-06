#!/bin/bash
NEW_VERSION=2.5.296
OLD_VERSION=2.5.296 

# function to get IP address
function get_ipaddr {
  local hostname=${1}
  local dnsserver=${2}
  local query_type=${3} # A or AAAA (IPv6)
  local ip_address=""

  # A and AAA record for IPv4 and IPv6, respectively
  # $1 stands for first argument
  if [ -n "${hostname}" ]; then
    if [ -z "${query_type}" ]; then
      query_type="A"
    fi
    # use host command for DNS lookup operations
    host -t ${query_type}  ${hostname} ${dnsserver} &>/dev/null 
    if [ "$?" -eq "0" ]; then
      # get ip address
      ip_address="$(host -t ${query_type} ${hostname} ${dnsserver}| awk '/has.*address/{print $NF; exit}')"
    else
      return 1
    fi
  else
    return 2
  fi
# display ip
 echo $ip_address
}

hostname="wiki.wysechoice.net"
dnsname="pihole.wysechoice.net"
STATIC_IP=$(get_ipaddr $hostname $dnsname)
DNS_SERVER_IP=$(get_ipaddr $dnsname $dnsname)

# Stop and remove container named "wiki-<old_version>"
docker stop wiki-${OLD_VERSION}
docker rm wiki-${OLD_VERSION}

# Pull latest image of Wiki.js
docker pull requarks/wiki:2

# Create new container of Wiki.js based on latest image
docker run -d                                                  \
           --ip="${STATIC_IP}"                                 \
           --dns="${DNS_SERVER_IP}"                            \
           --mac-address="02:42:c0:a8:28:21"                   \
           -p 3000:3000                                        \
           --net=dockernet.40                                  \
           --name wiki-${NEW_VERSION}                          \
           --hostname="wiki"                                   \
           --restart unless-stopped                            \
           -e "DB_TYPE=postgres"                               \
           -e "DB_HOST=postgres-14.1"                          \
           -e "DB_PORT=5432"                                   \
           -e "DB_USER=wikijs"                                 \
           -e "DB_PASS=wikijsrocks"                            \
           -e "DB_NAME=wiki"                                   \
           -v wiki_data:/wiki/data/content                     \
           requarks/wiki:2

# Use a second CPU for the container
docker update --cpus 3 wiki-${NEW_VERSION}

