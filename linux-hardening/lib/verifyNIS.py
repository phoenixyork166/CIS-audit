from . import user, sudo_password, distroName, initializeModules, Fore, sys, os, Back, Style, getpass, subprocess, re
# Import module specific variables
from . import thisTime

def verifyNIS():

    print(Fore.WHITE + f'=============================================================================')
    print(Fore.WHITE + f'===================2. Verifying NIS server is NOT running====================')
    print(Fore.WHITE + f'=============================================================================')
    print(Fore.WHITE + f'\n\nHi {user}\nProceeding to verify NIS server settings...\n')

    prefix = '/etc/'
    config = 'ypserv.conf'
    service = 'ypserv'

    # 1. Trying to locate /etc/ypserv.conf
    lsYpserv = f'echo {sudo_password} | sudo ls -la {prefix}{config}'
    doLsYpserv = subprocess.run(lsYpserv, shell=True, text=True, capture_output=True)

    if doLsYpserv.returncode == 0:
        print(Fore.RED + f'\n\nSucceeded in locating {prefix}{config} at:{thisTime}\nThis is a non-compliance!\nForce removing {prefix}{config}...\n')
        rmYpservConf = f'echo {sudo_password} | sudo rm -rf {prefix}{config}'
        doRmYpservConf = subprocess.run(rmYpservConf, shell=True, text=True, capture_output=True)

        if doRmYpservConf.returncode == 0:
            print(Fore.YELLOW + f'\n\nSucceeded in removing {prefix}{config} at:\n{thisTime}\nProceeding to Force-stop ypserv service\n')
            stopYpserv = f'echo {sudo_password} | sudo systemctl stop {service}'
            doStopYpserv = subprocess.run(stopYpserv, shell=True, text=True, capture_output=True)
            if doStopYpserv.returncode == 0:
                print(Fore.YELLOW + f'\n\nSucceeded in stopping service: {service} at:\n{thisTime}\nNIS server settings become compliant!\n')
            else:
                print(Fore.RED + f'\n\nFailed to stop NIS server service: {service} at:\n{thisTime}\n')
                print(Fore.RED + f'\n\nYou should always disable & stop NIS server service from running\nUse LDAP or Kerberoes instead!\n')
        else:
            print(Fore.RED + f'\n\nFailed to remove NIS service config file: {prefix}{config} at:\n{thisTime}\nYou should manually remove {prefix}{config} & manually stop NIS server service: {service}\nby sudo systemctl stop ypserv!\n')
            ###
            stopYpserv = f'echo {sudo_password} | sudo systemctl stop {service}'
            doStopYpserv = subprocess.run(stopYpserv, shell=True, text=True, capture_output=True)

            if doStopYpserv.returncode == 0:
                print(Fore.YELLOW + f'\n\nSucceeded in stopping service: {service} at:\n{thisTime}\nNIS server settings has become compliant!\n')
            else:
                print(Fore.RED + f'\n\nFailed to stop NIS server service: {service} at:\n{thisTime}')
                print(Fore.RED + f'\n\nYou should always disable & stop NIS server service from running\nUse LDAP or Kerberoes instead!\n')
                ###    

    else:
        print(Fore.YELLOW + f'\n\nNIS server settings seems to be compliant as I have failed to locate NIS server service config: {prefix}{config} at:\n{thisTime}\nProceeding to check whether NIS server service: {service} is running...\n')
        checkYpserv = f'echo {sudo_password} | sudo systemctl stop {service}'
        doCheckYpserv = subprocess.run(checkYpserv, shell=True, text=True, capture_output=True)
        if doCheckYpserv.returncode == 5:
            print(Fore.YELLOW + f'\n\nSucceeded in confirming that Unit {service}.service could not be found at:\n{thisTime}\nNIS server settings is compliant!\n')
        else:
            print(Fore.YELLOW + f'\n\nFailed to confirm whether NIS server service: {service} is NOT running!\nAs \'systemctl stop {service}\' has NOT returned exit code of 5!\nForce stopping NIS server service: {service} again!\n')
            stopYpserv = f'echo {sudo_password} | sudo systemctl stop {service}'
            doStopYpserv = subprocess.run(stopYpserv, shell=True, text=True, capture_output=True)
            if doStopYpserv.returncode == 5:
                print(Fore.YELLOW + f'\n\nSucceeded in stopping service: {service} at:\n{thisTime}\nNIS server settings has become compliant!\n')
            else:
                print(Fore.RED + f'\n\nFailed to stop NIS server service: {service} twice at:\n{thisTime}\nPlease confirm that {service} is NOT running')
                print(Fore.RED + f'\n\nYou should always disable & stop NIS server service from running...\nUse LDAP or Kerberoes instead!\n')
