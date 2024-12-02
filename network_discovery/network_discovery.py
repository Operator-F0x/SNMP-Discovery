# import ipaddress
# import networkx as nx
# import matplotlib.pyplot as plt
# import os
# from pysnmp.hlapi import *
# from screeninfo import get_monitors
# import concurrent.futures
# import mysql.connector
# from mysql.connector import Error
# import socket


# def get_dns_hostname(ip):
#     try:
#         hostname, _, _ = socket.gethostbyaddr(ip)
#         short_hostname = hostname.split(".")[0]
#         if short_hostname:
#             return short_hostname
#         else:
#             return ip
#     except socket.herror:
#         return ip


# def ping_ip(ip_str):
#     """
#     Ping an IP address and return if it is active.

#     Args:
#     ip_str (str): The IP address to ping.

#     Returns:
#     str: The IP address if it is active, otherwise None.
#     """
#     try:
#         # Check if the IP is valid
#         ipaddress.ip_address(ip_str)
#         # Simple ping command with a reduced timeout to check if the IP is active
#         response = os.system(f"ping -c 1 -W 1 {ip_str} > /dev/null 2>&1")
#         if response == 0:
#             return ip_str
#     except ValueError as e:
#         print(f"Invalid IP address '{ip_str}': {e}")
#     return None


# def get_ips_from_subnets(subnets):
#     """Get all IP addresses from a list of subnets."""
#     all_ips = []
#     for subnet in subnets:
#         try:
#             net = ipaddress.ip_network(subnet)
#             for ip in net.hosts():
#                 all_ips.append(str(ip))
#         except ValueError as e:
#             print(f"Invalid subnet {subnet}: {e}")
#     return all_ips


# def scan_subnet(ip_list):
#     """Scan a list of IP addresses and return active IP addresses."""
#     active_ips = []
#     with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
#         futures = {executor.submit(ping_ip, ip): ip for ip in ip_list}
#         for future in concurrent.futures.as_completed(futures):
#             result = future.result()
#             if result:
#                 active_ips.append(result)
#     return active_ips

#     """
#     for ip_str in ip_list:
#         try:
#             print(ip_str)
#             # Check if the IP is valid
#             ipaddress.ip_address(ip_str)
#             # Simple ping command to check if the IP is active
#             response = os.system(f"ping -c 1 -W 1 {ip_str} > /dev/null 2>&1")
#             if response == 0:
#                 print(ip_str)
#                 active_ips.append(ip_str)
#         except ValueError as e:
#             print(f"Invalid IP address '{ip_str}': {e}")
#     return active_ips
#     """


# def snmp_discovery(
#     target, user, auth_key, priv_key, auth_protocol, priv_protocol, base_oid
# ):
#     """Perform SNMP discovery for LLDP or CDP neighbors."""
#     results = []
#     for errorIndication, errorStatus, errorIndex, varBinds in nextCmd(
#         SnmpEngine(),
#         UsmUserData(
#             user,
#             auth_key,
#             priv_key,
#             authProtocol=auth_protocol,
#             privProtocol=priv_protocol,
#         ),
#         UdpTransportTarget((target, 161)),
#         ContextData(),
#         ObjectType(ObjectIdentity(base_oid)),
#         lexicographicMode=False,
#     ):
#         if errorIndication or errorStatus:
#             continue
#         else:
#             for varBind in varBinds:
#                 oid_str, value_str = varBind
#                 results.append((oid_str.prettyPrint(), value_str.prettyPrint()))
#     return results


# def get_snmp_neighbors(ip, user, auth_key, priv_key, auth_protocol, priv_protocol):
#     """Get LLDP and CDP neighbors for a given IP address."""

#     neighbors = []

#     def get_lldp_neighbors():
#         lldp_oid = "1.0.8802.1.1.2.1.4"  # LLDP OID - update with the correct one
#         return snmp_discovery(
#             ip, user, auth_key, priv_key, auth_protocol, priv_protocol, lldp_oid
#         )

#     def get_cdp_neighbors():
#         cdp_oid = ".1.3.6.1.4.1.9.9.23.1.2.1"  # CDP OID - update with the correct one
#         return snmp_discovery(
#             ip, user, auth_key, priv_key, auth_protocol, priv_protocol, cdp_oid
#         )

#     neighbors.extend(get_lldp_neighbors())
#     neighbors.extend(get_cdp_neighbors())

#     return neighbors


# def extract_remote_device(value):
#     """Extract remote device information from value."""
#     # Placeholder for extraction logic - customize as needed
#     return value


# def build_topology(active_ips, user, auth_key, priv_key, auth_protocol, priv_protocol):
#     """Build a network topology graph."""
#     G = nx.Graph()

#     for ip in active_ips:
#         dns_host_name = get_dns_hostname(ip)
#         print("DNS HOST NAME: " + dns_host_name)
#         remote_port_array = []
#         local_port_array = []
#         remote_device_array = []
#         local_ports = get_local_ports(
#             ip, user, auth_key, priv_key, auth_protocol, priv_protocol
#         )

#         device_name = get_host_name_by_address(ip)
#         G.add_node(device_name, label=device_name)
#         print(ip + " " + device_name)
#         neighbors = get_snmp_neighbors(
#             ip, user, auth_key, priv_key, auth_protocol, priv_protocol
#         )

#         for oid, value in neighbors:
#             local_device = device_name

#             # remote_device = extract_remote_device(value)

#             if oid:
#                 # remort_port_nmeber = ''
#                 if "0.8802.1.1.2.1.4.1.1.7" in oid:

#                     remote_port_array.append(value)
#                 if "0.8802.1.1.2.1.4.1.1.2" in oid:
#                     local_port = local_ports.get(value, "N/A")
#                     local_port_array.append(local_port)
#                     # print(local_port)
#                 if "0.8802.1.1.2.1.4.1.1.9" in oid:  # lldpRemPortId
#                     r1 = value.split(".")[0]
#                     remote_device_array.append(r1)
#                     # print(ip + " --> " + r1 )
#                     # G.add_node(r1, label=r1)

#                     # G.add_edge(local_device, r1, label=remort_port_numeber)

#         i = 0
#         for d in remote_device_array:
#             G.add_node(d, label=d)
#             G.add_edge(device_name, d, label=remote_port_array[i])
#             i = i + 1

#     return G


# def draw_topology(graph):
#     """Draw the network topology graph."""
#     screen_width_px, screen_height_px = get_screen_size()
#     dpi = 100  # Desired dots per inch

#     # Scale down the screen size if it exceeds the maximum limit
#     max_size_px = 16384  # Maximum allowable size in pixels
#     scale_factor = min(max_size_px / screen_width_px, max_size_px / screen_height_px, 1)
#     screen_width_px *= scale_factor
#     screen_height_px *= scale_factor

#     screen_width_inch = screen_width_px / dpi
#     screen_height_inch = screen_height_px / dpi
#     pos = nx.spring_layout(graph, seed=42)
#     # plt.figure(figsize=(screen_width_inch, screen_height_inch))
#     plt.figure(figsize=(18, 10))
#     nx.draw_networkx_nodes(
#         graph, pos, node_size=500, node_color="lightblue", edgecolors="black"
#     )
#     nx.draw_networkx_edges(graph, pos, width=1, alpha=0.7, edge_color="black")
#     nx.draw_networkx_labels(
#         graph,
#         pos,
#         labels=nx.get_node_attributes(graph, "label"),
#         font_size=10,
#         font_family="sans-serif",
#     )

#     # Draw edge labels
#     edge_labels = nx.get_edge_attributes(graph, "label")

#     nx.draw_networkx_edge_labels(
#         graph, pos, edge_labels=edge_labels, font_color="red", font_size=8
#     )

#     # Adjust the plot limits and aspect ratio
#     plt.axis("off")
#     plt.tight_layout()
#     # pos = nx.spring_layout(graph)
#     # nx.draw(graph, pos, with_labels=True, node_color='lightgreen', edge_color='red', node_size=300, font_size=6, font_weight='bold')
#     # plt.title('Network Topology')
#     plt.savefig("network_topology.png")


# def get_screen_size():
#     """Get the size of the primary monitor in pixels."""
#     monitor = get_monitors()[0]
#     width_px = monitor.width
#     height_px = monitor.height
#     return width_px, height_px


# def get_host_name_by_address(host_address):
#     """
#     Get the host name from the MySQL table by passing the host address.

#     Args:
#     host_address (str): The host address to search for.

#     Returns:
#     str: The host name associated with the given host address, or None if not found.
#     """
#     try:
#         # Establish the connection to the MySQL database
#         connection = mysql.connector.connect(
#             host="10.230.230.200", database="centreon", user="root", password="snms"
#         )

#         if connection.is_connected():
#             cursor = connection.cursor()
#             # Prepare the query to fetch the host name by host address
#             query = "SELECT host_name FROM host WHERE host_address = %s"
#             cursor.execute(query, (host_address,))
#             result = cursor.fetchone()

#             # If a result is found, return the host name
#             if result:
#                 return result[0]
#             else:
#                 return host_address

#     except Error as e:
#         print(f"Error while connecting to MySQL: {e}")
#         return None

#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()


# def get_local_ports(target, user, auth_key, priv_key, auth_protocol, priv_protocol):
#     local_ports = {}

#     # Base OID for ifDescr
#     # if_descr_oid = '1.3.6.1.2.1.2.2.1.2'
#     if_descr_oid = ".1.3.6.1.2.1.31.1.1.1.1"

#     # Iterate over the interface description table
#     for errorIndication, errorStatus, errorIndex, varBinds in nextCmd(
#         SnmpEngine(),
#         UsmUserData(
#             user,
#             auth_key,
#             priv_key,
#             authProtocol=auth_protocol,
#             privProtocol=priv_protocol,
#         ),
#         UdpTransportTarget((target, 161)),
#         ContextData(),
#         ObjectType(ObjectIdentity(if_descr_oid)),
#         lexicographicMode=False,
#     ):
#         if errorIndication:
#             print(f"Error: {errorIndication}")
#             break
#         elif errorStatus:
#             print(
#                 "%s at %s"
#                 % (
#                     errorStatus.prettyPrint(),
#                     errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
#                 )
#             )
#             break
#         elif varBinds:
#             for varBind in varBinds:
#                 oid, value = varBind

#                 oid_str = oid.prettyPrint()
#                 value_str = value.prettyPrint()

#                 port_index = oid_str.split(".")[-1]
#                 local_ports[port_index] = value_str

#     return local_ports


# # Example usage
# # subnet = ["10.231.230.0/24"]
# # all_ips = get_ips_from_subnets(subnet)
# # user = "massnmpadmn"
# # auth_key = "@Dm!n@SNMP3"
# # priv_key = "@Dm!n@SNMP3"
# # auth_protocol = usmHMACSHAAuthProtocol
# # priv_protocol = usmAesCfb128Protocol

# subnet = ["192.168.62.0/24"]
# all_ips = get_ips_from_subnets(subnet)
# user = "massnmpadmn"
# auth_key = "@Dm!n@SNMP3"
# priv_key = "@Dm!n@SNMP3"
# auth_protocol = usmHMACSHAAuthProtocol
# priv_protocol = usmAesCfb128Protocol

# active_ips = scan_subnet(all_ips)
# print(active_ips)
# graph = build_topology(
#     active_ips, user, auth_key, priv_key, auth_protocol, priv_protocol
# )
# draw_topology(graph)
