import os
import subprocess

class DatabaseExtraction:
    def __init__(self, target, output_dir, logger):
        self.target = target
        self.output_dir = output_dir
        self.logger = logger
        self.extracted_data = []
        
    def extract(self, service, creds):
        if service == 'mysql':
            self.dump_mysql(creds['user'], creds['password'])
            
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
