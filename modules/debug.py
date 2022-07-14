#import subprocess
#import os
#import sys
#from . import helper_functions as hf
#from .easyufw import easyufw as ufw

def debug(port, protocol='udp', ip=''):
    print('### DEBUG ###')
    # Firewall generator (Port Range: 0 - 65536)
    print('Start Firewall Generator')

    # 1x IP: ufw allow from 203.0.113.103 proto tcp to any port 22
    # Range: ufw allow from 203.0.113.0/24 proto tcp to any port 22
    # Für alle IPs
    if ip == '':
        print('## DEBUG ## Port ' + str(port) + '/' + str(protocol) + ' wird freigegeben')             # DEBUG
        #ufw.allow(port, protocol)
    # Nur bestimmte IPs
    else:
        print('## DEBUG ## Port ' + str(port) + '/' + str(protocol) + ' wird freigegeben für ' + str(ip))   # DEBUG
        #ufw.run('allow' + port + '/' + protocol + 'from' + ip)
    


    #os.system('sudo ufw enable')

    
    #ufw.allow(port int, protocol str ['tcp','udp'])

    #os.system('sudo ufw allow'+port)
    #os.system('sudo ufw allow out'+port)
    #os.system('sudo ufw deny'+port)
    #os.system('sudo ufw deny out'+port)

debug(22,'tcp', '192.168.1.1')
debug(54,'udp', '192.168.1.2')
debug(port=80,ip='192.168.1.3')
