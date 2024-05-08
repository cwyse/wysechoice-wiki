---
title: Ansible Semaphore
description: Installation and configuration of Ansible Semaphore
published: true
date: 2024-05-08T14:52:09.026Z
tags: 
editor: markdown
dateCreated: 2024-05-08T14:52:09.026Z
---

# Ansible Semaphore

## Installation
- Repository: https://github.com/semaphoreui/semaphore.git
- Documentation: 
  - https://docs.semui.co/
  - https://www.devopstricks.in/installing-semaphore-web-ui-for-ansible-on-ubuntu-22-04-lts/
- Binaries: https://github.com/semaphoreui/semaphore/releases/

### Install MariaDB Server
```
sudo apt-get update -y
sudo apt-get install mariadb-server -y
```
### Secure the installation
```
chris@Winterfell:~/Downloads$ sudo mysql_secure_installation

NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MariaDB
      SERVERS IN PRODUCTION USE!  PLEASE READ EACH STEP CAREFULLY!

In order to log into MariaDB to secure it, we'll need the current
password for the root user. If you've just installed MariaDB, and
haven't set the root password yet, you should just press enter here.

Enter current password for root (enter for none): 
OK, successfully used password, moving on...

Setting the root password or using the unix_socket ensures that nobody
can log into the MariaDB root user without the proper authorisation.

You already have your root account protected, so you can safely answer 'n'.

Switch to unix_socket authentication [Y/n] n
 ... skipping.

You already have your root account protected, so you can safely answer 'n'.

Change the root password? [Y/n] n
 ... skipping.

By default, a MariaDB installation has an anonymous user, allowing anyone
to log into MariaDB without having to have a user account created for
them.  This is intended only for testing, and to make the installation
go a bit smoother.  You should remove them before moving into a
production environment.

Remove anonymous users? [Y/n] y
 ... Success!

Normally, root should only be allowed to connect from 'localhost'.  This
ensures that someone cannot guess at the root password from the network.

Disallow root login remotely? [Y/n] y
 ... Success!

By default, MariaDB comes with a database named 'test' that anyone can
access.  This is also intended only for testing, and should be removed
before moving into a production environment.

Remove test database and access to it? [Y/n] y
 - Dropping test database...
 ... Success!
 - Removing privileges on test database...
 ... Success!

Reloading the privilege tables will ensure that all changes made so far
will take effect immediately.

Reload privilege tables now? [Y/n] y
 ... Success!

Cleaning up...

All done!  If you've completed all of the above steps, your MariaDB
installation should now be secure.

Thanks for using MariaDB!
chris@Winterfell:~/Downloads$ 
```
Make sure python3 and python3-pip are installed:
```
chris@Winterfell:~/Downloads$ python3 --version
Python 3.10.12
```
```
chris@Winterfell:~/Downloads$ pip3 --version
Command 'pip3' not found, but can be installed with:
sudo apt install python3-pip
chris@Winterfell:~/Downloads$
```
If necessary, install python3 and/or python3-pip:
```
sudo apt update
sudo apt install python3
sudo apt install python3-pip
```
Installation of python3-pip required fixing a  broken install:
```
sudo apt --fix-broken install

```
```
chris@Winterfell:~/Downloads$ pip3 --version
pip 22.0.2 from /usr/lib/python3/dist-packages/pip (python 3.10)
chris@Winterfell:~/Downloads$ 
```
Install Ansible:
```
sudo apt-get -y install software-properties-common
sudo apt-add-repository -y ppa:ansible/ansible
sudo apt-get -y update
sudo apt-get -y install ansible
```

Install dependencies:
```
sudo apt-get -y install python3-passlib
```

### Download the latest release:
```
chris@Winterfell:~/Downloads$ wget https://github.com/semaphoreui/semaphore/releases/download/v2.9.75/semaphore_2.9.75_linux_amd64.deb
--2024-05-08 09:55:23--  https://github.com/semaphoreui/semaphore/releases/download/v2.9.75/semaphore_2.9.75_linux_amd64.deb
Resolving github.com (github.com)... 140.82.112.4
Connecting to github.com (github.com)|140.82.112.4|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://objects.githubusercontent.com/github-production-release-asset-2e65be/23267883/db9a42d2-d849-4d22-8599-618299a03e0a?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=<store securely outside the repository>%2F20240508%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240508T135523Z&X-Amz-Expires=300&X-Amz-Signature=f886fc5b5e9740ec66977821748d9e99474a239fa2171dbb558d150ebfddd232&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=23267883&response-content-disposition=attachment%3B%20filename%3Dsemaphore_2.9.75_linux_amd64.deb&response-content-type=application%2Foctet-stream [following]
--2024-05-08 09:55:23--  https://objects.githubusercontent.com/github-production-release-asset-2e65be/23267883/db9a42d2-d849-4d22-8599-618299a03e0a?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=<store securely outside the repository>%2F20240508%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240508T135523Z&X-Amz-Expires=300&X-Amz-Signature=f886fc5b5e9740ec66977821748d9e99474a239fa2171dbb558d150ebfddd232&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=23267883&response-content-disposition=attachment%3B%20filename%3Dsemaphore_2.9.75_linux_amd64.deb&response-content-type=application%2Foctet-stream
Resolving objects.githubusercontent.com (objects.githubusercontent.com)... 185.199.108.133, 185.199.110.133, 185.199.109.133, ...
Connecting to objects.githubusercontent.com (objects.githubusercontent.com)|185.199.108.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 10109064 (9.6M) [application/octet-stream]
Saving to: ‘semaphore_2.9.75_linux_amd64.deb’

semaphore_2.9.75_linux_amd64.deb                  100%[============================================================================================================>]   9.64M  29.5MB/s    in 0.3s    

2024-05-08 09:55:24 (29.5 MB/s) - ‘semaphore_2.9.75_linux_amd64.deb’ saved [10109064/10109064]

chris@Winterfell:~/Downloads$
```

Your content here