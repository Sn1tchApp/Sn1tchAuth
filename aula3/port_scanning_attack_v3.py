import socket
from concurrent.futures import ThreadPoolExecutor

# Global list to store open ports
open_ports = []

def scan_port(host, port):
    """Attempts to connect to a specified port on a specified host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)  # Set timeout for the connection
        result = sock.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)  # Save open port to the global list

def port_scan(host, start_port, end_port):
    """Scans a range of ports on a specified host."""
    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, host, port)

if __name__ == "__main__":
    target_host = "18.231.148.22"
    start_port = 21
    end_port = 3000
    
    print(f"Scanning {target_host} from port {start_port} to {end_port}...")
    port_scan(target_host, start_port, end_port)

    # Print the list of open ports
    print("Open ports:", open_ports)
