from aiogram.utils import executor
from create_bot import dp, bot
from handlers import client, other


async def on_startup(_):
    print('Bot Online')


client.register_handlers_client(dp)
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


