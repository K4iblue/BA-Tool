#import subprocess
#import os
#import sys
#from . import helper_functions as hf
#from .easyufw import easyufw as ufw
import socket

def debug():
    test = socket.gethostbyname('de.archive.ubuntu.com')
    test2 = socket.gethostbyname('download.docker.com')
    print(test)
    print(test2)