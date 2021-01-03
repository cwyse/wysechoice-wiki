---
title: Miscellaneous To Do Items
description: Categorized To Do list
published: true
date: 2021-01-03T17:27:12.100Z
tags: 
editor: markdown
dateCreated: 2020-12-13T01:03:08.246Z
---

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


    

        