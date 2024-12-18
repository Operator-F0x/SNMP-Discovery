import ipaddress
import subprocess
import platform
import socket
import concurrent.futures

class NetworkUtils:
    @staticmethod
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            print(f"Error getting local IP: {e}")
            return None

    @staticmethod
    def save_local_ip_to_env():
        local_ip = NetworkUtils.get_local_ip()
        if local_ip:
            with open('.env', 'a') as env_file:
                env_file.write(f'\nDB_HOST={local_ip}\n')
        else:
            print("Failed to retrieve local IP address.")

    @staticmethod
    def get_dns_hostname(ip):
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            short_hostname = hostname.split(".")[0]
            return short_hostname if short_hostname else ip
        except socket.herror:
            return ip

    @staticmethod
    def ping_ip(ip_str):
        try:
            ipaddress.ip_address(ip_str)
            system = platform.system()
            command = ["ping", "-n", "1", "-w", "1000", ip_str] if system == "Windows" else ["ping", "-c", "1", "-W", "1", ip_str]
            response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return ip_str if response.returncode == 0 else None
        except ValueError as e:
            print(f"Invalid IP address '{ip_str}': {e}")
            return None

    @staticmethod
    def get_ips_from_subnets(subnets):
        all_ips = []
        for subnet in subnets:
            try:
                net = ipaddress.ip_network(subnet)
                all_ips.extend(str(ip) for ip in net.hosts())
            except ValueError as e:
                print(f"Invalid subnet {subnet}: {e}")
        return all_ips

    @staticmethod
    def scan_subnet(ip_list):
        active_ips = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(NetworkUtils.ping_ip, ip): ip for ip in ip_list}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    active_ips.append(result)
        return active_ips