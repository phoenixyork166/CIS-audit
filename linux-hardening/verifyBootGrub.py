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
    
    grubPath = '/boot/grub/'
    grubConfPath = '/boot/grub/grub.cfg'
    grubCfgName = 'grub.cfg'

    permission = '-rw------- 1 root root'
    #hardenedValue = re.search("(-rw-------)\s+\d+\s+(root)\s+(root)", permission)
    print(Fore.YELLOW + "\nCurrent /boot/grub/grub.cfg permission: \n")
    currentCfgPermission = os.system('ls -la /boot/grub/ | grep grub.cfg | awk \'{{print $1,$2,$3,$4}}\''.format(user))
    currentCfgPermission
    print(Fore.YELLOW + "====================================")
    ver = input(Fore.YELLOW + "\nEnter your Linux OS version [Suse15/Suse12/Suse11/Redhat/Debian/Kali]: ")
    
    if ver.lower() == str('kali'):       
        ##
        changeGrubConfPermission = f'echo {sudo_password} | sudo chmod 600 {grubConfPath}'
        doChangeGrubConfPermission = subprocess.Popen(changeGrubConfPermission, shell=True, text=True)
        doChangeGrubConfPermission.wait()
        if doChangeGrubConfPermission.returncode == 0:
            print(Fore.YELLOW + "\nChanging grub.cfg Permission has succeeded!\n")
            print(Fore.YELLOW + "\nVerifying the new grub.cfg Permission...\n")

            #verifyGrubConfPermission = f"echo {sudo_password} | sudo ls -la {grubPath} | grep {grubCfgName} | awk '{{print $1,$2,$3,$4}}'"
            #doVerifyGrubConfPermission = subprocess.Popen(verifyGrubConfPermission, shell=True)
            #doVerifyGrubConfPermission.wait()
            newPermission = os.system('ls -la /boot/grub/ | grep grub.cfg | awk \'{{print $1,$2,$3,$4}}\''.format(user))
            newPermission
            print(Fore.YELLOW + "\nHardening for /boot/grub/grub.cfg has succeeded!\n")
        else:
            print(Fore.RED + "\nFailed to change grub.cfg Permissions...\nSkipping...\n")
        ##

    # elif ver.lower() == str('suse11'):
    #     grubPath = '/boot/grub/'
    #     grubConfPath = '/boot/grub/menu.lst'
    #     grubCfgName = 'menu.lst'
    #     ##
    #     changeGrubConfPermission = f'echo {sudo_password} | sudo chmod 600 {grubConfPath}'
    #     doChangeGrubConfPermission = subprocess.Popen(changeGrubConfPermission, shell=True, text=True)
    #     doChangeGrubConfPermission.wait()
    #     if doChangeGrubConfPermission.returncode == 0:
    #         print(Fore.YELLOW + "\nChanging grub.cfg Permission has succeeded!\n")
    #         print(Fore.YELLOW + "\nVerifying grub.cfg Permission...\n")

    #         verifyGrubConfPermission = f"echo {sudo_password} | sudo ls -la {grubPath} | grep {grubCfgName} | awk '{{print $1,$2,$3,$4}}'"
    #         doVerifyGrubConfPermission = subprocess.Popen(verifyGrubConfPermission, shell=True, text=True, stdout=subprocess.PIPE)
    #         doVerifyGrubConfPermission.wait()
    #         os.system('sudo -u {} sudo ls -la {grubPath} | grep {grubCfgName} | awk '{print $1,$2,$3,$4}''.format(user))
    #         ##
    #     else:
    #         print(Fore.RED + "\nFailed to change grub.cfg Permissions...\nSkipping...\n")
    #     ##

    # elif ver.lower() == str('suse15') or str('suse12') or str('redhat'):
    #     grubPath = '/boot/grub2/'
    #     grubConfPath = '/boot/grub2/grub.cfg'
    #     grubCfgName = 'grub.cfg'
    #     ##
    #     changeGrubConfPermission = f'echo {sudo_password} | sudo chmod 600 {grubConfPath}'
    #     doChangeGrubConfPermission = subprocess.Popen(changeGrubConfPermission, shell=True, text=True)
    #     doChangeGrubConfPermission.wait()
    #     if doChangeGrubConfPermission.returncode == 0:
    #         print(Fore.YELLOW + "\nChanging grub.cfg Permission has succeeded!\n")
    #         print(Fore.YELLOW + "\nVerifying grub.cfg Permission...\n")

    #         verifyGrubConfPermission = f"echo {sudo_password} | sudo ls -la {grubPath} | grep {grubCfgName} | awk '{{print $1,$2,$3,$4}}'"
    #         doVerifyGrubConfPermission = subprocess.Popen(verifyGrubConfPermission, shell=True, text=True, stdout=subprocess.PIPE)
    #         doVerifyGrubConfPermission.wait()
    #         os.system('sudo -u {} sudo ls -la {grubPath} | grep {grubCfgName} | awk '{print $1,$2,$3,$4}''.format(user))
    #         ##
    #     else:
    #         print(Fore.RED + "\nFailed to change grub.cfg Permissions...\nSkipping...\n")
        ##

    else: 
        print(Fore.RED + "The entered os version is not supported...\Skipping...")

    
