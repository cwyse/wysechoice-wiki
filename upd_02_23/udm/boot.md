---
title: UDM Boot Script Utility
description: Configuration and setup for the unifi-utilities on-boot-script package
published: true
date: 2023-03-06T07:05:55.403Z
tags: 
editor: markdown
dateCreated: 2023-03-05T21:43:02.600Z
---

# Reference
The official documentation:  [UDM / UDMPro Boot Script](https://github.com/unifi-utilities/unifios-utilities/raw/main/on-boot-script-2.x/README.md)
&nbsp;
https://github.com/unifi-utilities/unifios-utilities/tree/main/on-boot-script-2.x
# Installation

Run the commands shown below to get version 1.0.7, or the latest at [https://udm-boot.boostchicken.dev](https://udm-boot.boostchicken.dev).  The first few commands will fail like below if the package wasn't already installed.  


Run the commands shown below to get version 1.0.7, or the latest at [https://udm-boot.boostchicken.dev](https://udm-boot.boostchicken.dev).  The first few commands will fail like below if the package wasn't already installed.  

## Clean (optional)

Start the install with a clean slate by running the following commands, ignoring any errors:
```
apt remove udm-boot
dpkg --purge udm-boot
systemctl stop udm-boot
systemctl disable udm-boot
rm /etc/systemd/system/udm-boot.service
rm /etc/systemd/system/udm-boot.service
rm /usr/lib/systemd/system/udm-boot.service
rm /usr/lib/systemd/system/udm-boot.service
systemctl daemon-reload
systemctl reset-failed
```
After execution of these commands, all traces of udm-boot should be gone:
```
root@UDM:~# find / -name "udm-boot*"
root@UDM:~# 
```

## Install
Now install the [udm-boot-2x_1.0.1_all.deb](https://github.com/unifi-utilities/unifios-utilities/blob/main/on-boot-script-2.x/packages/udm-boot-2x_1.0.1_all.deb?raw=true) (or later) using the following commands:
```
cd
curl -L https://github.com/unifi-utilities/unifios-utilities/blob/main/on-boot-script-2.x/packages/udm-boot-2x_1.0.1_all.deb?raw=true -o udm-boot-2x_1.0.1_all.deb
dpkg -i udm-boot-2x_1.0.1_all.deb
systemctl enable udm-boot
```
After installation, reboot and the udm-boot service should have started, and the package should be installed:
 ```
root@UDM:/data/on_boot.d# systemctl status udm-boot
● udm-boot.service - Run On Startup UDM 2.x
   Loaded: loaded (/lib/systemd/system/udm-boot.service; enabled; vendor preset: enabled)
   Active: active (exited) since Sun 2023-03-05 22:37:40 EST; 2min 20s ago
 Main PID: 15806 (code=exited, status=0/SUCCESS)
    Tasks: 0 (limit: 2388)
   Memory: 0B
      CPU: 0
   CGroup: /system.slice/udm-boot.service

Mar 05 22:37:40 UDM systemd[1]: Started Run On Startup UDM 2.x.
Mar 05 22:37:40 UDM bash[15806]: udm-boot.service: running /data/on_boot.d/05-install-cni-plugins.sh
Mar 05 22:37:40 UDM bash[15806]: Pouring /data/.cache/cni-plugins/cni-plugins-linux-arm64-v1.2.0.tgz
Mar 05 22:37:42 UDM bash[15806]: udm-boot.service: running /data/on_boot.d/06-cni-bridge.sh
root@UDM:/data/on_boot.d# apt list --installed|grep udm-boot

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

udm-boot-2x/now 1.0.1 all [installed,local]
root@UDM:/data/on_boot.d# 


```

Now that the package has been successfully installed, it can be used to start additional services by adding a startup script to the /data/on_boot.d directory.

# Update

To update, perform the same steps as the installation.