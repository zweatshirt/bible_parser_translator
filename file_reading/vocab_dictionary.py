from json import loads
import requests
from time import sleep
from bible_to_dicts.dict_two import DictTwo

"""
TODO:
    The functions in this file have been modified but need to be properly tested.
"""


DICTIONARY_API = 'https://api.dictionaryapi.dev/api/v2/entries/en/'


def append_api_data(file_name: str, d: DictTwo or []):
    """gets API data in the form of a json object and appends it to a .json file"""
    with open(file_name, 'a', encoding='utf-8') as f:
        for k in d:
            json_data = get_api_data(k, 60)
            if json_data:
                print(json_data)
                f.write("{}\n".format(json_data))


def get_api_data(word: str, sleep_time, sleep_count=0) -> str:
    """grabs definition of a given word from the API"""
    try:
        res = requests.get(DICTIONARY_API + word, timeout=5)
        return res.text if 'title' not in res.text else no_definition_for(word)
    except requests.exceptions.HTTPError:
        if sleep_count == 5:
            no_definition_for(word)
            raise Exception(
                'Unable to access {} for {}'.format(DICTIONARY_API, word)
            )
        sleep_count += 1
        sleep(sleep_time)
        get_api_data(word, sleep_time, sleep_count)


def no_definition_for(word: str):
    """
    if there are no definitions for a word we want to save the word for later attempts.
    should probably be rewritten so it doesn't open the file every time an append is needed.
    """

    f_append('data_files/unreadable_by_api', word)
    return None


def f_append(f_name, vals):
    """basic file append function"""
    with open(f_name, 'a', encoding='utf-8') as f:
        for v in vals:
            f.write(v)


def read_json_file(file_name) -> []:
    """returns list of all json objs from a file"""
    with open(file_name, 'r') as f:
        return [loads(line) for line in f if line.strip()]
