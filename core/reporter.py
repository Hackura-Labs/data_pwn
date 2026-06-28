import os
from datetime import datetime
from utils.helpers import Color

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
