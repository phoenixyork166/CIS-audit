from . import user, sudo_password, distroName, initializeModules, Fore, os, Back, Style, getpass, subprocess, re

# Linux Security in "General"
# 3.3 Boot Options
# 3.3.3 Grub
def verifyBootGrub():
    #confirm = input(Fore.WHITE + "\n[x] Do you wanna check 3.3.3 Boot Options for either of following: \n/boot/grub/grub.cfg\n/boot/grub2/grub.cfg\n/boot/grub/menu.lst\n[x] [y/N]: ")
    if user.lower() == "root":
        print(Fore.WHITE + "\nConfirmed you're ROOT\nProceeding...\n")
        
        prefixes = ['/boot/efi/EFI/'+distroName+'/', '/boot/grub/', '/boot/grub2/', '/etc/']
        configs = ['grub2.cfg', 'menu.lst', 'grub.cfg']
        
        regex = "^-rw-------\s+\d+\s+root\s+root$"
        #hardenedValue = re.search("(-rw-------)\s+\d+\s+(root)\user = input(Fore.WHITE + "Running this script as: ")    

        for prefix in prefixes:
            for config in configs:

                lsGrub = f'echo {sudo_password} | sudo ls -la {prefix}{config}'
                doLsGrub = subprocess.run(lsGrub, shell=True, text=True, capture_output=True)

                if doLsGrub.returncode == 0:
                    print(Fore.WHITE + f"\n{config} exists in {prefix}\n\nProceed to checking current config...\n")

                    check = f'echo {sudo_password} | sudo ls -la {prefix}{config} | awk \'{{print $1,$2,$3,$4}}\''
                    doCheck = subprocess.run(check, shell=True, text=True, capture_output=True)
                    print(doCheck.stdout)

                    validate = re.search(regex, doCheck.stdout)
                    print(validate)

                    ###
                    if not validate:
                        print(Fore.RED + "\nCurrent config is NOT compliant...\nProceeding to remediate...\n")
                        ##
                        print(Fore.YELLOW + f'\nchmod 600 {prefix}{config} in progress...\n')
                        grubChmod600 = f'echo {sudo_password} | sudo chmod 600 {prefix}{config}'
                        doGrubChmod600 = subprocess.Popen(grubChmod600, shell=True, text=True)
                        doGrubChmod600.wait()

                        if doGrubChmod600.returncode == 0:
                            print(Fore.YELLOW + f'\nchmod 600 {prefix}{config} has succeeded!\nProceeding to chown root {prefix}{config} ...\n')
                            grubChown = f'echo {sudo_password} | sudo chown root {prefix}{config}'
                            doGrubChown = subprocess.Popen(grubChown, shell=True, text=True)
                            doGrubChown.wait()

                            if doGrubChown.returncode == 0:
                                print(Fore.YELLOW + f'\nchown root {prefix}{config} has succeeded!\nProceeding to chgrp root {prefix}{config}\n')
                                grubChgrp = f'echo {sudo_password} | sudo chgrp root {prefix}{config}'
                                doGrubChgrp = subprocess.Popen(grubChgrp, shell=True, text=True)
                                doGrubChgrp.wait()

                                if doGrubChgrp.returncode == 0:
                                    print(Fore.YELLOW + f'\nchgrp root {prefix}{config} has succeeded!\nProceeding to verify latest permissions\n')
                                    print(Fore.YELLOW + f'\nLatest {prefix}{config} permissions are: ')
                                    readPermission = f'echo {sudo_password} | sudo ls -la {prefix}{config} | awk \'{{print $1,$2,$3,$4}}\''
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
                    ###
                else:
                    print(Fore.RED + f"\nFailed to locate {config} in {prefix}...\nSkipping...\n")
    else:
        print(Fore.RED + "You aren't ROOT\nTerminating...\n")




    

    
