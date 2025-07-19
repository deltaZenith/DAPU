#!/usr/bin/env bash
#Copyright (C) 2025 deltaZenith.
#This file is part of DAPU.
#DAPU is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/> .

FILELOCATION=/usr/local/bin/dapu
DIRECTORYLOCATION=/usr/local/bin/dapu.d
if [ $EUID -ne 0 ]; then
	printf "This script needs elevated (sudo) privileges to run. \n"
	exit 0
fi
if [ -e /usr/local/bin/dapu ]; then
	read -p "It looks like DAPU is already installed, would you like to uninstall it? [y/n] " confirm
	if [ $confirm == "y" ]; then
		rm $FILELOCATION
		printf "Removed file %s\n" "$FILELOCATION"
		rm -r $DIRECTORYLOCATION
		printf "Removed directory %s\n" "$DIRECTORYLOCATION"
	else
		exit 0
	fi
else
	read -p "Welcome to the DAPU setup, this script will install DAPU on your system, proceed? [y/n] " confirm
	if [ $confirm == "y" ]; then
		mkdir -p $DIRECTORYLOCATION
  		chmod +x dapu.py
		cp dapu.py $FILELOCATION
		printf "Created file %s\n" "$FILELOCATION"
  		chmod +x aur-setup.sh
		cp aur-setup.sh $DIRECTORYLOCATION/aur-setup.sh
		printf "Created file %s\n" "$DIRECTORYLOCATION/aur-setup.sh"
	else
		exit 0
	fi
fi

	

