import os
import sys
import shutil
from datetime import datetime

from config import Config
from utils.helpers import Color
from core.reporter import Logger
from core.scanner import Scanner
from modules.external.web import WebAttacks
from modules.external.services import ServiceAttacks
from modules.extraction.databases import DatabaseExtraction
from modules.extraction.files import FileExtraction

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
        
    def setup(self, target: str, stealth: bool = False):
        """Initialize the tool"""
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
║              {Color.YELLOW}DATA PWN v2.0 - Ultimate Data Hunter{Color.CYAN}              ║
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
            
    def recon_phase(self):
        """Run reconnaissance phase"""
        scanner = Scanner(self.target, self.stealth_mode, self.logger)
        if not scanner.check_host():
            self.logger.error("Host is unreachable or invalid")
            return
            
        self.port_info = scanner.fast_port_scan()
        self.logger.success("Reconnaissance completed")
        return self.port_info

    def web_phase(self):
        """Run web application attacks"""
        self.logger.scan("Phase 2: Web Application Attacks")
        
        if '80' not in self.port_info and '443' not in self.port_info:
            self.logger.warning("No web ports found")
            return
            
        web = WebAttacks(self.target, self.output_dir, self.logger, self.kali_available)
        web.check_exposed_files()
        
        if self.kali_available:
            web.run_sqlmap()
            web.run_gobuster()
            
        self.vulnerabilities.extend(web.vulnerabilities)
        self.logger.success("Web attacks completed")

    def service_phase(self):
        """Run service attacks"""
        self.logger.scan("Phase 3: Service Attacks")
        svc = ServiceAttacks(self.target, self.stealth_mode, self.logger)
        
        if '22' in self.port_info:
            svc.run_ssh_attack()
            
        db_ports = [p for p in self.port_info.keys() if int(p) in Config.DB_PORTS]
        for port in db_ports:
            db_type = Config.DB_PORTS.get(int(port), 'unknown')
            svc.run_db_attack(port, db_type)
            
        self.credentials.update(svc.credentials)
        self.logger.success("Service attacks completed")

    def extract_phase(self):
        """Extract data using found credentials"""
        self.logger.scan("Phase 4: Data Extraction")
        
        if not self.credentials:
            self.logger.warning("No credentials found")
            return
            
        db_ext = DatabaseExtraction(self.target, self.output_dir, self.logger)
        file_ext = FileExtraction(self.target, self.output_dir, self.logger)
        
        for service, creds in self.credentials.items():
            db_ext.extract(service, creds)
            file_ext.extract(service, creds)
            
        self.extracted_data.extend(db_ext.extracted_data)
        self.extracted_data.extend(file_ext.extracted_data)
        self.logger.success("Data extraction completed")

    def full_attack(self):
        """Run complete attack chain"""
        self.show_banner()
        self.logger.info("Starting full attack chain...")
        self.recon_phase()
        self.web_phase()
        self.service_phase()
        self.extract_phase()
        self.generate_report()
        self.logger.success("Full attack chain completed!")

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
        with open(f"{self.output_dir}/report.txt", 'w') as f:
            f.write(report)
        print(report)
        self.logger.success(f"Report saved to {self.output_dir}/report.txt")

    def run(self):
        """Run the tool"""
        self.show_banner()
        scanner = Scanner(self.target, self.stealth_mode, None)
        if not scanner.check_host():
            self.logger.error(f"Invalid target: {self.target}")
            return
        self.logger.info("Running quick recon...")
        self.recon_phase()
        self.show_menu()
