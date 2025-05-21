import socket
from datetime import datetime
import subprocess
import re

def scan_ports(target, file_to_write=None, port_range=range(1,1025)):
    print(f"\n[*] Scanning target: {target}")
    print(f"\n[*] Start time: {datetime.now()}")
    if file_to_write != None:
        print(f"\n[*] Writing results to file: {file_to_write}")
        with open(file_to_write, "a+") as f:
            f.write(f"[*] Scanning target: {target}\n[*] Start time: {datetime.now()}")

    for port in port_range:
        # Define a socket stream for IPv4 adresses and TCP connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Try to connect for 0.5 s, then move on
        sock.settimeout(0.5)

        result = sock.connect_ex((target, port))
        
        # If there isn't a file to write to, print output
        if file_to_write == None:
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
    
        # If there's a file to write to, export output
        else:
             # Check if port is open
            if result == 0:
                try:
                    # Check what the service looks like (ssh, http, https, etc.)
                    service = socket.getservbyport(port)
                except:
                    # Service is unusual or not recognized
                    service = "Unknown"
                out = f"\n[+] Port {port} is open - ({service})"
                sock.close()
            else:
                out = f"\n[-] Port {port} is closed"
            # Write to file if available
            with open(file_to_write, "a+") as f:
                f.write(out)

if __name__ == "__main__":
    auto_seek = input("Automatically seek target(s)? (Y/n)\n")
    if auto_seek == "n":
        target_host = input("Enter IP or Hostname to scan:\n")
        scan_ports(target_host)
    else:
        # determine all IPv4 addresses on current device
        try:
            # Mac
            raw_targets = subprocess.run(["ifconfig"], shell=True, text=True, capture_output=True).stdout
        except:
            # Windows
            raw_targets = subprocess.run("ipconfig")
        
        # Scrub this output to determine addresses
        ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        possible_targets = re.findall(ipv4_pattern, raw_targets)
        
        # Scan all targets
        for target_host in possible_targets:
            scan_ports(target_host, f"{target_host} Port Scan.txt")