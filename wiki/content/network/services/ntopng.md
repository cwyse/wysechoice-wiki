---
title: ntopng on UniFi Dream Machine
description: Traffic monitoring using ntopng in a Podman container
published: true
tags: network service monitoring
editor: markdown
---

# ntopng on UniFi Dream Machine

# Network


- Install ntopng on the Dream Machine in a podman container

    -  Source code: https://github.com/ntop/ntopng
    -  Container source:  https://github.com/tusc/ntopng-udm
    -  Installation on Dream Machine:
    
    ```
    # podman pull tusc/ntopng-udm:latest
    # mkdir -p /mnt/data/ntopng/redis
    # mkdir -p /mnt/data/ntopng/lib
    # touch /mnt/data/ntopng/GeoIP.conf
    # curl -Lo /mnt/data/ntopng/ntopng.conf https://github.com/tusc/ntopng-udm/blob/master/ntopng/ntopng.conf?raw=true
    # curl -Lo /mnt/data/ntopng/redis.conf https://github.com/tusc/ntopng-udm/blob/master/ntopng/redis.conf?raw=true
    # podman run -d --net=host --restart always \
        --name ntopng \
        -v /mnt/data/ntopng/GeoIP.conf:/etc/GeoIP.conf \
        -v /mnt/data/ntopng/ntopng.conf:/etc/ntopng/ntopng.conf \
        -v /mnt/data/ntopng/redis.conf:/etc/redis/redis.conf \
        -v /mnt/data/ntopng/lib:/var/lib/ntopng \
        docker.io/tusc/ntopng-udm:latest
    ```
    - Create a udm-boot script to start the container with the following command:
    	
    ```
    podman start ntopng
    ```


    

        