# DAPU
DAPU (Distro Agnostic Package Utility) aims to be a simple, no frills, cross-compatible, interactive script which simplifies package management across Linux distros.

## Features
This script is meant for users who do not wish to learn their distro's package manager's syntax and commands, this software's main goal is to facilitate package management by making it automated and interactive. While the script doesn't include any code from other projects, it wraps around the package manager which is detected automatically, therefore the script has your distro's package manager as a dependency alongside other Python libraries and the Python programming language itself.

### Cross compatibility
At the moment, the supported package managers are APT, dnf, zypper and pacman, with more to come. The script figures out what package manager is installed using the shutils library and determines the approriate command for each situation through the use of dictionaries.

### Automation
The process of managing packages is entirely automatic, the only thing the user has to do is provide the information required by DAPU to know what to do and what package to interact with (e.g. when installing or removing a package, the user will be prompted to specify its name and to confirm the operation.)

### Interactiveness
The script, upon launching, checks for elevated privileges and prints a list of options, each of which corresponds to a number, to know what to do, the script relies on user input which is expected to be one of the aforementioned numbers.

## Installation & Usage
### Dependecies
Python, which is preinstalled on most systems by default;  
Your distro's package manager which needs to be among the supported ones (APT, dnf, pacman.)
### Clone the repo
This will download the files in the repository to your current directory:  
``git clone https://github.com/deltaZenith/DAPU.git``
### CD into the DAPU folder
From the directory in which you cloned the repository, this command will change your working directory to DAPU's folder:  
``cd DAPU``  
### Run the script
Either run it with the python command directly:  
``sudo python3 dapu.py``  
or make it executable and run it:  
``chmod +x dapu.py``(This command is the one to make the script executable and only needs to be run once)   
``sudo ./dapu.py``
### Checking the logs
Upon running the script, a directory containing DAPU's logs will be created in /var/log/dapu/ .  
To check the logs, run:  
``cat /var/log/dapu/dapu.log``  
This will return the file's content which includes every command that has been run.

## To do list
Add zypper supported  
Add advanced features for each of the package managers

## Disclaimer
This software relies on pacman, the package manager for Arch Linux; APT and apt-get, the package managers for Debian; dnf, the package manager for Fedora: zypper, the package manager for OpenSUSE; the Python programming language and the "subprocess", the "shutils" and "os" Python libraries.
I do not own/ am not affiliated with any of those projects.  

By using this script you agree that the author is not responsible for any damage that may be caused by the script which is provided "as is" and without any warranty, any harm (malfunction, data loss, damage) done to the system is solely the user's responsability.  
Copyright (C) 2025 deltaZenith.  
This file is part of DAPU.  
DAPU is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.  
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/> .
