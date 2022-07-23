import os
from . import hardening
from . import network as net
from . import firewall as fw
from . import docker as doc
#from . import maintenance
from . import debug as de
from . import helper_functions as hf


# Main Menu
def main_menu():
    print('----------- Hauptmenü ----------- \n' +
          '0.\t Exit Programm \n' +
          '1.\t Härtung \n' +
          '2.\t Netzwerkkonfiguration \n' +
          '3.\t Container Verwaltung \n' +
          '4.\t Systempflege \n' +
          #'5.\t DEBUG \n' +
          '----- Please enter a number (0-4) -----')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,6)

    match case_number:
        case 0:
            quit()
        case 1:
            hardening_submenu()
        case 2:
            network_submenu()
        case 3:
            container_submenu()
        case 4:
            maintenance_submenu()
        case 5:
            debug_submenu()

# Hardening Menu
def hardening_submenu():
    print('----------- Hardening Menu ----------- \n' +
            '0.\t Main Menu \n' +
            '1.\t Härtung durchführen \n' +
            '2.\t Härtung Überprüfen \n' +
            '----- Please enter a number (0-2) -----')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,3)
    
    match case_number:
        case 0:
            main_menu()
        case 1:
            hardening.create_configfile()
        case 2:
            print('Case 2')

# Network Menu
def network_submenu():
    print('----------- Netzwerkkonfiguration ----------- \n' +
            '0.\t Main Menu \n' +
            '1.\t Vollständige Netzwerk Konfiguration \n' +
            '2.\t Netplan Konfiguration (DNS, Default Gateway, Static IP) \n' +
            '3.\t NTP Konfiguration \n' +
            '4.\t SNMPv3 Konfiguration \n' +
            '5.\t Syslog Konfiguration \n' +            
            '----- Please enter a number (0-5) -----')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,6)
    
    match case_number:
        case 0:
            main_menu()
        case 1:
            net.complete_configuration_dialog()
            network_submenu()
        case 2:
            net.config_netplan()
            network_submenu()
        case 3:
            net.config_ntp()
            network_submenu()
        case 4:
            net.config_syslog()
            network_submenu()
        case 5:
            net.config_snmp()
            network_submenu()
        case _:
            network_submenu()

# Container Menu
def container_submenu():
    print('----------- Container Verwaltung ----------- \n' +
            '0.\t Main Menu \n' +
            '1.\t Liste aller Container anzeigen \n' +
            '2.\t Liste aller Images anzeigen \n' +
            '3.\t Liste aller Volumes anzeigen \n' +
            '4.\t Container starten \n' +
            '5.\t Container stoppen \n' +
            '6.\t Container erstellen (Dockerfile) \n' +
            '7.\t Container erstellen (Image) \n' +
            '8.\t Container löschen \n' +
            '9.\t Image löschen \n' +
            '10.\t Volume löschen \n' +
            '----- Please enter a number (0-10) -----')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,11)
    
    match case_number:
        case 0:
            main_menu()
        case 1:
            doc.show_container_list()
            container_submenu()
        case 2:
            doc.show_images_list()
            container_submenu()
        case 3:
            doc.show_volumes_list()
            container_submenu()
        case 4:
            doc.start_container()
            container_submenu()
        case 5:
            doc.stop_container()
            container_submenu()
        case 6:
            doc.create_container_from_file()
            container_submenu()
        case 7:
            doc.create_container_from_image()
            container_submenu()
        case 8:
            doc.delete_container()
            container_submenu()
        case 9:
            doc.delete_image()
            container_submenu()
        case 10:
            doc.delete_volume()
            container_submenu()

# Maintenance Menu
def maintenance_submenu():
    print('----------- Maintenance Menu ----------- \n' +
            '0. Main Menu \n' +
            '1. Automatische Updates de-/aktivieren \n' +
            '2. Standardprogramme installieren \n' +
            '----- Please enter a number (0-2) -----')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,3)

    match case_number:
        case 0:
            main_menu()
        case 1:
            print('Case 1')
        case 2:
            print('Case 2')

# DEBUG Menu
def debug_submenu():
    print('----------- Debug Menu ----------- \n' +
            '0. \t Main Menu\n' +
            '1. \t DEBUG\n' +
            '----- Please enter a number (0-99) -----')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,99)
    match case_number:
        case 0:
            main_menu()
        case 1:
            de.debug()
            debug_submenu()
        case _:
            debug_submenu()
