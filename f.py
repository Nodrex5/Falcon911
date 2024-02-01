import sys, os
import time
import pyfiglet
from halo import Halo
from colorama import Fore
from logo import logo
import subprocess
# -----------

__author__ = 'Al-Mohammady Team.'
__version__ = '8.0'
__series__ = 'Attack.'

# -----------
os.system('clear')
def infoTool():
	spinner = Halo()
	spinner.start()
	spinner.succeed("Author  : %s" % __author__)
	spinner.succeed("Version : %s."%__version__)
	

infoTool()
print(f"{Fore.LIGHTBLACK_EX}-- Falcon 911 -- {Fore.RESET}")

# --------
methodList = [
	'UDP',
	'TCP',
	'HTTP',
]

print(f'''
{Fore.GREEN}―――――――――――――――――――――――――――――――――――――
1. {Fore.RED}UDP.
{Fore.GREEN}2. {Fore.RED}TCP (soon...)
{Fore.GREEN}3. {Fore.RED}HTTP.
{Fore.GREEN}―――――――――――――――――――――――――――――――――――――{Fore.RESET}
''')
print(f'{Fore.CYAN}[ ~ ] Choose a DDOS attack method.')
try:
	methodInput = (int(input(f'{Fore.GREEN}[ ~ ]{Fore.RED} method ~#{Fore.GREEN}')))
	if methodInput==1:
		os.system('clear')
		subprocess.run(["python","fu.py"])
	elif methodInput==2:
		print('soon ...')
	elif methodInput==3:
		os.system('clear')
		subprocess.run(["python","fh.py"])
	else:
		print(f'{Fore.RED}[ ! ]{Fore.CYAN} Please choose one of the numbers in the list.')
except ValueError as e:
	print(e)



