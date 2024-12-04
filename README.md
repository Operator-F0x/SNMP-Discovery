# SNMP Discovery Script

This Python script uses SNMP (Simple Network Management Protocol) to discover devices on a network. It queries network devices for information and displays the results.

## Features

- Discovers devices on the network using SNMP
- Retrieves and displays device information
- Supports SNMPv1, SNMPv2c, and SNMPv3

## Requirements

- Python 3.x
- `pysnmp` library
- `networkx` library
- `matplotlib` library
- `mysql-connector-python` library
- `screeninfo` library

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/KaSaNaa/SNMP-Discovery-Script.git
    ```

2. Navigate to the project directory:

    ```sh
    cd SNMP-Discovery-Script
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Set up the environment variables for the database connection in a `.env` file:

    ```sh
    DB_HOST=your_host
    DB_NAME=your_database
    DB_USER=your_user
    DB_PASSWORD=your_password
    ```

2. Run the script:

    ```sh
    python main.py
    ```

## Configuration

The script uses environment variables for configuration. Ensure that the `.env` file contains the necessary database connection details.

## Project Structure

The project is organized into the following modules:

- `network_utils.py`: Contains network-related utilities.
- `snmp_manager.py`: Manages SNMP-related functionalities.
- `database_manager.py`: Handles database interactions.
- `graph_manager.py`: Builds and draws network topology graphs.
- `screen_utils.py`: Provides screen-related utilities.

## Example

Here is an example of how to use the script:

```python
from utils.network_utils import NetworkUtils
from utils.snmp_manager import SNMPManager
from utils.graph_manager import GraphManager
import json

# Example usage
if __name__ == "__main__":
    subnet = ["192.168.62.0/24"]
    all_ips = NetworkUtils.get_ips_from_subnets(subnet)

    active_ips = NetworkUtils.scan_subnet(all_ips)
    print("\n\nActive IPs")
    for ip in active_ips:
        print(ip)
    
    all_neighbors = {}
    snmp_manager = SNMPManager(2, community="public")
    
    for ip in active_ips:
        neighbors = snmp_manager.get_snmp_neighbors(ip)
        local_ports = snmp_manager.get_local_ports(ip)
        all_neighbors[ip] = {
            "neighbors": neighbors,
            "ports": local_ports
        }

    print("\n\nNeighbors for", ip)
    print(neighbors)
    print("Ports for", ip)
    print(local_ports)
    
    graph_manager = GraphManager(2, community="public")
    G = graph_manager.build_topology(active_ips)
    graph_manager.draw_topology(G)

    # Save the neighbors and ports data to a JSON file
    with open('neighbors.json', 'w') as json_file:
        json.dump(all_neighbors, json_file, indent=4)
```

## Detailed Class and Function Usage

### `NetworkUtils`

- **`get_local_ip()`**: Retrieves the local IP address of the system.
- **`save_local_ip_to_env()`**: Saves the local IP address to the `.env` file under the `DB_HOST` variable.
- **`get_dns_hostname(ip)`**: Retrieves the DNS hostname for a given IP address.
- **`ping_ip(ip_str)`**: Pings an IP address to check if it is reachable.
- **`get_ips_from_subnets(subnets)`**: Generates a list of all possible IP addresses from a list of subnets.
- **`scan_subnet(ip_list)`**: Scans a list of IP addresses to determine which ones are active.

### `SNMPManager`

- **`__init__(version, community=None, user=None, auth_key=None, priv_key=None, auth_protocol=None, priv_protocol=None)`**: Initializes the SNMP manager with the specified SNMP version and credentials.
- **`snmp_discovery(target, base_oid='1.3.6.1.2.1.1')`**: Performs SNMP discovery on a target device.
- **`get_snmp_neighbors(ip)`**: Retrieves SNMP neighbors using LLDP and CDP protocols.
- **`get_local_ports(target)`**: Retrieves local ports information from a network device using SNMP.

### `DatabaseManager`

- **`__init__()`**: Initializes the database manager with connection details from environment variables.
- **`get_host_name_by_address(host_address)`**: Retrieves the hostname for a given IP address from the database.

### `GraphManager`

- **`__init__(version, community=None, user=None, auth_key=None, priv_key=None, auth_protocol=None, priv_protocol=None)`**: Initializes the graph manager with the specified SNMP version and credentials.
- **`build_topology(active_ips)`**: Builds a network topology graph using SNMP data.
- **`draw_topology(graph)`**: Draws the network topology graph and saves it as an image.

### `ScreenUtils`

- **`get_screen_size()`**: Retrieves the size of the primary monitor in pixels.

## License

This project is licensed under the GNU GENERAL PUBLIC License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
