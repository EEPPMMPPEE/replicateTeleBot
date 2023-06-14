# Replicate Telegram Bot

+ [About](#about)
+ [Requirements](#requirements)
+ [API tokens](#apitokens)
+ [Installation](#installation)
+ [Setup](#setup)
+ [Configuring](#configuring)
+ [License](#license)

## About <a name = "about"></a>
Many differently trained models such as stable diffusion and others already exist and do not cease to appear. This asynchronous telegram bot is designed to give easy and comfortable access to this great variety of models using telegram and replicate.

You can look on this bot in Telegram: [@how_to_AI](https://t.me/how_to_AI/2858)

At the moment, only text-to-image and text+image-to-image models are supported.

## Requirements <a name = "requirements"></a>

Running project requires:
* Python (tested under Python 3.11)

## API tokens <a name = "apitokens"></a>

These project needs these API tokens:

```TELEGRAM_BOT_TOKEN``` - Telegram Bot API token which you can get here after creation of your bot: [@BotFather](https://t.me/BotFather)

```REPLICATE_API_TOKEN``` - replicate API token which you can get here after registration: [Replicate](https://replicate.com/account/api-tokens)


## Installation <a name = "installation"></a>

1. Clone the repo
   ```sh
   git clone https://github.com/EEPPMMPPEE/replicateTeleBot
   ```

2. Install pip packages
   ```sh
   pip3 install -U -r requirements.txt
    ```


## Setup <a name = "setup"></a>

1. Enter your TELEGRAM_BOT_TOKEN and REPLICATE_API_TOKEN in `settings.py`.
    ```
    telegram_bot_api_token = "9876543210:XXX_XXXXXXXXXXXXX-XXXXXX-XXXXXXXXXX"
    replicate_api_token = "X9_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ```
2. Add the bot to the group chat in which it will be used. If you are only going to use the bot in a private chat, skip this step.
3. Run the bot for the first time.
    ```sh
    python3 bot.py
    ```
4. Send the message "/devtool id" to the bot. In response, you should get `your id` and the `id of the chat` in which you are writing. Enter this data into settings.py.
    ```
    dev_admin_id = "your id"
    main_chat_id = "chat id"
    ```
5. Finally, restart the bot. Everything is ready, the bot should work with the basic configuration. Send him the command "/help" to learn how to work with him.

## Configuring <a name = "configuring"></a>

* You can replace the text used in the bot in `template_objects/text.json`
* The models are configured in the file `ai_modules/replicate_models.json`
```json5
{
  "SD": { //The /{command} that the bot handles. In this situation "/SD"
    "thread_id": -1, //If you are using the threads in Telegram you can limit the handling of the request to a separate thread.
    "model": "stability-ai/stable-diffusion", //Model name, you can find the name at replicate.com
    "version": "db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf", //Model version, you can find the version at replicate.com
    "message_data_type": [ //The message type that will be handled by this command. Only "text" and "photo" are supported
      "text"
    ],
    "params": { //You can set the default generation parameters
      "negative_prompt": ""
    },
    "prompt_extend": "", //Extension for the prompt for all requests
    "neg_prompt_extend": "", //Extension for the negative_prompt for all requests
    "short_params_converter": { //The short name of the parameter that will be sent to the bot and the full name of the parameter that will be added to the generation request
      "no": "negative_prompt" //In this situation "/SD {prompt} ::no {negative_prompt}
    }
  }
}
```


## License <a name = "license"></a>

[License](https://github.com/EEPPMMPPEE/replicateTeleBot/blob/master/LICENSE) - this project is licensed under Apache-2.0 license.