#import subprocess
#import os
#import sys
#from . import helper_functions as hf
#from .easyufw import easyufw as ufw
import socket

from modules.network import ufw_rule_generator

def debug():
    test = socket.gethostbyname('de.archive.ubuntu.com')
    test2 = socket.gethostbyname('download.docker.com')
    print(test)
    print(test2)
    ufw_rule_generator(port=80, target_ip=test,protocol='tcp')
    ufw_rule_generator(port=80, target_ip=test2,protocol='tcp')
