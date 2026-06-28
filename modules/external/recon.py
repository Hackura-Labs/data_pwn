import socket
import subprocess

class ExternalRecon:
    """External reconnaissance module: nmap, DNS, subdomain enumeration, fingerprinting."""

    def __init__(self, target, output_dir, logger, kali_available):
        self.target = target
        self.output_dir = output_dir
        self.logger = logger
        self.kali_available = kali_available

    def run_nmap(self):
        """Run nmap scan if available."""
        if not self.kali_available:
            self.logger.warning("nmap not available - skipping")
            return
        self.logger.scan("Running nmap scan...")
        try:
            cmd = f"nmap -sV -T4 {self.target} -oN {self.output_dir}/nmap.txt 2>/dev/null"
            subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            self.logger.success("nmap scan completed")
        except Exception as e:
            self.logger.warning(f"nmap error: {e}")

    def dns_lookup(self):
        """Perform basic DNS lookup."""
        try:
            ip = socket.gethostbyname(self.target)
            self.logger.info(f"DNS resolved: {self.target} -> {ip}")
            return ip
        except Exception as e:
            self.logger.warning(f"DNS lookup failed: {e}")
            return None

    def run_whatweb(self):
        """Technology fingerprinting via whatweb (if available)."""
        if not self.kali_available:
            return
        self.logger.scan("Running whatweb fingerprinting...")
        try:
            cmd = f"whatweb {self.target} -o {self.output_dir}/whatweb.txt 2>/dev/null"
            subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            self.logger.success("whatweb completed")
        except Exception as e:
            self.logger.warning(f"whatweb error: {e}")
