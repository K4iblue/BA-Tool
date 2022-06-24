#from . import hardening
#from . import docker
#from . import maintenance
from . import helper_functions as hf

# Main and submenus

# Main Menu
def main_menu():
    print('----------- Main Menu ----------- \n' +
          '0. Exit program \n' +
          '1. Härtung durchführen \n' +
          '2. Härtung Überprüfen \n' +
          '3. Automatische Updates \n' +
          '4. Standardprogramme installieren \n' +
          '5. Docker: Image erstellen\n' +
          '6. Docker: Image starten \n' +
          '----- Please enter a number (0-6) -----')

    # Get Number from user in given range
    case_number = hf.get_int(0,7)

    match case_number:
        case 0:
            quit()
        case 1:
            # create_configfile()
            #start_hardening_script()
            #print('Case 1')
            main_menu()
        case 2:
            print('Case 2')
            main_menu()
        case 3:
            print('Case 3')
            main_menu()
        case 4:
            print('Case 4')
            main_menu()
        case 5:
            print('Case 5')
            main_menu()
        case 6:
            print('Case 6')
            main_menu()
        case _:
            main_menu()

# Hardening Menu
def hardening_submenu():
    print('----------- Hardening Menu ----------- \n' +
            '0. Main Menu \n' +
            '1. Härtung durchführen \n' +
            '2. Härtung Überprüfen \n' +
            '----- Please enter a number (0-2) -----')

    # Get Number from user in given range
    case_number = hf.get_int(0,3)
    
    match case_number:
        case 1:
            print('Case 1')
        case 2:
            print('Case 3')
        case _:
            print('Default Case')
            main_menu()

# Docker Menu
def docker_submenu():
    print('----------- Docker Menu ----------- \n' +
            '0. Main Menu \n' +
            '1. Härtung durchführen \n' +
            '2. Härtung Überprüfen \n' +
            '----- Please enter a number (0-2) -----')

    # Get Number from user in given range
    case_number = hf.get_int(0,3)
    
    match case_number:
        case 1:
            print('Case 1')
        case 2:
            print('Case 3')
        case _:
            print('Default Case')
            main_menu()

# Maintenance Menu
def maintenance_submenu():
    print('----------- Maintenance Menu -----------' +
            '0. Main Menu \n' +
            '1. Härtung durchführen \n' +
            '2. Härtung Überprüfen \n' +
            '----- Please enter a number (0-2) -----')

    # Get Number from user in given range
    case_number = hf.get_int(0,3)

    match case_number:
        case 1:
            print('Case 1')
        case 2:
            print('Case 3')
        case _:
            print('Default Case')
            main_menu()
