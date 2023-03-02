---
title: Garden Label Generation
description: Information on the configuration, tools, and generation of garden plant labels.
published: true
date: 2023-03-02T02:17:44.392Z
tags: garden, service
editor: markdown
dateCreated: 2023-02-25T23:59:47.252Z
---

# Plant labels
## Overview
Label printing is initiated from a host computer by running the labelgen program.  Labelgen queries the database and retrieves the necessary data to create the requested labels.  The data is passed to *glabels-batch-qt* and applied to a template label.  If no label template has been specified, a default template is used that is embedded in the labelgen script.  The *glabels-batch-qt* program outputs a PDF file containing all the labels.  *Imagemagick's convert* utility is used to split the labels into individual images.  The images are sent to the *ptouch-print* utility on the print server to print.<br><br>
<figure>
  <center>
    <img src="/label_printing_configuration.drawio.png" width="60%" height="60%" align="center"
       alt="Label Printing Overview"></center><center>
    <fig caption>Label Printing Overview</figcaption>
  </center>
</figure>

## Labelgen script

Usage information for the Label Generator for the Ghini Plant Database and the Brother PT-P700 printer.

```
Usage: labelgen [options]

Options:
  -h, --help                                  Display this screen
  -v, --version                               Display version
  -H, --host <database host>                  Database host server [default: postgres]
  -p, --port <database port>                  Database host server connection port [default: 5432]
  -d, --database <database name>              Database to query [default: ghini]
  -u, --user <user>                           Database user and password [default: chris]
  -P, --print-server <print server address>   Print server address [default: pentos]
  -g, --generate                              Only generate labels, don't print
  -w, --where <SQL where clause>              SQL where clause string (e.g. "where code like '2022.%' ") 
  -V, --view <viewname>                       View or table name to query (could be multiple, separated by commas) [default: plant_labels_living] 
  -o, --output <PDF file>                     Generate PDF file in addition to printing 
  -l, --label-dir <label storage directory>   Generate label images in this directory [ default: os.getcwd()]
  -s, --ssh <ssh connection string>           User and password (if needed) to SSH into print server (e.g. '<user>:<password>') [default: pi]
  -t, --template <template file>              Glabels generated label template 

This label generator script relies on two additional machines - the database host server, and the
print server.  The database host should be running postgres and serving the desired Ghini plant
database.  The print server should be connected to a Brother PT-P700 printer. 

Running this command without any parameters will select the currently (2/4/2023) configured
servers, and print labels for all living plants in the collection.
```

The script can be executed 
## Tools and Equipment
### PTouch Printer Tape: 
```
Brother Genuine P-Touch TSX-S251 Tape
1" (0.94") Wide Extra-Strength Adhesive Laminated Tape
Black on White
Laminated for Indoor or Outdoor Use
Water-Resistant
0.94" x 26.2' (24mm x 8M) 
TZES251
```
### Plant Markers
```
Kincaid Stainless Steel Plant Marker
10" A Style, 25 Piece Bundle
Standard Duty #13 Gauge Posts
Item #: 2A-10-25
```
### Plant Marker Sources
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



##### Ptouch Print
- Build dependencies
-- git
-- autogen
-- autoreconf
-- gettext
-- autopoint
- https://github.com/clarkewd/ptouch-print

