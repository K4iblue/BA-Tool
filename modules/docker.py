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
