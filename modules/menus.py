from . import hardening
from . import network as nw
#from . import docker
#from . import maintenance
from . import debug as de
from . import helper_functions as hf

# Main and submenus

# Main Menu
def main_menu():
    print('----------- Main Menu ----------- \n' +
          '0. Exit Programm \n' +
          '1. Härtung \n' +
          '2. Docker \n' +
          '3. Systempflege \n' +
          '4. DEBUG \n' +
          '----- Please enter a number (0-4) -----')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,5)

    match case_number:
        case 0:
            quit()
        case 1:
            hardening_submenu()
        case 2:
            docker_submenu()
        case 3:
            maintenance_submenu()
        case 4:
            debug_submenu()

# Hardening Menu
def hardening_submenu():
    print('----------- Hardening Menu ----------- \n' +
            '0. Main Menu \n' +
            '1. Härtung durchführen \n' +
            '2. Härtung Überprüfen \n' +
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

# Docker Menu
def docker_submenu():
    print('----------- Docker Menu ----------- \n' +
            '0. Main Menu \n' +
            '1. Docker Container erstellen \n' +
            '2. Docker Container starten \n' +
            '3. Docker Container stoppen \n' +
            '4. Docker Container löschen \n' +
            '5. Docker Container auflisten \n' +
            '6. Docker Image löschen \n' +
            '7. Docker Images auflisten \n' +
            '----- Please enter a number (0-7) -----')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,8)
    
    match case_number:
        case 0:
            main_menu()
        case 1:
            print('Case 1')
        case 2:
            print('Case 2')
        case 3:
            print('Case 3')
        case 4:
            print('Case 4')
        case 5:
            print('Case 5')
        case 6:
            print('Case 6')
        case 7:
            print('Case 7')

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
            '0. Main Menu \n' +
            '1. DEBUG\n' +
            '2. Netplan config\n' +
            '3. Syslog config\n' +
            '4. SNMP config\n' +
            '5. Debug UFW Initial Setup\n' +
            '6. Debug UFW Generator\n' + 
            '----- Please enter a number (0-99) -----')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,99)

    match case_number:
        case 0:
            main_menu()
        case 1:
            de.debug()
            debug_submenu()
        case 2:
            nw.config_netplan()
            debug_submenu()
        case 3:
            nw.config_syslog()
            debug_submenu()
        case 4:
            nw.config_snmp()
            debug_submenu()
        case 5:
            nw.ufw_initial_setup()
            debug_submenu()
        case 6:
            #print('Port=22, Target IP="192.168.231.1", Protocol=""')
            de.ufw_rule_generator(port=22, target_ip='192.168.231.1')

            #print('Port=53, Target IP=8.8.8.8, Protocol=""')
            de.ufw_rule_generator (port=53, target_ip='8.8.8.8', protocol='')
            de.ufw_rule_generator (port=443, target_ip='', protocol='')
            #print('Port=53, Target IP=8.8.8.8, Protocol=""')
            #de.ufw_rule_generator (port=53, target_ip='8.8.8.8', protocol='')

            debug_submenu()
        case _:
            debug_submenu()
