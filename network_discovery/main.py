from utils.network import get_ips_from_subnets, scan_subnet
from utils.graph import build_topology, draw_topology

# Example usage
if __name__ == "__main__":
    subnets = ["10.231.230.0/24"]
    all_ips = get_ips_from_subnets(subnets)
    user = "massnmpadmn"
    auth_key = "your_auth_key"
    priv_key = "your_priv_key"
    auth_protocol = "your_auth_protocol"
    priv_protocol = "your_priv_protocol"

    active_ips = scan_subnet(all_ips)
    topology = build_topology(active_ips, user, auth_key, priv_key, auth_protocol, priv_protocol)
    draw_topology(topology)