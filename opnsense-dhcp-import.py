# Simple script to generate a DHCP config for opnsense (and maybe pfSense?)
# 
# Imports from a csv with the columns:
# macaddr
# ipaddr
# hostname
# description

input_csv_folder = 'data'
input_csv_file = 'input_reservations.csv'

from pathlib import Path
import csv
from string import Template

expected_keys = ['macaddr','ipaddr','hostname','description']

entry_template_xml = \
"""      <staticmap>
        <mac>$macaddr</mac>
        <ipaddr>$ipaddr</ipaddr>
        <hostname>$hostname</hostname>
        <descr>$description</descr>
        <winsserver/>
        <dnsserver/>
        <ntpserver/>
      </staticmap>
"""

#################
# Process the CSV

# Cross-platform way to do "data/inputfile.csv"
csv_path = Path(input_csv_folder)
input_csv = csv_path / input_csv_file

static_mappings_segment = ""

with open (input_csv) as csvfile:
    csv_obj = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for reservation in csv_obj:
        # Check to make sure we have the expected properties in this entry
        for key_to_check in expected_keys:
            # if we don't have the expected properties, add them as empty strings
            if not key_to_check in reservation:
                reservation[key_to_check] = ""
        src = Template(entry_template_xml)
        result = src.substitute(reservation)
        static_mappings_segment+=result

print(static_mappings_segment)

