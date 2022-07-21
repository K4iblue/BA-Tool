import os

# Create Container, from file
def create_container_from_file():
    # Get dockerfile path from user
    print('Wie lautet der Pfad der Dockerfile?')
    path = input('Pfad: ')
    if os.path.exists(path):
        print('Klappt')
    else:
        print ('Directory not exists')

# Create Container, from Image
def create_container_from_image():

    # Get image name
    print('Aus welchen Image soll der Container erstellt werden?')
    image_name = str(input('Name oder ID: '))

    # Get name for container
    print('Wie soll der Container heißen?')
    container_name = str(input('Container Name: '))

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
    run_command += port_string
    run_command += ' --name ' + container_name + ' '
    run_command += image_name

    # Run the docker command
    os.system('sudo ' + str(run_command))


###################################################
######### Alles hier drunter funktioniert #########
###################################################
# Start given Container
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


# Stop given Container
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


# List all Containers
def show_container_list():
    os.system('sudo docker container ls --all')
    # Print 2 empty Lines for better reading
    print('\n\n')


# List all Images
def show_images_list():
    os.system('sudo docker image ls --all')
    # Print 2 empty Lines for better reading
    print('\n\n')


# Delete given Container
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


# Delete given Image
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


########## Löschen
#def create_docker_image():
#    # Get path of script and dockerfile
#    path = os.path.join(sys.path[0])
#    # User input for docker image name
#    print('--- Enter Docker Image Name ---')
#    image_name = input('Image Name: ').lower()
#    # Get ImageID from console and convert to string
#    # ImageId = subprocess.check_output(['docker', 'images', '-q', ImageName])
#    # ImageIdString = str(ImageId).replace(''','').replace('\\n','')
#    # Create image from Dockerfile
#    subprocess.run(['docker', 'build', path, '-t', image_name.replace('"', '')], shell=True, check=True)
#    # return image name for later use
#    return image_name


#def start_docker_container(image_name=''):
#    # Start Container from image
#    subprocess.run(['docker', 'run', image_name], shell=True, check=True)
