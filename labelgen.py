#!/usr/bin/env python3

HOST="192.168.40.30"
PORT="5432"
DBNAME="ghini"
USER="ghini"
PASSWORD="ig29LSOt&Fgb"

SQL="SELECT * FROM plant_labels_living"

CSV_FILE="plant_csv.csv"

GLABELS_FILE="PlantLabels.glabels"
PDF_FILE="PlantLabels.pdf"

GLABELS_CMD=["glabels-3-batch", "-i", CSV_FILE, "-o", PDF_FILE, GLABELS_FILE]
CONVERT_CMD=["convert", PDF_FILE, "-crop", "520x128", "-negate", "-threshold", "0", "-negate", "labels_%03d.png"]

import psycopg2
import sys
import subprocess



con = None

print("Reading database\n")
try:

    con = psycopg2.connect(host=HOST, port=PORT, dbname=DBNAME, 
                           user=USER, password=PASSWORD)

    cur = con.cursor()
#    cur.execute(SQL)

#    colnames = [desc.name for desc in cur.description]
#    print(colnames[0])

#    version = cur.fetchone()[0]
#    print(version)

    SQL_for_file_output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(SQL)

    try:
        with open(CSV_FILE, 'w') as f_output:
            cur.copy_expert(SQL_for_file_output, f_output)
    except psycopg2.Error as e:
        t_message = "Error: " + e + "/n query we ran: " + s + "/n t_path_n_file: " + CSV_FILE
        raise



except psycopg2.DatabaseError as e:

    print(f'Error {e}')
    sys.exit(1)

finally:

    if con:
        con.close()


print("Generating label images\n")
subprocess.run(GLABELS_CMD)
print("Processing label images\n")
subprocess.run(CONVERT_CMD)
            
import os
import shutil

if not os.path.exists('labels'):
    os.makedirs('labels')
os.chdir("labels")

cnt = 0
from csv import DictReader
# iterate over each line as a ordered dictionary and print only few column by   column name
with open("../" + CSV_FILE, 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:
        if row['infrasp1'] == '':
            label_filename = '%s_%s_%s' % (row['code'], row['genus'], row['species'])
        else:
            label_filename = '%s_%s_%s_%s' % (row['code'], row['genus'], row['species'], row['infrasp1'])
        new_label_filename = label_filename.replace(" ","_") + '.png'
        old_label_filename = "../labels_%03d.png" % cnt
        cnt = cnt + 1
        shutil.move(old_label_filename, new_label_filename)

