from aiogram import types, Dispatcher
from create_bot import dp, bot, dev_admin_id
from aiogram.dispatcher.filters import Text


async def my_id(message: types.Message):
    if dev_admin_id in (message.from_user.id, False):
        await message.answer(f'your id:\n{message.from_user.id}\n\nchat_id:\n{message.chat.id}')
    return


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(my_id, Text(startswith='/devtool id'))
