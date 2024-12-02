import networkx as nx
import matplotlib.pyplot as plt
from utils.network import get_dns_hostname
from utils.snmp import get_snmp_neighbors, get_local_ports
from utils.database import get_host_name_by_address
from utils.screen import get_screen_size

def build_topology(active_ips, user, auth_key, priv_key, auth_protocol, priv_protocol):
    G = nx.Graph()
    for ip in active_ips:
        dns_host_name = get_dns_hostname(ip)
        print("DNS HOST NAME: " + dns_host_name)
        remote_port_array = []
        local_port_array = []
        remote_device_array = []
        local_ports = get_local_ports(ip, user, auth_key, priv_key, auth_protocol, priv_protocol)
        device_name = get_host_name_by_address(ip)
        G.add_node(device_name, label=device_name)
        print(ip + " " + device_name)
        neighbors = get_snmp_neighbors(ip, user, auth_key, priv_key, auth_protocol, priv_protocol)
        for oid, value in neighbors:
            local_device = device_name
            if oid:
                if "0.8802.1.1.2.1.4.1.1.7" in oid:
                    remote_port_array.append(value)
                if "0.8802.1.1.2.1.4.1.1.2" in oid:
                    local_port = local_ports.get(value, "N/A")
                    local_port_array.append(local_port)
                if "0.8802.1.1.2.1.4.1.1.9" in oid:
                    r1 = value.split(".")[0]
                    remote_device_array.append(r1)
        i = 0
        for d in remote_device_array:
            G.add_node(d, label=d)
            G.add_edge(device_name, d, label=remote_port_array[i])
            i = i + 1
    return G

def draw_topology(graph):
    screen_width_px, screen_height_px = get_screen_size()
    dpi = 100
    max_size_px = 16384
    scale_factor = min(max_size_px / screen_width_px, max_size_px / screen_height_px, 1)
    screen_width_px *= scale_factor
    screen_height_px *= scale_factor
    screen_width_inch = screen_width_px / dpi
    screen_height_inch = screen_height_px / dpi
    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(18, 10))
    nx.draw_networkx_nodes(graph, pos, node_size=500, node_color="lightblue", edgecolors="black")
    nx.draw_networkx_edges(graph, pos, width=1, alpha=0.7, edge_color="black")
    nx.draw_networkx_labels(graph, pos, labels=nx.get_node_attributes(graph, "label"), font_size=10, font_family="sans-serif")
    edge_labels = nx.get_edge_attributes(graph, "label")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color="red", font_size=8)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("network_topology.png")