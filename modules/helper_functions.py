import ipaddress

# Validate IP addresses
def ip_validation(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


# Get a list of IP addresses from the user
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
                print(n + ' ist keine gültige IP-Adresse. Bitte eine gültigt IP-Adresse eingeben!')
                ip_valid = 0
    return ips


# Get a number from the user in a given range
def get_int(x,y):
    while True:
        try:
            number = int(input())
            while number not in range(x,y):
                try:
                    print('Please enter a valid number!')
                    number = int(input())
                except ValueError:
                    print('Please enter a valid number!')
        except ValueError:
            print('Please enter a valid number!')
            continue
        break
    return number
