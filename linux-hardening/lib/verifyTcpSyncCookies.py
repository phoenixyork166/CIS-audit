from . import user, sudo_password, distroName, initializeModules, Fore, sys, os, Back, Style, getpass, subprocess, re
# Import module specific variables
from . import thisTime

# 3.9 Security Features in the Kernel
# 3.9.1 Enable TCP SYN Cookie Protection (default in SUSE Linux Enterprise Server11)
# 3.9.1.1 Verify TCP SYNC Cookies Protection is Enabled
# SYNC attack = Denial of Service (DoS) attack consuming resources on linux system forcing it to reboot
# DoS is initiated by establishing a TCP connection handshake (sending SYNC packet requests from client)
# To your System
# Then never completing the TCP handshake process to open the TCP connection
# Leaving large numbers of half-open connections 
# Which is a fairly simple attack that should be protect against

# config = cat /etc/sysctl.conf | egrep '^net.ipv4.tcp\_syncookies'

def verifyTcpSyncCookies():
    
    print(Fore.WHITE + f'==========3. Verifying Security features in Linux Kernel ================')
    print(Fore.WHITE + f'==========3.9.1 Verifying TCP Syn Cookie Protection is Enabled ==================')
    
    # sysctl.conf prefix & config name
    prefix = '/etc/'
    confName = 'sysctl.conf'
    confPath = f'{prefix}{confName}'        
    hardenedValue = 'net.ipv4.tcp_syncookies=1'
    regex = '^\s*net\.ipv4\.tcp\_syncookies\s*=\s*1$'
    # print(Fore.WHITE + "\nHardened value as below: \n")
    # print(hardenedValue)

    print(Fore.YELLOW + f'\nLocating kernel configuration file {prefix}{confName}...\n')
    lsSysctlConf = f'echo {sudo_password} | sudo ls -la {prefix} | grep {confName}'
    doLsSysctlConf = subprocess.Popen(lsSysctlConf, shell=True, text=True)
    doLsSysctlConf.wait()
    # if /etc/sysctl.conf can be located
    if doLsSysctlConf.returncode == 0:
        print(Fore.YELLOW + f'\n\nSucceeded in locating kernel configuration file {prefix}{confName} at:\n{thisTime}\nProceeding to check current config...\n')

        readConf = f"echo {sudo_password} | sudo cat {confPath} | egrep '^\S*\s*net\.ipv4\.tcp\_syncookies\s*'"
        doReadConf = subprocess.run(readConf, shell=True, text=True, capture_output=True)
        # Storing doReadConf standard output into another variable 'output'
        output = doReadConf.stdout
        # Trailing all whitespace after output
        output = output.strip()
            
        if doReadConf.returncode == 0:
            print(Fore.YELLOW + f'\nChecking was done at:\n{thisTime}\nCurent config is as below: \n')
            print(output)

            if output == hardenedValue:
                print(Fore.YELLOW + f'\nCurrent net.ipv4.tcp_syncookies value is compliant...\nSkipping...\n')
            else:
                print(Fore.RED + f'\nCurrent net.ipv4.tcp_syncookies value is NOT compliant at:\n{thisTime}\nProceeding to remediate...\n')
                print(Fore.RED + f'\nDesired config value for {prefix}{confName} is: \n')
                print(Fore.YELLOW + hardenedValue)
                print(Fore.RED + f'\nWherease current value for {prefix}{confName} is: \n')
                print(Fore.YELLOW + output)

                remediate = f"echo {sudo_password} | sudo sed -i 's/{output}/{hardenedValue}/g' {confPath};"
                doRemediate = subprocess.run(remediate, shell=True, text=True, capture_output=True)
                print(doRemediate.stdout)

                if doRemediate.returncode == 0:
                    print(Fore.YELLOW + f'\nSucceeded in remediating {prefix}{confName}\nnet.ipv4.tcp_syncookies=1 at:\n{thisTime}\nProceeding to check against desired value...\n')
                    check = f"echo {sudo_password} | sudo cat {confPath} | egrep '^\S*\s*net\.ipv4\.tcp\_syncookies\s*'"
                    doCheck = subprocess.run(check, shell=True, text=True, capture_output=True)
                    output2 = doCheck.stdout
                    output2 = output2.strip()
                    print(Fore.YELLOW + f'\nCurrent net.ipv4.tcp_syncookies value in {prefix}{confName} is: \n')
                    print(output2)

                    if output2 == hardenedValue:
                        print(Fore.WHITE + f'\nCurrent net.ipv4.tcp_syncookies has become compliant!\nSucceeded in remediating 3.9.1.1 Verify TCP SYNC Cookies Protection at:\n{thisTime}\nnet.ipv4.tcp_syncookies=1\nhas succeeded!\n')
                    else:
                        print(Fore.RED + f'\nFailed to remediate net.ipv4.tcp_syncookies value in {prefix}{confName} at:\n{thisTime}\nMake sure you\'re root & try again...\n')
                else:
                    print(Fore.RED + f'\nFailed to remediate kernel config /etc/sysctl.conf\nnet.ipv4.tcp_syncookies=1 at:\n{thisTime}\nMake sure you\'re root & try again...\n')

        else:
            print(Fore.RED + f'\nFailed to check current net.ipv4.tcp_syncookies config at:\n{thisTime}\nMake sure you\'re running this script as root & try again...\n')

    else:
        print(Fore.RED + f'\nFailed to locate {prefix}{confName} at:\n{thisTime}\nMake sure you\'re running this script as root & try again...\n')