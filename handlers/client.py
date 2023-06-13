import functools
from itertools import count
from asyncio import sleep
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaPhoto
from aiogram.utils.exceptions import ChatNotFound, CantInitiateConversation, CantTalkWithBots, BotBlocked
from replicate.exceptions import ModelError, ReplicateError
from create_bot import dp, bot, main_chat_id, replicate_models, replicate_calls, restore_time, generations_available_to_user, text_dict
from ai_modules import replicate_gen, replicate_sd_regex


class OrdStates(StatesGroup):
    restore_state = State()


def auth_decorator(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        message, *_ = args
        message: types.Message
        checks = all([
            message.chat.id == main_chat_id
        ])
        if checks:
            await func(*args, **kwargs)
        else:
            return None

    return wrapper


def wait_redirection(func):
    async def please_wait(message: types.Message, state: FSMContext):
        text = text_dict["run_out_of_uses_please_wait"]
        await message.delete()
        try:
            await bot.send_message(message.from_user.id, text)
        except (ChatNotFound, CantInitiateConversation, CantTalkWithBots, BotBlocked):
            pass

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        message, *_ = args
        state = kwargs['state']
        message: types.Message
        state: FSMContext
        async with state.proxy() as data:
            check = data.get("last_num", generations_available_to_user)
        if check <= generations_available_to_user:
            await func(*args, **kwargs)
        else:
            await please_wait(*args, **kwargs)

    return wrapper


@auth_decorator
async def sd_prompt(message: types.Message, state: FSMContext):
    message_content_type = message.content_type
    message_text = {"text": message.text, "photo": message.caption}[message_content_type]
    regex_dict = replicate_sd_regex(message_text)

    if not regex_dict:
        return

    command, prompt, raw_params = regex_dict.values()

    if replicate_models[command]["thread_id"] not in (-1, message.message_thread_id):
        return
    if message_content_type not in replicate_models[command]["message_data_type"]:
        return

    if message_content_type == "photo":
        file_id = message.photo[-1].file_id
        file_path = (await bot.get_file(file_id)).file_path
        url = bot.get_file_url(file_path=file_path)
    else:
        url = False

    if not await state.get_state():
        await OrdStates.restore_state.set()
    async with state.proxy() as data:
        count_generator = data.setdefault("count_generation", count(start=2))
        user_count = next(count_generator)
        data["last_num"] = user_count

    mes_id = (await message.reply_photo(open(r'./template_objects/base_img.jpg', 'rb'), text_dict["generation_in_progress"]))[
        'message_id']
    try:
        output = await replicate_gen(prompt, replicate_models[command], raw_params=raw_params, media=url)
        media_file = InputMediaPhoto(media=output, caption="")
        await bot.edit_message_media(media=media_file, chat_id=message.chat.id, message_id=mes_id)
        try:
            await bot.send_document(chat_id=message.from_user.id, document=output)
        except (ChatNotFound, CantInitiateConversation, CantTalkWithBots, BotBlocked):
            pass
    except (ModelError, ReplicateError) as err:
        await bot.edit_message_caption(message.chat.id, mes_id, caption=f"{text_dict['an_error_has_occurred']}:\n{err}")

    if user_count == 2:
        await sleep(restore_time)
        await state.finish()


@auth_decorator
@wait_redirection
async def router_message_handler(message: types.Message, state: FSMContext):
    return await sd_prompt(message, state=state)


@auth_decorator
async def help_message(message: types.Message):
    await message.answer(text_dict["/help"])


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(help_message, Text(['/help']), content_types=["text"], state='*')
    dp.register_message_handler(router_message_handler, Text(startswith=replicate_calls), content_types=["text", "photo"],
                                state=OrdStates.restore_state)
    dp.register_message_handler(sd_prompt, Text(startswith=replicate_calls), content_types=["text", "photo"])
