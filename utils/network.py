import socket

def resolve_ip(hostname: str) -> str:
    """Resolve hostname to IP address."""
    try:
        return socket.gethostbyname(hostname)
    except:
        return ""

def reverse_resolve(ip: str) -> str:
    """Reverse DNS lookup."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return ip

def is_port_open(host: str, port: int, timeout: float = 0.5) -> bool:
    """Check if a single TCP port is open."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0
    except:
        return False

def get_local_ip() -> str:
    """Get the local machine's IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"
