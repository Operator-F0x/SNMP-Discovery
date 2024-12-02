from pysnmp.hlapi import *

def snmp_discovery(target, user, auth_key, priv_key, auth_protocol, priv_protocol, base_oid):
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