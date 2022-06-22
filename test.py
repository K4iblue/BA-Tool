import ipaddress

def main():
    print('SSH Ips?')
    ssh_ips = get_ips()
    print('NTP Ips?')
    ntp_ips = get_ips()

    print('DEBUG:  ' + str(ssh_ips))
    print('DEBUG:  ' + str(ntp_ips))

# Function to validate IP addresses
def ip_validation(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False

def get_ips():
    ip_valid = 0
    while ip_valid == 0:
        ips = input('IP-Adresse(n): ')
        # Remove spaces
        ips = ips.strip().replace(' ', '')
         # Create list from string
        ips = ips.split(',')
        # Validate ips, if all ip are correct break out of while loop
        ip_valid = 1
        for n in ips:
            if ip_validation(n) is False:
                print(n + ' is not a valid IP Adress. Please enter a valid IP Adress!\n')
                ip_valid = 0
    return ips

if __name__ == '__main__':
    main()
