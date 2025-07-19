## Version 0.2
Added advanced options for each of the package managers and a new script that copies each of the script's components in /usr/local/bin  
## New options for all package managers
Mark packages as user installed  
Remove unneeded packages (available for all package managers except zypper)  
### Package Manager specific options
### Pacman
Added AUR helper support for yay and paru, if they're installed, they'll be detected automatically, if not the user will be prompted to download one of them using a simple bash script.  
## APT
Added advanced options to fix missing/broken dependencies  
Added a distribution upgrades option  
Added an option to reconfigure all packages through dpkg  
## DNF
Added an option to check for package integrity  
Added an option to downgrade packages  
Added an option to run minimal upgrades  
## Version 0.1.1
Added functionality that detects whether zypper is being used on OpenSUSE Leap or Tumbleweed, this enables DAPU to follow best pratices depending on the respective version.  
## Version 0.1
Added Zypper support.  
This version marks DAPU's entrance in the beta phase since all package managers that were planned to be included originally are now supported.  
This doesn't mean that other ones aren't going to be supported, so look forward to future versions of DAPU that are even more distro-agnostic and with more advanced features to satisfy both newcomers and more seasoned users.

## Version 0.0.2
Added simple logging capabilities and dnf support.
## Version 0.0.1
The very first version of DAPU to be released, it includes APT and pacman support and a simple user interface to make for an easy to use, lightweight, interactive script. Its functionalities include installation, removal, updating of packages, listing the installed packages, searching for a package in the distro's repos, cleaning the package manager's cache.
## 
Copyright (C) 2025 deltaZenith.  
This file is part of DAPU.  
DAPU is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.  
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/> .
