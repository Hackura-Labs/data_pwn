import socket
import subprocess
import concurrent.futures

class InternalDiscovery:
    """Internal network discovery: ARP scan, ping sweep, internal port scanning."""

    def __init__(self, target, stealth_mode, logger):
        self.target = target
        self.stealth_mode = stealth_mode
        self.logger = logger
        self.discovered_hosts = []

    def ping_sweep(self, subnet: str):
        """Ping sweep a subnet (e.g. '192.168.1')."""
        self.logger.scan(f"Ping sweep on {subnet}.0/24 ...")
        live_hosts = []

        def ping(ip):
            try:
                result = subprocess.run(
                    ["ping", "-c", "1", "-W", "1", ip],
                    capture_output=True, timeout=2
                )
                if result.returncode == 0:
                    return ip
            except:
                pass
            return None

        ips = [f"{subnet}.{i}" for i in range(1, 255)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(ping, ips)
            for r in results:
                if r:
                    live_hosts.append(r)
                    self.logger.found(f"Host alive: {r}")

        self.discovered_hosts = live_hosts
        return live_hosts

    def resolve_hostname(self, ip: str) -> str:
        """Reverse DNS lookup."""
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return ip

    def internal_port_scan(self, host: str, ports=None):
        """Quick port scan on an internal host."""
        if ports is None:
            ports = [22, 80, 443, 3306, 5432, 445, 3389]
        open_ports = {}
        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5 if not self.stealth_mode else 2)
                if s.connect_ex((host, port)) == 0:
                    open_ports[port] = True
                    self.logger.found(f"{host}:{port} open")
                s.close()
            except:
                pass
        return open_ports
