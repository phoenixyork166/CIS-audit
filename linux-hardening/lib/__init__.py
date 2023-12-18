# Operating system
import os
# Screen font Color
import colorama
# Screen font display
from colorama import Fore, Back, Style
# File system processing
import subprocess
# To mask screen password inputs
import getpass
# Regex module
import re
# System module
import sys
# To record sys execution time
import time
from time import ctime

# To confirm Linux distribution in /etc/os-release
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
echoDistroName = f"Current distro is :{distroName}"
print(Fore.MAGENTA + echoDistroName)
print(type(distroName))

# A function to return all essential Python modules
def initializeModules():
    global os, Fore, Back, Style, getpass, subprocess, re

    # Initialize colorama
    colorama.init(autoreset=True)

    return os, Fore, Back, Style, getpass, subprocess, re
    # Initialize all modules

# Getting ROOT priviledge from users to allow sudo actions
def getCredentials():
    try:
        print(Fore.WHITE + "\nProceeding...\n")
        user = input(Fore.WHITE + "Please enter [root]: ")
        if user.lower() == "root":
            print(Fore.YELLOW + f'Verifying that your\'re {user}...')
            if os.geteuid() == 0:
                print(Fore.YELLOW + f"Successfully verified that you're root :)!\nProceeding...\n")
            else:
                print(Fore.RED + f'You aren\'t root :(\nExiting process...\n')
                exit()
        
        else:
            print(Fore.RED + f'Sorry, you aren\'t ROOT\nYou can only run this python as ROOT :(')
            exit()

        sudo_password = getpass.getpass(prompt='Enter sudo password: ')
        return user, sudo_password

    except Exception as e:
        # Handle exceptions
        print(Fore.RED + f'Error retrieving root credentials from script user: {str(e)}')
        print(Fore.RED + 'Terminating script running & all Shell processes...\n')

# Returning user, sudo_password from getCredentials()
user, sudo_password = getCredentials()

def timer():
    try:
        # Retrieve time whenever timer() functions is called
        thisTime = ctime(time.time())
        return thisTime

    except Exception as e:
        print(Fore.RED + f'Failed to retrieve current time :(\n')
        return None
thisTime = timer();