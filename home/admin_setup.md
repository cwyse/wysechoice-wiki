---
title: Initial Setup
description: Initial configuration for various components
published: true
date: 2021-02-01T03:28:39.504Z
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

## Rsyncd
This is required for backup purposes.  It should be set to restart on-failure by updating the /etc/systemd/system/mult-user.target.wants/rsync.service to include
```
Restart=on-failure
RestartSec=20s
```
in the [Service] stanza.