---
title: Setup
description: Network and Application Setup
published: true
date: 2020-11-15T15:43:00.152Z
tags: 
editor: markdown
dateCreated: 2020-11-15T09:50:55.982Z
---

# Dream Machine

- Dream Machine
  - Base Configuration
  - Extensions
- RPi4
  - Base OS
  - Dockernet
  - Postgres
  - Ghini
  - Wiki.js
- QNAP
  - Base Configuration
  - Apps
- Host
  - Associated Apps
    - Portainer
    - PgAdmin4

# Portainer

# Tabs {.tabset}

## Overview
Container maintenance is handled using the Portainer Docker image.  The image has is locally named according to the version.  In this instance, version 1.24.1 is named portainer1241.  The image mounts a volume, portainer_data, that is maintained across version upgrades.
<br>
<figure style="width:796px;" class="table">
  <table style="background-color:rgb(255, 255, 255);">
    <tbody>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">Image</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">portainer/portainer-ce:latest</td>
      </tr>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">Web Site</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;"><a class="is-external-link" href="https://www.portainer.io/">https://www.portainer.io/</a></td>
      </tr>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">Ports</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">0.0.0.0:8000 -&gt; 8000/tcp&nbsp; &nbsp;(Edge Agent Endpoint) (Currently not used)<br>0.0.0.0:9000 -&gt; 9000/tcp&nbsp; &nbsp;(Portainer Endpoint)</td>
      </tr>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">Data Volume</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">portainer_data</td>
      </tr>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">Network</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">bridge</td>
      </tr>
    </tbody>
  </table>
</figure>

## Initial Setup
```
$ docker volume create portainer_data
$ docker run -d -p 8000:8000 -p 9000:9000 --name=portainer-ce_2.0 --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
```

## Configuration

### Client Endpoints
The localhost endpoint is automatically enabled.  Remote hosts need to have their Docker API enabled.  An excerpt from "[How do I enable the remote API for dockerd](https://success.mirantis.com/article/how-do-i-enable-the-remote-api-for-dockerd)" is given below:

<div>
<figure style="width:796px;" class="table">
  <table style="background-color:rgb(255, 255, 255);">
    <tbody>
      <tr>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;width:55px;">&nbsp;</td>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;width:1107px;">
          <p>&nbsp;</p>
          <h2 class="toc-header" id="how-do-i-enable-the-remote-api-for-dockerd"> How do I enable the remote API for dockerd</h2>
          <p>After completing these steps, you will have enabled the remote API for dockerd, without editing the systemd unit file in place:</p>
          <p>Create a file at <code>/etc/systemd/system/docker.service.d/startup_options.conf</code> with the below contents:</p>
          <pre class="prismjs line-numbers"><code class="language-plaintext"># /etc/systemd/system/docker.service.d/override.conf
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2376
</code></pre>
          <blockquote>
            <p><strong>Note:</strong> The -H flag binds dockerd to a listening socket, either a Unix socket or a TCP port. You can specify multiple -H flags to bind to multiple sockets/ports. The default -H fd:// uses systemd's socket activation feature to refer to /lib/systemd/system/docker.socket.</p>
          </blockquote>
          <p>Reload the unit files:</p>
          <pre class="prismjs line-numbers"><code class="language-plaintext">$ sudo systemctl daemon-reload
</code></pre>
          <p>Restart the docker daemon with new startup options:</p>
          <pre class="prismjs line-numbers"><code class="language-plaintext">$ sudo systemctl restart docker.service
</code></pre>
          <p>Ensure that anyone that has access to the TCP listening socket is a trusted user since access to the docker daemon is root-equivalent.</p>
          <h1 class="toc-header" id="additional-documentation"> Additional Documentation</h1>
          <ul>
            <li><a class="is-external-link" href="https://docs.docker.com/engine/security/">https://docs.docker.com/engine/security/</a></li>
          </ul>
          <p>&nbsp;</p>
        </td>
      </tr>
    </tbody>
  </table>
</figure>
</div>


## Upgrade
From the Portainer website, select Images.  Pull the latest portainer image.  Since the _portainer/portainer:latest_ tag is already in use, the latest version will be _portainer/portainer:\<none\>_.

```
$ docker stop portainer<current_version>
$ docker rm portainer<current_version>
$ #  DON'T RECREATE VOLUME  # docker volume create portainer_data
$ docker run -d -p 8000:8000 -p 9000:9000 --name=portainer-ce_<new_version> --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce
```

## Backup
> TBD
{.is-info}

## Reference
> TBD
{.is-info}

## Support Files
> TBD
{.is-info}


    
# Dream Machine

## Tabs {.tabset}

### Overview
The network uses a Pi-hole domain name server.  The Pi-hole server provides both DNS lookup and filtering.  It utilizes various lists of known ad web sites to prevent them from being accessed.  

This server runs as podman container on the UDM router.  Although it is hosted on the UDM router (192.168.1.1), it appears on the network with its own MAC address.  The container resides on VLAN 5, which is a MACVLan network using the UDM router as it's network interface.

### Initial Setup
### Configuration
### Backup
### Reference
https://github.com/boostchicken/udm-utilities/tree/master/on-boot-script

https://github.com/boostchicken/udm-utilities/tree/master/run-pihole

http://192.168.5.3/admin/queries.php

https://github.com/boostchicken/udm-utilities/blob/master/cni-plugins/20-dns.conflist

https://github.com/boostchicken/udm-utilities/blob/master/dns-common/on_boot.d/10-dns.sh
### Support Files
10-dns.sh

20-dns.conflist

pihole.sh
