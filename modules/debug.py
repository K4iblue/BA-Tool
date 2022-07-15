import subprocess
#import os
#import sys
#from . import helper_functions as hf
from .easyufw import easyufw as ufw

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

def debug():
    print('DEBUG')

# UFW Rule Generator 
def ufw_rule_generator (port='', target_ip='', protocol=''):
    # Get interface name
    interface = subprocess.run("ip -o -4 route show to default | awk '{print $5}'", capture_output=True, shell=True, check=True)
    interface = str(interface.stdout).replace('b','').replace('\\n','').strip("'")

    # Incoming: "sudo ufw allow in from <ip> to any proto <protocol> port <port>"
    # DNS Beispiel: "sudo ufw allow in on ens33 to 8.8.8.8 port 53"
    
    # No IP-address given # DEBUGGING ! Falls sollte eigentlich niemals eintreten!
    if target_ip == '':
        print('DEBUG: Keine IP-Adresse angegeben!')
        # No protocol given
        if protocol == '':
            # Allow in from anywhere to given port
            ufw.run('allow in to any port ' + str(port))
            print('1')
        # Protocol given
        else:
            # Allow in from anywhere to given port + protocol
            ufw.run('allow in to any proto ' + str(protocol) + ' port ' + str(port))
            print('2')
    # IP-address given
    else:
        # No protocol given
        if protocol == '':
            # Allow in from given IP to given port
            ufw.run('allow in from ' + str(target_ip) + ' to any port ' + str(port))
            print('3')
        # Protocol given
        else:
            # Allow in from given IP to given port + protocol
            ufw.run('allow in from ' + str(target_ip) + ' to any proto ' + str(protocol) + ' port ' + str(port))
            print('4')

    # Outgoing: "sudo ufw allow out on <interface> to <ip> proto <protocol> port <port>"
    # DNS Beispiel: "sudo ufw allow out on ens33 to 8.8.8.8 port 53"
    
    # No IP-address given # DEBUGGING ! Falls sollte eigentlich niemals eintreten!
    if target_ip == '':
        print('DEBUG: Keine IP-Adresse angegeben!')
        # No protocol given
        if protocol == '':
            # Allow out to anywhere to given port
            ufw.run('allow out on ' + str(interface) + ' to any port ' + str(port))
            print('5')
        # Protocol given
        else:
            # Allow out to anywhere to given port + protocol
            ufw.run('allow out on ' + str(interface) + ' to any proto ' + str(protocol) + ' port ' + str(port))
            print('6')
    # IP-address given
    else:
        # No protocol given
        if protocol == '':
            # Allow out to given IP to given port
            ufw.run('allow out on ' + str(interface) + ' to ' + str(target_ip) + ' port ' + str(port))
            print('7')
        # Protocol given
        else:
            # Allow out to given IP to given port + protocol
            ufw.run('allow out on ' + str(interface) + ' to ' + str(target_ip) + ' proto ' + str(protocol) + ' port ' + str(port))
            print('8')
