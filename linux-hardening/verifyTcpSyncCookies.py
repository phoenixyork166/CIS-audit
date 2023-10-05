import os
from colorama import Fore, Back, Style
import subprocess
import getpass
import re

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
    confirm = input(Fore.WHITE + "\n[x] Do you wanna check 3.9.1.1 TCP Sync Cookies Protection in /etc/sysctl.conf[x] [y/N]: ")
    if confirm.lower() == "y":
        print(Fore.WHITE + "\nProceeding...\n")
        user = input(Fore.WHITE + "Running this script as: ")    
        sudo_password = getpass.getpass(prompt='Enter sudo password: ')

        kernelPath = '/etc/'
        confPath = '/etc/sysctl.conf'
        confName = 'sysctl.conf'
        hardenedValue = 'net.ipv4.tcp_syncookies=1'
        # print(Fore.WHITE + "\nHardened value as below: \n")
        # print(hardenedValue)

        print(Fore.YELLOW + "\nLocating kernel configuration file /etc/sysctl.conf...\n")
        lsSysctlConf = f'echo {sudo_password} | sudo ls -la {kernelPath} | grep {confName}'
        doLsSysctlConf = subprocess.Popen(lsSysctlConf, shell=True, text=True)
        doLsSysctlConf.wait()
        if doLsSysctlConf.returncode == 0:
            print(Fore.YELLOW + "\nLocating kernel configuration file /etc/sysctl.conf succeeded!\nProceeding to check current config...\n")

            readConf = f"echo {sudo_password} | sudo cat {confPath} | egrep '^\S*\s*net\.ipv4\.tcp\_syncookies\s*\=\s*\d*\s*'"
            doReadConf = subprocess.run(readConf, shell=True, text=True, capture_output=True)
            # Storing doReadConf standard output into another variable 'output'
            output = doReadConf.stdout
            # Trailing all whitespace after output
            output = output.strip()
            
            if doReadConf.returncode == 0:
                print(Fore.YELLOW + "\nChecking done!\nCurent config is as below: ")
                print(output)

                if output == hardenedValue:
                    print(Fore.YELLOW + "\nCurrent net.ipv4.tcp_syncookies value is compliant...\nSkipping...\n")
                else:
                    print(Fore.YELLOW + "\nHardened value is: \n")
                    print(hardenedValue)
                    print(Fore.YELLOW + "\nCurrent value is: \n")
                    print(output)
                    print(Fore.YELLOW + "\nCurrent net.ipv4.tcp_syncookies value is NOT compliant...\nProceeding...\n")


            else:
                print(Fore.RED + "\nFailed to check current net.ipv4.tcp_syncookies config...\nMake sure you're running this script as root & try again...\n")

        else:
            print(Fore.RED + "\nFailed to locate /etc/sysctl.conf...\nMake sure you're running this script as root & try again...\n")

    else:
        print(Fore.WHITE + "\nNot gonna harden 3.9.1.1 TCP Sync Cookies Protection in /etc/sysctl.conf...\nSkipping...\n")