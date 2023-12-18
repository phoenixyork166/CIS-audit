# --------------
# Imports modules
# --------------
#import os
#from colorama import Fore, Back, Style
#import subprocess
#import getpass
from lib import getCredentials, distroName, initializeModules, Fore, os, Back, Style, getpass, subprocess, re
import sys
sys.path.append(os.path.abspath("/home/phoenix/Desktop/tools/CIS-audit/linux-hardening"))

# ==============
# --------------
# Imports module 'webdriver' from 'selenium'
# Trying to automate some key send actions in Firefox
# --------------
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import action_chains
#from selenium.webdriver.firefox.firefox_binary import firefox_binary
#binary = firefox_binary('/usr/bin/firefox')
#browser = webdriver.firefox(firefox_binary=binary)
# ===============

# Example for modules import
# Add new Low Privilege User Account
# print(Fore.WHITE + "### Creating a Low Priv User ###")
# print(Style.RESET_ALL)
# import addUser
# addUser.addUser()
#user = input(Fore.WHITE + 'Running this script as: ')
#echo_password = getpass.getpass(prompt='Enter your echo password: ')

# Linux Security
# 1. Boot options
# Verify Boot Grub
from lib.verifyBootGrub import verifyBootGrub
verifyBootGrub()

# 2. Verify NIS Server
# Verify NIS Server services ypserv is disabled
from lib.verifyNIS import verifyNIS
verifyNIS()

# 3. Security Features in the Kernel
# 3.9.1 Enable TCP SYN Cookie Protection (default in SUSE Linux Enterprise Server11)
# 3.9.1.1 Verify TCP SYNC Cookie Protection is Enabled
# config = cat /etc/sysctl.conf | egrep '^\s*net\.ipv4\.tcp\_syncookies\s*=\s*(\d*)\s*'
#from lib.verifyTcpSyncCookies import verifyTcpSyncCookies
from lib.verifyTcpSyncCookies import verifyTcpSyncCookies
verifyTcpSyncCookies()

# 3.12.1 Verify TFTP service is disabled






