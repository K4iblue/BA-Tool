import subprocess
import os
import sys
import ipaddress


def main():
    print('-------------- Menu --------------')
    print('0. Exit program \n' +
          '1. Härtung durchführen \n' +
          '2. Automatische Updates \n' +
          '3. Standardprogramme installieren \n' +
          '4. Docker: Image erstellen\n' +
          '5. Docker: Image starten \n')
    print('--- Please enter a number (0-5) ---')

    case_number = int(input())
    print('\n')

    match case_number:
        case 0:
            quit()
        case 1:
            create_configfile()
            #start_hardening()
            #print('Case 1')
            main()
        case 2:
            #image_name = input('welches Image soll gestartet werden: ').lower()
            #start_docker_container(image_name)
            print('Case 2')
            main()
        case 3:
            #start_docker_container(create_docker_image())
            print('Case 3')
            main()
        case 4:
            print('Case 4')
        case 5:
            print('Case 5')
        case _:
            print('Please enter a valid number (0-5) !')
            main()


def create_configfile():
    # 1. The IP addresses that will be able to connect with SSH, separated by spaces // Default: '127.0.0.1'
    print('Welche IP Adressen sollen SSH Zugang bekommen? Mehrere IP Addressen durch ein Komma trennen!')
    print('Default: 127.0.0.1')
    ssh_ips_list = get_ips()
    # List to string, with spaces in between
    ssh_ips = ' '.join(ssh_ips_list)

    # 2. Which group the users have to be member of in order to acess via SSH, separated by spaces // Default: 'sudo'
    print('Welche User Gruppen sollen Zugang via SSH bekommen? Mehrere Gruppen durch ein Komma trennen!')
    print('Default: sudo')
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
    print('Default: 22')
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
    print('Default: 0.ubuntu.pool.ntp.org, 1.ubuntu.pool.ntp.org, 2.ubuntu.pool.ntp.org, 3.ubuntu.pool.ntp.org, pool.ntp.org')
    ntp_ips_list = get_ips()
    # List to string, with spaces in between
    ntp_ips = ' '.join(ntp_ips_list)

    # 9. Add a specific time zone or use the system default by leaving it empty // Default: ''
    timezone = ''

    # 10. If you want all the details or not // Default: 'N'
    verbose= 'N'

    # 11. Let the script guess the FW_ADMIN and SSH_GRPS settings // Default: 'N'
    script_guessing = 'N'

    # 12. Add a valid email address, so PSAD can send notifications // Default: 'root@localhost'
    psad_email = 'root@localhost'

    # 13. If 'Y' then the snapd package will be held to prevent removal // Default: 'Y'
    print('Wird snapd benötigt?')
    snapd_removal = input('(y/n): ').upper()
    # Only 'y' and 'n' allowed
    while not snapd_removal == 'y' or 'n':
        snapd_removal = input('(y/n): ').upper()

    # 14. Add something just to verify that you actually glanced the code // Default: ''
    change_me = 'OK'

    # Create empty a empty list and fill it with the config values
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

    path = os.path.join(sys.path[0]) + '\\scripts\\hardening\\ubuntu.cfg'
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


def start_hardening():
    # Install necessary packages
    subprocess.run(['sudo', 'apt-get', '-y', 'install', 'git', 'net-tools', 'procps', '--no-install-recommend'], shell=True, check=True)

    # Run Hardening Script
    subprocess.run(['sudo', 'bash', 'scripts/hardening/ubuntu.sh'], shell=True, check=True)


def create_docker_image():
    # Get path of script and dockerfile
    path = os.path.join(sys.path[0])

    # User input for docker image name
    print('--- Enter Docker Image Name ---')
    image_name = input('Image Name: ').lower()

    # Get ImageID from console and convert to string
    # ImageId = subprocess.check_output(['docker', 'images', '-q', ImageName])
    # ImageIdString = str(ImageId).replace(''','').replace('\\n','')

    # Create image from Dockerfile
    subprocess.run(['docker', 'build', path, '-t', image_name.replace('"', '')], shell=True, check=True)

    # return image name for later use
    return image_name


def start_docker_container(image_name):
    # Start Container from image
    subprocess.run(['docker', 'run', image_name], shell=True, check=True)


# Function to validate IP addresses
def ip_validation(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


# Function to get a list of IP addresses from the user
def get_ips():
    ip_valid = 0
    while ip_valid == 0:
        ips = input('IP-Adresse(n): ')
        # Remove spaces
        ips = ips.strip().replace(' ', '')
         # Create list from string
        ips = ips.split(',')
        # Validate IPs, if all IPs are correct break out of while loop
        ip_valid = 1
        for n in ips:
            if ip_validation(n) is False:
                print(n + ' is not a valid IP Adress. Please enter a valid IP Adress!')
                ip_valid = 0
    return ips


if __name__ == '__main__':
    main()
