#import subprocess
#import os
#import sys
#from . import helper_functions as hf
from .easyufw import easyufw as ufw

def debug_firewall():
    print('SSH')
    debug(22)
    print('DNS')
    debug(53,'udp', '192.168.1.2')
    print('HTTP')
    debug(port=80,ip='192.168.1.0/24')


def debug(port, protocol='', ip=''):
    print('DEBUG: Firewall function call')

    # Start UFW if disabled
    ufw.enable()

    # 1x IP: ufw allow from 203.0.113.103 proto tcp to any port 22
    # Range: ufw allow from 203.0.113.0/24 proto tcp to any port 22
    # Für alle IPs
    if ip == '':
        print('Port ' + str(port) + '/' + str(protocol) + ' wird freigegeben')
        if protocol == '':
            ufw.allow(port)
        else:
            ufw.allow(port, protocol)
    # Nur bestimmte IPs
    else:
        print('Port ' + str(port) + '/' + str(protocol) + ' wird freigegeben für ' + str(ip))
        if protocol == '':
            ufw.run('allow from' + str(ip) + 'to any' + str(port))
        else:
            ufw.run('allow from' + str(ip) + 'proto' + str(protocol) + 'to any' + str(port))
        
    print(ufw.status())


    #os.system('sudo ufw enable')

    
    #ufw.allow(port int, protocol str ['tcp','udp'])

    #os.system('sudo ufw allow'+port)
    #os.system('sudo ufw allow out'+port)
    #os.system('sudo ufw deny'+port)
    #os.system('sudo ufw deny out'+port)

#debug(22,'tcp', '192.168.1.1')
#debug(54,'udp', '192.168.1.2')
#debug(port=80,ip='192.168.1.3')
