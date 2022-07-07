import subprocess
import os
import sys
from . import helper_functions as hf

def debug():
    # Get interface name
    interface_name = subprocess.run("ip -o -4 route show to default | awk '{print $5}'", capture_output=True, shell=True, check=True)
    interface_name = str(interface_name.stdout).replace('b','').replace('\\n','').strip("'")

    # User input: DHCP needed?
    print('Wird DHCP benötigt?')
    dhcp_needed = input('(yes/no): ').upper()
    # Only 'yes' and 'no' allowed
    while not dhcp_needed == 'yes' or 'no':
        dhcp_needed = input('(yes/no): ').upper()

    # User input: Default gateway/route 
    print('Wie lautet die IP des Default gateways?')
    dgw_ips_list = hf.get_ips()
    # List to string, with spaces in between
    dgw_ips = ' '.join(dgw_ips_list)

    # User input: DNS server
    print('Wie lautet die IP des DNS-Servers? Mehrere IP Addressen durch ein Komma trennen!')
    dns_ips_list = hf.get_ips()
    # List to string, with commas in between
    dns_ips = ','.join(dns_ips_list)

    # Create empty a empty list and fill it with the config values
    config_list = []
    config_list += [interface_name]
    config_list += [dhcp_needed]
    config_list += [dgw_ips]
    config_list += [dns_ips]

    # Get path to template file
    template_backup_path = os.path.join(sys.path[0]) + '/scripts/netplan/template_netplan_backup.yaml'

    # Get filenames in netplan directory
    netplan_path = '/etc/netplan/'
    files = os.listdir(netplan_path)
    #netplan_file = netplan_path + files[0].strip("'")
    print('###### DEBUG: ' + files[0])

    # Read from template file
    with open (template_backup_path, 'r', encoding='UTF-8') as file:
        filedata = file.read()
    
    # Replace variable with config value from config_list
    count = 1
    for n in config_list:
        to_replace = '$'+str(count)+'$'
        filedata = filedata.replace(to_replace, n)
        count = count + 1

    # Create new template file and write config_list into it
    template_file = os.path.join(sys.path[0]) + '/scripts/netplan/' + files[0]
    with open (template_file, 'w', encoding='UTF-8') as file:
        file.write(filedata)

    # Backup netplan file
    #backup_file = netplan_file + '_backup'
    #backup_file = backup_file.strip("'")
    #subprocess.run(['sudo', 'cp', netplan_file, backup_file], shell=True, check=True)

    # Replace netplan with template
    #subprocess.run(['sudo', 'cat', template_file, '>|', netplan_file], shell=True, check=True)

    # Apply new netplan config
    #subprocess.run(['sudo', 'netplan', 'try'], shell=True, check=True)
