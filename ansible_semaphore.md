---
title: Ansible Semaphore
description: Installation and configuration of Ansible Semaphore
published: true
date: 2024-05-08T15:46:13.652Z
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

Change the root password? [Y/n] Y   (xxxxx)
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
### Creating Database, User for Semaphore
```
mysql -u root -p
```
To create database for Semaphore.

```
CREATE DATABASE `semaphore`;
```
To create and password.
```
CREATE USER 'semaphore' IDENTIFIED BY 'CHANGE-PASSWORD';
```
To Grant usages.
```
GRANT USAGE ON *.* TO 'semaphore'@localhost IDENTIFIED BY 'CHANGE-PASSWORD';
```
To grant all privileges.
```
GRANT ALL privileges ON `semaphore`.* TO 'semaphore'@localhost;
```
To flush privileges.
```
FLUSH PRIVILEGES;
```
    Note: We need to change username, password and database name in real environment.

### Install Semaphore Web UI
Install the debian binary package.
```
wget https://github.com/ansible-semaphore/semaphore/releases/\
download/v2.8.75/semaphore_2.8.75_linux_amd64.deb
sudo dpkg -i semaphore_2.8.75_linux_amd64.deb
```
Setup Semaphore by using the following command:
```
chris@Winterfell:~/Downloads$ semaphore setup

Hello! You will now be guided through a setup to:

1. Set up configuration for a MySQL/MariaDB database
2. Set up a path for your playbooks (auto-created)
3. Run database Migrations
4. Set up initial semaphore user & password

What database to use:
   1 - MySQL
   2 - BoltDB
   3 - PostgreSQL
 (default 1): 1

db Hostname (default 127.0.0.1:3306): 

db User (default root): 

db Password: <store securely outside the repository>

db Name (default semaphore): 

Playbook path (default /tmp/semaphore): 

Public URL (optional, example: https://example.com/semaphore): 

Enable email alerts? (yes/no) (default no): 

Enable telegram alerts? (yes/no) (default no): 

Enable slack alerts? (yes/no) (default no): 

Enable Rocket.Chat alerts? (yes/no) (default no): 

Enable Microsoft Team Channel alerts? (yes/no) (default no): 

Enable LDAP authentication? (yes/no) (default no): 

Config output directory (default /home/chris/Downloads): 

Running: mkdir -p /home/chris/Downloads..
Configuration written to /home/chris/Downloads/config.json..
 Pinging db..
Running db Migrations..
Executing migration v0.0.0 (at 2024-05-08 11:12:25.069642672 -0400 EDT m=+84.977603774)...
Creating migrations table
 [12/0]8]
Executing migration v1.0.0 (at 2024-05-08 11:12:25.267527689 -0400 EDT m=+85.175488302)...
 [4/87]
Executing migration v1.2.0 (at 2024-05-08 11:12:25.363494078 -0400 EDT m=+85.271454691)...
 [2/0]6]
Executing migration v1.3.0 (at 2024-05-08 11:12:25.382867579 -0400 EDT m=+85.290828611)...
 [4/0]]
Executing migration v1.4.0 (at 2024-05-08 11:12:25.442458698 -0400 EDT m=+85.350419730)...
 [5/0]]]
Executing migration v1.5.0 (at 2024-05-08 11:12:25.514378732 -0400 EDT m=+85.422339764)...
 [4/0]]]
Executing migration v1.6.0 (at 2024-05-08 11:12:25.579022232 -0400 EDT m=+85.486983334)...
 [5/0]]
Executing migration v1.7.0 (at 2024-05-08 11:12:25.655417115 -0400 EDT m=+85.563377728)...
 [2/0]]
Executing migration v1.8.0 (at 2024-05-08 11:12:25.677418183 -0400 EDT m=+85.585379285)...
 [2/0]]
Executing migration v1.9.0 (at 2024-05-08 11:12:25.698656076 -0400 EDT m=+85.606617597)...
 [2/0]]
Executing migration v2.2.1 (at 2024-05-08 11:12:25.720144496 -0400 EDT m=+85.628106017)...
 [5/0]]]
Executing migration v2.3.0 (at 2024-05-08 11:12:25.759539293 -0400 EDT m=+85.667499906)...
 [4/0]]
Executing migration v2.3.1 (at 2024-05-08 11:12:25.816521283 -0400 EDT m=+85.724482385)...
 [7/0]]]
Executing migration v2.3.2 (at 2024-05-08 11:12:25.902982094 -0400 EDT m=+85.810943126)...
 [6/0]]]
Executing migration v2.4.0 (at 2024-05-08 11:12:25.948960442 -0400 EDT m=+85.856921055)...
 [2/0]]
Executing migration v2.5.0 (at 2024-05-08 11:12:25.969916867 -0400 EDT m=+85.877877410)...
 [2/0]]
Executing migration v2.5.2 (at 2024-05-08 11:12:25.991024014 -0400 EDT m=+85.898985605)...
 [2/0]]
Executing migration v2.7.1 (at 2024-05-08 11:12:26.012159866 -0400 EDT m=+85.920120898)...
 [2/0]]
Executing migration v2.7.4 (at 2024-05-08 11:12:26.050438779 -0400 EDT m=+85.958399322)...
 [2/0]]
Executing migration v2.7.6 (at 2024-05-08 11:12:26.084525989 -0400 EDT m=+85.992486601)...
 [2/0]6]
Executing migration v2.7.8 (at 2024-05-08 11:12:26.089309543 -0400 EDT m=+85.997270156)...
 [4/57]
Executing migration v2.7.9 (at 2024-05-08 11:12:26.173374876 -0400 EDT m=+86.081335907)...
 [2/77]
Executing migration v2.7.10 (at 2024-05-08 11:12:26.219827598 -0400 EDT m=+86.127788630)...
 [1/43]
Executing migration v2.7.12 (at 2024-05-08 11:12:26.243877514 -0400 EDT m=+86.151838057)...
 [3/0]]
Executing migration v2.7.13 (at 2024-05-08 11:12:26.330226507 -0400 EDT m=+86.238187539)...
 [3/0]2]
Executing migration v2.8.0 (at 2024-05-08 11:12:26.363353164 -0400 EDT m=+86.271314265)...
 [8/0]]
Executing migration v2.8.1 (at 2024-05-08 11:12:26.526648171 -0400 EDT m=+86.434609203)...
 [1/63]
Executing migration v2.8.7 (at 2024-05-08 11:12:26.570954684 -0400 EDT m=+86.478915716)...
 [1/43]
Executing migration v2.8.8 (at 2024-05-08 11:12:26.59807665 -0400 EDT m=+86.506037682)...
 [2/98]]
Executing migration v2.8.20 (at 2024-05-08 11:12:26.671032039 -0400 EDT m=+86.578993070)...
 [3/0]9]
Executing migration v2.8.25 (at 2024-05-08 11:12:26.704623571 -0400 EDT m=+86.612584603)...
 [5/0]]]
Executing migration v2.8.26 (at 2024-05-08 11:12:26.806610995 -0400 EDT m=+86.714572027)...
 [2/0]]
Executing migration v2.8.36 (at 2024-05-08 11:12:26.829638478 -0400 EDT m=+86.737599091)...
 [4/0]]
Executing migration v2.8.38 (at 2024-05-08 11:12:26.895472454 -0400 EDT m=+86.803433066)...
 [9/0]]]
Executing migration v2.8.39 (at 2024-05-08 11:12:26.944289365 -0400 EDT m=+86.852250397)...
 [8/0]]]
Executing migration v2.8.40 (at 2024-05-08 11:12:27.033322987 -0400 EDT m=+86.941284089)...
 [7/0]]
Executing migration v2.8.42 (at 2024-05-08 11:12:27.196253274 -0400 EDT m=+87.104214306)...
 [1/26]
Executing migration v2.8.51 (at 2024-05-08 11:12:27.217723395 -0400 EDT m=+87.125684497)...
 [3/0]]
Executing migration v2.8.57 (at 2024-05-08 11:12:27.258086986 -0400 EDT m=+87.166047529)...
 [3/0]]
Executing migration v2.8.58 (at 2024-05-08 11:12:27.300533438 -0400 EDT m=+87.208494539)...
 [1/57]
Executing migration v2.8.91 (at 2024-05-08 11:12:27.32074345 -0400 EDT m=+87.228704062)...
 [3/46]
Executing migration v2.9.6 (at 2024-05-08 11:12:27.363863119 -0400 EDT m=+87.271823732)...
 [1/341]
Executing migration v2.9.46 (at 2024-05-08 11:12:27.380179587 -0400 EDT m=+87.288140689)...
 [2/0]]
Executing migration v2.9.60 (at 2024-05-08 11:12:27.40138172 -0400 EDT m=+87.309342752)...
 [5/0]6]
Executing migration v2.9.61 (at 2024-05-08 11:12:27.474488878 -0400 EDT m=+87.382450469)...
 [9/0]4]
Executing migration v2.9.62 (at 2024-05-08 11:12:27.596723052 -0400 EDT m=+87.504683595)...
 [5/0]4]
Executing migration v2.9.70 (at 2024-05-08 11:12:27.71129774 -0400 EDT m=+87.619258772)...
 [3/0]]
Migrations Finished


 > Username: semaphore
 > Email: chris.wyse@wysechoice.net
WARN[0141] no rows in result set                         fields.level=Warn
 > Your name: Chris Wyse
 > Password: <store securely outside the repository>

 You are all setup Chris Wyse!
 Re-launch this program pointing to the configuration file

./semaphore server --config /home/chris/Downloads/config.json

 To run as daemon:

nohup ./semaphore server --config /home/chris/Downloads/config.json &

 You can login with chris.wyse@wysechoice.net or semaphore.
chris@Winterfell:~/Downloads$ sudo mkdir /etc/semaphore
chris@Winterfell:~/Donwloads$ sudo mv /home/chris/Downloads/config.json /etc/semaphore/config.json

```
### Create the semaphore user

```
chris@Winterfell:~$ sudo adduser semaphore
[sudo] password for chris: 
Adding user `semaphore' ...
Adding new group `semaphore' (1001) ...
Adding new user `semaphore' (1001) with group `semaphore' ...
Creating home directory `/home/semaphore' ...
Copying files from `/etc/skel' ...
New password: 
Retype new password: 
passwd: password updated successfully
Changing the user information for semaphore
Enter the new value, or press ENTER for the default
	Full Name []: Chris Wyse
	Room Number []: 
	Work Phone []: 
	Home Phone []: 
	Other []: 
Is the information correct? [Y/n] Y
chris@Winterfell:~$
```

### Configure Semaphore as a Service
Create /etc/system/system/semaphore.service.
```[Unit]
Description=Ansible Semaphore
Documentation=https://docs.ansible-semaphore.com/
Wants=network-online.target
After=network-online.target
ConditionPathExists=/usr/bin/semaphore
ConditionPathExists=/etc/semaphore/config.json

[Service]
ExecStart=/usr/bin/semaphore server --config /etc/semaphore/config.json
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=10s
User=semaphore
Group=semaphore

[Install]
WantedBy=multi-user.target
```
Start and enable the service:
```
sudo systemctl start semaphore
sudo systemctl enable semaphore
sudo system status semaphore
```