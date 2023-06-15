# settings.py
import os
from dotenv import load_dotenv


dotenv_variables = True  # use a variable from .env, the same variables will be overwritten

main_chat_id = -1009876543210  # chat_id

telegram_bot_api_token = "9876543210:XXX_XXXXXXXXXXXXX-XXXXXX-XXXXXXXXXX"
replicate_api_token = "X9_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

dev_mode = True  # activate /handlers/other.py
dev_admin_id = -1  # -1 or telegram_user_id for restrict development commands

# the number of available AI generations to user and time before restore
generations_available_to_user = 25
restore_time = 60*60*24  # sec.


if dotenv_variables:
    if not os.path.isfile(".env"):
        open(".env", "w", encoding="utf-8")
    load_dotenv()
    main_chat_id = int(os.getenv("MAIN_CHAT_ID", main_chat_id))
    dev_mode = os.getenv("DEV_MODE", dev_mode)
    dev_admin_id = int(os.getenv("DEV_ADMIN_ID", dev_admin_id))
    generations_available_to_user = int(os.getenv("GENERATIONS_AVAILABLE_TO_USER", generations_available_to_user))
    restore_time = int(os.getenv("RESTORE_TIME", restore_time))

if not os.getenv("TELEGRAM_BOT_API_TOKEN", False):
    os.environ["TELEGRAM_BOT_API_TOKEN"] = telegram_bot_api_token
if not os.getenv("REPLICATE_API_TOKEN", False):
    os.environ["REPLICATE_API_TOKEN"] = replicate_api_token

