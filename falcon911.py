import sys, os
import time
import pyfiglet
from halo import Halo
from colorama import Fore
from Tools.logo import logo
import subprocess
# -----------

__author__ = 'Al-Mohammady Team.'
__version__ = '8.8'
__series__ = 'Attack.'

# -----------
os.system('clear')
logo()
def infoTool():
        spinner = Halo()
        spinner.start()
        spinner.succeed("Author  : %s" % __author__)
        spinner.succeed("Version : %s."%__version__)


infoTool()
#print(f"{Fore.LIGHTBLACK_EX}-- Falcon 911 -- {Fore.RESET}")

# --------
methodList = [
        'UDP',
        'TCP',
        'HTTP',
]

print(f'{Fore.GREEN}—'*40)
print(f'''{Fore.GREEN}1. {Fore.LIGHTRED_EX}UDP.
{Fore.GREEN}2. {Fore.LIGHTRED_EX}TCP (soon...)
{Fore.GREEN}3. {Fore.LIGHTRED_EX}HTTP.''')
print(f'{Fore.GREEN}—'*40)
print(f'{Fore.GREEN}[ ~ ]{Fore.RESET} Choose a DDOS attack method.')
try:
        methodInput = (int(input(f'{Fore.GREEN}[ ~ ]{Fore.LIGHTRED_EX} method ~#{Fore.GREEN}')))
        if methodInput==1:
                os.system('clear')
                fh_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Tools", "fu.py")
                subprocess.run(["python", fh_path])
        elif methodInput==2:
                print('soon ...')
        elif methodInput==3:
        	os.system('clear')
        	fh_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Tools", "f3.py")
        	subprocess.run(["python", fh_path])
        else:
        	print(f"{Fore.RED}Not Found !")
        	
except ValueError as e:
        print(f"{Fore.RED}Error, Enter The Number !, Ex : 3.")
        
        
