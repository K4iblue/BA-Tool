import os
import re

from modules.crontab.crontab import CronTab
#from ./crontab import CronTab
from . import docker as doc


# Start Automatic updates
def start_updates():
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

    while intervall[0] > 23 or intervall[1] > 59:
        print('Bitte eine gültige Uhrzeit eingeben!')
        intervall = str(input('Uhrzeit (HH:MM): '))
        intervall = intervall.split(':')

    # variables for hours and minute
    job_hours = int(intervall[0])
    job_minutes = int(intervall[1])

    print(job_hours)
    print(job_minutes)

    # Create new chronjob 
    job = cron.new(command='sudo apt update && sudo apt upgrade -y', comment='automatic_updates')
    job.hour.every(job_hours)
    job.minute.also.on(job_minutes)
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
        os.system('sudo apt-get install locate vim screen dnsutils iptables fail2ban openssh-server rsyslog snmpd snmp acpi cron -y')

        # Install Docker
        doc.install_docker()

        # Clean up after everything is installed
        os.system('sudo apt-get clean && sudo apt-get autoremove')

    else:
        print('Default Programme müssen zuerst installiert werden!')
        quit()
