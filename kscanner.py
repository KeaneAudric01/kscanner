import socket
import re
import time
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

VERSION = "0.1.0"
RED = '\033[91m'
RESET = '\033[0m'

def get_service_name(port: int) -> str:
    try:
        return socket.getservbyport(port)
    except OSError:
        return "Unknown service"

def scan_port(ip: str, port: int, open_ports: List[Tuple[int, str]], timeout: int):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        if result == 0:
            service = get_service_name(port)
            open_ports.append((port, service))
        sock.close()
    except Exception as e:
        print(f"{RED}Error scanning port {port}: {e}{RESET}")

def scan_ports(ip: str, port_ranges: List[Tuple[int, int]], timeout: int, max_workers: int):
    total_ports = sum(end - start + 1 for start, end in port_ranges)
    scanned_ports = 0
    open_ports = []

    def scan_port_with_progress(ip: str, port: int):
        nonlocal scanned_ports
        scan_port(ip, port, open_ports, timeout)
        scanned_ports += 1

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for start_port, end_port in port_ranges:
                for port in range(start_port, end_port + 1):
                    executor.submit(scan_port_with_progress, ip, port)

            while scanned_ports < total_ports:
                progress = (scanned_ports / total_ports) * 100
                bar_length = 40
                block = int(bar_length * progress / 100)
                bar = "#" * block + "-" * (bar_length - block)
                sys.stdout.write(f"\rScanning progress: [{bar}] {progress:.2f}%")
                sys.stdout.flush()
                time.sleep(0.1)

        print("\rScanning progress: [########################################] 100.00%")
        if open_ports:
            print("Open ports:")
            print(f"{'Port':<10}{'Service':<30}")
            print(f"{'-'*40}")
            for port, service in open_ports:
                print(f"{port:<10}{service:<30}")
        else:
            print("No open ports found.")
        
        print("--------------------------------------------------------------")
        print("kping by Keane Audric")
        print(f"Version: {VERSION}")
        print("GitHub: https://github.com/KeaneAudric01")
        print("--------------------------------------------------------------")
    except KeyboardInterrupt:
        print(f"\n{RED}Scan interrupted by user. Exiting...{RESET}")

def is_valid_ip(ip: str) -> bool:
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return pattern.match(ip) is not None

def parse_port_ranges(port_ranges: str) -> List[Tuple[int, int]]:
    ranges = port_ranges.split(',')
    parsed_ranges = []
    for port_range in ranges:
        try:
            start_port, end_port = map(int, port_range.replace(' ', '').split('-'))
            if start_port > end_port:
                raise ValueError("Start port must be less than or equal to end port.")
            if not (1 <= start_port <= 65535) or not (1 <= end_port <= 65535):
                raise ValueError("Port numbers must be in the range 1-65535.")
            parsed_ranges.append((start_port, end_port))
        except ValueError:
            raise ValueError("Invalid port range format. Please use the format 'start-end'.")
    return parsed_ranges

if __name__ == "__main__":
    try:
        while True:
            target_ip = input("Enter the IP address to scan: ")
            if is_valid_ip(target_ip):
                break
            else:
                print(f"{RED}Invalid IP address format. Please try again.{RESET}")
        
        print("Scanning protocol: TCP")
        
        print("Port range options:")
        print("1. All ports (1-65535)")
        print("2. Common ports")
        print("3. Custom range")
        port_option = input("Enter the port range option: ").strip()
        while port_option not in ['1', '2', '3']:
            print(f"{RED}Invalid option. Please enter '1', '2', or '3'.{RESET}")
            port_option = input("Enter the port range option: ").strip()
        
        if port_option == '1':
            port_ranges = [(1, 65535)]
        elif port_option == '2':
            port_ranges = [(20, 21), (22, 22), (23, 23), (25, 25), (53, 53), (80, 80), (110, 110), (143, 143),
                        (443, 443), (465, 465), (587, 587), (993, 993), (995, 995), (3306, 3306), (5432, 5432),
                        (6379, 6379), (8080, 8080), (8443, 8443), (27017, 27017), (27015, 27015), (25565, 25565),
                        (19132, 19132), (28960, 28960), (3478, 3480), (5223, 5223)]
        else:
            while True:
                port_ranges_input = input("Enter the port ranges (e.g., 1-50, 80-100): ").strip()
                try:
                    port_ranges = parse_port_ranges(port_ranges_input)
                    break
                except ValueError as e:
                    print(f"{RED}{e}{RESET}")
        
        max_workers = 100
        timeout = 1
        scan_ports(target_ip, port_ranges, timeout=timeout, max_workers=max_workers)
    except KeyboardInterrupt:
        print(f"\n{RED}Program interrupted by user. Exiting...{RESET}")