from utils.network import get_ips_from_subnets, scan_subnet
from utils.graph import build_topology, draw_topology

# Example usage
if __name__ == "__main__":
    subnet = ["192.168.62.0/24"]
    all_ips = get_ips_from_subnets(subnet)
    # print(all_ips)

    
    active_ips = scan_subnet(all_ips)
    print("\n\nActive IPs")
    for ip in active_ips:
        print(ip)
    # topology = build_topology(active_ips, user, auth_key, priv_key, auth_protocol, priv_protocol)
    # draw_topology(topology)