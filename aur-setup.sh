#! /usr/bin/env bash
#Copyright (C) 2025 deltaZenith.
#This file is part of DAPU.
#DAPU is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/> .

printf "================AUR SETUP===============\n "
while true; do
	printf "1) Yay \n 2) Paru \n 3) Exit \n "
	read -p "What AUR helper would you like to install? (1-3)" option
	if [ "$option" == "1" ]; then
		git clone https://aur.archlinux.org/yay-bin.git 
		cd yay-bin
		makepkg -si
		cd ..
		rm -rf yay-bin
		exit 0
	elif [ "$option" == "2" ]; then 
		git clone https://aur.archlinux.org/paru-bin.git
		cd paru-bin
		makepkg -si
		cd ..
		rm -rf paru-bin
		exit 0
	elif [ "$option" == "3" ]; then
		exit 0
	else
		printf "Invalid option. \n"
	fi
done
