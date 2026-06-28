import socket
import concurrent.futures

class Scanner:
    """Scanner module for port scanning and service detection"""
    
    def __init__(self, target, stealth_mode, logger):
        self.target = target
        self.stealth_mode = stealth_mode
        self.logger = logger
        self.port_info = {}
        
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
