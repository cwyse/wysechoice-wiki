---
title: Net Applications
description: 
published: true
date: 2022-01-09T16:19:05.444Z
tags: 
editor: markdown
dateCreated: 2022-01-09T15:29:28.378Z
---

# Network Applications

## Label Printing

## Tabs {.tabset}

### Overview
CUPS printing isn't working for the Brother PT-P700 label printer.  However, a combination of programs can be used to generate labels.
[plantlabels.glabels](/plantlabels.glabels)
https://sites.google.com/site/tingox/brother_pt-p700

#### print-driver-ptouch
```
apt install libcup2-dev libxml2 libxml2-dev libxml-libxml-perl
git clone https://github.com/philpem/printer-driver-ptouch.git
cd print-driver-ptouch
rm missing
autoreconf -i
./autogen.sh
./configure
make
make install
cd /etc/init.d
./dbus start
./avahi-daemon start
```
/dev/bus not present:
```
/dev/bus or /dev/serial do not show up under /dev in the container
Try this:

docker run -v /dev/bus:/dev/bus:ro -v /dev/serial:/dev/serial:ro -i -t --entrypoint /bin/bash --cap-add SYS_PTRACE debian:amd64

This will make /dev/bus and /dev/serial show up as bind mounts in your container. Yet you will find that _fastboot devices or adb_ will not work. Strace will show you permission denied. What you want instead is this:


docker run --device=/dev/bus -v /dev/serial:/dev/serial:ro -i -t --entrypoint /bin/bash --cap-add SYS_PTRACE debian:amd64
```

#### gLabels
https://blog.worldlabel.com/2008/glabels-ez-label-creator-for-linux.html

This package supports the creation of labels and mail merge.  The following settings should be used to create a template for the labels.  On the _Page Size_ tab of the template creation:
1. Page Size: Other
2. Width: 520 points
3. Height 128 points

On the _Label or Card Size_ tab:
1. Width: 520
2. Height 128
3. Round: 0
4. Horiz. waste: 0
5. Vert. waste: 0
6. Margin: 14

For the _Layout_ tab: 
1. Number accross: 1
2. Number down: 1
3. Distance from left: 0
4. Distance from top: 0
5. Horizontal pitch: 520
6. Vertical pitch: 128

Create the label, then print it to a PDF.

#### Mail Merge
Create a mail merge in gLabel.  The ghini database contains two views with plant label information: *plant_labels* and *plant_labels_living*.  Either of these views can be used to provide data to the mail merge.

Use pgadmin4, load a view with the desired plants, and export the data as a CSV file.  In gLabels, select Objects->Mail Merge, and import the CSV file.

Load the [PlantLabels template](/plantlabels.glabels), which has merge fields included.  Merge fields are in the format "${merge-field}", where the merge field value is the column header of the CSV file.  Select File->Print, and Print To File, to output the labels to a PDF file.

Convert the PDF file into multiple PNG images:
```
convert output.pdf -crop 520x128 -negate -threshold 0 -negate labels_%d.png
```

> **Update:**
Use the [labelgen.py](/labelgen.py) command to read the database, run the mailmerge, and create the label images.  Parameters must be configured within
the file.
{.is-info}

This file will scp the label file and issue the print command.
[print.py](/print.py)

#### GIMP
Start GIMP and open the PDF from the last step.  Use the default import settings.

Under Image->Mode, select 'Use black and white palette', and _Convert_.  Under _Scale Image_, select:
1. Width: 500 px (unlink)
2. Height 127 px

Set the Print Size to:
1. Width: 1.875 in
2. Height: 0.498 in
3. X res: 360 px/in
4. Y res: 255 px/in

Export the file as a PNG file.

#### PTouch-Print
https://github.com/clarkewd/ptouch-print
https://mockmoon-cybernetics.ch/computer/p-touch2430pc/

Download the ptouch-print git repository and compile it.
```
sudo apt install -y autogen autoconf gettext autopoint gcc libgd-dev libusb-dev libusb-1.0-0-dev make autofs udev dialog 
cd ptouch-print
./autogen.sh
./configure 
make
```
ptouch-print --image <filename.png>



## CUPS

## Tabs {.tabset}

### Overview
Cups is the Linux print daemon.

References:
##### Docker Image
- https://hub.docker.com/r/ydkn/cups
- https://gitlab.com/ydkn/docker-cups

##### Ptouch Print
- Build dependencies
-- git
-- autogen
-- autoreconf
-- gettext
-- autopoint
- https://github.com/clarkewd/ptouch-print


### Initial Setup
Download the QPKG from https://www.qnapclub.eu/en/qpkg/466.  Log in as an administrator to the QNAP machine.  Open the *App Center* and click the *+* next to the :gear: icon in the upper right.  This will open an *Install Manually* dialog box.  Browse to the QPKG file that you downloaded and click the Install button.

### Configuration

#### Client Endpoints
The localhost endpoint is automatically enabled.  Remote hosts need to have their Docker API enabled.  An excerpt from "[How do I enable the remote API for dockerd](https://success.mirantis.com/article/how-do-i-enable-the-remote-api-for-dockerd)" is given below:

```
<div>
<figure style="width:796px;">
  <table style="background-color:rgb(255, 255, 255);">
    <tbody>
      <tr>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;width:55px;">&nbsp;</td>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;width:1107px;">
          <p>&nbsp;</p><div style="font-size:22px">
<!--          <h2  id="how-do-i-enable-the-remote-api-for-dockerd"> --> <strong>How do I enable the remote API for dockerd</strong><hr></div><!--</h2>-->
          <p>After completing these steps, you will have enabled the remote API for dockerd, without editing the systemd unit file in place:</p>
          <p>Create a file at <code>/etc/systemd/system/docker.service.d/startup_options.conf</code> with the below contents:</p>
          <pre><code># /etc/systemd/system/docker.service.d/override.conf
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2376
</code></pre>
          <blockquote>
            <p><strong>Note:</strong> The -H flag binds dockerd to a listening socket, either a Unix socket or a TCP port. You can specify multiple -H flags to bind to multiple sockets/ports. The default -H fd:// uses systemd's socket activation feature to refer to /lib/systemd/system/docker.socket.</p>
          </blockquote>
          <p>Reload the unit files:</p>
          <pre><code>$ sudo systemctl daemon-reload
</code></pre>
          <p>Restart the docker daemon with new startup options:</p>
          <pre><code>$ sudo systemctl restart docker.service
</code></pre>
          <p>Ensure that anyone that has access to the TCP listening socket is a trusted user since access to the docker daemon is root-equivalent.</p><br>
<div style="font-size:25px;color:blue"><!--          <h1  id="additional-documentation">--><strong>Additional Documentation</strong><hr><!--</h1>--></div>
          <ul>
            <li><a href="https://docs.docker.com/engine/security/">https://docs.docker.com/engine/security/</a></li>
          </ul>
          <p>&nbsp;</p>
        </td>
      </tr>
    </tbody>
  </table>
</figure>
</div>
```

### Upgrade
TBD
### Backup
> TBD
The /opt/Portainer/data directory should be backed to retain the configuration.
{.is-info}

### Reference
> TBD
{.is-info}

### Support Files
> TBD
{.is-info}

## Portainer

## Tabs {.tabset}

### Overview
Container maintenance is handled using Portainer running on QNAP.  The QPKG is available on the Qnap.Club at https://www.qnapclub.eu/en/qpkg/466.  Portainer is run as an application on the QNAP machine - not insde a docker container.  The image mounts a volume, /opt/Portainer/data, which stores the portainer database and other customizable data.
<br>
<figure style="width:796px;">
  <table style="background-color:rgb(255, 255, 255);">
    <tbody>
            <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">Web Site</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;"><a href="https://www.portainer.io/">https://www.portainer.io/</a></td>
      </tr>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">Ports</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">127.0.0.1:2375 -&gt; 2375/tcp&nbsp; &nbsp;(Local endpoint URL)<br>0.0.0.0:9123 -&gt; 9123/tcp&nbsp; &nbsp;(Portainer Web Interface)</td>
      </tr>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">Data Volume</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">/opt/Portainer/data</td>
      </tr>
    </tbody>
  </table>
</figure>

### Initial Setup
Download the QPKG from https://www.qnapclub.eu/en/qpkg/466.  Log in as an administrator to the QNAP machine.  Open the *App Center* and click the *+* next to the :gear: icon in the upper right.  This will open an *Install Manually* dialog box.  Browse to the QPKG file that you downloaded and click the Install button.

### Configuration

#### Client Endpoints
The localhost endpoint is automatically enabled.  Remote hosts need to have their Docker API enabled.  An excerpt from "[How do I enable the remote API for dockerd](https://success.mirantis.com/article/how-do-i-enable-the-remote-api-for-dockerd)" is given below:

<div>
<figure style="width:796px;">
  <table style="background-color:rgb(255, 255, 255);">
    <tbody>
      <tr>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;width:55px;">&nbsp;</td>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;width:1107px;">
          <p>&nbsp;</p><div style="font-size:22px">
<!--          <h2  id="how-do-i-enable-the-remote-api-for-dockerd"> --> <strong>How do I enable the remote API for dockerd</strong><hr></div><!--</h2>-->
          <p>After completing these steps, you will have enabled the remote API for dockerd, without editing the systemd unit file in place:</p>
          <p>Create a file at <code>/etc/systemd/system/docker.service.d/startup_options.conf</code> with the below contents:</p>
          <pre><code># /etc/systemd/system/docker.service.d/override.conf
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2376
</code></pre>
          <blockquote>
            <p><strong>Note:</strong> The -H flag binds dockerd to a listening socket, either a Unix socket or a TCP port. You can specify multiple -H flags to bind to multiple sockets/ports. The default -H fd:// uses systemd's socket activation feature to refer to /lib/systemd/system/docker.socket.</p>
          </blockquote>
          <p>Reload the unit files:</p>
          <pre><code>$ sudo systemctl daemon-reload
</code></pre>
          <p>Restart the docker daemon with new startup options:</p>
          <pre><code>$ sudo systemctl restart docker.service
</code></pre>
          <p>Ensure that anyone that has access to the TCP listening socket is a trusted user since access to the docker daemon is root-equivalent.</p><br>
<div style="font-size:25px;color:blue"><!--          <h1  id="additional-documentation">--><strong>Additional Documentation</strong><hr><!--</h1>--></div>
          <ul>
            <li><a href="https://docs.docker.com/engine/security/">https://docs.docker.com/engine/security/</a></li>
          </ul>
          <p>&nbsp;</p>
        </td>
      </tr>
    </tbody>
  </table>
</figure>
</div>

### Upgrade
TBD
### Backup
> TBD
The /opt/Portainer/data directory should be backed to retain the configuration.
{.is-info}

### Reference
> TBD
{.is-info}

### Support Files
> TBD
{.is-info}

## Portainer (old)

## Tabs {.tabset}

### Overview
Container maintenance is handled using the Portainer Docker image.  The image has is locally named according to the version.  In this instance, version 1.24.1 is named portainer1241.  The image mounts a volume, portainer_data, that is maintained across version upgrades.
<br>
<figure style="width:796px;">
  <table style="background-color:rgb(255, 255, 255);">
    <tbody>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">Image</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">portainer/portainer-ce:latest</td>
      </tr>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">Web Site</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;"><a href="https://www.portainer.io/">https://www.portainer.io/</a></td>
      </tr>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">Ports</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">0.0.0.0:8000 -&gt; 8000/tcp&nbsp; &nbsp;(Edge Agent Endpoint) (Currently not used)<br>0.0.0.0:9000 -&gt; 9000/tcp&nbsp; &nbsp;(Portainer Endpoint)</td>
      </tr>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">Data Volume</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">portainer_data</td>
      </tr>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">Network</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">bridge</td>
      </tr>
    </tbody>
  </table>
</figure>

### Initial Setup
```
$ docker volume create portainer_data
$ docker run -d -p 8000:8000 -p 9000:9000 --name=portainer-ce_2.0 --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
```

### Configuration

#### Client Endpoints
The localhost endpoint is automatically enabled.  Remote hosts need to have their Docker API enabled.  An excerpt from "[How do I enable the remote API for dockerd](https://success.mirantis.com/article/how-do-i-enable-the-remote-api-for-dockerd)" is given below:

<div>
<figure style="width:796px;">
  <table style="background-color:rgb(255, 255, 255);">
    <tbody>
      <tr>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;width:55px;">&nbsp;</td>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;width:1107px;">
          <p>&nbsp;</p><div style="font-size:22px">
<!--          <h2  id="how-do-i-enable-the-remote-api-for-dockerd"> --> <strong>How do I enable the remote API for dockerd</strong><hr></div><!--</h2>-->
          <p>After completing these steps, you will have enabled the remote API for dockerd, without editing the systemd unit file in place:</p>
          <p>Create a file at <code>/etc/systemd/system/docker.service.d/startup_options.conf</code> with the below contents:</p>
          <pre><code># /etc/systemd/system/docker.service.d/override.conf
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2376
</code></pre>
          <blockquote>
            <p><strong>Note:</strong> The -H flag binds dockerd to a listening socket, either a Unix socket or a TCP port. You can specify multiple -H flags to bind to multiple sockets/ports. The default -H fd:// uses systemd's socket activation feature to refer to /lib/systemd/system/docker.socket.</p>
          </blockquote>
          <p>Reload the unit files:</p>
          <pre><code>$ sudo systemctl daemon-reload
</code></pre>
          <p>Restart the docker daemon with new startup options:</p>
          <pre><code>$ sudo systemctl restart docker.service
</code></pre>
          <p>Ensure that anyone that has access to the TCP listening socket is a trusted user since access to the docker daemon is root-equivalent.</p><br>
<div style="font-size:25px;color:blue"><!--          <h1  id="additional-documentation">--><strong>Additional Documentation</strong><hr><!--</h1>--></div>
          <ul>
            <li><a href="https://docs.docker.com/engine/security/">https://docs.docker.com/engine/security/</a></li>
          </ul>
          <p>&nbsp;</p>
        </td>
      </tr>
    </tbody>
  </table>
</figure>
</div>

### Upgrade
From the Portainer website, select Images.  Pull the latest portainer image.  Since the _portainer/portainer:latest_ tag is already in use, the latest version will be _portainer/portainer:\<none\>_.

```
$ docker stop portainer<current_version>
$ docker rm portainer<current_version>
$ #  DON'T RECREATE VOLUME  # docker volume create portainer_data
$ docker run -d -p 8000:8000 -p 9000:9000 --name=portainer-ce_<new_version> --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce
```

### Backup
> TBD
{.is-info}

### Reference
> TBD
{.is-info}

### Support Files
> TBD
{.is-info}


    
## Wiki.js

## Tabs {.tabset}

### Overview
This Wiki is served from a Docker container.  It uses both Wiki.js and a Postgres database image to store the content.
<br>
    
<figure style="width:796px;">
  <table style="background-color:rgb(255, 255, 255);">
    <tbody>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;text-align:left;">Docker Host</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">qnap.wysechoice.net (192.168.1.8)</td>
      </tr>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;text-align:left;">Docker Base Image</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">requarks/wiki:2 (latest version 2)</td>
      </tr>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;text-align:left;">Docker Image</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">wiki_01_31_21</td>
      </tr>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;text-align:left;">Data Volumes</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">${HOME}/docker_vols/wiki, ${HOME}/docker_vols/postgres</td>
      </tr>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;text-align:left;">Network</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">dockernet (192.168.40.0/24)</td>
      </tr>
      <tr>
        <th style="border-top:5px solid rgb(221, 221, 221);padding:8px;vertical-align:top;text-align:left;">Host</th>
        <td style="border-top:5px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">wiki.wysechoice.net (192.168.40.128)</td>
      </tr>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;text-align:left;">Port</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">3000 -> 8080</td>
      </tr>
      <tr>
        <th style="border-top:5px solid rgb(221, 221, 221);padding:8px;vertical-align:top;text-align:left;">Docker Database Host</th>
        <td style="border-top:5px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">qnap.wysechoice.net (192.168.1.8)</td>
      </tr>
      <tr>
        <th style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;text-align:left;">Database Host</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">postgres.wysechoice.net (192.168.40.30)</td>
      </tr>
      <tr>
        <th style="border-top:px solid rgb(221, 221, 221);padding:8px;vertical-align:top;text-align:left;">Docker Database Image</th>
        <td style="border-top:1px solid rgb(221, 221, 221);padding:8px;vertical-align:top;">postgres:9.5</td>
      </tr>
      <tr>
        <th style="border-top:5px solid rgb(221, 221, 221);padding:8px;vertical-align:top;text-align:left;">Reference</th>
        <td style="border-top:5px solid rgb(221, 221, 221);padding:8px;vertical-align:top;"><a href="https://hub.docker.com/_/postgres">https://hub.docker.com/_/postgres</a>,<a href="https://hub.docker.com/r/requarks/wiki">https://hub.docker.com/r/requarks/wiki</a></td>
      </tr>
    </tbody>
  </table>
</figure>

### Notes
#### Wiki Conventions & Plans
The intent of this Wiki is to provide an easily accessible set of documents that assist in the maintenance of an increasingly complex network configuration.  A secondary goal is establish a forum for information and content relevant to the Wyse household.

Ease of use is accomplished by using a standard way to provide information.  Inconsistencies in format should be reduced, allowing a user to quickly find the needed information for a specific server or service.  The following list are guidelines to support this goal.

##### General Guidance
- **Completeness:** All network and application services provided on/by this network should be listed on this Wiki
- **Dedicated Content:**  Content for each service should be available on it's own section or page
- **Common Content:** Documentation that is common across services and/or servers should be found in every associated service section.  In-lined content is preferred, but a link to common content may be required.
{.grid-list}
##### Server sections
Descriptions of servers should be displayed in a standard way.  The content below lists the base information that should be the minimum information provided for each server.  It should be displayed the same way for each server.
- **Machine name:** &nbsp;&nbsp;&nbsp;Hostname and IP address of server
- **Architecture:** &nbsp;&nbsp;&nbsp;Server CPU model and any specific hardware
- **Operating System:**&nbsp;&nbsp;&nbsp;Operating System and version
- **Firmware:**&nbsp;&nbsp;&nbsp;Any relevant firmware and version(s)
- **Address(es):** &nbsp;&nbsp;&nbsp;Static IP address(es) and interfaces
- **Location:** &nbsp;&nbsp;&nbsp;Physical location of server
- **Primary software list:** &nbsp;&nbsp;&nbsp;List of major software components with links to support references
- **Configuration:** &nbsp;&nbsp;&nbsp;Current configuration settings and/or link to configuration procedure
- **Backup:** &nbsp;&nbsp;&nbsp;Quick description and link to backup procedure
- **Services:** &nbsp;&nbsp;&nbsp;List of service links
- **Date:**&nbsp;&nbsp;&nbsp;Date information was last updated
{.grid-list}
3. Service section content
- **Service type:** &nbsp;&nbsp;&nbsp;Type of service being provided (file server, DHCP, etc).
- **Service name:** &nbsp;&nbsp;&nbsp;Name of service application
- **Service host:** &nbsp;&nbsp;&nbsp;DNS name of service host
- **Interface link:** &nbsp;&nbsp;&nbsp;Link to any web based administrative interface
- **Virtualization Software:** &nbsp;&nbsp;&nbsp;Type of virtualization software (Docker, podman, Virtual Box, etc) if used
- **Configuration:** &nbsp;&nbsp;&nbsp;Current configuration settings and/or link to configuration procedure
- **Backup:** &nbsp;&nbsp;&nbsp;Quick description and link to backup procedure
- **Date:**&nbsp;&nbsp;&nbsp;Date information was last updated

{.grid-list}

#### Non-Wiki Specific Guidelines
> This information does not belong here.  Once it is provided in other sections of the Wiki, it should be removed.
{.is-warning}

- Backups to another machine will be scheduled for all configuration and data
- Monthly restore operations will be scheduled to test backup
- Docker will be used for all services if possible

### Initial Setup
```
$ mkdir ~/docker_vols/wiki_data
$ docker run --net=dockernet --name postgres-9.5 --ip 192.168.40.30 -p 5432:5432 -m 4g -v ~/docker_vols/postgres:/var/lib/postgresql/data -e POSTGRES_ROOT_PASSWORD=xwiki -e POSTGRES_USER=xwiki -e POSTGRES_PASSWORD=xwiki -e POSTGRES_DB=xwiki -e POSTGRES_INITDB_ARGS="--encoding=UTF8" -d postgres:9.5
$ docker run -d -p 8080:3000 --net=dockernet --name wiki --restart unless-stopped -e "DB_TYPE=postgres" -e "DB_HOST=postgres-9.5" -e "DB_PORT=5432" -e "DB_USER=wikijs" -e "DB_PASS=wikijsrocks" -e "DB_NAME=wiki" -v /home/pi/docker_vols/wiki_data requarks/wiki:2
$ docker update --cpus 2 -m 4g
```

### Configuration
To provide search capability for the web site content, the search engine usage needs to be configured.  From the administration page, select the search engine configuration page.  Choose the PostGresql search engine.  This engine also requires an extension to be enabled in the Wiki database.  Execute `CREATE EXTENSION pg_trgm;` against the Wiki database to enable the required extension (e.g. - via pgadmin4).

https://docs.requarks.io

### Upgrade
```
# Stop and remove container named "wiki-2.5.201"
docker stop wiki-<old_version>
docker rm wiki-<old_version>

# Pull latest image of Wiki.js
docker pull requarks/wiki:2

# Create new container of Wiki.js based on latest image
docker run -d -p 8080:3000 --net=dockernet --name wiki-<new_version> --restart unless-stopped -e "DB_TYPE=postgres" -e "DB_HOST=postgres-9.5" -e "DB_PORT=5432" -e "DB_USER=wikijs" -e "DB_PASS=wikijsrocks" -e "DB_NAME=wiki" -v /home/pi/docker_vols/wiki_data requarks/wiki:2

# Use a second CPU for the container
docker update --cpus 2 wiki-<new_version>
```

### Backup
``` 
docker exec postgres-9.5 pg_dump wiki -U wikijs -F c > ~/wikibackup.dump
```

### Reference
> TBD
{.is-info}

### Support Files
> TBD
{.is-info}

## Ghini

## Tabs {.tabset}

### Overview


### Initial Setup


### Configuration
- Ghini database is served on the Postgres server, postgres.wysechoice.net*
- Ghini database will be backed up nightly to postgres2.wysechoice.net (planned), which will be the failsafe database server
- User: chris  Password: <store securely outside the repository>
- Pictures:  [fileserver.wysechoice.net://srv/ghini/pictures](fileserver.wysechoice.net://srv/ghini/pictures) (planned)

### Upgrade
> TBD
{.is-info}

### Backup
> TBD
{.is-info}

### Reference
> TBD
{.is-info}

### Support Files
> TBD
{.is-info}

## Grafana

## Tabs {.tabset}

### Overview

Grafana is install on the QNAP server (192.168.1.8), listening on port 3000.  

The installation was done via a QPKG file downloaded from the QNAPClub Store at https://www.qnapclub.eu/en/qpkg/812.  It is installed into /opt/Grafana.  The default configuration (/opt/Grafana/conf/defaults.ini) uses relative paths from the installation directory.  Manually installed plugins need to specify the plugin directory, e.g.:
```
grafana-cli --pluginsDir /opt/Grafana/data/plugins --debug --homepath /opt/Grafana --config /opt/Grafana/conf/defaults.ini plugins install simpod-json-datasource
```


### Initial Setup

#### API Keys
Create API Keys for various Grafana roles:
##### Viewer
```
Key
<store securely outside the repository>
curl -H "Authorization: Bearer <store securely outside the repository>" http://192.168.1.8:3000/api/dashboards/home
```
##### Editor
```
Key
eyJrIjoia29xa0liWDROcHMxRGhYR0xNTmV5V0hqVkl6aWFDcEkiLCJuIjoiRWRpdG9yS2V5IiwiaWQiOjF9
curl -H "Authorization: Bearer eyJrIjoia29xa0liWDROcHMxRGhYR0xNTmV5V0hqVkl6aWFDcEkiLCJuIjoiRWRpdG9yS2V5IiwiaWQiOjF9" http://192.168.1.8:3000/api/dashboards/home
```
##### Admin
```
Key
<store securely outside the repository>
curl -H "Authorization: Bearer <store securely outside the repository>" http://192.168.1.8:3000/api/dashboards/home
```

### Configuration

#### Plugins:

- [JSON Datasource – a generic backend datasource](https://grafana.com/grafana/plugins/simpod-json-datasource?pg=plugins&plcmt=featured-undefined)
  

### Upgrade
> TBD
{.is-info}

### Backup
> TBD
{.is-info}

### Reference
> TBD
{.is-info}

### Support Files
> TBD
{.is-info}

## Syslog

## Tabs {.tabset}

### Overview
> TBD
{.is-info}


### Initial Setup
> TBD
{.is-info}


### Configuration
> TBD
{.is-info}

### Upgrade
> TBD
{.is-info}

### Backup
> TBD
{.is-info}

### Reference
> TBD
{.is-info}

### Support Files
> TBD
{.is-info}

## CheckMK

## Tabs {.tabset}

### Overview
> TBD
{.is-info}


### Initial Setup
> TBD
{.is-info}


### Configuration
> TBD
{.is-info}

### Upgrade
> TBD
{.is-info}

### Backup
> TBD
{.is-info}

### Reference
> TBD
{.is-info}

### Support Files
> TBD
{.is-info}


