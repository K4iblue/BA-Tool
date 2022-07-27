from gettext import install
import subprocess
import os
import sys
from . import helper_functions as hf

def complete_hardening():
    print('Soll die Systemhärtung gestartet werden?')
    complete_config_needed = ''
    # Only 'y' and 'n' allowed
    while complete_config_needed not in ['Y','N']:
        complete_config_needed = input('(y/n): ').upper()
    
    complete_config_needed = True if complete_config_needed == 'Y' else False

    if complete_config_needed is True:
        install_hardening_packages()
        create_configfile()
        start_hardening_script()
    else:
        return

# Install necessary packages for the hardening script
def install_hardening_packages():
    subprocess.run(['sudo', 'apt-get', '-y', 'install', 'git', 'net-tools', 'procps', '--no-install-recommend'], shell=True, check=True)


# Start hardening script
def start_hardening_script():
    # Run Hardening Script
    subprocess.run(['sudo', 'bash', 'scripts/hardening/ubuntu.sh'], shell=True, check=True)


# Create configfile for hardening script
def create_configfile():
    # 1. The IP addresses that will be able to connect with SSH, separated by spaces // Default: '127.0.0.1'
    print('Welche IP Adressen sollen SSH Zugang bekommen? Mehrere IP Addressen durch ein Komma trennen!')
    ssh_ips_list = hf.get_ips()
    # List to string, with spaces in between
    ssh_ips = ' '.join(ssh_ips_list)

    # 2. Which group the users have to be member of in order to acess via SSH, separated by spaces // Default: 'sudo'
    print('Welche User Gruppen sollen Zugang via SSH bekommen? Mehrere Gruppen durch ein Komma trennen!')
    user_groups_list = input('Gruppe(n): ')
    # No empty input allowed
    while not user_groups_list:
        user_groups_list = input('Gruppe(n): ')
    # Create list from string
    user_groups_list = user_groups_list.split(',')
    # List to string, with spaces in between
    user_groups = ' '.join(user_groups_list)

    # 3. Configure SSH port // Default: 22
    print('Welcher Port soll für SSH benutzt werden?')
    ssh_port = input('SSH Port: ')
    # No empty input allowed
    while not ssh_port:
        ssh_port = input('SSH Port: ')

    # 4. Stricter sysctl settings // Default: './misc/sysctl.conf'
    strict_sysctl = './misc/sysctl.conf'

    # 5. Auditd failure mode 0=silent 1=printk 2=panic // Default: '1'
    auditd_mode = '1'

    # 6. Auditd rules // Default: './misc/audit-base.rules ./misc/audit-aggressive.rules ./misc/audit-docker.rules'
    auditd_rules = './misc/audit-base.rules ./misc/audit-aggressive.rules ./misc/audit-docker.rules'

    # 7. Logrotate settings // Default: './misc/logrotate.conf'
    logrotate_settings = './misc/logrotate.conf'

    # 8. NTP server pool // Default: '0.ubuntu.pool.ntp.org 1.ubuntu.pool.ntp.org 2.ubuntu.pool.ntp.org 3.ubuntu.pool.ntp.org pool.ntp.org'
    print('Sind NTP Server vorhanden? Mehrere IP Addressen durch ein Komma trennen!')
    ntp_ips_list = hf.get_ips()
    # List to string, with spaces in between
    ntp_ips = ' '.join(ntp_ips_list)

    # 9. Add a specific time zone or use the system default by leaving it empty // Default: ''
    timezone = ''

    # 10. If you want all the details or not // Default: 'N'
    verbose= 'Y'

    # 11. Let the script guess the FW_ADMIN and SSH_GRPS settings // Default: 'N'
    script_guessing = 'N'

    # 12. Add a valid email address, so PSAD can send notifications // Default: 'root@localhost'
    psad_email = 'root@localhost'

    # 13. If 'Y' then the snapd package will be held to prevent removal // Default: 'Y'
    print('Wird snapd benötigt?')
    snapd_removal = ''
    # Only 'y' and 'n' allowed
    while snapd_removal not in ['Y','N']:
        snapd_removal = input('(y/n): ').upper()

    # 14. Add something just to verify that you actually glanced the code // Default: ''
    change_me = 'OK'

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
    config_list += [change_me]

    path = os.path.join(sys.path[0]) + '/scripts/hardening/ubuntu.cfg'
    # Read from file
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


def test_hardening():
    # Install Bats
    os.system('sudo apt-get -y install bats')

    print('Soll die Härtung des Systems überprüft werden?')
    testing_needed = ''
    lynis_needed = ''
    # Only 'y' and 'n' allowed
    while testing_needed not in ['Y','N']:
        testing_needed = input('(y/n): ').upper()
    
    testing_needed = True if testing_needed == 'Y' else False

    if testing_needed is True:
        # Bats tests
        os.system('sudo bats ./scripts/hardening/tests/')
        print('Bats Test durchgeführt')
        print('Fortfahren?')
        
        while lynis_needed not in ['Y','N']:
            lynis_needed = input('(y/n): ').upper()
        lynis_needed = True if lynis_needed == 'Y' else False

        if lynis_needed is True:
            # Lynis testing
            os.chmod('./scripts/lynis/', 0o775)
            os.system('./scripts/lynis/lynis audit system')
    else:
        return
