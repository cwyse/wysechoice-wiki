#!/usr/bin/env python3

"""Label Generator for Ghini Plant Database w/ Brother PT-P700 printer

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

"""

from docopt import docopt
import psycopg2
import sys
import subprocess
import re
import os
import xml.etree.ElementTree as ET
import tempfile
import shutil
from csv import DictReader
from contextlib import contextmanager
import paramiko
from scp import SCPClient, SCPException
import fnmatch

# The latest glabels-batch does not support the -i option anymore.  To work around the
# issue, unzip the glables file (it's actually a zip file) to obtain the xml.  The
# XML contains a Merge element with a src file that points to the input field.  Modify
# that file with the CSV path placeholder.  This program looks for the placeholder and
# inserts the actual path, and passes the XML file to the batch processor.
#


def get_template_default():

    label_template = '''<?xml version="1.0"?>
    <Glabels-document version="4.0">
      <Template brand="Brother" width="520pt" part="TZe" size="Other" description="128x520" height="128pt">
        <Label-rectangle id="0" width="520pt" height="128pt" round="0pt" x_waste="0pt" y_waste="0pt">
          <Markup-margin size="14pt"/>
          <Layout nx="1" x0="0pt" dy="128pt" dx="520pt" ny="1" y0="0pt"/>
        </Label-rectangle>
      </Template>
      <Objects id="0" rotate="false">
        <Object-text align="left" auto_shrink="false" shadow_x="0pt" lock_aspect_ratio="false" a5="0" wrap="word" x="451.254pt" shadow="false" a1="0" font_family="Sans" y="99.0918pt" a3="1" font_size="9" w="57.7813pt" a0="1" a2="0" a4="0" h="21pt" shadow_color="0x0" font_underline="false" color="0xff" font_italic="false" line_spacing="1" font_weight="normal" shadow_y="0pt" shadow_opacity="1" valign="top">
          <p>${code}</p>
        </Object-text>
        <Object-text align="left" auto_shrink="false" shadow_x="0pt" lock_aspect_ratio="false" a5="0" wrap="word" x="14.6932pt" shadow="false" a1="0" font_family="Sans" y="99.5541pt" a3="1" font_size="9" w="62.875pt" a0="1" a2="0" a4="0" h="21pt" shadow_color="0x0" font_underline="false" color="0xff" font_italic="false" line_spacing="1" font_weight="normal" shadow_y="0pt" shadow_opacity="1" valign="top">
          <p>${name}</p>
        </Object-text>
        <Object-text align="left" auto_shrink="false" shadow_x="0pt" lock_aspect_ratio="false" a5="0" wrap="word" x="164.354pt" shadow="false" a1="0" font_family="Sans" y="26.3615pt" a3="1" font_size="9" w="87.5625pt" a0="1" a2="0" a4="0" h="35pt" shadow_color="0x0" font_underline="false" color="0xff" font_italic="false" line_spacing="1" font_weight="normal" shadow_y="0pt" shadow_opacity="1" valign="top">
          <p>${title_line1}</p>
          <p>${title_line2}</p>
        </Object-text>
        <Object-image y="0pt" shadow_x="0pt" w="520pt" shadow_opacity="1" a0="1" a4="0" a5="0" x="0pt" src="Box.png" shadow="false" h="128pt" lock_aspect_ratio="false" shadow_y="0pt" a2="0" a3="1" a1="0" shadow_color="0x0"/>
        <Object-text align="right" auto_shrink="false" shadow_x="0pt" lock_aspect_ratio="false" a5="0" wrap="word" x="343.008pt" shadow="false" a1="0" font_family="Sans" y="85.968pt" a3="1" font_size="15" w="155pt" a0="1" a2="0" a4="0" h="31.752pt" shadow_color="0x0" font_underline="false" color="0xff" font_italic="false" line_spacing="1" font_weight="normal" shadow_y="0pt" shadow_opacity="1" valign="top">
          <p>${code}</p>
        </Object-text>
        <Object-text align="left" auto_shrink="true" shadow_x="0pt" lock_aspect_ratio="false" a5="0" wrap="word" x="18.72pt" shadow="false" a1="0" font_family="Sans" y="85.968pt" a3="1" font_size="15" w="329.04pt" a0="1" a2="0" a4="0" h="31.7867pt" shadow_color="0x0" font_underline="false" color="0xff" font_italic="false" line_spacing="1" font_weight="normal" shadow_y="0pt" shadow_opacity="1" valign="top">
          <p>${name}</p>
        </Object-text>
        <Object-text align="hcenter" auto_shrink="true" shadow_x="0pt" lock_aspect_ratio="false" a5="0" wrap="word" x="12.1404pt" shadow="false" a1="0" font_family="Sans" y="16.935pt" a3="1" font_size="18" w="494.86pt" a0="1" a2="0" a4="0" h="35pt" shadow_color="0x0" font_underline="false" color="0xff" font_italic="true" line_spacing="1" font_weight="normal" shadow_y="0pt" shadow_opacity="1" valign="top">
          <p>${title_line1}</p>
        </Object-text>
        <Object-text align="hcenter" auto_shrink="true" shadow_x="0pt" lock_aspect_ratio="false" a5="0" wrap="word" x="11.7331pt" shadow="false" a1="0" font_family="Sans" y="51.9677pt" a3="1" font_size="18" w="495.267pt" a0="1" a2="0" a4="0" h="35pt" shadow_color="0x0" font_underline="false" color="0xff" font_italic="true" line_spacing="1" font_weight="normal" shadow_y="0pt" shadow_opacity="1" valign="top">
          <p>${title_line2}</p>
        </Object-text>
      </Objects>
      <Merge type="Text/Comma/Line1Keys" src="/home/chris/Downloads/plant_labels_living.csv"/>
      <Data>
        <File mimetype="image/png" encoding="base64" name="Box.png">iVBORw0KGgoAAAANSUhEUgAAAf8AAAB+CAYAAAAqahh3AAAACXBIWXMAAA7EAAAOxAGVKw4bAAACnElEQVR4nO3cMYrbQBiA0VHYwvgStluD738Qg1v7FMadU6XZFSKBSLvwvVeOpvi7TzMITWOM9wAAMn599wAAwLbEHwBixB8AYsQfAGI+5hZPp9PWcwAAK7jf71/WZuO/2+3G7XZbfSAAYD2Xy2V2fTb+f8y9LQAAP9/SLf5i/F+v1zifz/99IABgPdfrdfG5D/4AIEb8ASBm8dr/s/fbn4AB4Ceapumv9zr5A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0CM+ANAjPgDQIz4A0DMx79snqZprTkAgI04+QNAjPgDQMzitf9+vx+Px2OjUQCALSzG/3A4bDUHALCR2fg/n89xPB43HgUA2MI0xnh/9xAAwHZ88AcAMeIPADHiDwAx4g8AMb8B+cIba3wu8b4AAAAASUVORK5CYII=</File>
      </Data>
    </Glabels-document>
    '''
    root = ET.fromstring(label_template)
    tree = ET.ElementTree(root)
    return tree

def get_template(template_file):
    tree = ET.parse(template_file)
    return tree

def set_template_csv_input(template_tree, inputfile):

    merge = template_tree.find('Merge')
    merge.set('type', 'Text/Comma/Line1Keys')
    merge.set('src', inputfile)

    return template_tree

def open_template_instance(template_tree):

    fp = tempfile.NamedTemporaryFile()
    template_tree.write(fp, encoding='utf8', method='xml')
    return fp

def close_template_instance(fp):
    fp.close

def get_template_fields(template_tree):
    exp=r"^\${(.*)}$"

    # Initialize set to include any columns needed for processing
    columns = set(['infrasp1', 'code', 'genus', 'species', ])

    # Now search the template to find any additional columns specified in the template
    objects = template_tree.getroot().find('Objects')

    for obj_text in objects.findall('Object-text'):
        for para in obj_text.findall('p'):
            try:
                column_name = re.match(exp, para.text).groups()
                columns.add(column_name[0])
                print(f'{para.text} {column_name} {columns}')
            except:
                pass
 
    print(f'{para} {column_name} {columns}')
    return columns


def write_csv(fp, args, columns, whereclause=None):

    print("Reading database\n")
    PASSWORD='<store securely outside the repository>'

    try:
        host=args['--host']
        port=args['--port']
        dbname=args['--database'] 
        user=args['--user']

        con = psycopg2.connect(host=host, port=port, dbname=dbname, 
                               user=user, password=PASSWORD)
    except psycopg2.Error as err:
        print(f'Error: {err}\nUnable to connect to database at [host: {host}, port: {port}, database: {dbname}, user: {user}]\n' )
        raise        

    try:
        cur = con.cursor()

        # Create a comma separated list of columns from the columns set
        commacols = ", ".join([str(i) for i in columns])

        viewname = args['--view']
        whereclause = args['--where']

        # Create the SQL statement 
        if whereclause is not None:
            sql_statement = "SELECT " + commacols + ' FROM ' + viewname + ' ' + whereclause
        else:
            sql_statement = "SELECT " + commacols + ' FROM ' + viewname

        try:
            sql_to_csv_statement = f'COPY ({sql_statement}) TO STDOUT WITH CSV HEADER'
            cur.copy_expert(sql_to_csv_statement, fp)
            fp.flush()
            print(f'Cursor status = {cur.statusmessage}\n')
            print (f'fp.name={fp.name}')
            print (f'fp.name={fp.name}')
        except psycopg2.Error as err:
            print(f'Error: {err}\nUnable to export data to CSV file.connect to {fp.name}.\n' )
            raise
    except psycopg2.Error as err:
        print(f'Error: {err}\nUnknown failure.  Closing database.\n' )
        con.close()
        raise
    finally:
        con.close()
    
def rename_labels(label_tmp_dirname, label_dirname, csv_filename):
    cnt = 0
    labelfiles = {}

    # iterate over each line as a ordered dictionary and print only few column by   column name
    with open(csv_filename, 'r') as read_obj:
        csv_dict_reader = DictReader(read_obj)
        for row in csv_dict_reader:
            if row['infrasp1'] == '':
                label_filename = '%s_%s_%s' % (row['code'], row['genus'], row['species'])
            else:
                label_filename = '%s_%s_%s_%s' % (row['code'], row['genus'], row['species'], row['infrasp1'])
            new_label_filename = label_filename.replace(" ","_") + '.png'
            new_label_filename = f'{label_dirname}/{new_label_filename}'
            old_label_filename = f'{label_tmp_dirname}/labels_{cnt:03d}.png'
            cnt = cnt + 1
            shutil.move(old_label_filename, new_label_filename)
            labelfiles[row['code']] = new_label_filename
    return labelfiles


def gen_labels(pdf_filename, label_filename):
    print("Generating label images\n")

    glables_cmd = ["glabels-batch-qt", "-o", pdf_filename, label_filename]
    subprocess.run(glables_cmd)

    count = len(os.listdir(os.getcwd()))
    return count

def convert_pdf(pdf_filename, label_dirname):
    print("Processing label images\n")

    convert_cmd = ["convert", pdf_filename, "-crop", "520x128", "-negate", "-threshold", "0", "-negate", "labels_%03d.png"]

    with cwd(label_dirname):
        subprocess.run(convert_cmd)


@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)

def print_batch(ssh, scp_client, label_batch, ptouch_cmd, rm_cmd):
    try:
        scp_client.put(label_batch, '/tmp')
        # Should now be printing the current progress of your put function.
        stdin, stdout, stderr = ssh.exec_command(ptouch_cmd)
        exit_status = stdout.channel.recv_exit_status()
        if exit_status != 0:
            print(f'ERROR: Remote print command for {label_basename} failed (rc = {exit_status}).  Continuing.\n')
        # Remove the temporary label files
        stdin, stdout, stderr = ssh.exec_command(rm_cmd)
        exit_status = stdout.channel.recv_exit_status()
        if exit_status != 0:
            print(f'ERROR: Remote print command for {label_basename} failed (rc = {exit_status}).  Continuing.\n')
    except (SCPException, SSHException, socket.timeout) as err:
        # SSH blew up :(
        print(f'ERROR: {err}.  Failed to transfer {os.path.basename(label_basename)} to printer.  Skipping.\n')

def print_labels(print_server, ssh_user, label_files):
    try:
        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname = print_server, port = '22', username = ssh_user, password = '<store securely outside the repository>', allow_agent=False, look_for_keys=False)
    except paramiko.AuthenticationException as authException:
            print("Authentication failed: {authException}")
    except paramiko.SSHException as sshException:
            print(f'Unable to establish SSH connection: {sshException}')
    except paramiko.BadHostKeyException as badHostKeyException:
            print(f"Unable to verify server's host key: {badHostKeyException}")

    try:
        scp_client = SCPClient(ssh.get_transport())
    except SCPException as err:
        print(f'Error executing SCPClient: {err}')

    cnt = 0
    batch_cnt = 10
    for label_file in label_files.values():
        label_basename = os.path.basename(label_file)
        if cnt == 0:
            label_batch = []
            label_batch.append(label_file)
            rm_cmd = f'rm -f /tmp/{label_basename} '
            ptouch_cmd = f'ptouch-print --image /tmp/{label_basename} '

        else:
            label_batch.append(label_file)
            rm_cmd += f'/tmp/{label_basename} '
            ptouch_cmd += f'--pad 10 --cutmark --pad 10 --image /tmp/{label_basename} '

        cnt += 1
        if cnt < batch_cnt:
            continue

        cnt = 0
        print_batch(ssh, scp_client, label_batch, ptouch_cmd, rm_cmd)
        cnt = 0

    if cnt > 0:
        print_batch(ssh, scp_client, label_batch, ptouch_cmd, rm_cmd)


    scp_client.close()
    ssh.close()


def confirm_prompt(question: str, default: str = 'n') -> bool:
    reply = None

    default=default.lower()

    values = 'y/N'
    if default == 'y':
        values = 'Y/n'

    while reply not in ("y", "n"):
        reply = input(f"{question} ({values}): ").casefold()
    return (reply == "y")

def main():
    args = docopt(__doc__)

    # Everything has a default value, so no parameter checking right now

    # Get the label template object
    if args['--template'] is None:
        label_tree = get_template_default()
    else:
        label_tree = get_template(args['--template'])

    # Create and open a temporary file to store the CSV data
    csv_file = tempfile.NamedTemporaryFile()

    # Insert the temporary file name into the label template object
    set_template_csv_input(label_tree, csv_file.name)

    # Write the update template to a temporary file
    label_file = open_template_instance(label_tree)
    print(f'label_file = {label_file.name}')

    # Get the list of columns from the label tree
    label_fields = get_template_fields(label_tree)

    # Read from the database and store it in the CSV file
    write_csv(csv_file, args, label_fields)

    # Create a PDF file for the label images
    if args['--output'] is None:
        pdf_file = tempfile.NamedTemporaryFile()
        pdf_filename = pdf_file.name
    else:
        pdf_filename = args['--output']

    # Determine where to store labels
    if args['--label-dir'] is None:
        #label_dir = tempfile.TemporaryDirectory()
        #label_dirname = os.path.abspath(label_dir.name)
        #label_dir = tempfile.TemporaryDirectory()
        label_dirname = os.getcwd() + f'/labels'
    else:
        label_dirname = args['--label-dir']
        
    pdf_filename = os.path.abspath(pdf_filename)
    label_filename = os.path.abspath(label_file.name)
    label_dirname = os.path.abspath(label_dirname)

    print(label_dirname)
    with cwd(label_dirname):
        # Populate PDF file with label images
        label_count = gen_labels(pdf_filename, label_filename)

        label_tmp_dir = tempfile.TemporaryDirectory()

        # Create PNG files from the PDF file
        convert_pdf(pdf_filename, label_tmp_dir.name)

        labelfiles = rename_labels(label_tmp_dir.name, label_dirname, csv_file.name)

    close_template_instance(label_file)
    csv_file.close
    pdf_file.close

    print(f'Generated {label_count} labels in: {label_dirname}.\n\n')

    cnt = 1
    reply = confirm_prompt("Show label files?")
    if reply:
        for key, filename in labelfiles.items():
            print(f'   {os.path.basename(filename):50}', end='')
            if cnt == 2:
                cnt = 1
                print(f'')
            else:
                cnt += 1

    print(f'\n')
    reply = confirm_prompt("Print labels?")
    if reply:
        print_labels(args['--print-server'], args['--ssh'], labelfiles)

if __name__ == '__main__':
    main()


