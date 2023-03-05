---
title: Unifi Dream Machine Router
description: All aspects of maintenance for the Unifi Dream Machine router configuration
published: true
date: 2023-03-05T19:10:34.928Z
tags: 
editor: markdown
dateCreated: 2023-03-05T19:10:34.928Z
---

# UDM Route Configuration & Maintenance

## UDM Base configuration
### General
### Backup

The Dream Machine configuration is backed up to both the Unifi Cloud and to the QNAP NAS.  The cloud backup should always be enabled in the UDM console settings.  The [Cloud Config Backup](https://192.168.1.1/settings/system) page shows whether it is enabled or not, and is the support page used to restore and/or backup a configuration to/from the cloud.




The Dream Machine is a special configuration case, since when the NAS backup connects with the RSync daemon, it is running inside of the podman container.  The configuration of rsyncd.conf needs to be inside the container as well, yet it would typically be lost once the container is recreated (e.g. on a firmware update).

This situation is circumvented through a somewhat complex path to update the appropriate files.  Specifically, the rsyncd.conf file gets created when the container boots.  Additionally, it requires support to ensure the the rsync daemon stays running.

The solution relies on the udm-boot package.  This package provides an on_boot.d directory that perists through firmware updates.  Any scripts in the directory will be executed when the container boots.  However, these scripts run on the _host_ operating system, not the container.

The commands for the rsync support need to be executed in the container.  The solution was to create a script in the on_boot.d directory that supports executing scripts in the container using the `podman exec` command.  The 99-on-boot-podman.sh script provides that support by executing any scripts found in ../podman/on_boot.d using the `podman exec` command.

`/mnt/data/on_boot.d/99-on-boot-podman.sh`
```
#!/bin/sh
      
# Persistent bootup scripts
ON_BOOT_DIR=/mnt/data/on_boot.d
                               
# Persistent bootup scripts executed in podman container
POD_BOOT_DIR=/mnt/data/podman/on_boot.d                 
                                       
# Shared directory used by podman container
SHARED_DIR=/mnt/persistent                 
                          
echo "Executing $ON_BOOT_DIR/99_on_boot_podman.sh"
if [ -d $POD_BOOT_DIR ]; then                     
    # Copy to location accessible to podman container
    cp -rfp $POD_BOOT_DIR $SHARED_DIR                
    for i in $SHARED_DIR/on_boot.d/*.sh; do
        if [ -r $i ]; then                 
            podman exec unifi-os $i
        fi                         
    done  
fi      
  
# Make sure rsync is installed in unifi-os container
podman exec unifi-os apt install rsync -y           
                                         
echo "Finished $ON_BOOT_DIR/99_on_boot_podman.sh"

```

The script below update the rsyncd.conf file in the podman container to make the directory available to the NAS.  It also updates a crontab on the UDM to restart the rsync daemon each night at 1:10 AM.  If the daemon had trapped during the day or had been stopped, the cronjob will restart it prior to the backup later that night.

`/mnt/data/podman/on_boot.d/20-rsync.sh`
```
#!/usr/bin/env bash                                                       
                                                                                      
systemctl stop rsync                                                                           

## 
## These are the master copies of                 
## /etc/rsyncd.conf & /etc/rsyncd.secrets.         
## They are overwritten with this content
## every time the container boots.              
##
cat << RSYNCD.CONF >/etc/rsyncd.conf 
log file = /var/log/rsyncd.log                                                                 
pid file = /var/run/rsyncd.pid                                                                 
lock file = /var/run/rsync.lock 

[unifi]
   path = /          
   comment = Root directory                
   read only = true
   uid = 902
   gid = 902
RSYNCD.CONF                                                                                     

#
# If the rsync daemon is stopped (possibly be a firmware update) without a reboot,
# it won't be restarted by systemd.  The default service doesn't have the Restart=on-failure
# set.                                        
#
# To get around this problem before the backup at around 2 AM, we enable a cron job that
# hopefully persists through an update.  If not, the alternative would be to restart it
# either remotely or from the pi-hole container.
#
SYSD_CMD="systemctl restart rsync"
CRON_TIME='10 1    * * *   root   '
grep "${SYSD_CMD}" /etc/crontab || echo "${CRON_TIME} ${SYSD_CMD}" >>/etc/crontab

systemctl start rsync               
systemctl enable rsync     

# Restart cron to reread the configuration file
systemctl restart cron

```

For the initial installation, create the files, then execute the following commands:
```
# unifi-os shell
root@ubnt:/# apt install rsync -y
root@ubnt:/# ssh-proxy /mnt/data/on_boot.sh
```
On subsequent boots, the server will be started automatically.

### Restore
If the UDM has failed completely, loosing all configuration data, the first thing to do is to restore internet connectivity.  From a web browser, enter 192.168.1.1 in the URL, and the following screen will be displayed. Press the button to start the setup. 

&nbsp;
<figure>
  <center>
    <img src="/assets/udm_restore/udm_restore.png" width="40%" height="40%" align="center"
       alt="UDM Restore: Initial Screen"></center><center>
    <fig caption>UDM Restore: Initial Screen</figcaption>
  </center>
</figure>

Enter the required information to restore internet connectivity, and then sign into your UI.com account to retrieve the latest backup.  

&nbsp;
<figure>
  <center>
    <img src="/assets/udm_restore/unifi_login.png" width="40%" height="40%" align="center"
       alt="UDM Restore: Unifi Login"></center><center>
    <fig caption>UDM Restore: Unifi Login</figcaption>
  </center>
</figure>

&nbsp;
<figure>
  <center>
    <img src="/assets/udm_restore/udm_backups.png" width="40%" height="40%" align="center"
       alt="UDM Restore: Cloud Backups page"></center><center>
    <fig caption>UDM Restore: Cloud Backups page</figcaption>
  </center>
</figure>

