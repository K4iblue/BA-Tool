import os
import sys
import json
import uuid
from .pyufw import pyufw

# Create Image
def create_image():
    # Get dockerfile path from user
    print('Wie lautet der Pfad der Dockerfile?')
    path = input('Pfad: ')

    # Check if path exists
    if os.path.isdir(path):
        print('Wie soll das Image genannt werden?')
        image_name = input('Image Name: ').replace(' ','')
        print('sudo docker build -t ' + str(image_name) + ' ' + str(path) )
        os.system('sudo docker build -t ' + str(image_name) + ' ' + str(path))


# Create Container, Host Port variante
def create_container():
    # Get image name
    print('Aus welchen Image soll der Container erstellt werden?')
    image_name = str(input('Name oder ID: '))

    # Get name for container
    print('Wie soll der Container genannt werden?')
    container_name = str(input('Container Name: '))

    # Docker volume needed?
    print('Wird ein Docker Volume zum persistenten speichern benötigt?')
    volume_needed = ''
    # Only 'y' and 'n' allowed
    while volume_needed not in ['Y','N']:
        volume_needed = input('(y/n): ').upper()
    volume_needed = True if volume_needed == 'Y' else False

    if volume_needed is True:
        print('Wie soll das Volumen genannt werden?')
        volume_name = str(input('Volume Name: '))
        print('Bitte den Mounting Pfad im Container angeben')
        print('z.b: /var/lib/mysql/data')
        volume_mounting = str(input('Mounting point: '))
        volume_string = ' -v ' + volume_name + ':' + volume_mounting

    # Get Ports that are needed for the container
    print('Welche Ports werden für den Container benötigt?')
    print('Syntax: Extern:Intern ')
    print('Bsp.: 8080:80 (Map 80 in the container to port 8080 on the Docker host)')

    # Force to two ports
    port_list = []
    while len(port_list) != 2:
        ports = str(input('Ports: '))
        # Remove Spaces
        ports = ports.replace(' ', '')
        # Create list from string
        port_list = ports.split(':')

    # Create port string
    port_string = (' -p ' + str(port_list[0])+ ':' + str(port_list[1]))

    # Create docker run command
    run_command = 'docker run -d'
    if volume_needed is True: 
        run_command += volume_string
    run_command += port_string
    run_command += ' --name ' + container_name + ' '
    run_command += image_name

    # Run the docker command
    os.system('sudo ' + str(run_command))

    # Add firewall rule for container and add port-mapping to json file
    add_container_port_mapping(port=str(port_list[0]),container_name=str(container_name))
    add_container_firewall_rule(port=str(port_list[0]),container_name=str(container_name))


# Start given container
def start_container(container_name=''):
    if container_name == '':
        print('Welcher Container soll gestartet werden?')
        container_name = input('Container Name oder ID: ')
        os.system('sudo docker start ' + str(container_name))
        
        # Add firewall rule for container
        add_container_firewall_rule(port=str(get_container_port(container_name)),container_name=container_name)
        
        # Print 2 empty Lines for better reading
        print('\n\n')
    else:
        os.system('sudo docker start ' + str(container_name))

        # Add firewall rule for container
        add_container_firewall_rule(port=str(get_container_port(container_name)),container_name=container_name)

        # Print 2 empty Lines for better reading
        print('\n\n')


# Stop given container
def stop_container(container_name=''):
    if container_name == '':
        print('Welcher Container soll gestoppt werden?')
        container_name = input('Container Name oder ID: ')
        os.system('sudo docker stop ' + str(container_name))
        
        # Remove firewall rule for container
        remove_container_firewall_rule(container_name=container_name)
        
        # Print 2 empty Lines for better reading
        print('\n\n')
    else:
        os.system('sudo docker stop ' + str(container_name))
        
        # Remove firewall rule for container
        remove_container_firewall_rule(container_name=container_name)

        # Print 2 empty Lines for better reading
        print('\n\n')


# List all containers
def show_container_list():
    os.system('sudo docker container ls --all')
    # Print 2 empty Lines for better reading
    print('\n\n')


# List all images
def show_images_list():
    os.system('sudo docker image ls --all')
    # Print 2 empty Lines for better reading
    print('\n\n')


# List all volumes
def show_volumes_list():
    os.system('sudo docker volume ls')
    # Print 2 empty Lines for better reading
    print('\n\n')


# Delete given container
def delete_container(container_name=''):
    if container_name == '':
        print('Welcher Container soll entfernt werden?')
        container_name = input('Container Name oder ID: ')
        os.system('sudo docker rm --force ' + str(container_name))
        
        # Remove firewall rule for container
        remove_container_firewall_rule(container_name=container_name)

        # Print 2 empty Lines for better reading
        print('\n\n')
    else:
        os.system('sudo docker rm --force ' + str(container_name))
        
        # Remove firewall rule for container
        remove_container_firewall_rule(container_name=container_name)

        # Print 2 empty Lines for better reading
        print('\n\n')


# Delete given image
def delete_image(image_name=''):
    if image_name == '':
        print('Welches Image soll entfernt werden?')
        image_name = input('Image Name oder ID: ')
        os.system('sudo docker image rm --force ' + str(image_name))
        # Print 2 empty Lines for better reading
        print('\n\n')
    else:
        os.system('sudo docker image rm --force ' + str(image_name))
        # Print 2 empty Lines for better reading
        print('\n\n')


# Delete given volume
def delete_volume(volume_name=''):
    if volume_name == '':
        print('Welches Volume soll entfernt werden?')
        volume_name = input('Volume Name oder ID: ')
        os.system('sudo docker volume rm --force ' + str(volume_name))
        # Print 2 empty Lines for better reading
        print('\n\n')
    else:
        os.system('sudo docker volume rm --force ' + str(volume_name))
        # Print 2 empty Lines for better reading
        print('\n\n')


# Save container port-mapping to a json file
def add_container_port_mapping(port='', container_name=''):
    port_mapping_dict = {}
    # Create dict with random ID, add dict with parameters to it
    port_mapping_dict[str(uuid.uuid4())] = {'name':container_name, 'port':port}
    
    docker_json = os.path.join(sys.path[0]) + '/config/docker/container-port-mapping.json'
    with open(docker_json, encoding='UTF-8') as fp:
        data = json.load(fp)

    data.update(port_mapping_dict)

    with open(docker_json, 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=4)


# Remove container port-mapping from json file
def remove_container_port_mapping(container_name=''):
    # Read json file
    docker_json = os.path.join(sys.path[0]) + '/config/docker/container-port-mapping.json'
    with open(docker_json, encoding='UTF-8') as fp:
        data = json.load(fp)
    
    # Iterate over dict
    for key, val in data.items():
        get_key = (data.get(key))
        if container_name in get_key.values():
            remove_key = key
    
    # Remove entry
    data.pop(remove_key)

    # Write back to file
    with open(docker_json, 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=4)

    
# Add Firewall rule for given container
def add_container_firewall_rule(port='', container_name=''):
    # Get container ip
    container_ip = os.popen("sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + str(container_name)).read()

    # Add forwarding rule for container to firewall, set container name as a comment
    os.system('sudo ufw route allow from any to ' + str(container_ip) + ' port ' + str(port) + ' comment ' + str(container_name))


# Remove Firewall rule for given container
def remove_container_firewall_rule(container_name=''):
    # Get all rules
    all_rules = pyufw.get_rules()

    # Get rule index
    for key, val in all_rules.items():
        get_values = all_rules.get(key)
        if container_name in get_values:
            rule_index = key

    # Delete rule
    os.system("echo 'y' | sudo ufw delete " + str(rule_index))


def get_container_port(container_name):
    # Read from json file
    docker_json = os.path.join(sys.path[0]) + '/config/docker/container-port-mapping.json'
    with open(docker_json, encoding='UTF-8') as fp:
        data = json.load(fp)

    # Get container port
    for key, val in data.items():
        get_key = (data.get(key))
        if container_name in get_key.values():
            container_port = get_key.get('port')
    
    return container_port

