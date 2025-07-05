#!/usr/bin/env python3
# Copyright (C) 2025 deltaZenith
# This file is part of DAPU
# DAPU is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import subprocess
import shutil
import os
import logging

pm=""
supported_pms=["pacman", "apt", "dnf", "zypper"]
options=["Install packages", "Update the system", "Remove a package", "List installed packages", "Search for a package in the repos", "Clear the package cache", "Exit"]
commands={
        "pacman":{"install":["pacman", "-S", "--noconfirm"], "update":["pacman", "-Syu", "---noconfirm"], "remove":["pacman", "-Rns", "--noconfirm"], "query":["pacman", "-Q"], "search":["pacman", "-Ss"], "cache":["pacman", "-Sc", "--noconfirm"]},
        "apt-get":{"install":["apt-get", "install", "-y"], "update":["apt-get", "update"], "upgrade":["apt-get", "upgrade", "-y"] ,"remove":["apt-get", "purge", "-y"], "query":["apt", "list", "--installed"], "search": ["apt", "search"], "cache":["apt-get", "autoclean", "-y"]},
        "dnf":{"install":["dnf", "install", "-y"], "update":["dnf", "upgrade", "-y"], "remove":["dnf", "remove", "-y"], "query":["dnf", "list", "--installed"], "search":["dnf", "search"], "cache":["dnf", "clean", "all"]},
        "zypper":{"install":["zypper", "install", "-y"], "update":["zypper", "dup", "-y"], "remove":["zypper", "remove", "--clean-deps", "-y"], "query":["zypper", "se", "-si"], "search":["zypper", "search"], "cache":["zypper", "clean",]}
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

def list_options():  
    print("=================DAPU==================")
    for i, item in enumerate(options):
        print(i+1, ")", item)
    print("=======================================")
def check_command():
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
    check_command()
