import subprocess
import os
import sys
from . import helper_functions as hf

def debug():
    # 1. Get interface name
    interface_name = subprocess.run("ip -o -4 route show to default | awk '{print $5}'", capture_output=True, shell=True, check=True)
    interface_name = str(interface_name.stdout).replace('b','').replace('\\n','').strip("'")

    # 2. DHCP needed ?
    print('Wird DHCP benötigt?')
    dhcp_needed = input('(y/n): ').upper()
    dhcp_needed = dhcp_needed.upper()
    # Only 'y' and 'n' allowed
    while dhcp_needed not in ['Y','N']:
        dhcp_needed = input('(y/n): ')
        dhcp_needed = dhcp_needed.upper()
    
    if dhcp_needed == 'Y':
        dhcp_needed = 'true'
    else:
        dhcp_needed = 'false'

    # 3. Static IP, with subnetprefix (IPv4: range 1-32)
    print('Wie lautet die Statische IP des Interfaces?')
    static_ips_list = hf.get_ips()
    # List to string, with commas in between
    static_ips_list = ' '.join(static_ips_list)
    # Get subnet prefix
    print('Wie lautet das Subnet Präfix der Statische IP des Interfaces?')
    print('Subnet (1-32):')
    static_ips_subnet =hf.get_int(1,33)
    # Add slash and transforms int to string
    static_ips_subnet = '/' + str(static_ips_subnet)
    # Combine static ip with subnetmask
    static_ip = static_ips_list + static_ips_subnet

    # 4. DNS server
    print('Wie lautet die IP des DNS-Servers? Mehrere IP Addressen durch ein Komma trennen!')
    dns_ips_list = hf.get_ips()
    # List to string, with commas in between
    dns_ips = ','.join(dns_ips_list)

    # 4. Default gateway 
    print('Wie lautet die IP des Default gateways?')
    dgw_ips_list = hf.get_ips()
    # List to string, with spaces in between
    dgw_ips = ' '.join(dgw_ips_list)

    # Create empty a empty list and fill it with the config values
    config_list = []
    config_list += [interface_name] # 1. Interface
    config_list += [dhcp_needed]    # 2. DHCP true/false
    config_list += [static_ip]      # 3. Static IP for interface, with subnetprefix
    config_list += [dns_ips]        # 4. DNS
    config_list += [dgw_ips]        # 5. Default gateway

    # Get path to template file
    template_backup_path = os.path.join(sys.path[0]) + '/scripts/netplan/template_netplan_backup.yaml'

    # Get filenames in netplan directory
    netplan_path = '/etc/netplan/'
    files = os.listdir(netplan_path)
    netplan_file = netplan_path + files[0].strip("'")
    print('###### DEBUG: ' + files[0])      # DEBUG

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

    # Change file permissions to "666" so everyone can read and write
    os.chmod(netplan_file, 0o666)

    # # Replace netplan with template file
    os.system('cat ' + template_file + ' > ' + netplan_file)

    # Change file permissions to "644" so everyone can read, but only owner can write
    os.chmod(netplan_file, 0o644)

    # Remove symlink "/etc/resolv.conf" and relink to "/run/systemd/resolve/resolv.conf"
    # Because netplan writes to "/run/systemd/resolve/resolv.conf"
    # https://serverfault.com/questions/1032595/how-to-get-netplan-to-set-the-dns-server-in-etc-resolv-conf-based-on-info-comin   
    os.system('sudo unlink /etc/resolv.conf')
    os.system('sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf')

    # Apply new netplan config
    # os.system('sudo netplan --debug try')     # For debugging use only 
    os.system('sudo netplan apply')
