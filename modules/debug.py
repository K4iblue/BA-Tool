#import subprocess
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

def debug(port, protocol='', sender_ip='', target_ip=''):
    # Start UFW if disabled and print status 
    ufw.enable()         # enable firewall
    print(ufw.status())  # DEBUG

    # UFW default => deny everything even ping!
    ufw.run('default deny incoming')
    ufw.run('default deny outgoing')
    # but allow SSH (Port 22)
    print('SSH (Port: 22) freigeben')
    ufw.allow(22)
    print(ufw.status()) # DEBUG

    # Allow SSH only from specific IP-address
    # ufw.run('allow from ' + str(ip) + ' to any port ' str(port))

    # Define outgoing rules only !!!
    # sudo ufw allow out from <sender.ip> to <target.ip> port <port>

    # No IP-address give
    if sender_ip == '' and target_ip == '':
        # No protocol given
        if protocol == '':
            ufw.allow(port)
        # Protocol given
        else:
            ufw.allow(port, protocol)

    # only sender IP given 
    elif sender_ip == '':
        # No protocol given
        if protocol == '':
            ufw.run('ufw allow out from ' + sender_ip + ' to any port ' + port)
        # Protocol given
        else:
            ufw.run('ufw allow out from ' + sender_ip + ' to any proto ' + protocol + ' port ' + port)

    # only target IP given
    elif target_ip == '':
        # No protocol given
        if protocol == '':
            ufw.run('ufw allow out from ' + sender_ip + ' to ' + target_ip + ' port ' + port)
        # Protocol given
        else:
            ufw.run('ufw allow out from ' + sender_ip + ' to ' + target_ip + ' proto ' + protocol + ' port ' + port)

    

    #ufw.run('allow out from 1.1.1.1 to any port')
   
   # Working DNS
   # sudo ufw allow out to 8.8.8.8 port 53
   # sudo ufw allow in from 8.8.8.8 port 53

   # Working SSH
   # sudo ufw allow from 192.168.231.1 proto tcp to any port 22


#############################################################################
# Working SSH from one IP and receiving DNS answer from 8.8.8.8

# Mit TCP als protocol
# sudo ufw allow from 192.168.231.1 proto tcp to any port 22

# Ohne Protocol
# sudo ufw allow from 8.8.8.8 to any port 53