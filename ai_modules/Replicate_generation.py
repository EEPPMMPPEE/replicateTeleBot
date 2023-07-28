import replicate
import re
from replicate.exceptions import ModelError, ReplicateError
from asyncio import sleep
from datetime import datetime, timedelta


def replicate_sd_regex(in_str: str):
    text = in_str.replace("\n", " ")
    match = re.fullmatch(r"^/(?P<model>[a-z]{2,3})\s(?P<prompt>.+?)(?P<params>\s::.+)?$", text, flags=re.DOTALL)
    if not match:
        return None
    match_dict = match.groupdict()
    if match_dict['params']:
        params_dict = dict()
        raw_params_list = re.split(r"\s(?=::)", match_dict['params'].strip(), flags=re.DOTALL)
        for param in raw_params_list:
            param_match = re.fullmatch(r"::(?P<param_name>.*?)\s(?P<param_prompt>.*)", param, flags=re.DOTALL)
            if not param_match:
                continue
            param_name, param_prompt = param_match.groups()
            params_dict[param_name] = f"{params_dict.get(param_name, '')}, {param_prompt}".strip(', ')
        match_dict['params'] = params_dict
    return match_dict


def params_name_converter(short_params_converter, raw_params=None):
    if raw_params is None:
        raw_params = {}
    res_dict = {}
    for key, value in raw_params.items():
        if key in short_params_converter:
            res_dict[short_params_converter[key]] = value
    return res_dict


async def replicate_gen(prompt, model_dict, raw_params=None, reload_time=15, media=False):
    model_name, version_name = model_dict['model'], model_dict['version']
    params = model_dict["params"] | params_name_converter(model_dict['short_params_converter'], raw_params=raw_params)
    if model_dict['prompt_extend']:
        prompt = f"{prompt}, {model_dict['prompt_extend']}"
    negative_param_name = model_dict['short_params_converter'].get('no', '')
    if model_dict['neg_prompt_extend'] and negative_param_name:
        params[negative_param_name] = f"{params.get(negative_param_name, '')}, {model_dict['neg_prompt_extend']}".strip(', ')
    if media:
        params['image'] = media

    model = replicate.models.get(model_name)
    version = model.versions.get(version_name)
    prediction = replicate.predictions.create(
        version=version,
        input={"prompt": prompt} | params)

    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=8)

    while True:
        await sleep(reload_time)
        prediction.reload()
        if prediction.status == 'succeeded':
            break
        if datetime.now() > end_time:
            prediction.cancel()
            raise ReplicateError("timeoutError")
        if prediction.status == 'failed':
            raise ModelError(prediction.error)
    return prediction.output[0]

