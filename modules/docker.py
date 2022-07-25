import os


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


# Create Container
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
    print('Welche Ports werden für den Container benötigt? Mehrere Ports durch ein Komma trennen!')
    ports = str(input('Ports: '))

    # Remove Spaces
    ports = ports.replace(' ', '')
    # Create list from string
    port_list = ports.split(',')
    # Append ports for the run command if multiple are needed
    port_string = ''
    for n in port_list:
        port_string += ' -p ' + str(n)+ ':' + str(n)
    
    # Create docker run command
    run_command = 'docker run -d'
    if volume_needed is True: 
        run_command += volume_string
    run_command += port_string
    run_command += ' --name ' + container_name + ' '
    run_command += image_name

    # Run the docker command
    os.system('sudo ' + str(run_command))


# Start given container
def start_container(container_name=''):
    if container_name == '':
        print('Welcher Container soll gestartet werden?')
        container_name = input('Container Name oder ID: ')
        os.system('sudo docker start ' + str(container_name))
        # Print 2 empty Lines for better reading
        print('\n\n')
    else:
        os.system('sudo docker stop ' + str(container_name))
        # Print 2 empty Lines for better reading
        print('\n\n')


# Stop given container
def stop_container(container_name=''):
    if container_name == '':
        print('Welcher Container soll gestoppt werden?')
        container_name = input('Container Name oder ID: ')
        os.system('sudo docker stop ' + str(container_name))
        # Print 2 empty Lines for better reading
        print('\n\n')
    else:
        os.system('sudo docker stop ' + str(container_name))
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
        print('Welcher Container soll gelöscht werden?')
        container_name = input('Container Name oder ID: ')
        os.system('sudo docker rm --force ' + str(container_name))
        # Print 2 empty Lines for better reading
        print('\n\n')
    else:
        os.system('sudo docker rm --force ' + str(container_name))
        # Print 2 empty Lines for better reading
        print('\n\n')


# Delete given image
def delete_image(image_name=''):
    if image_name == '':
        print('Welches Image soll gelöscht werden?')
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
        print('Welches Volume soll gelöscht werden?')
        volume_name = input('Volume Name oder ID: ')
        os.system('sudo docker volume rm --force ' + str(volume_name))
        # Print 2 empty Lines for better reading
        print('\n\n')
    else:
        os.system('sudo docker volume rm --force ' + str(volume_name))
        # Print 2 empty Lines for better reading
        print('\n\n')


# Installation according to https://docs.docker.com/engine/install/ubuntu/
def install_docker():
    print('Starte Docker Installation')

    # Update the apt package index and install packages to allow apt to use a repository over HTTPS:
    os.system('sudo apt-get update')
    os.system('sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release')

    # Add Docker’s official GPG key:
    os.system('sudo mkdir -p /etc/apt/keyrings')
    os.system('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg')

    # Use the following command to set up the repository:
    os.system('echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')

    # Update the apt package index, and install the latest version of Docker Engine
    os.system('sudo apt-get update')
    os.system('sudo apt-get install docker-ce -y')

    # Start Docker Deamon
    os.system('sudo systemctl start docker')
