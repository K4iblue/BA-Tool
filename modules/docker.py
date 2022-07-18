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


def start_docker_container(image_name):
    # Start Container from image
    subprocess.run(['docker', 'run', image_name], shell=True, check=True)

def check_docker_install():
    print('Check: Docker Installation')
    if os.system('docker -v') == 'docker: not found': #os.system('echo $?') == 0:
        print('Docker ist installiert')
    else:
        print('Docker ist nicht installiert')
        install_docker()

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
