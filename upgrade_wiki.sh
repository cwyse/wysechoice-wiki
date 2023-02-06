#!/bin/bash
NEW_VERSION=2.5.296
OLD_VERSION=2.5.286 
# Stop and remove container named "wiki-<old_version>"
docker stop wiki-${OLD_VERSION}
#docker rm wiki-${NEW_VERSION}

# Pull latest image of Wiki.js
docker pull requarks/wiki:2

# Create new container of Wiki.js based on latest image
docker run -d                                                  \
           --ip="192.168.40.33"                                \
           --dns="192.168.5.3"                                 \
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
           -v wiki_data:/home/pi/docker_vols/wiki_data         \
           -v wiki_content:/wiki/data/content                  \
           requarks/wiki:2

# Use a second CPU for the container
docker update --cpus 2 wiki-${NEW_VERSION}

