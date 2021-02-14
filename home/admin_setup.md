---
title: Initial Setup
description: Initial configuration for various components
published: true
date: 2021-02-14T09:40:22.588Z
tags: 
editor: markdown
dateCreated: 2021-02-01T03:28:39.504Z
---

# Raspberry PI 4
The Raspberry PI 4 image should be:

xxxxxx

It should have the following packages installed:

docker
rsync
...

A docker network should be created at installation time even if it is not configured in the router.

## Timezone
Docker images (or at least containers) should run `dpkg-reconfigure tzdata` to set the timezone to New York.

## Rsyncd
This is required for backup purposes.  It should be set to restart on-failure by updating the /etc/systemd/system/mult-user.target.wants/rsync.service to include
```
Restart=on-failure
RestartSec=20s
```
in the [Service] stanza.

# Cloudflare Certificates

Cloudflare certificates have been created and installed on the QNAP NAS under *Control Panel->Security->Certificate & Private Key*.  Copies of these keys and certificates are also attached to this web page.

The origin certificate was created in Cloudflare, for hosts `*.wysechoice.net,wysechoice.net`.
The origin certificate is named *wysechoice.net.cert.pem*, and expires
in 2035.  The associated key was stored in the same directory, in *wysechoice.net.key.pem*.  

Cloudflare requires an intermediate certificate thate can be downloaded from their site:
  https://support.cloudflare.com/hc/article_attachments/360037885371/origin_ca_rsa_root.pem
It needs to be installed into /etc/ssl/certs of any image using these certificates either through the command line or throught the QNAP GUI.

Some applications require a certificate bundle containing the primary certificate (wysechoice.net.cert.pem) and
the intermediate certificate (origin_ca_rsa_root.pem) concatenated into a single file:
    `cat wysechoice.net.cert.pem origin_ca_rsa_root.pem >> bundle.crt`
The bundle needs to be installed in /etc/ssl/certs with the others if needed.

[wysechoice.net.cert.pem](/wysechoice.net.cert.pem) 
[wysechoice.net.key.pem](/wysechoice.net.key.pem)
[origin_ca_rsa_root.pem](/origin_ca_rsa_root.pem)