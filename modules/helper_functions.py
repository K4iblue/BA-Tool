import ipaddress

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
