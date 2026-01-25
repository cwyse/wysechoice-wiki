#!/bin/bash

#
# The calls to RsyncBackup.sh utilitize the /etc/rsyncd.conf file on 
# the client system to determine the initial path for the source files.
#
# For example in rsyncd.conf:
#
#   [postgres]
#      path = /home/pi/docker_vols/postgres
#      comment = Home directory
#      read only = true
#      uid = 999
#      uid = 999
# 
# When the RSyncBackup.sh script connects with the client using the postgres source model,
# its current directory on the client will be /home/pi/docker_vols/postgres.  The script will
# change directory from the to the srcpath specified on the command line.
#


#
# Host: Raspberry Pi 4B
# Hostname: rpi4
# Address: 192.168.1.2
# Model(s): 
#   Name: pi
#   Path: /home/pi
#
#   Name: postgres
#   Path: /home/pi/docker_vols/postgres
#
#sshpass -p ${PASSWORD} ssh -t root@${REMOTE_PW} "podman stop pihole"
/share/CACHEDEV1_DATA/backup/RSync/RSyncBackup.sh 192.168.1.2 pi docker_vols/wiki_data
/share/CACHEDEV1_DATA/backup/RSync/RSyncBackup.sh 192.168.1.2 postgres .

#
# Host: Chris-Laptop
# Address: 192.168.1.118
# Model(s): 
#   Name: chris
#   Path: /home/chris
#
#   Name: media
#   Path: /media/chris/DATA
#
/share/CACHEDEV1_DATA/backup/RSync/RSyncBackup.sh 192.168.1.118 chris personal/Pictures
/share/CACHEDEV1_DATA/backup/RSync/RSyncBackup.sh 192.168.1.118 media personal/Pictures

#
# Host: Ubiquiti Dream Machine
# Address: 192.168.1.1
# Model(s): 
#   Name: unifi
#   Path: /
#
# Note: Rsync runs inside unifi-os shell, so path is inside the podman container
#
/share/CACHEDEV1_DATA/backup/RSync/RSyncBackup.sh 192.168.1.1 unifi data/unifi/data/backup/autobackup


