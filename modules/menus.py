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
    print('----------- Hauptmenü ----------- \n' +
          '0.\t Exit Programm \n' +
          '1.\t Härtung \n' +
          '2.\t Netzwerkkonfiguration \n' +
          '3.\t Container Verwaltung \n' +
          '4.\t Systempflege \n' +
          '5.\t DEBUG \n' +
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
            '2.\t Netplan Konfiguration (DHCP, DNS, Default Gateway, Static IP) \n' +
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
            '3.\t Container starten \n' +
            '4.\t Container stoppen \n' +
            '5.\t Container löschen \n' +
            '6.\t Container erstellen \n' +
            '7.\t Image löschen \n' +
            '----- Please enter a number (0-7) -----')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,8)
    
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
            doc.start_container()
            container_submenu()
        case 4:
            doc.stop_container()
            container_submenu()
        case 5:
            doc.delete_container()
            container_submenu()
        case 6:
            doc.create_container()
            container_submenu()
        case 7:
            print('Case 7')
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
