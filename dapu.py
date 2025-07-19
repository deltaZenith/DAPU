#!/usr/bin/env python3
# Copyright (C) 2025 deltaZenith
# This file is part of DAPU
# DAPU is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import subprocess
import shutil
import os
import logging
user = str(os.environ.get("SUDO_USER"))
pm=""
ext_list=False
supported_pms=["pacman", "apt", "dnf", "zypper"]
supported_aurhelpers=["yay", "paru"]
options=["Install packages", "Update the system", "Remove a package", "List installed packages", "Search for a package in the repos", "Clear the package cache", "Advanced options", "Exit"]
adv_options=["Mark a package"]
commands={
        "pacman":{"install":["pacman", "-S"], "update":["pacman", "-Syu"], "remove":["pacman", "-Rns"], "query":["pacman", "-Q"], "search":["pacman", "-Ss"], "cache":["pacman", "-Sc"], "mark":["pacman", "-D", "--asexplicit"]},
        "apt-get":{"install":["apt-get", "install"], "update":["apt-get", "update"], "upgrade":["apt-get", "upgrade"] ,"remove":["apt-get", "purge", "--autoremove"], "query":["apt", "list", "--installed"], "search": ["apt", "search"], "cache":["apt-get", "autoclean"], "rm_unneeded":["apt-get", "autoremove"], "mark":["apt-mark", "manual"], "sys-up":["apt-get", "dist-upgrade"]},
        "dnf":{"install":["dnf", "install"], "update":["dnf", "upgrade"], "remove":["dnf", "remove"], "query":["dnf", "list", "--installed"], "search":["dnf", "search"], "cache":["dnf", "clean", "all"], "rm_unneeded":["dnf", "autoremove"], "mark":["dnf", "mark", "user"]},
        "zypper":{"install":["zypper", "install"], "update":["zypper", "dup"], "remove":["zypper", "remove", "--clean-deps"], "query":["zypper", "se", "-si"], "search":["zypper", "search"], "cache":["zypper", "clean",], "mark":["zypper", "in", "-f"]}
        }

def check_euid():
    if os.geteuid()==0:
        pass
    else:
        exit("You need elevated (sudo) privileges to run this program.")
def init_logs():
    os.makedirs("/var/log/dapu", exist_ok=True)
    logging.basicConfig(filename="/var/log/dapu/dapu.log", format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

def check_pm():
    global pm
    if shutil.which("pacman"):
        pm="pacman"
    elif shutil.which("apt-get"):
        pm="apt-get"
    elif shutil.which("dnf"):
        pm="dnf"
    elif shutil.which("zypper"):
        pm="zypper"
    else:
        subprocess.run(["clear"])
        exit(f"Your package manager isn't supported. The supported package managers are: {supported_pms}")
    logging.info(f" Detected package manager: {pm}")
   
def check_opensuseleap():
    global leap
    try:
        leap = subprocess.run(["grep", "Leap", "-m1", "-o", "-q", "/etc/os-release"], check=True)
    except subprocess.CalledProcessError:
        leap=False

def list_options():  
    print("=================DAPU==================")
    for i, item in enumerate(options):
        print(i+1, ")", item)
    print("=======================================")
def check_aur():
    global aurhelper
    if shutil.which("paru"):
        aurhelper="paru"
    elif shutil.which("yay"):
        aurhelper="yay"
    else:
        aurhelper="none"
        setup_aur=input("No AUR helper was found would you like to set one up? [y/n] ")
        if setup_aur == "y":
            subprocess.run(["sudo", "-u", user, "/usr/local/bin/dapu.d/aur-setup.sh"])
            logging.info("Ran bash script to install AUR helper.")
            if shutil.which("paru"):
                aurhelper="paru"
            elif shutil.which("yay"):
                aurhelper="yay"
    logging.info(f"Detected AUR helper: {aurhelper}")
 
def pm_specific_adv_options():
    global ext_list
    if not ext_list:
        if pm != "zypper":
            adv_options.append("Remove unneeded packages")
        if pm == "pacman":
            adv_options.extend(["Install from the AUR", "Update AUR packages", "Search for an AUR package", "Clear system and/or AUR packages"])
        elif pm=="apt-get":
            adv_options.extend(["Full system upgrade", "Reconfigure all packages", "Fix broken dependencies"])
        elif pm=="dnf":
            adv_options.extend(["Full system upgrade", "Minimal update", "Downgrade a package"])
        elif pm=="zypper":
            if check_opensuseleap() == True:
                adv_options.append("System upgrade")
        adv_options.append("Go back")
        ext_list=True

def list_adv_options():  
    print("============ADVANCED OPTIONS=============")
    for i, item in enumerate(adv_options):
        print(i+1, ")", item)
    print("=========================================")

def adv_menu():
    global ext_list
    pm_specific_adv_options()
    if pm == "pacman":
        check_aur()
    while True:
        list_adv_options()
        command=input(f"What do you want to do? (1-{str(len(adv_options))}) ")
        if command == str(len(adv_options)):
            break
        elif command == "1":
            pkg=input("Enter the name of the package to mark as user-installed: ").lower()
            confirm=(f"The package '{pkg}' will be marked as user-installed, do you wish to continue? [y/n] ")
            subprocess.run(commands[pm]["mark"]+[pkg])
            logging.info(f" Ran: {' '.join(commands[pm]['mark'] + [pkg])}")
        elif command == "1":
            confirm=input("All uneeded packages will be removed, do you wish to continue? [y/n] ")
            if pm == "pacman":
                unneeded=subprocess.run(["pacman", "-Qtdq"], capture_output=True, text=True)
                pkg=unneeded.stdout.splitlines()
                subprocess.run(["pacman", "-Rns"]+pkg)
            else:
                subprocess.run(commands[pm]["rm_unneeded"])
            print("========UNNEEDED PACKAGES REMOVED=========")
        elif command == "3":
            if pm == "pacman":
                pkg=input("Which AUR package would you like to install? ").lower()
                confirm =input(f"The package '{pkg}' will be installed, do you wish to continue? [y/n] ")
                if confirm == "y":
                    subprocess.run(["sudo", "-u", user ,aurhelper, "-S", pkg])
                    logging.info(f"Ran: {aurhelper} -S {pkg}")
                    print("=========INSTALLATION COMPLETED=========")
            elif pm == "apt-get":
                confirm=input("A full system upgrade will be run, do you wish to continue? [y/n] ")
                if confirm =="y":
                    subprocess.run(commands[pm]["update"])
                    logging.info(f" Ran: {' '.join(commands[pm]['update'])}")
                    subprocess.run(commands[pm]["sys-up"])
                    logging.info(f" Ran: {' '.join(commands[pm]['sys-up'])}")
                    print("=========SYSTEM UPDATE COMPLETED=========")
            elif pm == "dnf":
                confirm=input("The integrity of all install packages will be checked, do you wish to continue? [y/n] ")
                if confirm == "y":
                    subprocess.run(["dnf", "check"])
                    print("=========SYSTEM UPDATE COMPLETED=========")
            elif pm == "zypper" and check_opensuseleap():
                confirm=input("A full system upgrade will be run, do you wish to continue? [y/n] ")
                if confirm == "y":
                    subprocess.run(commands[pm]["update"])
                    logging.info(f" Ran: {' '.join(commands[pm]['upgrade'])}")
        elif command == "4":
            if pm == "pacman":
                confirm=input("The system and AUR packages will be updated, continue? [y/n] ")
                if confirm == "y":
                    print("Updating...")
                    subprocess.run(["sudo", "-u", user, aurhelper])
                    logging.info(f"Ran: {aurhelper}")
                    print("============UPDATE COMPLETED============")
            elif pm == "apt-get":
                confirm=input("All packages will be reconfigured, do you wish to continue? [y/n] ")
                if confirm == "y":
                    subprocess.run(["dpkg --configure", "-a"])
                    logging.info("Ran: dpkg --configure -a")
            elif pm == "dnf":
                confirm=input("A minimal update will be run, do you wish to continue? [y/n] ")
                if confirm == "y":
                    subprocess.run(["dnf", "upgrade-minimal"])
                    print("========MINIMAL UPDATE COMPLETED========")
        elif command == "5":
            if pm =="pacman":
                pkg=input("Which package would you like to search for? ").lower()
                print("==================RESULTS================")
                subprocess.run(["sudo", "-u", user, aurhelper, "-Ss", pkg])
                logging.info(f"Ran: {aurhelper} -Ss {pkg}")
            elif pm == "apt-get":
                confirm=input("APT will try to fix broken dependencies, do you wish to continue? [y/n] ")
                if confirm == "y":
                    subprocess.run(["apt-get", "--fix-broken", "install"])
                    logging.info("Ran: apt-get --fix-broken install")
            elif pm == "dnf":
                pkg=input("Enter the name of the package you want to downgrade ")
                confirm=input(f"The package '{pkg}' will be downgraded, do you wish to continue? [y/n] ")
                if confirm=="y":
                    subprocess.run(["dnf", "downgrade", pkg])
                    logging.info(f"Ran: dnf downgrade {pkg} ")
                    print("===========DOWNGRADE COMPLETED===========")
        elif command == "6":
            if pm=="pacman":
                confirm=input("The system and/or AUR packages' cache will be cleaned, do you wish to continue? [y/n] ")
                subprocess.run([aurhelper, "-Sc"])
                logging.info(f"Ran {aurhelper} -Sc")

        else:
            print("Invalid Option")
def main():
    command=input(f"What do you want to do? (1-{str(len(options))}) ")
    print("=======================================") 
    if command=="1":
        pkg=input("Enter the name of the package to install: ").lower()
        confirm = input(f"The package '{pkg}' will be installed, do you wish to continue? [y/n] ")
        if confirm == "y":
            print("Installing", pkg,"...")
            subprocess.run(commands[pm]["install"]+[pkg])
            logging.info(f" Ran: {' '.join(commands[pm]['install'] + [pkg])}")
            print("==========INSTALLATION COMPLETED==========")
        else:
            pass
    elif command=="2":
        confirm = input("The system will be updated, do you wish to continue? [y/n] ")
        if confirm == "y":
            print("Updating the system...")
            if pm=="zypper":
                check_opensuseleap()
                if leap:
                    subprocess.run(["zypper", "up", "-y"])
                    logging.info(" Ran: zypper up -y")
                    print("========UPDATE COMPLETED========")
                else:
                    pass
            else:
                subprocess.run(commands[pm]["update"])
                logging.info(f" Ran: {' '.join(commands[pm]['update'])}")
                if pm == "apt-get":
                    subprocess.run(commands[pm]["upgrade"])
                    logging.info(f" Ran: {' '.join(commands[pm]['upgrade'])}")
            print("========UPDATE COMPLETED========")
        else:
            pass
    elif command=="3":
        pkg=input("Enter the name of the package to remove: ").lower()
        try:
            confirm = input(f"The package '{pkg}' will be removed, do you wish to continue? [y/n] ")
            if confirm == "y":
                print("Removing", pkg, "...")
                subprocess.run(commands[pm]["remove"]+[pkg])
                logging.info(f" Ran: {' '.join(commands[pm]['remove'] + [pkg])}")
                if pm == "apt-get":
                    subprocess.run(["apt-get", "autoremove", "--purge", "-y"])
                    logging.info(f" Ran: {' '.join('apt-get autoremove --purge -y')}")
                print("===========REMOVAL COMPLETED===========")
            else:
                pass
        except subprocess.CalledProcessError:
            print("An error occurred, verify that the package you're trying to remove is installed.")
    elif command=="4":
        output= subprocess.run(commands[pm]["query"], capture_output=True, text=True)
        print("=======INSTALLED PACKAGES=======")
        print(output.stdout)
    elif command=="5":
        pkg=input("Enter the name of the package to search for: ").lower()
        output = subprocess.run(commands[pm]["search"] + [pkg], capture_output=True, text=True)
        logging.info(f" Ran: {' '.join(commands[pm]['search'] + [pkg])}")
        print("================RESULTS================")
        print(output.stdout)
    elif command=="6":
        confirm = input("The cache will be cleaned, do you wish to continue? [y/n] ")
        if confirm == "y":
            print("Cleaning cache...")
            subprocess.run(commands[pm]["cache"])
            logging.info(f" Ran: {' '.join(commands[pm]['cache'])}")
            print("==============CACHE CLEANED==============")
        else:
            pass
    elif command == "7":
        adv_menu()
    elif command ==(str(len(options))):
        logging.info(f"{(' Exited.')}")
        exit("Exited successfully")
    else:
        print("Invalid option.")
        pass

check_euid()
init_logs()
check_pm()
while True:
    list_options()
    main()
