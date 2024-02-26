import sys

if not sys.version_info.major == 3 and sys.version_info.minor >= 9:
    print("Python 3.9 or higher is required")
    sys.exit(-1)

import asyncio
import config


async def on_startup(dispatcher):
    from utils.event_handlers import send_admin_token
    from utils.throttling import ThrottlingMiddleware
    from ui.commands import set_default_commands
    import logging

    dispatcher.middleware.setup(ThrottlingMiddleware())

    if config.DEBUG:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging_level)

    loop = asyncio.get_event_loop()

    await loop.create_task(send_admin_token())
    await set_default_commands(dispatcher)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
