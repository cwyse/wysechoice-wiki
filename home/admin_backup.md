---
title: Backup and Restore
description: 
published: true
date: 2021-11-07T16:01:02.654Z
tags: 
editor: markdown
dateCreated: 2020-12-18T03:10:24.783Z
---


# User Data Backups

User backups are handled in three separate ways.
1. Frequent backups to the QNAP NAS server
2. Long term backups to Google Drive
3. Long term backups to Amazon Glacier

## QNAP NAS Backups

The QNAP NAS initiates RSyncD backups using the BackupAll.sh script in the /share/CACHEDEV1_DATA/backup/RSync directory, which maps to DATAVOL1/backup/RSync in FileManager on the NAS.

This script contains stanzas for each client machine being backed up.  It relies on each client system being configured in advance to allow the NAS to access the system via rsync.  The clients must enable passwordless SSH access from the NAS.

The backups run every night at 2:15AM by the WebCrontab application.  

The backups are all in subdirectories of /share/CACHEDEV1_DATA/backup/RSync, which maps to DATAVOL1/backup/RSync in FileManager on the NAS.  That directory contains two scripts: 
- [BackupAll.sh](/backupall.sh) 
- [RSyncBackup.sh](/rsyncbackup.sh)

The RSyncBackup.sh script handles individual backups.  The starting directory for each backup on the client is based on the source path defined in the client's rsyncd.conf file.  The third parameter of the script is the subdirectory to backup.

Backups are incremental, with a total of seven separate backups saved.  

The backup creates subdirectories beneath the RSync directory with a very specific layout.  The top subdirectory is the remote client name or IP address.  Subdirectories below that are for the specific model (defined in client's rsyncd.conf) being backed up.  The next level _was intended_ to be the path, but currently there is a bug.  Instead, there is a _data_ directory and a _backup.N_ directory for each prior backup.  

Additionally, there is an _.rsync-incremental-backup_ directory that contains the log files.

Reference: https://github.com/pedroetb/rsync-incremental-backup

### Standard Rsyncd Client Configuration

The following is a typical rsyncd.conf file for a client.  It specified 'chris' as the source model, and allows read access to everything below the /home/chris directory.  The RSync backup could backup any directory in the 'chris' home directory.

`/etc/rsyncd.conf`
```
log file = /var/log/rsyncd.log
pid file = /var/run/rsyncd.pid
lock file = /var/run/rsync.lock

[chris]
   path = /home/chris
   comment = Home directory
   read only = true                                                                                                                                
```
Once the rsync configuration is set up, the service should be started and enabled:

```
chris@chris-Precision-7740:/etc$ sudo systemctl start rsync
chris@chris-Precision-7740:/etc$ sudo systemctl enable rsync
Synchronizing state of rsync.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable rsync
chris@chris-Precision-7740:/etc$ 
```


### On the Dream Machine

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

# Google Drive Backups
These backups are intended to be for relatively long term storage.  It's meant to be used if the NAS backup fails.  The backup is initiated from the QNAP NAS.  It runs a scheduled backup to Google Drive once per week.  Backups are stored in a subdirectory of "My Drive/QNAP_Backup".  The backups use the chris.wyse.1965@gmail.com Google account.

Backup Host: qnap.wysechoice.net
Backup Server: drive.google.com
Backup Server Account: chris.wyse.1965@gmail.com
Backup Utility (on host): HBS 3 Hybrid Backup Sync
Data Compression: None
Client Side Encryption Cipher: aes-256-cbc
Message digest: md5
Encryption Password: <store securely outside the repository>

The files are sent to Google Drive after encryption.  The directory structure is maintained, but the specific files will not be available until they are decrypted.  The command to decrypt is:
```
openssl enc -md md5 -aes-256-cbc -d -in <encrypted file> -out <decrypted file>
```
# Amazon Glacier Backup

These backups are intended for very long term storage.  Retrieval is extremely slow (although storage is very cheap).  This is a last resort to recover data.

Like the Google Drive backup, it is initiated from the QNAP NAS.  It runs a scheduled backup to Amazon Glacier once per month.  Backups are stored in a an Amazon vault, 'QNAP_Vault'.  The backups use the chris.wyse@wysechoice.net Amazon account.

Backup Host: qnap.wysechoice.net
Backup Server: aws.amazon.com
Backup Server Account: chris.wyse@wysechoice.net
AWS Access Key ID: <store securely outside the repository>
AWS Secret Access Key: <store securely outside the repository>
AWS Region: us-east-1
Backup Utility (on host): HBS 3 Hybrid Backup Sync
Data Compression: None
Client Side Encryption Cipher: aes-256-cbc
Message digest: md5
Encryption Password: <store securely outside the repository>

Retrieval and deletion requires scripting.  The AWS CLI must be installed, and credentials stored in ~/.aws/credentials, with the config file in ~/.aws/config.

## Retrieval

The files are retrieved via the Amazon CLI using *aws glacier* commands.  The retrieval process is still TBD.

The files are sent to Amazon after encryption.  The directory structure is maintained, but the specific files will not be available until they are decrypted.  The command to decrypt is:
```
openssl enc -md md5 -aes-256-cbc -d -in <encrypted file> -out <decrypted file>
```

## Deletion

Deletion of all archives in the vault may take hours or days.  The easiest was to accomplish the is to run a the script below.  The script requests a list of archives to delete.  It polls for the list every 10 minutes until it is received.  Once received, it issues a delete command for each of the archives found.

Archive deletion script: [delAWSVault](/delawsvault)


> The docker image information in yellow below did not complete successfully.  The shell script above was created to address the problem.  The content below is left as a reference only.
{.is-danger}


> Deletion of all archives in the vault may take hours or days.  The easiest was to accomplish the is to run a docker image.  The image requests a list of archives to delete.  It polls for the list every 10 minutes until it is received.  Once received, it issues a delete command for each of the archives found, then deletes the vault.
> 
> ```
> #!/bin/bash
> 
> AWS_ACCOUNT_ID=741335856197
> AWS_REGION=us-east-1
> AWS_VAULT_NAME=QNAP_Vault
> AWS_OUTPUT='./output.json'
> 
> AWS_CREDENTIALS_JSON='/home/chris/.aws/credentials.json'
> 
> # https://github.com/leeroybrun/glacier-vault-remove
> #docker run -v ${AWS_CREDENTIALS_JSON}:/app/credentials.json -d leeroyb/glacier-vault-remove ${AWS_REGION} [${AWS_VAULT_NAME}|LIST] [DEBUG] [NUM_PROCESSES] [<job_id>|LIST|NEW|LATEST]
> docker run -v ${AWS_CREDENTIALS_JSON}:/app/credentials.json -d leeroyb/glacier-vault-remove ${AWS_REGION} ${AWS_VAULT_NAME} DEBUG 10
> ```
> 
> The credentials for the deletion script should be in JSON format:
> ```
> {
> 	"AWSAccessKeyId": "<set via environment/secret storage>",
> 	"AWSSecretKey":   "<set via environment/secret storage>"
> }
> ```
> The credentials for the CLI:
{.is-warning}

```
[default]
aws_access_key_id=<set via environment/secret storage>
aws_secret_access_key=<set via environment/secret storage>
```
The config for the CLI:
```
[default]
region=us-east-1
output=json
```

# Network Configuration Backup

Network configuration backup is handled separately from user data backup.  The LibreNMS application is used to consolidate various configurations.  

LibreNMS will probably back up to GitLab.  It will run as a stack of docker containers, which will be used for additional network support, like reverse proxy, syslog server, and other network tools.

https://codingpackets.com/blog/oxidized-gitlab-storage-backend/

# General Backup
**Current backup location**: chris-Precision-7740:/home/chris/personal/backups

# Postgres Backup
**Current backup location**: <postgres_host>:~/docker_vols/postgres

### Complete Database Backup / Restore
The `<postgres-username>` should be the owner of the postgres database.  Usually *postgres* is the owner of the postgres database.
  
```
$ # Dump database to <backup-clean-file>
$ pg_dumpall --verbose --clean --host=<postgres-server> --port 5432 --username=<postgres-username> --file=<backup-clean-file>
$
$ # Restore database from <backup-clean-file>, dropping existing tables
$ psql --host=<postgres-server> --port 5432 --file=<backup-clean-file> --dbname=postgres --echo-all --log-file=<backup-clean-log-file> --output=<backup-clean-output-file> --username=<postgres-username>
$
$ # Dump database to <backup-file>
$ pg_dumpall --verbose --host=<postgres-server> --port 5432 --username=<postgres-username> --file=<backup-file>
$
$ # Restore all databases from <backup-file>
$ psql --host=<postgres-server> --port 5432 --file=<backup-file> --dbname=postgres --echo-all --log-file=<backup-log-file> --output=<backup-output-file> --username=<postgres-username>
```
Example backup:

- postgres-server:  192.168.40.30
- postgres-username: postgres
- backup-clean-file: backup.clean.file
- ~/.pgpass:
    - 192.168.40.30:5432:*:wikijs:wikijsrocks
    
```
$ pg_dumpall --verbose --clean --host 192.168.40.30 --port 5432 --username postgres --file backup.clean.file
```
Example restore:

- postgres-server:  192.168.40.30
- postgres-username: xwiki
- backup-clean-file: backup.clean.file
- ~/.pgpass:
    - 192.168.40.30:5432:*:wikijs:wikijsrocks

```
$ psql --host=192.168.40.30 --port 5432 --file=backup.clean.file --dbname=postgres --echo-all --log-file=backup.clean.file.log --output=backup.clean.file.out -U xwiki
```
You need to restart the postgres server to update the ownership of the databases.