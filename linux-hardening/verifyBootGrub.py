import os
from colorama import Fore, Back, Style
import subprocess
import getpass
import re

# 3. Linux Security in "General"
# 3.3 Boot Options
# 3.3.3 Grub

def verifyBootGrub():
    user = input(Fore.WHITE + "Running this script as: ")    
    sudo_password = getpass.getpass(prompt='Enter sudo password: ')
    print(Fore.WHITE + "Changing /boot/grub/grub.cfg permissions...\n")
    grubPath = '';
    grubConf = '';
    permission = '-rw------- 1 root root'
    hardenedValue = re.search("(-rw-------)\s+\d+\s+(root)\s+(root)", permission)
    print(hardenedValue)
    os = input(Fore.YELLOW + "\nEnter your Linux OS version [Suse15/Suse12/Suse11/Redhat/Debian/Kali]: ")
    
    if os.lower() == "suse15" or "suse12" or "redhat":
        grubPath = '/boot/grub/'
        grubConfPath = '/boot/grub/grub.cfg'
        grubConfName = 'grub.cfg'
        
        ##
        changeGrubConfPermission = f'echo {sudo_password} | sudo chmod 600 {grubConfPath}'
        doChangeGrubConfPermission = subprocess.Popen(changeGrubConfPermission, shell=True, text=True)
        doChangeGrubConfPermission.wait()
        if doChangeGrubConfPermission.returncode == 0:
            print(Fore.YELLOW + "\nChanging grub.cfg Permission has succeeded!\n")
            print(Fore.YELLOW + "\nVerifying grub.cfg Permission...\n")
            awk = "awk '{print $1,$2,$3,$4}'"
            verifyGrubConfPermission = f"echo {sudo_password} | sudo ls -la {grubPath} | grep {grubConfName} | awk '{print \$1,\$2,\$3,\$4}'"
            doVerifyGrubConfPermission = subprocess.Popen(verifyGrubConfPermission, shell=True, text=True, stdout=subprocess.PIPE)
            doVerifyGrubConfPermission.wait()
            if doVerifyGrubConfPermission.returncode == 0:
                print(doVerifyGrubConfPermission.stdout)
                ##
                            
            else:
                print(Fore.RED + "\nFailed to verify grub.cfg permissions...\nSkipping...\n")
        else:
            print(Fore.RED + "\nFailed to change grub.cfg Permissions...\nSkipping...\n")
        ##

    elif os.lower() == "suse11":
        grubPath = '/boot/grub/'
        grubConfPath = '/boot/grub/menu.lst'
        grubConfName = 'menu.lst'
        ##
        changeGrubConfPermission = f'echo {sudo_password} | sudo chmod 600 {grubConfPath}'
        doChangeGrubConfPermission = subprocess.Popen(changeGrubConfPermission, shell=True, text=True)
        doChangeGrubConfPermission.wait()
        if doChangeGrubConfPermission.returncode == 0:
            print(Fore.YELLOW + "\nChanging grub.cfg Permission has succeeded!\n")
            print(Fore.YELLOW + "\nVerifying grub.cfg Permission...\n")
            awk = "awk '{print $1,$2,$3,$4}'"
            verifyGrubConfPermission = f"echo {sudo_password} | sudo ls -la {grubPath} | grep {grubConfName} | awk '{print \$1,\$2,\$3,\$4}'"
            doVerifyGrubConfPermission = subprocess.Popen(verifyGrubConfPermission, shell=True, text=True, stdout=subprocess.PIPE)
            doVerifyGrubConfPermission.wait()
            if doVerifyGrubConfPermission.returncode == 0:
                print(doVerifyGrubConfPermission.stdout)
                ##
                            
            else:
                print(Fore.RED + "\nFailed to verify grub.cfg permissions...\nSkipping...\n")
        else:
            print(Fore.RED + "\nFailed to change grub.cfg Permissions...\nSkipping...\n")
        ##

    elif os.lower() == "kali":
        grubPath = '/boot/grub/'
        grubConfPath = '/boot/grub/grub.cfg'
        grubConfName = 'grub.cfg'
        ##
        changeGrubConfPermission = f'echo {sudo_password} | sudo chmod 600 {grubConfPath}'
        doChangeGrubConfPermission = subprocess.Popen(changeGrubConfPermission, shell=True, text=True)
        doChangeGrubConfPermission.wait()
        if doChangeGrubConfPermission.returncode == 0:
            print(Fore.YELLOW + "\nChanging grub.cfg Permission has succeeded!\n")
            print(Fore.YELLOW + "\nVerifying grub.cfg Permission...\n")
            awk = "awk '{print $1,$2,$3,$4}'"
            verifyGrubConfPermission = f"echo {sudo_password} | sudo ls -la {grubPath} | grep {grubConfName} | awk '{print \$1,\$2,\$3,\$4}'"
            doVerifyGrubConfPermission = subprocess.Popen(verifyGrubConfPermission, shell=True, text=True, stdout=subprocess.PIPE)
            doVerifyGrubConfPermission.wait()
            if doVerifyGrubConfPermission.returncode == 0:
                print(doVerifyGrubConfPermission.stdout)
                ##
                           
            else:
                print(Fore.RED + "\nFailed to verify grub.cfg permissions...\nSkipping...\n")
        else:
            print(Fore.RED + "\nFailed to change grub.cfg Permissions...\nSkipping...\n")
        ##

    else: 
        print(Fore.RED + "The entered os version is not supported...\Skipping...")

    
