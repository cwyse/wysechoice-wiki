---
title: Net Applications
description: 
published: true
date: 2022-01-09T16:18:20.129Z
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
