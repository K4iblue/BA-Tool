from . import hardening as hard
from . import network as net
from . import firewall as fw
from . import docker as doc
from . import maintenance as main
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
          '-- Please enter a number (0-4) --')

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
    print('----------- Härtung ----------- \n' +
          '0.\t Main Menu \n' +
          '1.\t Härtung durchführen \n' +
          '2.\t Härtung Überprüfen \n' +
          '-- Please enter a number (0-2) --')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,3)
    
    match case_number:
        case 0:
            main_menu()
        case 1:
            hard.complete_hardening()
            hardening_submenu()
        case 2:
            hard.test_hardening()
            hardening_submenu()


# Network Menu
def network_submenu():
    print('----------- Netzwerk Konfiguration ----------- \n' +
          '0.\t Main Menu \n' +
          '1.\t Vollständige Netzwerk Konfiguration \n' +
          '2.\t Netplan Konfiguration (DNS, Default Gateway, Static IP) \n' +
          '3.\t NTP Konfiguration \n' +
          '4.\t SNMPv3 Konfiguration \n' +
          '5.\t Syslog Konfiguration \n' +
          '-- Please enter a number (0-7) --')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,8)
    
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
            net.config_snmp()
            network_submenu()
        case 5:
            net.config_syslog()
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
          '6.\t Container erstellen \n' +
          '7.\t Image erstellen \n' +
          '8.\t Container löschen \n' +
          '9.\t Image löschen \n' +
          '10.\t Volume löschen \n' +
          '11. \t Container von Compose File starten' +
          '12. \t Container von Compose File stoppen'
          '-- Please enter a number (0-12) --')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,13)
    
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
            doc.create_container()
            container_submenu()
        case 7:
            doc.create_image()
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
        case 11:
            doc.start_container_from_compose_file()
            container_submenu()


# Maintenance Menu
def maintenance_submenu():
    print('----------- Systempflege Menu ----------- \n' +
          '0. Main Menu \n' +
          '1. Automatische Updates de-/aktivieren \n' +
          '2. Standardprogramme installieren \n' +
          '3. Update Tool \n' +
          '-- Please enter a number (0-3) --')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,4)

    match case_number:
        case 0:
            main_menu()
        case 1:
            main.toggle_automatic_updates()
            maintenance_submenu()
        case 2:
            main.install_default_programs()
            maintenance_submenu()
        case 3:
            main.update_script()
            quit()


# Debug Menu
def debug_submenu():
    print('----------- Debug Menu ----------- \n' +
          '0. \t Main Menu\n' +
          '1. \t DEBUG\n' +
          '2. \t add ssh\n' +
          '3. \t add Repos to Firewall\n' +
          '4. \t UFW Debug Rule adding\n' +
          '5. \t UFW get all rules\n' +
          '6. \t UFW all docker\n' +
          '-- Please enter a number (0-99) --')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,99)
    match case_number:
        case 0:
            main_menu()
        case 1:
            de.debug()
            debug_submenu()
        case 2:
            fw.ufw_rule_generator(port=22, target_ip='192.168.231.1')
            debug_submenu()
        case 3:
            fw.ufw_rules_add_lists(port=80, ip_list=fw.get_repo_list(), protocol='tcp')
            debug_submenu()
        case 4:
            fw.ufw_rule_generator(port=22, target_ip='192.168.231.1')
            fw.ufw_rule_generator (port=53, target_ip='8.8.8.8', protocol='')
            fw.ufw_rule_generator (port=443, target_ip='', protocol='')
        case 5:
            doc.remove_container_firewall_rule(container_name='test')
        case 6:
            fw.ufw_allow_docker()
        case _:
            debug_submenu()
