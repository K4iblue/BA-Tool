from modules import menus
from modules import maintenance

def main(): 
    if maintenance.first_start()is True:
        print('Erster Programm Start. Es werden nun alle benötigten Packages installiert')
        maintenance.install_all_needed_packages()
    else:
        menus.main_menu()

if __name__ == '__main__':
    main()
