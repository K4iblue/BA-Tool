import subprocess
import os
import sys


def main():
    print("-------------- Menu --------------")
    print("0. Exit program \n" +
          "1. Härtung durchführen \n" +
          "2. Automatische Updates \n" +
          "3. Standardprogramme installieren \n" +
          "4. Docker: Image erstellen\n" +
          "5. Docker: Image starten \n")
    print("--- Please enter a number (0-5) ---")

    case_number = int(input())
    match case_number:
        case 0:
            quit()
        case 1:
            start_hardening()
            print("Case 1")
            main()
        case 2:
            #image_name = input("welches Image soll gestartet werden: ").lower()
            #start_docker_container(image_name)
            print("Case 2")
            main()
        case 3:
            #start_docker_container(create_docker_image())
            print("Case 3")
            main()
        case 4:
            print("Case 4")
        case 5:
            print("Case 5")
        case _:
            print("Please enter a valid number (0-5) !")
            main()

def start_hardening():
    # Install necessary packages
    subprocess.run(["sudo", "apt-get", "-y", "install", "git", "net-tools", "procps", "--no-install-recommend"], shell=True, check=True)

    # Run Hardening Script
    subprocess.run(["sudo", "bash", "scripts/hardening/ubuntu.sh"], shell=True, check=True)

def create_docker_image():
    # Get path of script and dockerfile
    path = os.path.join(sys.path[0])

    # User input for docker image name
    print("--- Enter Docker Image Name ---")
    image_name = input("Image Name: ").lower()

    # Get ImageID from console and convert to string
    # ImageId = subprocess.check_output(["docker", "images", "-q", ImageName])
    # ImageIdString = str(ImageId).replace("'","").replace("\\n","")

    # Create image from Dockerfile
    subprocess.run(["docker", "build", path, "-t", image_name.replace('"', '')],
                    shell=True, check=True)

    # return image name for later use
    return image_name

def start_docker_container(image_name):
    # Start Container from image
    subprocess.run(["docker", "run", image_name], shell=True, check=True)

if __name__ == "__main__":
    main()
