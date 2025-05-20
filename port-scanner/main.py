import socket
from datetime import datetime
import subprocess

def scan_ports(target, port_range=range(1,1025)):
    print(f"\n[*] Scanning target: {target}")
    print(f"\n[*] Start time: {datetime.now()}")

    for port in port_range:
        # Define a socket stream for IPv4 adresses and TCP connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Try to connect for 0.5 s, then move on
        sock.settimeout(0.5)

        result = sock.connect_ex((target, port))
        
        # Check if port is open
        if result == 0:
            try:
                # Check what the service looks like (ssh, http, https, etc.)
                service = socket.getservbyport(port)
            except:
                # Service is unusual or not recognized
                service = "Unknown"
            print(f"[+] Port {port} is open - ({service})")
            sock.close()
        else:
            print(f"[-] Port {port} is closed")

if __name__ == "__main__":
    auto_seek = input("Automatically seek target(s)? (Y/n)\n")
    if auto_seek == "n":
        target_host = input("Enter IP or Hostname to scan:\n")
        scan_ports(target_host)
    else:
        # determine all IPv4 addresses on current device
        possible_targets = subprocess.run(["ifconfig | grep inet"], shell=True, text=True, capture_output=True)
        # TODO - Scrub this output by "\t" to determine addresses
        # Scan all targets
        for target_host in possible_targets:
            scan_ports(target_host)