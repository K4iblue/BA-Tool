import os
import sys
from . import helper_functions as hf


# Complete hardening dialog
def complete_hardening():
    print('Soll die Systemhärtung gestartet werden?')
    complete_config_needed = ''
    # Only 'y' and 'n' allowed
    while complete_config_needed not in ['Y','N']:
        complete_config_needed = input('(y/n): ').upper()
    
    complete_config_needed = True if complete_config_needed == 'Y' else False

    if complete_config_needed is True:
        create_configfile()
        start_hardening_script()
        test_hardening()
    else:
        return


# Create configfile for hardening script
def create_configfile():
    print('Welche IP Adresse(n) sollen SSH Zugang bekommen?')
    ssh_ips_list = hf.get_ips()
    ssh_ips = ' '.join(ssh_ips_list)

    print('Welche User Gruppen sollen Zugang via SSH bekommen?')
    user_groups_list = input('Gruppe(n): ')
    while not user_groups_list:
        user_groups_list = input('Gruppe(n): ')
    # Create list from string -> List to string, with spaces in between
    user_groups_list = user_groups_list.split(',')
    user_groups = ' '.join(user_groups_list)

    print('Welcher Port soll fuer SSH benutzt werden?')
    ssh_port = input('SSH Port: ')
    while not ssh_port:
        ssh_port = input('SSH Port: ')

    print('Wird snapd benoetigt?')
    snapd_removal = ''
    while snapd_removal not in ['Y','N']:
        snapd_removal = input('(y/n): ').upper()

	# Static Config
    strict_sysctl = './misc/sysctl.conf'
    auditd_mode = '1'
    auditd_rules = './misc/audit-base.rules ./misc/audit-aggressive.rules ./misc/audit-docker.rules'
    logrotate_settings = './misc/logrotate.conf'
    ntp_ips = ''
    timezone = 'Europe/Berlin'
    verbose= 'Y'
    script_guessing = 'N'
    psad_email = 'root@localhost'

    # Create a empty list and fill it with the config values
    config_list = []
    config_list += [ssh_ips]
    config_list += [user_groups]
    config_list += [ssh_port]
    config_list += [strict_sysctl]
    config_list += [auditd_mode]
    config_list += [auditd_rules]
    config_list += [logrotate_settings]
    config_list += [ntp_ips]
    config_list += [timezone]
    config_list += [verbose]
    config_list += [script_guessing]
    config_list += [psad_email]
    config_list += [snapd_removal]

	# Read from file
    path = os.path.join(sys.path[0]) + '/scripts/hardening/ubuntu.cfg'
    with open (path, 'r', encoding='UTF-8') as file:
        filedata = file.read()

    # Replace variable with config value from config_list
    count = 1
    for n in config_list:
        to_replace = '$'+str(count)+'$'
        filedata = filedata.replace(to_replace, n)
        count = count + 1

    # Write back to file
    with open (path, 'w', encoding='UTF-8') as file:
        file.write(filedata)

# Start hardening script
def start_hardening_script():
    # Change folder, otherwise its not working?
    current_dir = os.getcwd()
    os.chdir(str(current_dir) + '/scripts/hardening/')
    # Run hardening script
    os.system('sudo bash ubuntu.sh')
    # Go back to tool folder
    os.chdir(current_dir)


# Start bats and lynis tests
def test_hardening():
    print('Soll die Härtung des Systems überprüft werden?')
    testing_needed = ''
    # Only 'y' and 'n' allowed
    while testing_needed not in ['Y','N']:
        testing_needed = input('(y/n): ').upper()
    
    testing_needed = True if testing_needed == 'Y' else False

    if testing_needed is True:
        # Get path to current and test folder
        current_dir = os.path.join(sys.path[0])
        test_dir = os.path.join(sys.path[0]) + '/scripts/hardening/tests/'
        # Change to test folder, otherwise its not working?
        os.chdir(test_dir)
        # Run bats tests
        os.system('sudo bats .')
        # Go back to tool folder
        os.chdir(current_dir)
        print('Bats Test durchgeführt \nFortfahren?')
        
        lynis_needed = ''
        while lynis_needed not in ['Y','N']:
            lynis_needed = input('(y/n): ').upper()
        lynis_needed = True if lynis_needed == 'Y' else False

        if lynis_needed is True:
            # Lynis testing
            os.system('lynis audit system')
    else:
        return
 