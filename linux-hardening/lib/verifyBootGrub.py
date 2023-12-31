from . import user, sudo_password, distroName, initializeModules, Fore, sys, os, Back, Style, getpass, subprocess, re
# Import module specific variables
from . import thisTime

# Linux Security in "General"
# 3.3 Boot Options
# 3.3.3 Grub
def verifyBootGrub():
    
    print(Fore.WHITE + f'=============1. Verifying Linux Grub Boot options ===============')

    prefixes = ['/boot/efi/EFI/'+distroName+'/', '/boot/grub/', '/boot/grub2/', '/etc/']
    configs = ['grub2.cfg', 'menu.lst', 'grub.cfg']
        
    regex = '^-rw-------\s+\d+\s+root\s+root$'
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

                validate = re.match(regex, doCheck.stdout)
                print(validate)

                ###
                if not validate:
                    print(Fore.RED + f'\nCurrent config: {prefix}{config} is NOT compliant...\nProceeding to remediate...\n')
                    ##
                    print(Fore.YELLOW + f'\nchmod 600 {prefix}{config} in progress...\n')
                    grubChmod600 = f'echo {sudo_password} | sudo chmod 600 {prefix}{config}'
                    doGrubChmod600 = subprocess.Popen(grubChmod600, shell=True, text=True)
                    doGrubChmod600.wait()

                    if doGrubChmod600.returncode == 0:
                        print(Fore.YELLOW + f'\n\nSucceeded in chmod 600 {prefix}{config} at:\n{thisTime}\nProceeding to chown root {prefix}{config} ...\n')
                        grubChown = f'echo {sudo_password} | sudo chown root {prefix}{config}'
                        doGrubChown = subprocess.Popen(grubChown, shell=True, text=True)
                        doGrubChown.wait()

                        if doGrubChown.returncode == 0:
                            print(Fore.YELLOW + f'\n\nSucceeded in chown root {prefix}{config} at:\n{thisTime}\nProceeding to chgrp root {prefix}{config}\n')
                            grubChgrp = f'echo {sudo_password} | sudo chgrp root {prefix}{config}'
                            doGrubChgrp = subprocess.Popen(grubChgrp, shell=True, text=True)
                            doGrubChgrp.wait()

                            if doGrubChgrp.returncode == 0:
                                print(Fore.YELLOW + f'\n\nSucceeded in chgrp root {prefix}{config} at:\n{thisTime}\nProceeding to verify latest permissions\n')
                                print(Fore.YELLOW + f'\n\n\nLatest {prefix}{config} permissions are: ')
                                readPermission = f'echo {sudo_password} | sudo ls -la {prefix}{config} | awk \'{{print $1,$2,$3,$4}}\''
                                doReadPermission = subprocess.run(readPermission, shell=True, text=True, capture_output=True)
                                doReadPermission_output = doReadPermission.stdout
                                doReadPermission_output = doReadPermission_output.strip()
                                print(doReadPermission_output)
                                    
                                hardenedValue = re.match(regex, doReadPermission_output)
                                # If hardenedValue match regex => Remediation succeeded
                                if hardenedValue:
                                    print(Fore.WHITE + f'\n\nSucceeded in remediating {prefix}{config} at:\n{thisTime}\n')
                                else:
                                    print(Fore.RED + f'\n\nFailed to remediate {prefix}{config} at:\n{thisTime}\nMake sure you\'re root & try again...\n')
                            else:
                                print(Fore.RED + f'\n\nFailed to chgrp root {prefix}{config} at:{thisTime}\nMake sure you\'re root & try again...\n')
                        else:
                            print(Fore.RED + f'\n\nFailed to chown root {prefix}{config} at:\n{thisTime}\nMake sure you\'re root & try again...\n')
                    else:
                        print(Fore.RED + f'\n\nFailed to chmod 600 {prefix}{config} at:\n{thisTime}\nMake sure you\'re root & try again...\n')
                else:                
                    print(Fore.WHITE + f'\n\nCurrent config: {prefix}{config} is compliant...\nSkipping remediation...\n')
                    ###
            else:
                print(Fore.RED + f'\n\nFailed to locate any {config} in {prefix} at:\n{thisTime}\nSkipping...\n')





    

    
