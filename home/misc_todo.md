---
title: Miscellaneous To Do Items
description: Categorized To Do list
published: true
date: 2021-01-16T01:55:02.121Z
tags: 
editor: markdown
dateCreated: 2020-12-13T01:03:08.246Z
---

# TODO List

1. Reverse proxy support
1. Print server
1. Label printer support on Linux
1. Print plant labels
1. Get 3D printer working again
1. Finish door for shed
1. Network config backup
1. Rsync server support for backup
1. Cleanup RasperryPI
1. Kiosk for Wiki
1. Calendar on Wiki
1. Weathermap support for LibreNMS
1. Oxidized config scripts for servers
1. Move LibreMNS to new server
1. Fix up tractor
1. Photo updates
   1. Identify locations of pictures
   1. Create photo database schema
   1. Import photo meta-data
   1. Filter photos without good meta-data
   1. Remove easy duplicates
   1. Remove harder duplicates
   1. Manually update filtered photos
   1. Organize results
   1. Backup plan
   1. Plan to handle additions
1. Create photo albums





# Laminar Flow Hood Notes

The filters are actually two Hunter replacement filters (#30930), that I siliconed together. I bought them online along with the blower. Filters ~$45.00 and the blower ~$90.00. Make sure the blower has enough air moving capacity, the one I used has 465 cfm. And I do use an autoclave to sterilize the media by dissolving the media powder in near boiling water pouring it into the container autoclaving it with the lids just resting on top of the opening. Once everything has cooled down I seal the lids on the containers.
```
I know how expensive commercial laminar flow hoods can be, and even the smaller laminar flow hoods that I have seen around the internet which are more or less for hobbiest can be ~$500. I will post a picture of my setup tonight, hopefully, but for now the cost of the unit breatks down (roughly) like this:

Blower 465cfm (w/shipping): $93.50
HEPA filters (2 w/shipping): $40.00
Wood (I bought extra): $100.00
Plexiglass: $13.00
Total: (approx) $246.50

So I paid about half of the cost of the cheapest hood on the internet.

Ryan
```
As promised, a picture of my laminar flow hood. The opening in the front is ~29"x9".
![laminarflowhood1.jpg](/laminarflowhood1.jpg)
![laminarflowhood2.jpg](/laminarflowhood2.jpg)
![laminarflowhood3.png](/laminarflowhood3.png)
![hoods_dimensions1.jpg](/hoods_dimensions1.jpg)
https://www.shroomery.org/8491/I-want-to-construct-a-HEPA-hood-How-do-I-match-a-blower-to-a-HEPA-filter
https://www.orchideenvermehrung.at/english/lfh/index.htm

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


    

        