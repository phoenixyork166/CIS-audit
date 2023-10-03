# --------------
# Imports modules
# --------------
import os
from colorama import Fore, Back, Style
import subprocess
import getpass
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
user = input(Fore.WHITE + 'Running this script as: ')
echo_password = getpass.getpass(prompt='Enter your echo password: ')

