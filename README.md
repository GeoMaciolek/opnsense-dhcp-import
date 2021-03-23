## OPNSense DHCP Import

### Overview

This simple script allows you to bulk import DHCP reservations to your OPNSense router.

It currently supports .csv files with a very specific format.

### How-to

1. Generate a .csv file with the columns: 
 - `macaddr`
 - `ipaddr`
 - `hostname`
 - `description`
2. Put your data into said CSV
3. Save the file into `data/input_reservations.csv`
4. Run `opnsense-dhcp-import.py`
5. Import generated XML backup `data/output_dhcp_reservations.xml` into OPNSense (specify DHCP only!)
6. Cross fingers, and test!

### TODO

- Actually saving XML
- Other input formats
 - JSON
 - Other router backups?
- Testing
 - OPNSense
 - pfSense
- Maybe update OPNSense directly with API??!
