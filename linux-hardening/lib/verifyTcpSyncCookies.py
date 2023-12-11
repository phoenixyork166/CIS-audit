from . import user, sudo_password, distroName, initializeModules, Fore, os, Back, Style, getpass, subprocess, re

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
    
    if user.lower() == "root":
        prefix = '/etc/'
        confName = 'sysctl.conf'
        confPath = f'{prefix}{confName}'        
        hardenedValue = 'net.ipv4.tcp_syncookies=1'
        # print(Fore.WHITE + "\nHardened value as below: \n")
        # print(hardenedValue)

        print(Fore.YELLOW + "\nLocating kernel configuration file /etc/sysctl.conf...\n")
        lsSysctlConf = f'echo {sudo_password} | sudo ls -la {prefix} | grep {confName}'
        doLsSysctlConf = subprocess.Popen(lsSysctlConf, shell=True, text=True)
        doLsSysctlConf.wait()
        # if /etc/sysctl.conf can be located
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
                    print(Fore.YELLOW + "\nDesired config value is: \n")
                    print(hardenedValue)
                    print(Fore.YELLOW + "\nCurrent value is: \n")
                    print(output)
                    print(Fore.YELLOW + "\nCurrent net.ipv4.tcp_syncookies value is NOT compliant...\nProceeding to remediate...\n")

                    remediate = f"echo {sudo_password} | sudo sed -i 's/{output}/{hardenedValue}/g' {confPath};"
                    doRemediate = subprocess.run(remediate, shell=True, text=True, capture_output=True)
                    print(doRemediate.stdout)

                    if doRemediate.returncode == 0:
                        print(Fore.YELLOW + "\nRemediation for setting kernel config /etc/sysctl.conf\nnet.ipv4.tcp_syncookies=1\nhas succeeded!\nProceeding to check against desired value...\n")
                        check = f"echo {sudo_password} | sudo cat {confPath} | egrep '^\S*\s*net\.ipv4\.tcp\_syncookies\s*\=\s*\d*\s*'"
                        doCheck = subprocess.run(check, shell=True, text=True, capture_output=True)
                        output2 = doCheck.stdout
                        output2 = output2.strip()
                        print(Fore.YELLOW + "\nCurrent net.ipv4.tcp_syncookies value in /etc/sysctl.conf is: \n")
                        print(output2)

                        if output2 == hardenedValue:
                            print(Fore.WHITE + "\nCurrent net.ipv4.tcp_syncookies has become compliant!\nRemediation for 3.9.1.1 Verify TCP SYNC Cookies Protection is Enabled\nnet.ipv4.tcp_syncookies=1\nhas succeeded!\n")
                        else:
                            print(Fore.RED + "\nFailed to remediate net.ipv4.tcp_syncookies value...\nMake sure correct sudo password is entered & try again...\n")
                    else:
                        print(Fore.RED + "\nFailed to remediate kernel config /etc/sysctl.conf\nnet.ipv4.tcp_syncookies=1\nMake sure correct sudo password is entered & try again...\n")

            else:
                print(Fore.RED + "\nFailed to check current net.ipv4.tcp_syncookies config...\nMake sure you're running this script as root & try again...\n")

        else:
            print(Fore.RED + "\nFailed to locate /etc/sysctl.conf...\nMake sure you're running this script as root & try again...\n")

    else:
        print(Fore.WHITE + "\nNot gonna harden 3.9.1.1 TCP Sync Cookies Protection in /etc/sysctl.conf...\nSkipping...\n")