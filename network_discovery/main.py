from utils.network import get_ips_from_subnets, scan_subnet
from utils.snmp import get_snmp_neighbors
import json

# Example usage
if __name__ == "__main__":
    subnet = ["192.168.62.0/24"]
    all_ips = get_ips_from_subnets(subnet)

    
    active_ips = scan_subnet(all_ips)
    print("\n\nActive IPs")
    for ip in active_ips:
        print(ip)
    
    all_neighbors = {}
    
    for ip in active_ips:
        neighbors = get_snmp_neighbors(ip, 2, community="public")
        all_neighbors[ip] = neighbors
        print("\n\nNeighbors for", ip)
        print(neighbors)
    
    # Save the neighbors data to a JSON file
    with open('neighbors.json', 'w') as json_file:
        json.dump(all_neighbors, json_file, indent=4)