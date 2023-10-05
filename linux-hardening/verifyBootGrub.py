import os
from colorama import Fore, Back, Style
import subprocess
import getpass
import re

# 3. Linux Security in "General"
# 3.3 Boot Options
# 3.3.3 Grub

def verifyBootGrub():
    confirm = input(Fore.WHITE + "\n[x] Do you wanna harden 3.3.3 Boot Options for either of following: \n/boot/grub/grub.cfg\n/boot/grub2/grub.cfg\n/boot/grub/menu.lst\n[x] [y/N]: ")
    if confirm.lower() == "y":
        print(Fore.WHITE + "\nProceeding...\n")
        user = input(Fore.WHITE + "Running this script as: ")    
        sudo_password = getpass.getpass(prompt='Enter sudo password: ')
        
        regex = "^-rw-------\s+\d+\s+root\s+root$"
        #hardenedValue = re.search("(-rw-------)\s+\d+\s+(root)\user = input(Fore.WHITE + "Running this script as: ")    

        grubPath = '/boot/grub/'
        grubConfPath = '/boot/grub/grub.cfg'
        grubCfgName = 'grub.cfg'

        # Grub1
        # Try listing /boot/grub 1st...
        print(Fore.YELLOW + "\nTrying to list /boot/grub/grub.cfg...\n")
        lsGrub = f'echo {sudo_password} | sudo ls -la {grubPath}'
        doLsGrub = subprocess.Popen(lsGrub, shell=True, text=True)
        doLsGrub.wait()

        if doLsGrub.returncode == 0:
            print(Fore.YELLOW + "\ngrub.cfg exists in /boot/grub/\n\nProceeding to checking current config...\n")
            check = f'echo {sudo_password} | sudo ls -la {grubPath} | grep {grubCfgName} | awk \'{{print $1,$2,$3,$4}}\''
            doCheck = subprocess.run(check, shell=True, text=True, capture_output=True)
            #print(doCheck.stdout)
            # Store output from doCheck stdout
            output = doCheck.stdout
            # Trim whitespace
            output = output.strip()
            print(output)

            validate = re.search(regex, output)
            print(validate)
            
            print(Fore.YELLOW + "\nComparing current config to desired config...\n")
            
            if not validate:
                print(Fore.RED + "\nCurrent config is NOT compliant...\nProceeding to hardening...\n")
                ##
                print(Fore.YELLOW + "\nchmod 600 /boot/grub/grub.cfg in progress...\n")
                grubChmod600 = f'echo {sudo_password} | sudo chmod 600 {grubConfPath}'
                doGrubChmod600 = subprocess.Popen(grubChmod600, shell=True, text=True)
                doGrubChmod600.wait()

                if doGrubChmod600.returncode == 0:
                    print(Fore.YELLOW + "\nchmod 600 /boot/grub/grub.cfg has succeeded!\nProceeding to chown root /boot/grub/grub.cfg ...\n")
                    grubChown = f'echo {sudo_password} | sudo chown root {grubConfPath}'
                    doGrubChown = subprocess.Popen(grubChown, shell=True, text=True)
                    doGrubChown.wait()

                    if doGrubChown.returncode == 0:
                        print(Fore.YELLOW + "\nchown root /boot/grub/grub.cfg has succeeded!\nProceeding to chgrp root /boot/grub/grub.cfg\n")
                        grubChgrp = f'echo {sudo_password} | sudo chgrp root {grubConfPath}'
                        doGrubChgrp = subprocess.Popen(grubChgrp, shell=True, text=True)
                        doGrubChgrp.wait()

                        if doGrubChgrp.returncode == 0:
                            print(Fore.YELLOW + "\nchgrp root /boot/grub/grub.cfg has succeeded!\nProceeding to verify latest permissions for /boot/grub/grub.cfg: ")
                            print(Fore.YELLOW + "\nLatest /boot/grub/grub.cfg permissions are: ")
                            readPermission = f'echo {sudo_password} | sudo ls -la {grubPath} | grep {grubCfgName} | awk \'{{print $1,$2,$3,$4}}\''
                            doReadPermission = subprocess.run(readPermission, shell=True, text=True, capture_output=True)
                            doReadPermission_output = doReadPermission.stdout
                            doReadPermission_output = doReadPermission_output.strip()
                            print(doReadPermission_output)
                        
                            hardenedValue = re.match(regex, doReadPermission_output)

                            if hardenedValue.start() == 0:
                                print(Fore.YELLOW + "\nHardening for /boot/grub/grub.cfg has succeeded!\n")
                            else:
                                print(Fore.RED + "\nFailed to harden /boot/grub/grub.cfg...\nEnsure you entered a correct sudo password & try again...\n")
                        else:
                            print(Fore.RED + "\nFailed to chgrp root /boot/grub/grub.cfg...\nEnsure you entered a correct sudo password & try again...\n")
                    else:
                        print(Fore.RED + "\nFailed to chown root /boot/grub/grub.cfg...\nEnsure you entered a correct sudo password & try again...\n")
                else:
                    print(Fore.RED + "\nFailed to chmod 600 /boot/grub/grub.cfg...\nEnsure you entered a correct sudo password & try again...\n")
            else:                
                print(Fore.YELLOW + "\nCurrent config is compliant...\nSkipping hardening...\n")
        
        else:
            print(Fore.RED + "\ngrub.cfg does NOT exist in /boot/grub/\nProceeding to attempt for /boot/grub2/grub.cfg ...\n")

            grub2Path = '/boot/grub2/'
            grub2ConfPath = '/boot/grub2/grub.cfg'
            grub2CfgName = 'grub.cfg'

            # Grub2
            # Try listing /boot/grub2/ 
            # If listing /boot/grub2/ failed...
            lsGrub2 = f'echo {sudo_password} | sudo ls -la {grub2Path}'
            doLsGrub2 = subprocess.Popen(ls2Grub, shell=True, text=True)
            doLsGrub2.wait()

            # if /boot/grub2/grub.cfg is located
            if doLsGrub2.returncode == 0:
                print(Fore.YELLOW + "\ngrub.cfg exists in /boot/grub2/\nProceeding to hardening...\n")
                # Hardening /boot/grub2/grub.cfg
                grub2Chmod600 = f'echo {sudo_password} | sudo chmod 600 {grub2ConfPath}'
                doGrub2Chmod600 = subprocess.Popen(grub2Chmod600, shell=True, text=True)
                doGrub2Chmod600.wait()

                if doGrub2Chmod600.returncode == 0:
                    print(Fore.YELLOW + "\nchmod 600 /boot/grub2/grub.cfg has succeeded!\nProceeding to chown root /boot/grub2/grub.cfg\n")
                    ## chown root /boot/grub/grub.cfg
                    grub2Chown = f'echo {sudo_password} | sudo chown root {grub2ConfPath}'
                    doGrub2Chown = subprocess.Popen(grub2Chown, shell=True, text=True)
                    doGrub2Chown.wait()

                    if doGrub2Chown.returncode == 0:
                        print(Fore.YELLOW + "\nchown root /boot/grub2/grub.cfg has succeeded!\nProceeding to chgrp root /boot/grub2/grub.cfg\n")
                        ### chgrp root /boot/grub2/grub.cfg
                        grub2Chgrp = f'echo {sudo_password} | sudo chgrp root {grub2ConfPath}'
                        doGrub2Chgrp = subprocess.Popen(grub2Chgrp, shell=True, text=True)
                        doGrub2Chgrp.wait()

                        if doGrub2Chgrp.returncode == 0:
                            print(Fore.YELLOW + "\nchgrp root /boot/grub2/grub.cfg has succeeded!\nProceeding to verify latest permissions for /boot/grub2/grub.cfg: ")
                            ##
                            print(Fore.YELLOW + "\nLatest /boot/grub2/grub.cfg permissions are: ")
                            #newPermission = os.system('ls -la /boot/grub/ | grep grub.cfg | awk \'{{print $1,$2,$3,$4}}\''.format(user))
                            readPermission2 = f'echo {sudo_password} | sudo ls -la {grub2Path} | grep {grub2CfgName} | awk \'{{print $1,$2,$3,$4}}\''
                            doReadPermission2 = subprocess.run(readPermission2, shell=True, text=True, capture_output=True)
                            print(doReadPermission2.stdout)
                            
                            hardenedValue2 = re.match(regex, doReadPermission2.stdout)
                            # printing match object 
                            #print(hardenedValue2) # span=(0,22)
                            # span=(start, end)
                            #print(hardenedValue2.start()) #
                            if hardenedValue2.start() == 0:
                                print(Fore.YELLOW + "\nCIS 3.3.3 Hardening for /boot/grub2/grub.cfg has succeeded!\n")
                            else:
                                print(Fore.RED + "\nFailed to harden /boot/grub2/grub.cfg...\nMake sure you're running this script as root & try again...\n")
                        
                        else:
                            print(Fore.RED + "\nFailed to chgrp root /boot/grub2/grub.cfg...\nMake sure you're running this script as root & try again...\n")

                    else:
                        print(Fore.RED + "\nFailed to chown root /boot/grub2/grub.cfg...\nMake sure you're running this script as root & try again...\n")
                
                else:
                    print(Fore.RED + "\nFailed to chmod 600 /boot/grub2/grub.cfg...\nMake sure you're running this script as root & try again...\n")
            
            else:
                print(Fore.RED + "\nFailed to locate : \n/boot/grub/grub.cfg\nOR\n/boot/grub2/grub.cfg\nProceeding to last attempt for /boot/grub/menu.lst...")
                # menu.lst
                # Try listing /boot/grub/menu.lst
                # If listing /boot/grub/ failed...
                menuPath = '/boot/grub/'
                menuLstPath = '/boot/grub/menu.lst'
                menuLstName = 'menu.lst'

                lsMenu = f'echo {sudo_password} | sudo ls -la {menuPath}'
                doLsMenu = subprocess.Popen(lsMenu, shell=True, text=True)
                doLsMenu.wait()

                if doLsMenu.returncode == 0:
                    print(Fore.YELLOW + "\nmenu.lst exists in /boot/grub/\nProceeding to hardening...\n")
                    # Hardening /boot/grub/menu.lst
                    menuChmod600 = f'echo {sudo_password} | sudo chmod 600 {menuLstPath}'
                    doMenuChmod600 = subprocess.Popen(menuChmod600, shell=True, text=True)
                    doMenuChmod600.wait()

                    if doMenuChmod600.returncode == 0:
                        print(Fore.YELLOW + "\nchmod 600 /boot/grub/menu.lst has succeeded!\nProceeding to chown root /boot/grub/menu.lst\n")
                        ## chown root /boot/grub/menu.lst
                        menuChown = f'echo {sudo_password} | sudo chown root {menuLstPath}'
                        doMenuChown = subprocess.Popen(menuChown, shell=True, text=True)
                        doMenuChown.wait()

                        if doMenuChown.returncode == 0:
                            print(Fore.YELLOW + "\nchown root /boot/grub/menu.lst has succeeded!\nProceeding to chgrp root /boot/grub/menu.lst\n")
                            ## chgrp root /boot/grub/menu.lst
                            menuChgrp = f'echo {sudo_password} | sudo chgrp root {menuLstPath}'
                            doMenuChgrp = subprocess.Popen(menuChgrp, shell=True, text=True)
                            doMenuChgrp.wait()

                            if doMenuChgrp.returncode == 0:
                                ##
                                print(Fore.YELLOW + "\nchgrp root /boot/grub/menu.lst has succeeded!\nProceeding to verify latest permissions for /boot/grub/menu.lst: ")
                                ##
                                print(Fore.YELLOW + "\nLatest /boot/grub/menu.lst permissions are: ")
                                #newPermission = os.system('ls -la /boot/grub/ | grep grub.cfg | awk \'{{print $1,$2,$3,$4}}\''.format(user))
                                readPermission3 = f'echo {sudo_password} | sudo ls -la {menuPath} | grep {menuLstName} | awk \'{{print $1,$2,$3,$4}}\''
                                doReadPermission3 = subprocess.run(readPermission3, shell=True, text=True, capture_output=True)
                                print(doReadPermission3.stdout)
                                
                                hardenedValue3 = re.match(regex, doReadPermission3.stdout)
                                # printing match object 
                                #print(hardenedValue) # span=(0,22)
                                # span=(start, end)
                                #print(hardenedValue.start()) #
                                if hardenedValue3.start() == 0:
                                    print(Fore.YELLOW + "\nHardening for /boot/grub/menu.lst has succeeded!\n")
                                else:
                                    print(Fore.RED + "\nFailed to harden /boot/grub/menu.lst...\nMake sure you're running this script as root & try again...\n")
                                ##
                            else:
                                print(Fore.RED + "\nFailed to chgrp root /boot/grub/menu.lst...\nMake sure you're running this script as root & try again...\n")
                        else:
                            print(Fore.RED + "\nFailed to chown root /boot/grub/menu.lst...\nMake sure you're running this script as root & try again...\n")
                    else:
                        print(Fore.RED + "\nFailed to chmod 600 /boot/grub/menu.lst...\nMake sure you're running this script as root & try again...\n")
                else:
                    print(Fore.RED + "\nCould not find any of following: \n/boot/grub2/grub.cfg\n/boot/grub/grub.cfg\n/boot/grub/menu.lst\nSkipping to harden 3.3.3 Boot Options...\n")
    else:
        print(Fore.WHITE + "\nNot gonna harden 3.3.3 Boot Options...\nSkipping...\n")






    

    
