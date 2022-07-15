import subprocess
import os
import sys
import random
import socket
from string import ascii_letters
from .easyufw import easyufw as ufw
from urllib.parse import urlparse

# Import helper functions
from . import helper_functions as hf

# Netplan configuration (DHCP, Static IP, DNS, Default Gateway)
# Netplan: /etc/netplan/
# DNS: /etc/resolv.conf
def config_netplan():
    # 1. Get interface name
    interface_name = subprocess.run("ip -o -4 route show to default | awk '{print $5}'", capture_output=True, shell=True, check=True)
    interface_name = str(interface_name.stdout).replace('b','').replace('\\n','').strip("'")

    # 2. DHCP needed ?
    print('Wird DHCP benötigt?')
    dhcp_needed = ''
    # Only 'y' and 'n' allowed
    while dhcp_needed not in ['Y','N']:
        dhcp_needed = input('(y/n): ').upper()

    dhcp_needed = 'true' if dhcp_needed == 'Y' else 'false'

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

    # Create a empty list and fill it with the config values
    config_list = []
    config_list += [interface_name] # 1. Interface
    config_list += [dhcp_needed]    # 2. DHCP true/false
    config_list += [static_ip]      # 3. Static IP for interface, with subnetprefix
    config_list += [dns_ips]        # 4. DNS
    config_list += [dgw_ips]        # 5. Default gateway

    # Get path to template file
    netplan_template = os.path.join(sys.path[0]) + '/config/templates/netplan.template'

    # Get filenames in netplan directory
    netplan_path = '/etc/netplan/'
    files = os.listdir(netplan_path)
    netplan_file = netplan_path + files[0].strip("'")

    # Read from template file
    with open (netplan_template, 'r', encoding='UTF-8') as file:
        filedata = file.read()
    
    # Replace variable with config value from config_list
    count = 1
    for n in config_list:
        to_replace = '$'+str(count)+'$'
        filedata = filedata.replace(to_replace, n)
        count = count + 1

    # Write to file in current config folder
    netplan_current_config = os.path.join(sys.path[0]) + '/config/current_config/' + files[0]
    with open (netplan_current_config, 'w+', encoding='UTF-8') as file:
        file.write(filedata)

    # Change file permissions to "666" so everyone can read and write
    os.chmod(netplan_file, 0o666)

    # # Replace netplan with template file
    os.system('cat ' + netplan_current_config + ' > ' + netplan_file)

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

# Syslog configuration
# /etc/rsyslog.conf
def config_syslog():
    print('Wird Syslog benötigt?')
    syslog_needed = ''
    # Only 'y' and 'n' allowed
    while syslog_needed not in ['Y','N']:
        syslog_needed = input('(y/n): ').upper()
    
    syslog_needed = True if syslog_needed == 'Y' else False

    if syslog_needed is True:
        # Get Syslog Server IP
        print('Wie lautet die IP des Syslog Servers?')
        syslog_server_ip_list = hf.get_ips()
        # List to string, with spaces in between
        syslog_server_ip = ' '.join(syslog_server_ip_list)

        # Create a empty list and fill it with the syslog server IP
        config_list = []
        config_list += [syslog_server_ip]

        # Get path to template file
        syslog_template = os.path.join(sys.path[0]) + '/config/templates/syslog.template'

        # Read from template file
        with open (syslog_template, 'r', encoding='UTF-8') as file:
            filedata = file.read()
    
        # Replace variable with config value from config_list
        count = 1
        for n in config_list:
            to_replace = '$'+str(count)+'$'
            filedata = filedata.replace(to_replace, n)
            count = count + 1
    
        # Write to file in current config folder
        syslog_current_config = os.path.join(sys.path[0]) + '/config/current_config/syslog.cfg'
        with open (syslog_current_config, 'w+', encoding='UTF-8') as file:
            file.write(filedata)

        syslog_file = '/etc/rsyslog.conf'
        # Change file permissions to "666" so everyone can read and write
        os.chmod(syslog_file, 0o666)

        # Replace syslog file with template file
        os.system('cat ' + syslog_current_config + ' > ' + syslog_file)

        # Change file permissions to "644" so everyone can read, but only owner can write
        os.chmod(syslog_file, 0o644)

        # Restart syslog service
        os.system('systemctl restart rsyslog')
    else:
        return

# SNMP configuration
# /etc/snmp/snmpd.conf
def config_snmp():
    print('Wird SNMPv3 benötigt?')
    snmp_needed = ''
    # Only 'y' and 'n' allowed
    while snmp_needed not in ['Y','N']:
        snmp_needed = input('(y/n): ').upper()
    
    snmp_needed = True if snmp_needed == 'Y' else False

    if snmp_needed is True:
        # Create a dict with user, password and encryption_key
        config_dict = {'USER': '', 'PASSWORD': '', 'ENCRYPTION_KEY': ''}

        # Get user and password
        print('Bitte einen Usernamen eingeben')        
        config_dict['USER']= input('User: ')

        # Min password length 8 characters 
        snmp_password = ''
        while len(snmp_password) < 8:
            print('Bitte ein Passwort eingeben (min. 8 Zeichen)')
            snmp_password = input('Passwort: ')
        config_dict['PASSWORD']= snmp_password

        # Generate random encryption key with 16 characters
        config_dict['ENCRYPTION_KEY']= ''.join(random.sample(ascii_letters,16))
        # Get path to template file
        snmp_template = os.path.join(sys.path[0]) + '/config/templates/snmp.template'
    
        # Read from template file
        with open (snmp_template, 'r', encoding='UTF-8') as file:
            filedata = file.read()
    
        # Replace variable with config value from config_dict
        for key in config_dict:
            to_replace = '$'+key+'$'
            filedata = filedata.replace(to_replace, config_dict.get(key))
    
        # Write to file in current config folder
        snmp_current_config = os.path.join(sys.path[0]) + '/config/current_config/snmp.cfg'
        with open (snmp_current_config, 'w+', encoding='UTF-8') as file:
            file.write(filedata)

        # Activate current config
        snmp_file = '/etc/snmp/snmpd.conf'
        # Change file permissions to "666" so everyone can read and write
        os.chmod(snmp_file, 0o666)

        # Replace snmp file with template file
        os.system('cat ' + snmp_current_config + ' > ' + snmp_file)

        # Change file permissions to "644" so everyone can read, but only owner can write
        os.chmod(snmp_file, 0o644)

        # Restart SNMP Service
        os.system('systemctl restart snmpd')
    else:
        return

def firewall_generator():
    print('TEST')

# NTP configuration
# /etc/systemd/timesyncd.conf
def config_ntp():
    print('NTP Test')

# EasyUFW => A thin wrapper over the thin wrapper that is ufw
    # Usage:
    #   ufw.disable()        # disable firewall
    #   ufw.enable()         # enable firewall
    #   ufw.allow()          # default allow -- allow all
    #   ufw.allow(22)        # allow port 22, any protocol
    #   ufw.allow(22,'tcp')  # allow port 22, tcp protocol
    #   ufw.allow('22/tcp')  # allow port 22, tcp protocol
    #   ufw.allow(53,'udp')  # allow port 53, udp protocol
    #   ufw.allow(53,'udp')  # allow port 53, udp protocol
    #   ufw.deny()           # default deny -- deny all
    #   ufw.deny(22,'tcp')   # deny port 22, tcp protocol
    #   ufw.delete(22)       # delete rules referencing port 22
    #   ufw.reset()          # restore defaults
    #   ufw.status()         # return status string (default verbose=True)
    #   ufw.run("allow 22") # directly run command as if from command line

# UFW Default Setup
def ufw_initial_setup():
    # Enable UFW
    print('DEBUG: Enable UFW')
    ufw.enable()
    # Enable UFW logging
    print('DEBUG: Enable UFW logging')
    ufw.run('logging on')
    # Deny everything
    print('DEBUG: Deny all incoming and outgoing traffic')
    ufw.run('default deny incoming')
    ufw.run('default deny outgoing')
    # Allow SSH on IP 192.168.231.1
    print('DEBUG: Allow SSH from IP 192.168.231.1')
    ufw_rule_generator(port=22,target_ip='192.168.231.1')
    # Show UFW Status
    print(ufw.status())


# UFW Rule Generator 
def ufw_rule_generator (port='', target_ip='', protocol=''):
    # Get interface name
    interface = subprocess.run("ip -o -4 route show to default | awk '{print $5}'", capture_output=True, shell=True, check=True)
    interface = str(interface.stdout).replace('b','').split('\\n', 1)[0].strip("'") # Get only the first Interface entry

    # DEBUG
    print('DEBUG: Port=' + str(port) + '|| IP=' + str(target_ip) + '|| Protocol=' + str(protocol) + '|| Interface=' + str(interface))

    # Create Incoming Rules:
    # Syntax: "sudo ufw allow in from <ip> to any proto <protocol> port <port>"
    # DNS example: "sudo ufw allow in on ens33 to 8.8.8.8 port 53"
    # No IP-address given, not recommended!
    if target_ip == '':
        print('DEBUG: No IP-address given, not recommended!')
        # No protocol given
        if protocol == '':
            # Allow in from anywhere to given port
            ufw.run('allow in to any port ' + str(port))
        # Protocol given
        else:
            # Allow in from anywhere to given port + protocol
            ufw.run('allow in to any proto ' + str(protocol) + ' port ' + str(port))
    # IP-address given
    else:
        # No protocol given
        if protocol == '':
            # Allow in from given IP to given port
            ufw.run('allow in from ' + str(target_ip) + ' to any port ' + str(port))
        # Protocol given
        else:
            # Allow in from given IP to given port + protocol
            ufw.run('allow in from ' + str(target_ip) + ' to any proto ' + str(protocol) + ' port ' + str(port))

    # Create Outgoing Rules:
    # Syntax: "sudo ufw allow out on <interface> to <ip> proto <protocol> port <port>"
    # DNS example: "sudo ufw allow out on ens33 to 8.8.8.8 port 53"
    # No IP-address given, not recommended!
    if target_ip == '':
        print('DEBUG: No IP-address given, not recommended!')
        # No protocol given
        if protocol == '':
            # Allow out to anywhere to given port
            ufw.run('allow out on ' + str(interface) + ' to any port ' + str(port))
        # Protocol given
        else:
            # Allow out to anywhere to given port + protocol
            ufw.run('allow out on ' + str(interface) + ' to any proto ' + str(protocol) + ' port ' + str(port))
    # IP-address given
    else:
        # No protocol given
        if protocol == '':
            # Allow out to given IP to given port
            ufw.run('allow out on ' + str(interface) + ' to ' + str(target_ip) + ' port ' + str(port))
        # Protocol given
        else:
            # Allow out to given IP to given port + protocol
            ufw.run('allow out on ' + str(interface) + ' to ' + str(target_ip) + ' proto ' + str(protocol) + ' port ' + str(port))


def get_repo_list():
    # Get Repos
    repo_list = subprocess.run("apt-cache policy |grep http |awk '{print $2}' |sort -u", capture_output=True, shell=True, check=True)
    repo_list = str(repo_list.stdout).replace('b','',1).strip("'").split("\\n")

    # Remove empty entries
    repo_list = list(filter(None, repo_list))

    # Create empty list
    url_list = []

    count = 0
    for n in repo_list:
        url_list.append(fqdn_to_ip_translator(urlparse(n).netloc))
        count += 1

    return url_list

# Translates Hostname to IP
def fqdn_to_ip_translator(hostname):
    hostname_ip = socket.gethostbyname(str(hostname))
    return str(hostname_ip)

def ufw_rules_add_lists(port='', ip_list='', protocol=''):
    for n in ip_list:
        print(n)
        ufw_rule_generator(port, n, protocol)
