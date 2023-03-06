---
title: UDM Boot Script Utility
description: Configuration and setup for the unifi-utilities on-boot-script package
published: true
date: 2023-03-06T02:33:38.122Z
tags: 
editor: markdown
dateCreated: 2023-03-05T21:43:02.600Z
---

# Reference
The official documentation:  [UDM / UDMPro Boot Script](https://github.com/unifi-utilities/unifios-utilities/raw/main/on-boot-script/README.md)
&nbsp;
https://github.com/unifi-utilities/unifios-utilities/tree/main/on-boot-script

# Installation

Run the commands shown below to get version 1.0.7, or the latest at [https://udm-boot.boostchicken.dev](https://udm-boot.boostchicken.dev).  The first few commands will fail like below if the package wasn't already installed.  

```
root@UDM:~# rm /etc/init.d/udm.sh
rm: cannot remove '/etc/init.d/udm.sh': No such file or directory
root@UDM:~# systemctl disable udmboot
Failed to disable unit: Unit file udmboot.service does not exist.
root@UDM:~# rm /etc/systemd/system/udmboot.service
rm: cannot remove '/etc/systemd/system/udmboot.service': No such file or directory
root@UDM:~# curl -L https://unifi.boostchicken.io/udm-boot_1.0.7_all.deb -o udm-boot_1.0.7_all.deb
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  3502  100  3502    0     0    125      0  0:00:28  0:00:28 --:--:--   940
root@UDM:~# dpkg -i udm-boot_1.0.7_all.deb 
(Reading database ... 39572 files and directories currently installed.)
Preparing to unpack udm-boot_1.0.7_all.deb ...
Unpacking udm-boot (1.0.7) over (1.0.7) ...
Setting up udm-boot (1.0.7) ...
root@UDM:~# systemctl enable udm-boot
root@UDM:~# 
 ```
 After installation, reboot and the udm-boot service should have started:
 ```
 root@UDM:~# systemctl status udm-boot
● udm-boot.service - Run On Startup UDM
   Loaded: loaded (/etc/systemd/system/udm-boot.service; enabled; vendor preset: enabled)
   Active: inactive (dead) since Sun 2023-03-05 17:14:28 EST; 8min ago
      CPU: 2.075s

Mar 05 17:14:19 UDM systemd[1]: Starting Run On Startup UDM...
Mar 05 17:14:19 UDM bash[2704]: udm-boot.service: running /data/on_boot.d/05-install-cni-plugins.sh
Mar 05 17:14:20 UDM bash[2704]: curl: (6) Could not resolve host: github.com
Mar 05 17:14:20 UDM systemd[1]: udm-boot.service: Current command vanished from the unit file, execution of the command list won't be resumed.
Mar 05 17:14:20 UDM bash[2704]: Pouring /data/.cache/cni-plugins/cni-plugins-linux-arm64-latest.tgz
Mar 05 17:14:21 UDM bash[2704]: udm-boot.service: running /data/on_boot.d/06-cni-bridge.sh
Mar 05 17:14:28 UDM systemd[1]: udm-boot.service: Succeeded.
Mar 05 17:14:28 UDM systemd[1]: Started Run On Startup UDM.
Mar 05 17:14:28 UDM systemd[1]: udm-boot.service: Consumed 2.075s CPU time.
root@UDM:~# 
```
Note the it didn't actually work correctly yet, since it couldn't resolve github.com.  Therefore, modify /data/on_boot.d/05-install-cni-plugins.sh to include a test to see if the DNS service is running.

```
#!/bin/bash

# Make sure DNS is working
while ! ping -c 1 example.com; do sleep 1; done

# Get DataDir location
DATA_DIR="/data"
case "$(ubnt-device-info firmware || true)" in
```
 