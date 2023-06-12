import asyncio
import logging

from dynaconf import Dynaconf
from flask import Flask

from app import PLUGINS_DIR
from app import PROJECT_DIR
from app.utils.ioc import ioc
from app.utils.message_bus.MessageBus import MessageBus
from app.utils.plugins_manager.impl.plugins_manager import plugins_manager
from app.utils.plugins_manager.utils import loads_plugins

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d/%b/%Y %H:%M:%S",
)

message_bus: MessageBus = None


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
    get_app = ioc.get_object(object_type=Flask)
    app = get_app()
    app.run(host='0.0.0.0', port=8080, debug=True)


loop = asyncio.get_event_loop()
try:
    message_bus = MessageBus(loop=loop)
    asyncio.run(main())
finally:
    loop.run_until_complete(plugins_manager.unloads())
    loop.close()
