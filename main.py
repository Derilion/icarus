#!/usr/bin/env python3

"""
Project Icarus

creator: derilion
date: 01.07.2019
version: 0.1a
"""

"""
TODO:
- Installer
- Database Structure
- Special Characters in *.ini 
- Setup of skills
- Configuration of Clients
- multi language support
"""

# imports
from icarus.icarus import Icarus

# thread safe init
if __name__ == "__main__":
    Icarus().start()
