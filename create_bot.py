import os
import json
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pathlib import Path
from settings import main_chat_id, dev_mode, dev_admin_id, generations_available_to_user, restore_time


script_dir = Path(__file__).parent


def get_replicate_models(path=(script_dir / "ai_modules" / "replicate_models.json").resolve()):
    def create_default_file(path=path):
        command, model, version = \
            "SD", "stability-ai/stable-diffusion", "db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf"
        message_data_type = ["text"]
        prompt_extend, neg_prompt_extend = "", ""
        params = {"negative_prompt": ""}
        short_params_converter = {"no": "negative_prompt"}
        default_replicate_models = {
            command: {
                "thread_id": -1,
                "model": model,
                "version": version,
                "message_data_type": message_data_type,
                "params": params,
                "prompt_extend": prompt_extend,
                "neg_prompt_extend": neg_prompt_extend,
                "short_params_converter": short_params_converter
            }
        }
        with open(path, 'w') as new_file:
            json.dump(default_replicate_models, new_file, indent=2)
        return default_replicate_models

    if not os.path.isfile(path):
        return create_default_file()

    try:
        with open(path) as file:
            replicate_models = json.load(file)
    except json.JSONDecodeError:
        print('JSONDecodeError: "ai_modules/replicate_models.json"\n'
              '"ai_modules/replicate_models_default.json" was used instead')
        replicate_models = create_default_file(path=(script_dir / "ai_modules" / "replicate_models_default.json").resolve())

    return replicate_models


def get_text_dict(path=(script_dir / "template_objects" / "texts.json").resolve()):
    def create_default_file(path=path):
        text_dict = {
            "generation_in_progress": "Generation in progress...",
            "an_error_has_occurred": "An error has occurred",
            "run_out_of_uses_please_wait": "Run out of uses, please wait",
            "/help": "/draw <<prompt>>"
        }
        with open(path, 'w') as new_file:
            json.dump(text_dict, new_file, indent=2)
        return text_dict

    if not os.path.isfile(path):
        return create_default_file()

    try:
        with open(path) as file:
            text_dict = json.load(file)
    except json.JSONDecodeError:
        print('JSONDecodeError: "template_objects/text.json"\n'
              '"template_objects/text_default.json" was used instead')
        text_dict = create_default_file(path=(script_dir / "template_objects" /" text_default.json").resolve())

    return text_dict


storage = MemoryStorage()

dev_mode = dev_mode
dev_admin_id = dev_admin_id
main_chat_id = main_chat_id
generations_available_to_user = generations_available_to_user
restore_time = restore_time

replicate_models = get_replicate_models()
replicate_calls = [f"/{x} " for x in replicate_models.keys()]

text_dict = get_text_dict()

bot = Bot(token=os.getenv('TELEGRAM_BOT_API_TOKEN'))
dp = Dispatcher(bot, storage=storage)
