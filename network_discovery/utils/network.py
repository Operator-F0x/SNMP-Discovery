import ipaddress
import os
import socket
import concurrent.futures

def get_dns_hostname(ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        short_hostname = hostname.split(".")[0]
        if short_hostname:
            return short_hostname
        else:
            return ip
    except socket.herror:
        return ip

def ping_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        response = os.system(f"ping -c 1 -W 1 {ip_str} > /dev/null 2>&1")
        if response == 0:
            return ip_str
    except ValueError as e:
        print(f"Invalid IP address '{ip_str}': {e}")
    return None

def get_ips_from_subnets(subnets):
    all_ips = []
    for subnet in subnets:
        try:
            net = ipaddress.ip_network(subnet)
            for ip in net.hosts():
                all_ips.append(str(ip))
        except ValueError as e:
            print(f"Invalid subnet {subnet}: {e}")
    return all_ips

def scan_subnet(ip_list):
    active_ips = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(ping_ip, ip): ip for ip in ip_list}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                active_ips.append(result)
    return active_ips