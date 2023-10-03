# --------------
# Imports modules
# --------------
import os
import time
from colorama import Fore, Back, Style
import subprocess
import getpass

def addUser():

    # Adding a new privileged user
    addingUser = input(
        Fore.WHITE + "[x] Do you wanna add a privileged user? [x] (y/N): "
    )
    print(Style.RESET_ALL)

    if addingUser.lower() == "y": 
        thisTime = time.localtime(time.time())

        user = input("Running this script as: ")
        sudo_password = getpass.getpass(prompt='Please enter your sudo password: ')
        newUser = input("Enter new privileged user name: ")

        print(Fore.YELLOW + "Adding a new privileged user for you :)")
        #os.system('echo {sudo_password} | sudo adduser' + user)
        addPrivUser = f'sudo adduser {newUser}'
        doAddPrivUser = subprocess.Popen(addPrivUser, shell=True)
        doAddPrivUser.wait()

        if doAddPrivUser.returncode == 0:
            print(Fore.YELLOW + "\nAdding this new privileged user has succeeded at {thisTime}!\n")
            print(doAddPrivUser.stdout)
            print(Fore.YELLOW + "\nDone! Welcome {}\n".format(newUser))
            print(Style.RESET_ALL)

            # Adding 'user' to sudoers
            #addSudoer = os.system("sudo usermod -aG sudo " + user)
            print(Fore.WHITE + "\nAdding this new privileged user to Sudoers...")
            print(Style.RESET_ALL)
            addSudoer = f'echo {sudo_password} | sudo usermod -aG sudo {newUser}'
            doAddSudoer = subprocess.Popen(addSudoer, shell=True)
            doAddSudoer.wait()

            if doAddSudoer.returncode == 0:
                print(Fore.YELLOW + "\nAdding this privileged user to sudoers group is successful!\n")
                print(doAddSudoer.stdout)
                print(Style.RESET_ALL)

                # Allowing 'user' to run Bash
                print(Fore.YELLOW + "\nAdding this privileged user to Bash runner...\n")
                print(Style.RESET_ALL)
                #addBash = os.system("sudo chsh -s /bin/bash " + user)
                addBash = f'echo {sudo_password} | sudo chsh -s /bin/bash {newUser}'
                doAddBash = subprocess.Popen(addBash, shell=True)
                doAddBash.wait()

                if doAddBash.returncode == 0:
                    print(Fore.WHITE + "\nAdding this privileged user to Bash runner has succeeded!\n")
                    print(doAddBash.stdout)
                    print(Style.RESET_ALL)
                else:
                    print(Fore.RED + "Adding this privileged user to Bash runner failed :(")
                    print(doAddBash.stderr)
                    print(Style.RESET_ALL)
    
            else:
                print(Fore.RED + "Adding this privileged user to sudoers group failed :(")
                print(doAddSudoer.stderr)
                print(Style.RESET_ALL)
        
        else:
            print(Fore.RED + "\nFailed to add this new privileged user :(\n")
            print(doAddPrivUser.stderr)
            print(Style.RESET_ALL)
    else:
        print(Fore.WHITE + "\nNot gonna add a new privileged user...\nSkipping...\n")
    ###

    
