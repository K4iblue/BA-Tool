import os
from . import hardening
from . import network as net
from . import firewall as fw
from . import docker as doc
#from . import maintenance
from . import debug as de
from . import helper_functions as hf

# Main and submenus

# Main Menu
def main_menu():
    print('----------- Main Menu ----------- \n' +
          '0. \t Exit Programm \n' +
          '1. \t Härtung \n' +
          '2. \t Netzwerk \n' +
          '3. \t Docker \n' +
          '4. \t Systempflege \n' +
          '5. \t DEBUG \n' +
          '----- Please enter a number (0-5) -----')

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
            docker_submenu()
        case 4:
            maintenance_submenu()
        case 5:
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

# Network Menu
def network_submenu():
    print('----------- Network Menu ----------- \n' +
            '0. Main Menu \n' +
            '1. Vollständige Netzwerk Konfiguration \n' +
            '2. Härtung Überprüfen \n' +
            '----- Please enter a number (0-2) -----')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,3)
    
    match case_number:
        case 0:
            main_menu()
        case 1:
            net.complete_configuration_dialog()
            network_submenu()
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
            '0. \t Main Menu\n' +
            '1. \t DEBUG\n' +
            '2. \t Netplan config\n' +
            '3. \t Syslog config\n' +
            '4. \t SNMP config\n' +
            '5. \t Debug UFW Delete Rules and Default Setup\n' +
            '6. \t Debug UFW Generator\n' + 
            '7. \t Debug UFW add APT repos\n' +
            '8. \t Debug UFW add NTP server\n' +
            '9. \t UFW -> Disable\n' +
            '10. \t UFW -> Reset\n' +
            '11. \t UFW -> Enable\n' +
            '12. \t UFW -> Logging OFF\n' +
            '13. \t UFW -> Logging Low\n' +
            '14. \t UFW -> Delete all Rules\n' +
            '15. \t Config NTP Server\n' +
            '16. \t UFW -> Allow outgoing Ping # WIP #\n' +
            '17. \t UFW -> Disable IPv6\n' +
            '18. \t Install Needed Network Packages\n' + 
            '19. \t Docker Installation\n' + 
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
            net.config_netplan()
            debug_submenu()
        case 3:
            net.config_syslog()
            debug_submenu()
        case 4:
            net.config_snmp()
            debug_submenu()
        case 5:
            fw.ufw_delete_rules()
            fw.ufw_set_default_settings()
            debug_submenu()
        case 6:
            fw.ufw_rule_generator(port=22, target_ip='192.168.231.1')
            fw.ufw_rule_generator (port=53, target_ip='8.8.8.8', protocol='')
            fw.ufw_rule_generator (port=443, target_ip='', protocol='')
            debug_submenu()
        case 7:
            fw.ufw_rules_add_lists(80, fw.get_repo_list(),'tcp')
            debug_submenu()
        case 8:
            fw.ufw_rules_add_lists(123, fw.get_ntp_list())
            debug_submenu()
        case 9:
            os.system('sudo ufw --force disable')
            debug_submenu()
        case 10:
            os.system('sudo ufw --force reset')
            debug_submenu()
        case 11:
            os.system('sudo ufw --force enable')
            debug_submenu()
        case 12:
            os.system('sudo ufw logging off')
            debug_submenu()
        case 13:
            os.system('sudo ufw logging low')
            debug_submenu()
        case 14:
            fw.ufw_delete_rules()
            debug_submenu()
        case 15:
            net.config_ntp()
            debug_submenu()
        case 16:
            fw.ufw_allow_ping()
            debug_submenu()
        case 17:
            fw.ufw_disable_ipv6()
            debug_submenu()
        case 18:
            net.install_networking_packages()
            if hf.restart_system is False:
                debug_submenu()
        case 19:
            doc.install_docker()
        case _:
            debug_submenu()
