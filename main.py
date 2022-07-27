import os
import sys
from modules import menus
from modules import maintenance

def main():
    # Read from config file
    config_file = os.path.join(sys.path[0]) + '/config/tool_config.cfg'
    with open (config_file, 'r', encoding='UTF-8') as file:
        filedata = file.read()

    if 'first_start=yes' in filedata:
        print('Erster Programm Start. Es werden nun alle benötigten Packages installiert \n Fortfahren?')
        print('Fortfahren?')

        start_download = ''
        while start_download not in ['Y','N']:
            start_download = input('(y/n): ').upper()
        start_download = True if start_download == 'Y' else False
        
        if start_download is True:
            maintenance.install_all_needed_packages()
            # Replace first start line
            filedata = filedata.replace('first_start=yes', 'first_start=no')
            # Write to file
            with open (config_file, 'w+', encoding='UTF-8') as file:
                file.write(filedata)
        else:
            quit()
        
    else:
        menus.main_menu()

if __name__ == '__main__':
    main()
