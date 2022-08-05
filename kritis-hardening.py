from modules import menus
from modules import maintenance

def main():

    if maintenance.first_start_check() is True:
        maintenance.first_start_installer()
    
    menus.main_menu()

if __name__ == '__main__':
    main()
