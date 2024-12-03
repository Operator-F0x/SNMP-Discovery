from pysnmp.hlapi import *

def snmp_discovery(target, version, community=None, user=None, auth_key=None, priv_key=None, auth_protocol=None, priv_protocol=None, base_oid='1.3.6.1.2.1.1'):
    """
    Perform SNMP discovery on a target device.

    Parameters:
    target (str): The IP address or hostname of the target device.
    version (int): The SNMP version to use (1, 2, or 3).
    community (str, optional): The community string for SNMPv1 and SNMPv2c.
    user (str, optional): The username for SNMPv3.
    auth_key (str, optional): The authentication key for SNMPv3.
    priv_key (str, optional): The privacy key for SNMPv3.
    auth_protocol (Object, optional): The authentication protocol for SNMPv3.
    priv_protocol (Object, optional): The privacy protocol for SNMPv3.
    base_oid (str, optional): The base OID to start the discovery from. Default is '1.3.6.1.2.1.1'.

    Returns:
    list: A list of tuples containing OID and value pairs discovered.

    Raises:
    ValueError: If required parameters for the specified SNMP version are missing or if an invalid SNMP version is provided.

    Example:
    >>> snmp_discovery('192.168.1.1', 2, community='public')
    [('1.3.6.1.2.1.1.1.0', 'Linux server 3.10.0-957.el7.x86_64'), ('1.3.6.1.2.1.1.5.0', 'my-server')]
    """
    results = []

    if version == 1 or version == 2:
        if not community:
            raise ValueError("Community string is required for SNMPv1 and SNMPv2c")
        user_data = CommunityData(community, mpModel=0 if version == 1 else 1)
    elif version == 3:
        if not user or not auth_key or not priv_key or not auth_protocol or not priv_protocol:
            raise ValueError("User, auth_key, priv_key, auth_protocol, and priv_protocol are required for SNMPv3")
        user_data = UsmUserData(
            user,
            auth_key,
            priv_key,
            authProtocol=auth_protocol,
            privProtocol=priv_protocol,
        )
    else:
        raise ValueError("Invalid SNMP version. Must be 1, 2, or 3.")

    for errorIndication, errorStatus, errorIndex, varBinds in nextCmd(
        SnmpEngine(),
        user_data,
        UdpTransportTarget((target, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(base_oid)),
        lexicographicMode=False,
    ):
        if errorIndication or errorStatus:
            continue
        else:
            for varBind in varBinds:
                oid_str, value_str = varBind
                results.append((oid_str.prettyPrint(), value_str.prettyPrint()))
    return results

def get_snmp_neighbors(ip, version, community=None, user=None, auth_key=None, priv_key=None, auth_protocol=None, priv_protocol=None):
    """
    Retrieve SNMP neighbors using LLDP and CDP protocols.
    This function queries the specified device for its neighbors using both
    LLDP (Link Layer Discovery Protocol) and CDP (Cisco Discovery Protocol)
    via SNMP (Simple Network Management Protocol).
    
    Parameters:
    ip (str): The IP address of the target device.
    version (int): The SNMP version to use (1, 2c, or 3).
    community (str, optional): The SNMP community string (for SNMP v1/v2c).
    user (str, optional): The SNMP user name (for SNMP v3).
    auth_key (str, optional): The authentication key (for SNMP v3).
    priv_key (str, optional): The privacy key (for SNMP v3).
    auth_protocol (str, optional): The authentication protocol (e.g., 'MD5', 'SHA') (for SNMP v3).
    priv_protocol (str, optional): The privacy protocol (e.g., 'DES', 'AES') (for SNMP v3).
    
    Returns:
    list: A list of neighbors discovered via LLDP and CDP.
    
    Example:
    >>> neighbors = get_snmp_neighbors("192.168.1.1", 2, community="public")
    >>> print(neighbors)
    [{'neighbor_ip': '192.168.1.2', 'interface': 'GigabitEthernet0/1', 'protocol': 'LLDP'}, ...]
    """
    
    neighbors = []

    def get_lldp_neighbors():
        lldp_oid = "1.0.8802.1.1.2.1.4"
        return snmp_discovery(ip, version, community, user, auth_key, priv_key, auth_protocol, priv_protocol, lldp_oid)

    def get_cdp_neighbors():
        cdp_oid = ".1.3.6.1.4.1.9.9.23.1.2.1"
        return snmp_discovery(ip, version, community, user, auth_key, priv_key, auth_protocol, priv_protocol, cdp_oid)

    neighbors.extend(get_lldp_neighbors())
    neighbors.extend(get_cdp_neighbors())

    return neighbors

def get_local_ports(target, version, community=None, user=None, auth_key=None, priv_key=None, auth_protocol=None, priv_protocol=None):
    """
    Retrieve local ports information from a network device using SNMP.

    Parameters:
    target (str): The IP address or hostname of the target device.
    version (int): The SNMP version to use (1, 2, or 3).
    community (str, optional): The community string for SNMPv1 and SNMPv2c.
    user (str, optional): The username for SNMPv3.
    auth_key (str, optional): The authentication key for SNMPv3.
    priv_key (str, optional): The privacy key for SNMPv3.
    auth_protocol (Object, optional): The authentication protocol for SNMPv3.
    priv_protocol (Object, optional): The privacy protocol for SNMPv3.

    Returns:
    dict: A dictionary where the keys are port indices and the values are port descriptions.

    Raises:
    ValueError: If required parameters for the specified SNMP version are missing or if an invalid SNMP version is provided.

    Example:
    >>> get_local_ports("192.168.1.1", 2, community="public")
    {'1': 'GigabitEthernet0/1', '2': 'GigabitEthernet0/2', ...}
    """
    local_ports = {}
    if_descr_oid = ".1.3.6.1.2.1.31.1.1.1.1"

    if version == 1 or version == 2:
        if not community:
            raise ValueError("Community string is required for SNMPv1 and SNMPv2c")
        user_data = CommunityData(community, mpModel=0 if version == 1 else 1)
    elif version == 3:
        if not user or not auth_key or not priv_key or not auth_protocol or not priv_protocol:
            raise ValueError("User, auth_key, priv_key, auth_protocol, and priv_protocol are required for SNMPv3")
        user_data = UsmUserData(
            user,
            auth_key,
            priv_key,
            authProtocol=auth_protocol,
            privProtocol=priv_protocol,
        )
    else:
        raise ValueError("Invalid SNMP version. Must be 1, 2, or 3.")

    for errorIndication, errorStatus, errorIndex, varBinds in nextCmd(
        SnmpEngine(),
        user_data,
        UdpTransportTarget((target, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(if_descr_oid)),
        lexicographicMode=False,
    ):
        if errorIndication:
            print(f"Error: {errorIndication}")
            break
        elif errorStatus:
            print(
                "%s at %s"
                % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
                )
            )
            break
        elif varBinds:
            for varBind in varBinds:
                oid, value = varBind
                oid_str = oid.prettyPrint()
                value_str = value.prettyPrint()
                port_index = oid_str.split(".")[-1]
                local_ports[port_index] = value_str

    return local_ports