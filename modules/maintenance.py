import os
import re

from modules.crontab.crontab import CronTab
#from ./crontab import CronTab
from . import docker as doc


# Start Automatic updates
def start_updates():
    # Load crontab of root user
    cron = CronTab(user='root')

    # Check if automtatic updates are activated at the moment
    find_job = cron.find_comment('automatic_updates')

    # Get list of cronjobs
    for job in find_job:
        if job.is_enabled() is True:
            job.enable(False)
            print('Automatische Updates deaktiviert')
            return
        elif job.is_enabled() is False:
            job.enable()
            print('Automatische Updates aktiviert')
            return

    # If no cronjob was found, we create one
    print('Zur welcher Uhrzeit sollen die Täglichen Updates durchgeführt werden?')
    print('Bitte eine Uhrzeit zwischen 00:00Uhr - 23:59Uhr auswählen')
    intervall = str(input('Uhrzeit (HH:MM): '))

    # String to list
    intervall = intervall.split(':')

    # Create new chronjob 
    job = cron.new(command='sudo apt update && sudo apt upgrade -y', comment='automatic_updates')
    job.hour(int(intervall[0]))
    job.minute(int(intervall[1]))

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
        os.system('sudo apt-get install locate vim screen dnsutils iptables fail2ban openssh-server rsyslog snmpd snmp acpi cron -y')

        # Install Docker
        doc.install_docker()

        # Clean up after everything is installed
        os.system('sudo apt-get clean && sudo apt-get autoremove')

    else:
        print('Default Programme müssen zuerst installiert werden!')
        quit()
