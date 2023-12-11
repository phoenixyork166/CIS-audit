import os
from colorama import Fore, Back, Style
import subprocess
import re
from . import user, sudo_password, distroName

# Linux Security in "General"
# 3.3 Boot Options
# 3.3.3 Grub
def verifyBootGrub():
    #confirm = input(Fore.WHITE + "\n[x] Do you wanna check 3.3.3 Boot Options for either of following: \n/boot/grub/grub.cfg\n/boot/grub2/grub.cfg\n/boot/grub/menu.lst\n[x] [y/N]: ")
    if user.lower() == "root":
        print(Fore.WHITE + "\nConfirmed you're ROOT\nProceeding...\n")
        
        prefixes = ['/boot/grub/', '/boot/efi/EFI/{distroName}/', '/boot/grub2/', '/etc/']
        configs = ['grub2.cfg', 'menu.lst', 'grub2.cfg']
        
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
                print(Fore.RED + "\nCurrent config is NOT compliant...\nProceeding to remediate...\n")
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
                                print(Fore.WHITE + "\nRemediation for /boot/grub/grub.cfg has succeeded!\n")
                            else:
                                print(Fore.RED + "\nFailed to remediate /boot/grub/grub.cfg...\nEnsure you entered a correct sudo password & try again...\n")
                        else:
                            print(Fore.RED + "\nFailed to chgrp root /boot/grub/grub.cfg...\nEnsure you entered a correct sudo password & try again...\n")
                    else:
                        print(Fore.RED + "\nFailed to chown root /boot/grub/grub.cfg...\nEnsure you entered a correct sudo password & try again...\n")
                else:
                    print(Fore.RED + "\nFailed to chmod 600 /boot/grub/grub.cfg...\nEnsure you entered a correct sudo password & try again...\n")
            else:                
                print(Fore.YELLOW + "\nCurrent config is compliant...\nSkipping remediation...\n")
        
        else:
            print(Fore.RED + "\ngrub.cfg does NOT exist in /boot/grub/\nProceeding to attempt for /boot/grub2/grub.cfg ...\n")

            grub2Path = '/boot/grub2/'
            grub2ConfPath = '/boot/grub2/grub.cfg'
            grub2CfgName = 'grub.cfg'

            # Grub2
            # Try listing /boot/grub2/ 
            # If listing /boot/grub2/ failed...
            lsGrub2 = f'echo {sudo_password} | sudo ls -la {grub2Path}'
            doLsGrub2 = subprocess.Popen(lsGrub2, shell=True, text=True)
            doLsGrub2.wait()

            # if /boot/grub2/grub.cfg can be located
            if doLsGrub2.returncode == 0:
                print(Fore.YELLOW + "\ngrub.cfg exists in /boot/grub2/\nProceeding to checking...\n")
                ##
                check2 = f'echo {sudo_password} | sudo ls -la {grub2Path} | grep {grub2CfgName} | awk \'{{print $1,$2,$3,$4}}\''
                doCheck2 = subprocess.run(check2, shell=True, text=True, capture_output=True)
                #print(doCheck.stdout)
                # Store output from doCheck stdout
                output2 = doCheck2.stdout
                # Trim whitespace
                output2 = output2.strip()
                print(output2)

                validate2 = re.search(regex, output2)
                print(validate2)
            
                print(Fore.YELLOW + "\nComparing current config to desired config...\n")
            
                if not validate2:
                    print(Fore.RED + "\nCurrent /boot/grub2/grub.cfg config is NOT compliant...\nProceeding to remediaton...\n")
                    ##
                    print(Fore.YELLOW + "\nchmod 600 /boot/grub2/grub.cfg in progress...\n")
                    grub2Chmod600 = f'echo {sudo_password} | sudo chmod 600 {grub2ConfPath}'
                    doGrub2Chmod600 = subprocess.Popen(grub2Chmod600, shell=True, text=True)
                    doGrub2Chmod600.wait()

                    if doGrub2Chmod600.returncode == 0:
                        print(Fore.YELLOW + "\nchmod 600 /boot/grub2/grub.cfg has succeeded!\nProceeding to chown root /boot/grub2/grub.cfg ...\n")
                        grub2Chown = f'echo {sudo_password} | sudo chown root {grub2ConfPath}'
                        doGrub2Chown = subprocess.Popen(grub2Chown, shell=True, text=True)
                        doGrub2Chown.wait()

                        if doGrub2Chown.returncode == 0:
                            print(Fore.YELLOW + "\nchown root /boot/grub2/grub.cfg has succeeded!\nProceeding to chgrp root /boot/grub2/grub.cfg\n")
                            grub2Chgrp = f'echo {sudo_password} | sudo chgrp root {grub2ConfPath}'
                            doGrub2Chgrp = subprocess.Popen(grubChgrp, shell=True, text=True)
                            doGrub2Chgrp.wait()

                            if doGrub2Chgrp.returncode == 0:
                                print(Fore.YELLOW + "\nchgrp root /boot/grub2/grub.cfg has succeeded!\nProceeding to verify latest permissions for /boot/grub2/grub.cfg: ")
                                print(Fore.YELLOW + "\nLatest /boot/grub2/grub.cfg permissions are: ")
                                readPermission2 = f'echo {sudo_password} | sudo ls -la {grub2Path} | grep {grub2CfgName} | awk \'{{print $1,$2,$3,$4}}\''
                                doReadPermission2 = subprocess.run(readPermission2, shell=True, text=True, capture_output=True)
                                doReadPermission2_output = doReadPermission2.stdout
                                # Trim whitespace
                                doReadPermission2_output = doReadPermission2_output.strip()
                                print(doReadPermission2_output)
                        
                                hardenedValue2 = re.match(regex, doReadPermission2_output)

                                if hardenedValue2.start() == 0:
                                    print(Fore.WHITE + "\nRemediation for /boot/grub2/grub.cfg has succeeded!\n")
                                else:
                                    print(Fore.RED + "\nFailed to remediate /boot/grub2/grub.cfg...\nEnsure you entered a correct sudo password & try again...\n")
                            else:
                                print(Fore.RED + "\nFailed to chgrp root /boot/grub2/grub.cfg...\nEnsure you entered a correct sudo password & try again...\n")
                        else:
                            print(Fore.RED + "\nFailed to chown root /boot/grub2/grub.cfg...\nEnsure you entered a correct sudo password & try again...\n")
                    else:
                        print(Fore.RED + "\nFailed to chmod 600 /boot/grub2/grub.cfg...\nEnsure you entered a correct sudo password & try again...\n")
                else:                
                    print(Fore.YELLOW + "\nCurrent config /boot/grub2/grub.cfg is compliant...\nSkipping remediation...\n")
            
            # if 
            # /boot/grub/grub.cfg
            # /boot/grub2/grub.cfg 
            # both cannot be located
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
                    print(Fore.YELLOW + "\nmenu.lst has been located in /boot/grub/\nProceeding to checking...\n")
                    ##
                    check3 = f'echo {sudo_password} | sudo ls -la {menuPath} | grep {menuLstName} | awk \'{{print $1,$2,$3,$4}}\''
                    doCheck3 = subprocess.run(check3, shell=True, text=True, capture_output=True)
                    #print(doCheck3.stdout)
                    # Store output from doCheck3 stdout
                    output3 = doCheck3.stdout
                    # Trim whitespace
                    output3 = output3.strip()
                    print(output3)

                    validate3 = re.search(regex, output3)
                    print(validate3)
            
                    print(Fore.YELLOW + "\nComparing current /boot/grub/menu.lst config to desired config...\n")
            
                    if not validate3:
                        print(Fore.RED + "\nCurrent /boot/grub/menu.lst config is NOT compliant...\nProceeding to remediation...\n")
                        ##
                        print(Fore.YELLOW + "\nchmod 600 /boot/grub/menu.lst in progress...\n")
                        menuLstChmod600 = f'echo {sudo_password} | sudo chmod 600 {menuLstPath}'
                        doMenuLstChmod600 = subprocess.Popen(menuLstChmod600, shell=True, text=True)
                        doMenuLstChmod600.wait()

                        if doMenuLstChmod600.returncode == 0:
                            print(Fore.YELLOW + "\nchmod 600 /boot/grub/menu.lst has succeeded!\nProceeding to chown root /boot/grub/menu.lst ...\n")
                            menuLstChown = f'echo {sudo_password} | sudo chown root {menuLstPath}'
                            doMenuLstChown = subprocess.Popen(menuLstChown, shell=True, text=True)
                            doMenuLstChown.wait()

                            if doMenuLstChown.returncode == 0:
                                print(Fore.YELLOW + "\nchown root /boot/grub/menu.lst has succeeded!\nProceeding to chgrp root /boot/grub/menu.lst\n")
                                menuLstChgrp = f'echo {sudo_password} | sudo chgrp root {menuLstPath}'
                                doMenuLstChgrp = subprocess.Popen(menuLstChgrp, shell=True, text=True)
                                doMenuLstChgrp.wait()

                                if doMenuLstChgrp.returncode == 0:
                                    print(Fore.YELLOW + "\nchgrp root /boot/grub/menu.lst has succeeded!\nProceeding to verify latest permissions for /boot/grub/menu.lst: ")
                                    print(Fore.YELLOW + "\nLatest /boot/grub/menu.lst permissions are: ")
                                    readPermission3 = f'echo {sudo_password} | sudo ls -la {menuPath} | grep {menuLstName} | awk \'{{print $1,$2,$3,$4}}\''
                                    doReadPermission3 = subprocess.run(readPermission3, shell=True, text=True, capture_output=True)
                                    doReadPermission3_output = doReadPermission3.stdout
                                    doReadPermission3_output = doReadPermission3_output.strip()
                                    print(doReadPermission3_output)
                        
                                    hardenedValue3 = re.match(regex, doReadPermission3_output)

                                    if hardenedValue3.start() == 0:
                                        print(Fore.YELLOW + "\nRemediation for /boot/grub/menu.lst has succeeded!\n")
                                    else:
                                        print(Fore.RED + "\nFailed to harden /boot/grub/menu.lst...\nEnsure you entered a correct sudo password & try again...\n")
                                else:
                                    print(Fore.RED + "\nFailed to chgrp root /boot/grub/menu.lst...\nEnsure you entered a correct sudo password & try again...\n")
                            else:
                                print(Fore.RED + "\nFailed to chown root /boot/grub/menu.lst...\nEnsure you entered a correct sudo password & try again...\n")
                        else:
                            print(Fore.RED + "\nFailed to chmod 600 /boot/grub/menu.lst...\nEnsure you entered a correct sudo password & try again...\n")
                    else:                
                        print(Fore.YELLOW + "\nCurrent /boot/grub/menu.lst config is compliant...\nSkipping remediation...\n")
                    ##
                else:
                    print(Fore.RED + "\nCould not find any of following: \n/boot/grub2/grub.cfg\n/boot/grub/grub.cfg\n/boot/grub/menu.lst\nSkipping to remediate 3.3.3 Boot Options...\n")
    else:
        print(Fore.WHITE + "Not ROOT\nNot gonna check 3.3.3 Boot Options...\nSkipping...\n")






    

    
