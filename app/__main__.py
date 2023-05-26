import asyncio

from app import PLUGINS_DIR
from app.utils.plugins_manager.impl import plugins_manager
from app.utils.plugins_manager.utils import loads_plugins


async def main():
    loads_plugins(path_to_plugins=PLUGINS_DIR)
    print(plugins_manager.list())


loop = asyncio.get_event_loop()
try:
    asyncio.run(main())
finally:
    loop.run_until_complete(plugins_manager.unloads())
    loop.close()
