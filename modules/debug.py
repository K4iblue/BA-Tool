import subprocess
#import os
#import sys
#from . import helper_functions as hf
from .easyufw import easyufw as ufw

def debug():
    print('DEBUG')

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
