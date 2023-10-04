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
    print(Fore.YELLOW + "Changing /boot/grub/grub.cfg permissions...\n")
    
    grubPath = '/boot/grub/'
    grubConfPath = '/boot/grub/grub.cfg'
    grubCfgName = 'grub.cfg'

    grub2Path = '/boot/grub2/'
    grub2ConfPath = '/boot/grub2/grub.cfg'
    grub2CfgName = 'grub.cfg'

    regex = "^-rw-------\s+\d+\s+root\s+root$"
    #hardenedValue = re.search("(-rw-------)\s+\d+\s+(root)\s+(root)", permission)
    print(Fore.YELLOW + "\nCurrent /boot/grub/grub.cfg permission: \n")
    currentPermission = os.system('ls -la /boot/grub/ | grep grub.cfg | awk \'{{print $1,$2,$3,$4}}\''.format(user))
    print(Fore.YELLOW + "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
      
    # Grub1
    ## chmod 600 /boot/grub/grub.cfg
    grubChmod600 = f'echo {sudo_password} | sudo chmod 600 {grubConfPath}'
    doGrubChmod600 = subprocess.Popen(grubChmod600, shell=True, text=True)
    doGrubChmod600.wait()

    if doGrubChmod600.returncode == 0:
        print(Fore.YELLOW + "\nchmod 600 /boot/grub/grub.cfg has succeeded!\nProceeding to chown root /boot/grub/grub.cfg\n")
        ## chown root /boot/grub/grub.cfg
        grubChown = f'echo {sudo_password} | sudo chown root {grubConfPath}'
        doGrubChown = subprocess.Popen(grubChown, shell=True, text=True)
        doGrubChown.wait()

        if doGrubChown.returncode == 0:
            print(Fore.YELLOW + "\nchown root /boot/grub/grub.cfg has succeeded!\nProceeding to chgrp root /boot/grub/grub.cfg\n")
            ### chgrp root /boot/grub/grub.cfg
            grubChgrp = f'echo {sudo_password} | sudo chgrp root {grubConfPath}'
            doGrubChgrp = subprocess.Popen(grubChgrp, shell=True, text=True)
            doGrubChgrp.wait()

            if doGrubChgrp.returncode == 0:
                print(Fore.YELLOW + "\nchgrp root /boot/grub/grub.cfg has succeeded!\nProceeding to verify latest permissions for /boot/grub/grub.cfg: ")
                ##
                print(Fore.YELLOW + "\nLatest /boot/grub/grub.cfg permissions are: ")
                #newPermission = os.system('ls -la /boot/grub/ | grep grub.cfg | awk \'{{print $1,$2,$3,$4}}\''.format(user))
                readPermission = f'echo {sudo_password} | sudo ls -la {grubPath} | grep {grubCfgName} | awk \'{{print $1,$2,$3,$4}}\''
                doReadPermission = subprocess.run(readPermission, shell=True, text=True, capture_output=True)
                print(doReadPermission.stdout)
                
                hardenedValue = re.match(regex, doReadPermission.stdout)
                # printing match object 
                #print(hardenedValue) # span=(0,22)
                # span=(start, end)
                #print(hardenedValue.start()) #
                if hardenedValue.start() == 0:
                    print(Fore.YELLOW + "\nHardening for /boot/grub/grub.cfg has succeeded!\n")
                else:
                    print(Fore.RED + "\nFailed to harden /boot/grub/grub.cfg...\nSkipping...\n")
        else:
            print(Fore.RED + "\nFailed to chown root /boot/grub/grub.cfg...\nSkipping...\n")
        
    else:
        print(Fore.RED + "\nFailed to chmod 600 /boot/grub/grub.cfg...\nSkipping...\n")
    

    
