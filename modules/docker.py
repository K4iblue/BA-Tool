import subprocess
import os
import sys

def create_docker_image():
    # Get path of script and dockerfile
    path = os.path.join(sys.path[0])

    # User input for docker image name
    print('--- Enter Docker Image Name ---')
    image_name = input('Image Name: ').lower()

    # Get ImageID from console and convert to string
    # ImageId = subprocess.check_output(['docker', 'images', '-q', ImageName])
    # ImageIdString = str(ImageId).replace(''','').replace('\\n','')

    # Create image from Dockerfile
    subprocess.run(['docker', 'build', path, '-t', image_name.replace('"', '')], shell=True, check=True)

    # return image name for later use
    return image_name


def start_docker_container(image_name=''):
    # Start Container from image
    subprocess.run(['docker', 'run', image_name], shell=True, check=True)


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


# List all Containers
def show_container_list():
    print('Container List...')
    os.system('sudo docker container ls --all')

# List all Images
def show_images_list():
    os.system('sudo docker image ls --all')

# Start given Container
def start_container(container_name=''):
    print('Starte Container XXX...')
    os.system('sudo docker start ' + str(container_name))


# Stop given Container
def stop_container(container_name=''):
    print('Stop Container XXX...')


# Delete given Container
def delete_container(container_name=''):
    if container_name == '':
        print('Welcher Container soll gelöscht werden?')
        container_name = input('Container Name oder ID: ')
        os.system('sudo docker rm --force' + str(container_name))
    else:
        os.system('sudo docker rm --force' + str(container_name))
    # Wenn Container läuft muss dieser zuerst gestoppt werden
    # Dann kann der Container gelöscht wgit erden


# Create Container
def create_container():
    print('Create Container XXX...')
    # Dockerfile angeben -> Image daraus erstellen -> Container daraus erstellen
    # Docker Image runterladen als Option ?

# Delete given Image
def delete_image(image_name=''):
    if image_name == '':
        print('Welches Image soll gelöscht werden?')
        image_name = input('Image Name oder ID: ')
        os.system('sudo docker image rm --force' + str(image_name))
    else:
        os.system('sudo docker image rm --force' + str(image_name))
    # Wenn Container läuft muss dieser zuerst gestoppt werden
    # Dann kann der Container gelöscht werden
