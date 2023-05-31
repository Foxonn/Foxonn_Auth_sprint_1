import asyncio

from dynaconf import Dynaconf

from app import PLUGINS_DIR
from app import PROJECT_DIR
from app.utils.plugins_manager.impl import plugins_manager
from app.utils.plugins_manager.utils import loads_plugins


async def main():
    settings = Dynaconf(
        envvar_prefix="AUTH",
        root_path=str(PROJECT_DIR),
        dotenv_path=PROJECT_DIR,
        load_dotenv=True,
        settings_files=["settings.toml"],
    )
    loads_plugins(path_to_plugins=PLUGINS_DIR)
    await plugins_manager.loads(plugins_settings=settings.plugins, orders=settings.orders_plugin)


loop = asyncio.get_event_loop()
try:
    asyncio.run(main())
finally:
    loop.run_until_complete(plugins_manager.unloads())
    loop.close()
