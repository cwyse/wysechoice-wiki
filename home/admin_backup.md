---
title: Backup and Restore
description: 
published: true
date: 2021-02-07T19:51:30.452Z
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

This script contains stanzas for each client machine being backed up.  It relies on each client system being configured in advance to allow the NAS to access the system via rsync.  The clients have the option of enabling passwordless SSH access from the NAS, or adding a username and password to the BackupAll.sh script.  For example:
	`sshpass -p ${PASSWORD} ssh -t root@${REMOTE_PW} "podman stop pihole"`
where PASSWORD and REMOTE_PW are set ???


The backups run every night at 2:15AM.  The backups are all in subdirectories of /share/CACHEDEV1_DATA/backup/RSync, which maps to DATAVOL1/backup/RSync in FileManager on the NAS.  That directory contains two scripts: BackupAll.sh and RSyncBackup.sh.  The RSyncBackup.sh script handles individual backups.  Backups are incremental, with a total of seven separate backups saved.  Subdirectories are: `<remote>/<model>/<path>/data`.  In addition to the data directory, backup.N directories are used for prior backups.
  
The BackupAll.sh script is executed nightly by a cron job.  
https://github.com/pedroetb/rsync-incremental-backup

### Standard Rsyncd configuration
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

```
chris@chris-Precision-7740:/etc$ sudo systemctl start rsync
chris@chris-Precision-7740:/etc$ sudo systemctl enable rsync
Synchronizing state of rsync.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable rsync
chris@chris-Precision-7740:/etc$ 
```


### On the Dream Machine
`/mnt/data/on_boot.d/20-rsync.sh`
```
#!/usr/bin/env bash                                                       
                                                                                      
systemctl stop rsync                                                                           

## 
## These are the master copies of                 
## /etc/rsyncd.conf & /etc/rsyncd.secrets.         
## They are overwritten with this content
## every time the container boots.              
##
cat << RSYNCD.CONF >/etc/rsyncd.conf                                                           log file = /var/log/rsyncd.log                                                                 pid file = /var/run/rsyncd.pid                                                                 lock file = /var/run/rsync.lock 

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

systemctl start rsync                                                                           systemctl enable rsync                                                                         
```

Create the file, the type execute the following commands:
```
unifi-os shell
sudo apt install rsync -y
ssh-proxy /mnt/data/on_boot.sh
```

#### NAS Storage Spaces
The backups run every night at 2:15AM.  The backups are all in subdirectories of /share/CACHEDEV1_DATA/backup/RSync, which maps to DATAVOL1/backup/RSync in FileManager on the NAS.  That directory contains two scripts: BackupAll.sh and RSyncBackup.sh.  The RSyncBackup.sh script handles individual backups.  Backups are incremental, with a total of seven separate backups saved.  Subdirectories are: `<remote>/<model>/<path>/data`.  In addition to the data directory, backup.N directories are used for prior backups.
  
The BackupAll.sh script is executed nightly by a cron job.  

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
> 	"AWSAccessKeyId": "<store securely outside the repository>",
> 	"AWSSecretKey":   "<store securely outside the repository>"
> }
> ```
> The credentials for the CLI:
{.is-warning}

```
[default]
aws_access_key_id=<store securely outside the repository>
aws_secret_access_key=<store securely outside the repository>
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