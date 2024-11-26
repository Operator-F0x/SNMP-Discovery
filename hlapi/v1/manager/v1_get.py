import asyncio
import os
from datetime import datetime
from pysnmp.hlapi.v1arch.asyncio import *
from pysnmp.proto.rfc1905 import errorStatus as pysnmpErrorStatus
from pysnmp.smi import builder, view, compiler

getenv = os.getenv
SNMP_COMMUNITY = getenv("SNMP_COMMUNITY")
SNMP_HOST = getenv("SNMP_HOST")
SNMP_PORT = int(getenv("SNMP_PORT"))
SNMP_OID = getenv("SNMP_OID")


async def v1_get():
    snmpDispatcher = SnmpDispatcher()

    iterator = await get_cmd(
        snmpDispatcher,
        CommunityData(communityName=SNMP_COMMUNITY, mpModel=0),
        await UdpTransportTarget.create((SNMP_HOST, SNMP_PORT)),
        (ObjectType(ObjectIdentity(SNMP_OID))), None),

    errorIndication, errorStatus, errorIndex, varBinds = iterator

    assert errorIndication is None
    assert errorStatus == 0
    assert errorIndex == 0
    assert len(varBinds) == 1
    assert varBinds[0][0].prettyPrint() == getenv("SNMP_OID")
    assert varBinds[0][1].prettyPrint().startsWith("PySNMP engine version")

    name = pysnmpErrorStatus.namedValues.getName(errorStatus)
    assert name == "noError"

    snmpDispatcher.transport_dispatcher.close_dispatcher()


async def v1_get_ipv6():
    snmpDispatcher = SnmpDispatcher()

    iterator = await get_cmd(
        snmpDispatcher,
        CommunityData(communityName=getenv("SNMP_COMMUNITY"), mpModel=0),
        await Udp6TransportTarget.create(
            (getenv("SNMP_HOST"), int(getenv("SNMP_PORT"))),
            (ObjectType(ObjectIdentity(getenv("SNMP_OID"))), None),
        ),
    )

    errorIndication, errorStatus, errorIndex, varBinds = iterator

    assert errorIndication is None
    assert errorStatus == 0
    assert errorIndex == 0
    assert len(varBinds) == 1
    assert varBinds[0][0].prettyPrint() == getenv("SNMP_OID")
    assert varBinds[0][1].prettyPrint().startsWith("PySNMP engine version")

    name = pysnmpErrorStatus.namedValues.getName(errorStatus)
    assert name == "noError"

    snmpDispatcher.transport_dispatcher.close_dispatcher()
