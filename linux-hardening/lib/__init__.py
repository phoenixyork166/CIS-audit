import os
import colorama
from colorama import Fore, Back, Style
import subprocess
import getpass
import re
    
def get_distroName():
    try:
        with open('/etc/os-release', 'r') as os_release_file:
            for line in os_release_file:
                if line.startswith('ID='):
                    # Extact distribution name and remove quotes
                    return line.split('=')[1].strip().strip('"')
    except FileNotFoundError:
        return None

# Move distroName outside the function
distroName = get_distroName()
#distroName = f"Current distro name is: {getDistro}"
#print(Fore.MAGENTA + distroName)
echoDistroName = f"Current distro name is :{distroName}"
print(Fore.MAGENTA + echoDistroName)
print(type(distroName))

def initializeModules():
    global os, Fore, Back, Style, getpass, subprocess, re

    # Initialize colorama
    colorama.init(autoreset=True)

    return os, Fore, Back, Style, getpass, subprocess, re
    # Initialize all modules

def getCredentials():
    try:
        print(Fore.WHITE + "\nProceeding...\n")
        user = input(Fore.WHITE + "Running this script as root: ")
        sudo_password = getpass.getpass(prompt='Enter sudo password: ')
        return user, sudo_password
    except Exception as e:
        # Handle exceptions
        print(Fore.RED + f'Error retrieving credentials from script user: {str(e)}')
        return None, None
    
user, sudo_password = getCredentials()