# import asyncio
# from tests.agent_context import start_agent

# async def main():
#     await start_agent(enable_custom_objects=True)

# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
from pysnmp.hlapi.asyncio import (
    SnmpEngine,
    UdpTransportTarget,
    CommunityData,
    ContextData,
    ObjectType,
    ObjectIdentity,
    next_cmd as nextCmd,
)

async def snmp_walk(target, community, oid, port=161):
    snmp_engine = SnmpEngine()
    transport = await UdpTransportTarget.create((target, port))
    community_data = CommunityData(community)
    context_data = ContextData()

    iterator = await nextCmd(
        snmp_engine,
        community_data,
        transport,
        context_data,
        [ObjectType(ObjectIdentity(oid))],
        lexicographicMode=False,
    )

    async for error_indication, error_status, error_index, var_binds in iterator:
        if error_indication:
            print(error_indication)
            break
        elif error_status:
            print(
                "%s at %s"
                % (
                    error_status.prettyPrint(),
                    error_index and var_binds[int(error_index) - 1][0] or "?",
                )
            )
            break
        else:
            for var_bind in var_binds:
                print(" = ".join([x.prettyPrint() for x in var_bind]))

if __name__ == "__main__":
    target = "192.168.1.1"  # Replace with the target IP address
    community = "public"  # Replace with the SNMP community string
    oid = "1.3.6.1.2.1.1"  # Replace with the OID you want to walk

    asyncio.run(snmp_walk(target, community, oid))