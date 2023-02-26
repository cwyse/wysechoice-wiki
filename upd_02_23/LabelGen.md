---
title: Garden Label Generation
description: Information on the configuration, tools, and generation of garden plant labels.
published: true
date: 2023-02-25T23:59:47.252Z
tags: garden, service
editor: markdown
dateCreated: 2023-02-25T23:59:47.252Z
---

# Plant labels
## PTouch Printer Tape: 
```
Brother Genuine P-Touch TSX-S251 Tape
1" (0.94") Wide Extra-Strength Adhesive Laminated Tape
Black on White
Laminated for Indoor or Outdoor Use
Water-Resistant
0.94" x 26.2' (24mm x 8M) 
TZES251
```
## Plant Markers
```
Kincaid Stainless Steel Plant Marker
10" A Style, 25 Piece Bundle
Standard Duty #13 Gauge Posts
Item #: 2A-10-25
```
## Plant Marker Sources
- [Kincaid Plant Markers](https://www.kincaidplantmarkers.com/)
- [IDeal Garden Markers](https://www.idealgardenmarkers.com/)
- [Lark Label](https://larklabel.com/)
- [MyPlantLabel](https://myplantlabel.com/)

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

