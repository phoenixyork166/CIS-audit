import os
from colorama import Fore, Back, Style
import subprocess
import getpass
import re


def doChangeGrub():
    
    changeGrubConfPermission = f'echo {sudo_password} | sudo chmod 600 {grubConfPath}'
    doChangeGrubConfPermission = subprocess.Popen(changeGrubConfPermission, shell=True, text=True)
    doChangeGrubConfPermission.wait()
    if doChangeGrubConfPermission.returncode == 0:
        print(Fore.YELLOW + "\nChanging grub.cfg Permission has succeeded!\n")
        print(Fore.YELLOW + "\nVerifying grub.cfg Permission is -rw-------\s+\d+\s+root\s+root\n")
        awk = "awk '{print $1,$2,$3,$4}'"
        verifyGrubConfPermission = f'echo {sudo_password} | sudo ls -la {grubPath} | grep {grubConfName} | {awk}'
        doVerifyGrubConfPermission = subprocess.Popen(verifyGrubConfPermission, shell=True, text=True)
        doVerifyGrubConfPermission.wait()
        if doVerifyGrubConfPermission.returncode == 0:
            print(Fore.YELLOW + "\nGrepping grub.cfg permissions has succeeded!\nProceeding to comparing hardened value...\n")
            print(doVerifyGrubConfPermission)            
        else:
            print(Fore.RED + "\nFailed to verify grub.cfg permissions...\nSkipping...\n")
    else:
        print(Fore.RED + "\nFailed to change grub.cfg Permissions...\nSkipping...\n")