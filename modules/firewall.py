import subprocess
import os
import sys
import socket
from urllib.parse import urlparse
from .pyufw import pyufw
from . import helper_functions as hf


# UFW set default settings and enable
def ufw_set_default_settings():
    # Disable UFW
    os.system('sudo ufw --force disable')
    #subprocess.run('sudo ufw --force enable', capture_output=True, shell=True, check=True)
    
    # Set Default settings
    #print('DEBUG: Deny all incoming and outgoing traffic, set logging to medium')
    subprocess.run('sudo ufw default deny incoming', capture_output=True, shell=True, check=True)
    subprocess.run('sudo ufw default deny outgoing', capture_output=True, shell=True, check=True)
    subprocess.run('sudo ufw logging medium', capture_output=True, shell=True, check=True)

    # Add SSH IP
    print('Welche IPs soll SSH Zugang bekommen? Mehrere IP Addressen durch ein Komma trennen!')
    ufw_ssh_ip_list = hf.get_ips()
    ufw_rules_add_lists(port=22, ip_list=ufw_ssh_ip_list)
    #ufw_rule_generator(port=22, target_ip='192.168.231.1')

    # Enable UFW
    os.system('sudo ufw --force enable')


# UFW Rule Generator 
def ufw_rule_generator (port='', target_ip='', protocol=''):
    # Get interface name
    interface = subprocess.run("ip -o -4 route show to default | awk '{print $5}'", capture_output=True, shell=True, check=True)
    interface = str(interface.stdout).replace('b','').split('\\n', 1)[0].strip("'") # Get only the first Interface entry

    # DEBUG
    print('DEBUG: Port=' + str(port) + ' || IP=' + str(target_ip) + ' || Protocol=' + str(protocol) + ' || Interface=' + str(interface))

    # Create Incoming Rules:
    # Syntax: "sudo ufw allow in from <ip> to any proto <protocol> port <port>"
    # DNS example: "sudo ufw allow in on ens33 to 8.8.8.8 port 53"
    # No IP-address given, not recommended!
    if target_ip == '':
        #print('DEBUG: No IP-address given, not recommended!')
        # No protocol given
        if protocol == '':
            # Allow in from anywhere to given port
            subprocess.run(('sudo ufw allow in to any port ' + str(port)), capture_output=True, shell=True, check=True)
        # Protocol given
        else:
            # Allow in from anywhere to given port + protocol
            subprocess.run(('sudo ufw allow in to any proto ' + str(protocol) + ' port ' + str(port)), capture_output=True, shell=True, check=True)
    # IP-address given
    else:
        # No protocol given
        if protocol == '':
            # Allow in from given IP to given port
            subprocess.run(('sudo ufw allow in from ' + str(target_ip) + ' to any port ' + str(port)), capture_output=True, shell=True, check=True)
        # Protocol given
        else:
            # Allow in from given IP to given port + protocol
            subprocess.run(('sudo ufw allow in from ' + str(target_ip) + ' to any proto ' + str(protocol) + ' port ' + str(port)), capture_output=True, shell=True, check=True)

    # Create Outgoing Rules:
    # Syntax: "sudo ufw allow out on <interface> to <ip> proto <protocol> port <port>"
    # DNS example: "sudo ufw allow out on ens33 to 8.8.8.8 port 53"
    # No IP-address given, not recommended!
    if target_ip == '':
        #print('DEBUG: No IP-address given, not recommended!')
        # No protocol given
        if protocol == '':
            # Allow out to anywhere to given port
            subprocess.run(('sudo ufw allow out on ' + str(interface) + ' to any port ' + str(port)), capture_output=True, shell=True, check=True)
        # Protocol given
        else:
            # Allow out to anywhere to given port + protocol
            subprocess.run(('sudo ufw allow out on ' + str(interface) + ' to any proto ' + str(protocol) + ' port ' + str(port)), capture_output=True, shell=True, check=True)
    # IP-address given
    else:
        # No protocol given
        if protocol == '':
            # Allow out to given IP to given port
            subprocess.run(('sudo ufw allow out on ' + str(interface) + ' to ' + str(target_ip) + ' port ' + str(port)), capture_output=True, shell=True, check=True)
        # Protocol given
        else:
            # Allow out to given IP to given port + protocol
            subprocess.run(('sudo ufw allow out on ' + str(interface) + ' to ' + str(target_ip) + ' proto ' + str(protocol) + ' port ' + str(port)), capture_output=True, shell=True, check=True)


# UFW Rule Generator (for lists of IPs)
def ufw_rules_add_lists(port='', ip_list='', protocol=''):
    for n in ip_list:
        ufw_rule_generator(port, n, protocol)


# UFW delete all Rules
def ufw_delete_rules():
    # Get all rules
    all_rules = pyufw.get_rules()
    
    # Delete rules individually
    for n in all_rules:
        subprocess.run(('sudo ufw delete ' + all_rules.get(n)), capture_output=True, shell=True, check=True)
        #print('DEBUG: || Delete rule = ' + all_rules.get(n))


# UFW disable IPv6
# /etc/default/ufw
def ufw_disable_ipv6():
    print('Soll IPv6 in der Firewall deaktiviert werden?')
    ipv6_ufw_needed = ''
    # Only 'y' and 'n' allowed
    while ipv6_ufw_needed not in ['Y','N']:
        ipv6_ufw_needed = input('(y/n): ').upper()
    
    ipv6_ufw_needed = True if ipv6_ufw_needed == 'Y' else False

    if ipv6_ufw_needed is True:
        # Backup "default/ufw" file to a backup folder
        os.system('sudo mkdir -p "/etc/default/ufw-backup/" && sudo cp -n /etc/default/ufw /etc/default/ufw-backup/ufw.backup')

        # Path to "/etc/default/ufw"
        default_ufw = '/etc/default/ufw'
    
        # Read from template file
        with open (default_ufw, 'r', encoding='UTF-8') as file:
            filedata = file.read()
    
        # Replace IPv6=yes line
        filedata = filedata.replace('IPV6=yes', 'IPV6=no')
    
        # Write back to file
        with open (default_ufw, 'w', encoding='UTF-8') as file:
            filedata = file.write(filedata)

        # Need to reload firewall
        os.system('sudo ufw reload')
    else:
        return


#### WIP ####
# UFW Allow outgoing Ping
# /etc/default/ufw/before.rules
def ufw_allow_ping():
    # Backup before.rules file to a backup folder
    os.system('sudo mkdir -p "/etc/ufw/backups/" && sudo cp -n /etc/ufw/before.rules /etc/ufw/backups/before.rules.backup')

    # Get path to template file
    before_rules_template = os.path.join(sys.path[0]) + '/config/templates/ufw_before_rules.template'

    # Path to original "before.rule" file
    before_rules_file = '/etc/ufw/before.rules'

    # Overwrite original "before.rule" file with template
    subprocess.run(('sudo cat ' + before_rules_template + ' > ' + before_rules_file), capture_output=True, shell=True, check=True)

    # Reload UFW rules to allow the ICMP changes
    #subprocess.run('sudo ufw reload', capture_output=True, shell=True, check=True)


# Get a list of all added "apt-get" Repositories
def get_repo_list():
    # Get Repos
    repo_list = subprocess.run("apt-cache policy |grep http |awk '{print $2}' |sort -u", capture_output=True, shell=True, check=True)
    repo_list = str(repo_list.stdout).replace('b','',1).strip("'").split("\\n")

    # Remove empty entries
    repo_list = list(filter(None, repo_list))

    # Create empty list
    url_list = []

    # Add translated IPs to new list
    count = 0
    for n in repo_list:
        url_list.append(fqdn_to_ip_translator(urlparse(n).netloc))
        count += 1

    return url_list


#Get a list of all added NTP Servers
def get_ntp_list():
    # Get ntp server list
    ntp_list = subprocess.run("grep -v '^\s*$\|^\s*\# NTP=' '/etc/systemd/timesyncd.conf' |awk '!/^ *#/ &&  NF'", capture_output=True, shell=True, check=True)

    # String to list
    ntp_list = str(ntp_list.stdout).replace("'",'').replace('NTP=','').split("\\n")

    # Pop first element and remove empty entries
    ntp_list.pop(0)
    ntp_list = list(filter(None, ntp_list))

    # List to string, split string again at whitespaces
    if len(ntp_list) != 0:
        ntp_list_string = ntp_list[0]
        ntp_list = ntp_list_string.split(' ')
    else:
        return 

    # Create empty list
    url_list = []

    # Add translated IPs to new list
    count = 0
    for n in ntp_list:
        if hf.ip_validation(n) is False:
            url_list.append(fqdn_to_ip_translator(n))
            count += 1
        else:
            url_list.append(n)
            count += 1

    return url_list


# Translates Hostname to IP
def fqdn_to_ip_translator(hostname):
    hostname_ip = socket.gethostbyname(str(hostname))
    return str(hostname_ip)
