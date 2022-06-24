from . import hardening
#from . import docker
#from . import maintenance
from . import helper_functions as hf

# Main and submenus

# Main Menu
def main_menu():
    print('----------- Main Menu ----------- \n' +
          '0. Exit Programm \n' +
          '1. Härtung \n' +
          '2. Docker \n' +
          '3. Systempflege \n' +
          '----- Please enter a number (0-3) -----')

    # Get a Number from the user in given range
    case_number = hf.get_int(0,4)

    match case_number:
        case 0:
            quit()
        case 1:
            hardening_submenu()
        case 2:
            docker_submenu()
        case 3:
            maintenance_submenu()

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
