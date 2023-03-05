---
title: UDM Boot Script Utility
description: Configuration and setup for the unifi-utilities on-boot-script package
published: true
date: 2023-03-05T22:23:55.617Z
tags: 
editor: markdown
dateCreated: 2023-03-05T21:43:02.600Z
---

# Installation
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