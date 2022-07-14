#import subprocess
#import os
#import sys
#from . import helper_functions as hf
from .easyufw import easyufw as ufw

#def debug_firewall():
#    print('SSH')
#    debug(22)
#    print('DNS')
#    debug(53,'udp', '192.168.1.2')
#    print('HTTP')
#    debug(port=80,ip='192.168.1.0/24')

# A thin wrapper over the thin wrapper that is ufw
# Usage:
#   import easyufw as ufw
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
#def debug(port, protocol='', ip='', direction=''):
def debug():
    # DEBUGGING IP
    ip = '1.1.1.1'
    port = 53

    # Start UFW if disabled and print status 
    ufw.enable()         # enable firewall
    print(ufw.status())

    # UFW default deny everything, but allow SSH (Port 22)
    ufw.run('default deny incoming')
    ufw.run('default deny outgoing')
    print('SSH (Port: 22) freigeben')
    ufw.allow(22)

    print('DNS (Port: 53) für 1.1.1.1 freigeben')
    ufw.run('allow from ' + str(ip) + ' to any port ' + str(port))

    print(ufw.status())
    #print('DEBUG: Firewall function call')
#
    ## Start UFW if disabled
    #ufw.enable()
#
    ## 1x IP: ufw allow from 203.0.113.103 proto tcp to any port 22
    ## Range: ufw allow from 203.0.113.0/24 proto tcp to any port 22
    ## Für alle IPs
    #if ip == '':
    #    print('Port ' + str(port) + '/' + str(protocol) + ' wird freigegeben')
    #    if protocol == '':
    #        ufw.allow(port)
    #    else:
    #        ufw.allow(port, protocol)
    ## Nur bestimmte IPs
    #else:
    #    print('Port ' + str(port) + '/' + str(protocol) + ' wird freigegeben für ' + str(ip))
    #    if protocol == '':
    #        print('Test 1')
    #        ufw.run('allow from' + str(ip) + 'to any' + str(port))
    #    else:
    #        print('Test 2')
    #        ufw.run('allow proto' + str(protocol) + 'from any')
    #        ufw.run('allow from' + str(ip) + 'to any' + str(port) + 'proto' + )
    #
    ## Alles außer IP übergeben
    #if ip == '':
    #    # Nur Port und Richtung übergeben
    #    if protocol == '':
    #        # Nur Port übergeben
    #        if direction == '':
    #            ufw.run('allow ' + str(port))
    #        else:
    #            ufw.run('allow ' + str(direction) + ' any' + )
    #    else:
    ## Alles übergeben
    #else:
#
#
    #print(ufw.status())


    #os.system('sudo ufw enable')

    
    #ufw.allow(port int, protocol str ['tcp','udp'])

    #os.system('sudo ufw allow'+port)
    #os.system('sudo ufw allow out'+port)
    #os.system('sudo ufw deny'+port)
    #os.system('sudo ufw deny out'+port)

#debug(22,'tcp', '192.168.1.1')
#debug(54,'udp', '192.168.1.2')
#debug(port=80,ip='192.168.1.3')


# Default UFW Regeln, Logging und erweiterter Status
# sudo ufw logging on
# sudo ufw status verbose
# sudo ufw default deny incoming
# sudo ufw default allow outgoing
# sudo ufw allow from 192.168.178.49 port 22