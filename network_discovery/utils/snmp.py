from pysnmp.hlapi import *

def snmp_discovery(target, user, auth_key, priv_key, auth_protocol, priv_protocol, base_oid):
    """
    Perform SNMP discovery on a target device.

    This function uses SNMPv3 to query a target device and retrieve information
    based on the provided base OID. The results are returned as a list of tuples,
    where each tuple contains the OID and its corresponding value.

    Parameters:
    target (str): The IP address or hostname of the target device.
    user (str): The SNMPv3 username.
    auth_key (str): The SNMPv3 authentication key.
    priv_key (str): The SNMPv3 privacy key.
    auth_protocol (Object): The SNMPv3 authentication protocol (e.g., usmHMACSHAAuthProtocol).
    priv_protocol (Object): The SNMPv3 privacy protocol (e.g., usmAesCfb128Protocol).
    base_oid (str): The base OID to start the SNMP walk.

    Returns:
    list: A list of tuples, where each tuple contains an OID (str) and its corresponding value (str).

    Example:
    >>> results = snmp_discovery(
    ...     target='192.168.1.1',
    ...     user='myUser',
    ...     auth_key='authKey123',
    ...     priv_key='privKey123',
    ...     auth_protocol=usmHMACSHAAuthProtocol,
    ...     priv_protocol=usmAesCfb128Protocol,
    ...     base_oid='1.3.6.1.2.1.1'
    ... )
    >>> for oid, value in results:
    ...     print(f"{oid}: {value}")
    1.3.6.1.2.1.1.1.0: My Device Description
    1.3.6.1.2.1.1.2.0: 1.3.6.1.4.1.8072.3.2.10
    1.3.6.1.2.1.1.3.0: 123456
    """
    results = []
    for errorIndication, errorStatus, errorIndex, varBinds in nextCmd(
        SnmpEngine(),
        UsmUserData(
            user,
            auth_key,
            priv_key,
            authProtocol=auth_protocol,
            privProtocol=priv_protocol,
        ),
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

def get_snmp_neighbors(ip, user, auth_key, priv_key, auth_protocol, priv_protocol):
    """
    Retrieve SNMP neighbors using LLDP and CDP protocols.
    This function queries the given IP address for neighbors using both LLDP (Link Layer Discovery Protocol)
    and CDP (Cisco Discovery Protocol) via SNMP (Simple Network Management Protocol).
    Parameters:
    ip (str): The IP address of the device to query.
    user (str): The SNMPv3 username.
    auth_key (str): The SNMPv3 authentication key.
    priv_key (str): The SNMPv3 privacy key.
    auth_protocol (str): The SNMPv3 authentication protocol (e.g., 'MD5', 'SHA').
    priv_protocol (str): The SNMPv3 privacy protocol (e.g., 'DES', 'AES').
    Returns:
    list: A list of neighbors discovered via LLDP and CDP.
    Example:
    >>> neighbors = get_snmp_neighbors("192.168.1.1", "snmpuser", "authkey", "privkey", "SHA", "AES")
    >>> for neighbor in neighbors:
    ...     print(neighbor)
    """
    neighbors = []

    def get_lldp_neighbors():
        lldp_oid = "1.0.8802.1.1.2.1.4"
        return snmp_discovery(ip, user, auth_key, priv_key, auth_protocol, priv_protocol, lldp_oid)

    def get_cdp_neighbors():
        cdp_oid = ".1.3.6.1.4.1.9.9.23.1.2.1"
        return snmp_discovery(ip, user, auth_key, priv_key, auth_protocol, priv_protocol, cdp_oid)

    neighbors.extend(get_lldp_neighbors())
    neighbors.extend(get_cdp_neighbors())

    return neighbors

def get_local_ports(target, user, auth_key, priv_key, auth_protocol, priv_protocol):
    """
    Retrieve local port descriptions from a target SNMP-enabled device.
    This function uses SNMP to query a target device for its local port descriptions
    and returns them in a dictionary where the keys are port indices and the values
    are the port descriptions.
    Parameters:
    target (str): The IP address or hostname of the target SNMP device.
    user (str): The SNMPv3 username.
    auth_key (str): The SNMPv3 authentication key.
    priv_key (str): The SNMPv3 privacy key.
    auth_protocol (Object): The SNMPv3 authentication protocol (e.g., usmHMACSHAAuthProtocol).
    priv_protocol (Object): The SNMPv3 privacy protocol (e.g., usmAesCfb128Protocol).
    Returns:
    dict: A dictionary where the keys are port indices (as strings) and the values
          are the corresponding port descriptions.
    Example:
    >>> target = "192.168.1.1"
    >>> user = "snmpuser"
    >>> auth_key = "authkey123"
    >>> priv_key = "privkey123"
    >>> auth_protocol = usmHMACSHAAuthProtocol
    >>> priv_protocol = usmAesCfb128Protocol
    >>> ports = get_local_ports(target, user, auth_key, priv_key, auth_protocol, priv_protocol)
    >>> print(ports)
    {'1': 'GigabitEthernet0/1', '2': 'GigabitEthernet0/2', ...}
    Note:
    This function requires the `pysnmp` library to be installed.
    """
    local_ports = {}
    if_descr_oid = ".1.3.6.1.2.1.31.1.1.1.1"

    for errorIndication, errorStatus, errorIndex, varBinds in nextCmd(
        SnmpEngine(),
        UsmUserData(
            user,
            auth_key,
            priv_key,
            authProtocol=auth_protocol,
            privProtocol=priv_protocol,
        ),
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