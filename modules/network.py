#from ipaddress import ip_address
import subprocess
import os
import sys
import random
import time
from string import ascii_letters, punctuation, digits
from . import firewall as fw
from . import helper_functions as hf


# Configuration of all Networking parts
def complete_configuration_dialog():
    print('Netzwerk komplett konfigurieren?')
    complete_config_needed = ''
    # Only 'y' and 'n' allowed
    while complete_config_needed not in ['Y','N']:
        complete_config_needed = input('(y/n): ').upper()
    
    complete_config_needed = True if complete_config_needed == 'Y' else False

    if complete_config_needed is True:
        # Install UFW, rsyslog and snmp
        install_networking_packages()

        # Reset Firewall, disable IPv6, set Default Settings
        fw.ufw_disable_ipv6()
        fw.ufw_delete_rules()
        fw.ufw_set_default_settings()
        fw.ufw_allow_docker()

        # Configure Network
        config_netplan()
        config_ntp()
        config_syslog()
        config_snmp()



        # Add UFW rules, if not already added
        # UFW add APT repos
        fw.ufw_rules_add_lists(port=80, ip_list=fw.get_repo_list(), protocol='tcp')
        # UFW add NTP server if missing
        fw.ufw_rules_add_lists(port=123, ip_list=fw.get_ntp_list())
    else:
        return


# Netplan configuration (DHCP, Static IP, DNS, Default Gateway)
# Netplan: /etc/netplan/
# DNS: /etc/resolv.conf
def config_netplan():
    # 1. Get interface name
    interface_name = subprocess.run("ip -o -4 route show to default | awk '{print $5}'", capture_output=True, shell=True, check=True)
    interface_name = str(interface_name.stdout).replace('b','').replace('\\n','').strip("'")

    # 2. DHCP needed ?
    #print('Wird DHCP benötigt?')
    #dhcp_needed = ''
    ## Only 'y' and 'n' allowed
    #while dhcp_needed not in ['Y','N']:
    #    dhcp_needed = input('(y/n): ').upper()

    #dhcp_needed = 'true' if dhcp_needed == 'Y' else 'false'

    #if dhcp_needed = 'true':
    #    # Create a empty list and fill it with the config values
    #    config_list = []
    #    config_list += [interface_name] # 1. Interface

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
    print(dns_ips)

    # 4. Default gateway 
    print('Wie lautet die IP des Default gateways?')
    dgw_ips_list = hf.get_ips()
    # List to string, with spaces in between
    dgw_ips = ' '.join(dgw_ips_list)

    # Create a empty list and fill it with the config values
    config_list = []
    config_list += [interface_name] # 1. Interface
    #config_list += [dhcp_needed]    # 2. DHCP true/false
    config_list += [static_ip]      # 3. Static IP for interface, with subnetprefix
    config_list += [dns_ips]        # 4. DNS
    config_list += [dgw_ips]        # 5. Default gateway

    # Generate Firewall Rules for DNS
    fw.ufw_rules_add_lists(port=53,ip_list=dns_ips_list)

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
    os.system('sudo systemctl restart systemd-resolved.service')
    # Sleep 3 seconds so DNS Server can get up
    time.sleep(3)


# NTP configuration
# /etc/systemd/timesyncd.conf
def config_ntp():
    print('Wird NTP benötigt?')
    ntp_needed = ''
    # Only 'y' and 'n' allowed
    while ntp_needed not in ['Y','N']:
        ntp_needed = input('(y/n): ').upper()
    
    ntp_needed = True if ntp_needed == 'Y' else False
    
    if ntp_needed is True:
        # Get NTP Servers
        print('Wie lauten die NTP Server (IPs oder Domains)? Mehrere Server durch ein Komma trennen!')
        ntp_server_list = input('NTP Server: ')
        # Remove Spaces
        ntp_server_list = ntp_server_list.replace(' ', '')
        # Create list from string
        ntp_server_list = ntp_server_list.split(',')
        # List to string, with spaces in between
        ntp_server = ' '.join(ntp_server_list)

        # Create a empty list and fill it with the syslog server IP
        config_list = []
        config_list += [ntp_server]

        # Get path to template file
        ntp_template = os.path.join(sys.path[0]) + '/config/templates/ntp.template'

        # Read from template file
        with open (ntp_template, 'r', encoding='UTF-8') as file:
            filedata = file.read()

        # Replace variable with config value from config_list
        count = 1
        for n in config_list:
            to_replace = '$'+str(count)+'$'
            filedata = filedata.replace(to_replace, n)
            count = count + 1

        # Write to file in current config folder
        ntp_current_config = os.path.join(sys.path[0]) + '/config/current_config/ntp.cfg'
        with open (ntp_current_config, 'w+', encoding='UTF-8') as file:
            file.write(filedata)

        ntp_file = '/etc/systemd/timesyncd.conf'
        # Change file permissions to "666" so everyone can read and write
        os.chmod(ntp_file, 0o666)

        # Replace syslog file with template file
        os.system('cat ' + ntp_current_config + ' > ' + ntp_file)

        # Change file permissions to "644" so everyone can read, but only owner can write
        os.chmod(ntp_file, 0o644)

        # Restart NTP Service
        os.system('systemctl restart systemd-timesyncd.service')

        # Generate Firewall Rules for NTP
        # fw.ufw_rules_add_lists(port=123,ip_list=fw.get_ntp_list())
    else:
        return


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

        # Generate Firewall Rules for Syslog
        fw.ufw_rules_add_lists(port=514,ip_list=syslog_server_ip_list,protocol='udp')
        fw.ufw_rules_add_lists(port=50514,ip_list=syslog_server_ip_list,protocol='tcp')

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
        config_dict = {'AGENT-IP':'','USER': '', 'PASSWORD': '', 'ENCRYPTION_KEY': ''}

        # Get Agent IP Adresse
        print('Wie lautet die IP des SNMP Managers?') 
        config_dict['AGENT-IP']= hf.get_ips()

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
        config_dict['ENCRYPTION_KEY']= ''.join(random.sample(ascii_letters + digits + punctuation,16))
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
        snmp_current_config = os.path.join(sys.path[0]) + '/config/current_config/snmpd.conf'
        with open (snmp_current_config, 'w+', encoding='UTF-8') as file:
            file.write(filedata)

        # Activate current config
        snmp_file = '/etc/snmp/snmpd.conf'
        # Change file permissions to "666" so everyone can read and write
        #os.chmod(snmp_file, 0o666)

        # Replace snmp file with template file
        os.system('sudo cp ' + snmp_current_config + ' ' + snmp_file)

        # Change file permissions to "644" so everyone can read, but only owner can write
        os.chmod(snmp_file, 0o644)

        # Generate Firewall Rules for SNMPv3
        fw.ufw_rule_generator(port=161,target_ip=config_dict['AGENT-IP'],protocol='udp')
        #fw.ufw_rule_generator(port=162,target_ip=config_dict['AGENT-IP'],protocol='udp')   # Traps needed?

        # Restart SNMP Service
        os.system('systemctl restart snmpd')
    else:
        return


# Install UFW, rsyslog and snmp
def install_networking_packages():
    print('Installing Syslog, SNMP if not already installed')
    os.system('sudo apt install rsyslog snmpd snmp -y')
