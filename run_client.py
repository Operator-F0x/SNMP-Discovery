import asyncio
from snmp_hlapi.v1.v1_get import v1_get

if __name__ == "__main__":
    asyncio.run(v1_get())