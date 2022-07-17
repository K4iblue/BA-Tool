import subprocess
import os
import sys
from .pyufw import pyufw

# UFW set default settings and enable
def ufw_set_default_settings():
    # Enable UFW
    os.system('sudo ufw --force enable')
    #subprocess.run('sudo ufw --force enable', capture_output=True, shell=True, check=True)
    
    # Set Default settings
    #print('DEBUG: Deny all incoming and outgoing traffic, set logging to medium')
    subprocess.run('sudo ufw default deny incoming', capture_output=True, shell=True, check=True)
    subprocess.run('sudo ufw default deny outgoing', capture_output=True, shell=True, check=True)
    subprocess.run('sudo ufw logging medium', capture_output=True, shell=True, check=True)

    # DEBUG: Add SSH IP
    ufw_rule_generator(port=22, target_ip='192.168.231.1')


# UFW Rule Generator 
def ufw_rule_generator (port='', target_ip='', protocol=''):
    # Get interface name
    interface = subprocess.run("ip -o -4 route show to default | awk '{print $5}'", capture_output=True, shell=True, check=True)
    interface = str(interface.stdout).replace('b','').split('\\n', 1)[0].strip("'") # Get only the first Interface entry

    # DEBUG
    #print('DEBUG: Port=' + str(port) + ' || IP=' + str(target_ip) + ' || Protocol=' + str(protocol) + ' || Interface=' + str(interface))

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

# UFW Allow outgoing Ping
# /etc/default/ufw/before.rules
def ufw_allow_ping():
    # Backup before.rules file
    os.system('sudo cp -n /etc/ufw/before.rules /etc/ufw/backups/before.rules.backup')

    # Get path to template file
    before_rules_template = os.path.join(sys.path[0]) + '/config/templates/ufw_before_rules.template'

    # Path to original "before.rule" file
    before_rules_file = '/etc/ufw/before.rules'

    # Overwrite original "before.rule" file with template
    subprocess.run(('sudo cat ' + before_rules_template + ' > ' + before_rules_file), capture_output=True, shell=True, check=True)

    # Reload UFW rules to allow the ICMP changes
    subprocess.run('sudo ufw reload', capture_output=True, shell=True, check=True)
