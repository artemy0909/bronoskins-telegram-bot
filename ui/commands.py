from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    command_list = [
        types.BotCommand("create", "Новая пленка"),
        types.BotCommand("change", "Смена"),
        types.BotCommand("find", "Найти запись о пленке"),
        types.BotCommand("materials", "Списание и приход материала"),
        types.BotCommand("cash", "Касса"),
        types.BotCommand("today", "Сверка на сегодня"),
        types.BotCommand("cuts", "Добавить резы"),
        types.BotCommand("reports", "Ежемесячные отчеты"),
        types.BotCommand("stuff", "Работники"),

    ]
    await dp.bot.set_my_commands(command_list)
