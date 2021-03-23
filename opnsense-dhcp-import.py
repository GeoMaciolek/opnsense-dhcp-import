# Simple script to generate a DHCP config for opnsense (and maybe pfSense?)
# 
# Imports from a csv with the columns:
# macaddr
# ipaddr
# hostname
# description

network_interface = 'lan' # The interface name as defined in OPNSense - lan, opt1, etc
platform_name = 'opnsense' # as used in the config file - only OPNSense tested

input_csv_folder = 'data'
input_csv_file = 'input_reservations.csv'

output_xml_filename = 'dhcp_reservation_output.xml'

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
full_xml_template = \
"""<$platformname>
  <dhcpd>
    <$network>
$reservations
    </$network>
  </dhcpd>
</$platformname>
"""

#################
# Process the CSV

# Cross-platform way to do "data/inputfile.csv"
csv_path = Path(input_csv_folder)
input_csv = csv_path / input_csv_file
output_XML_file = csv_path / output_xml_filename

# Make this empty string; we'll append each entry to it as we go
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

# insert the relevant keys into the configuration dictionary 
main_xml_config_dict = dict( 
    platformname=platform_name,
    network=network_interface,
    reservations= static_mappings_segment
)

full_xml_output = Template(full_xml_template).substitute(main_xml_config_dict)

print(full_xml_output)

print("Writing to data file",output_XML_file)

with open(output_XML_file, 'w') as outfile:
    outfile.write(full_xml_output + "\n")