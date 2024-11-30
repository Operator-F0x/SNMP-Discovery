import wmi
import winrm

def discover_windows_server(ip, username, password):
    # Create a WMI connection
    connection = wmi.WMI(ip, user=username, password=password, namespace="root\\cimv2")
    
    # Query to get the device name
    device_info = connection.Win32_ComputerSystem()[0]
    device_name = device_info.Name

    # Query to get the connected ports
    ports_info = connection.Win32_NetworkAdapterConfiguration(IPEnabled=True)
    connected_ports = []
    for port in ports_info:
        if port.DefaultIPGateway:
            connected_ports.append((port.Description, port.MACAddress))

    return device_name, connected_ports

if __name__ == "__main__":
    # Replace with your target IP, username, and password
    target_ip = "10.230.235.125"
    username = "***"
    password = "***"

    device_name, connected_ports = discover_windows_server(target_ip, username, password)

    print(f"Device Name: {device_name}")
    for port in connected_ports:
        print(f"Connected Port: {port[0]}, MAC Address: {port[1]}")

