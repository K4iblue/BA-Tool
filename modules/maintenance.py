import os
from . import docker as doc


# Start Automatic updates
def start_updates():
    print('')


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
        os.system('sudo apt-get install locate vim screen dnsutils iptables fail2ban openssh-server rsyslog snmpd snmp acpi cron -y')

        # Install Docker
        doc.install_docker()

        # Clean up after everything is installed
        os.system('sudo apt-get clean && sudo apt-get autoremove')

    else:
        print('Default Programme müssen zuerst installiert werden!')
        quit()
