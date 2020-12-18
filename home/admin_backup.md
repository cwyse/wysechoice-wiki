---
title: Backup and Restore
description: 
published: true
date: 2020-12-18T03:10:24.783Z
tags: 
editor: markdown
dateCreated: 2020-12-18T03:10:24.783Z
---

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