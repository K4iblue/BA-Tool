import os
import sys
from modules.crontab.crontab import CronTab
from . import firewall as fw


# Start Automatic updates
def toggle_automatic_updates():
    # Load crontab of root user
    cron = CronTab(user='root')

    # Check if automatic updates are activated at the moment
    find_job = cron.find_comment('automatic_updates')

    # Get list of cronjobs, with the comment 'automatic_updates'
    for job in find_job:
        if job.is_enabled() is True:
            for job in cron:
                cron.remove(job)
            print('Automatische Updates deaktiviert')
            # Write to crontab
            cron.write()
            return

    # If no cronjob was found, we create one
    print('Zur welcher Uhrzeit sollen die Täglichen Updates durchgeführt werden?')
    print('Bitte eine Uhrzeit zwischen 00:00Uhr - 23:59Uhr auswählen')
    intervall = str(input('Uhrzeit (HH:MM): '))
    intervall = [int(n) for n in intervall.split(':')]

    while intervall[0] not in range (0,24) or intervall[1] not in range (0,60) or len(intervall) != 2:
        print('Bitte eine gültige Uhrzeit eingeben!')
        intervall = str(input('Uhrzeit (HH:MM): '))
        intervall = [int(n) for n in intervall.split(':')]

    # Create new chronjob
    job = cron.new(command='sudo apt update && sudo apt upgrade -y', comment='automatic_updates')
    # intervall[0] = hours, intervall[1] = minutes
    job.setall(intervall[1], intervall[0])
    print('Automatische Updates aktiviert')

    # Write to crontab
    cron.write()


# Install default programs definied by K-Businesscom
def install_default_programs():
    print('Default Programme installieren?')
    start_installation = ''
    # Only 'y' and 'n' allowed
    while start_installation not in ['Y','N']:
        start_installation = input('(y/n): ').upper()
    start_installation = True if start_installation == 'Y' else False

    if start_installation is True:
        # Update Repos and upgrade all packages
        os.system('sudo apt-get update && sudo apt-get upgrade -y')

        # Install default programs
        os.system('sudo apt-get install locate vim screen fail2ban acpi -y')

        # Clean up after everything is installed
        os.system('sudo apt-get clean && sudo apt-get autoremove')


# Install all needed packages
def install_all_needed_packages():
    print('Install all needed packages...')

    os.system('sudo apt-get update')
    os.system('sudo apt-get install ca-certificates curl gnupg lsb-release')

    # Installation according to https://docs.docker.com/engine/install/ubuntu/
    # Add Docker’s official GPG key:
    os.system('sudo mkdir -p /etc/apt/keyrings')
    os.system('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg')

    # Use the following command to set up the repository:
    os.system('echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')

    # Install lynis
    os.system('sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 013baa07180c50a7101097ef9de922f1c2fde6c4')

    os.system('echo "deb https://packages.cisofy.com/community/lynis/deb/ stable main" | sudo tee /etc/apt/sources.list.d/cisofy-lynis.list')

    # Update repos
    os.system('sudo apt-get update')

    # Install all programs
    os.system('sudo DEBIAN_FRONTEND=noninteractive apt-get install net-tools procps openssh-server iptables iputils-ping dnsutils openssh-server rsyslog snmpd snmp cron bats lynis docker-ce -y')
    
    # Update all other packages if needed
    os.system('sudo apt-get upgrade -y')

    # Start docker deamon
    os.system('sudo systemctl start docker')

    # Restart all services, not sure if working
    os.system('sudo needrestart -r a')

    # Clear console
    os.system('clear')


# Check for first program start
def first_start_check():
    # Read from config file
    config_file = os.path.join(sys.path[0]) + '/config/tool_config.cfg'
    with open (config_file, 'r', encoding='UTF-8') as file:
        filedata = file.read()

    if 'first_start=yes' in filedata:
        return True
    else:
        return False


# Install packages on first start
def first_start_installer():
    print('Erster Programm Start. Es werden nun alle benötigten Packages installiert \nFortfahren?')

    start_download = ''
    while start_download not in ['Y','N']:
        start_download = input('(y/n): ').upper()
    start_download = True if start_download == 'Y' else False
    
    if start_download is True:
        # Install Packages and clear terminal afterwards
        install_all_needed_packages()
        #os.system('clear')

        # Edit config file
        config_file = os.path.join(sys.path[0]) + '/config/tool_config.cfg'
        with open (config_file, 'r', encoding='UTF-8') as file:
            filedata = file.read()

        filedata = filedata.replace('first_start=yes', 'first_start=no')
        with open (config_file, 'w+', encoding='UTF-8') as file:
            file.write(filedata)
    else:
        quit()


# Update the script
def update_script():
    print('Updating the tool via git...')
    fw.ufw_allow_outgoing()
    os.system('git config --global --add safe.directory "*"')
    os.system('sudo git pull')
    fw.ufw_deny_outgoing()
    print('Quitting Tool...')
