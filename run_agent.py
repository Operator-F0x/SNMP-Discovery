import asyncio
from tests.agent_context import start_agent

async def main():
    await start_agent(enable_custom_objects=True)

if __name__ == "__main__":
    asyncio.run(main())