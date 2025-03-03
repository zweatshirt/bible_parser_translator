from json import loads
import requests
from time import sleep

from bible_to_dicts.DictTwo import DictTwo
from constants import *
from open_api_key import OPEN_API_KEY
from openai import OpenAI



"""
TODO:
    The functions in this file have been modified but need to be properly tested.
"""

client = OpenAI(api_key=OPEN_API_KEY) # chat gpt for words not provided by other API
thread = assistant = message = None # used for openAI API


def init_openai():
    assistant = client.beta.assistants.create(
        name="Dictionary",
        instructions="You provide the definitions and pronunciation of Old English words as well as their modern counterparts, returning these details in a JSON object similar to this JSON object provided but better: [{\"word\":\"snuffed\",\"phonetics\":[],\"meanings\":[{\"partOfSpeech\":\"verb\",\"definitions\":[{\"definition\":\"To inhale through the nose.\",\"synonym\":[],\"antonyms\":[]},{\"definition\":\"To turn up the nose and inhale air, as an expression of contempt; hence, to take offence.\",\"synonyms\":[],\"antonyms\":[]}],\"synonyms\":[],\"antonyms\":[]},{\"partOfSpeech\":\"verb\",\"definitions\":[{\"definition\":\"To extinguish a candle or oil-lamp flame by covering the burning end of the wick until the flame is suffocated.\",\"synonyms\":[],\"antonyms\":[]},{\"definition\":\"To trim the burnt part of a candle wick.\",\"synonyms\":[],\"antonyms\":[]},{\"definition\":\"To kill a person; to snuff out.\",\"synonyms\":[],\"antonyms\":[]}],\"synonyms\":[],\"antonyms\":[]}],\"license\":{\"name\":\"CC BY-SA 3.0\",\"url\":\"https://creativecommons.org/licenses/by-sa/3.0\"},\"sourceUrls\":[\"https://en.wiktionary.org/wiki/snuff\",\"https://en.wiktionary.org/wiki/snuffed\"]}].",
        model="gpt-4-turbo",
    )

    thread = client.beta.threads.create()

def get_openai_api_data(word):
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"I need the JSON object containing the definition and other information of this word: {word}"
)


def append_api_data(d: DictTwo or []):
    """gets API data in the form of a json object and appends it to a .json f_name"""
    with open(DEFINITIONS_JSON_FILE, 'a', encoding='utf-8') as f:
        for k in d:
            json_data = get_api_data(k, 60)
            if json_data:
                print(json_data)
                f.write("{}\n".format(json_data))


def get_api_data(word: str, sleep_time, sleep_count=0, open_ai=False) -> str:
    """grabs definition of a given word from the API"""
    word = word.casefold()  # hmmm
    if open_ai:
        get_openai_api_data(word)
    else: 
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
            get_api_data(word, sleep_time, sleep_count, open_ai=False)


def no_definition_for(word: str):
    """
    if there are no definitions for a word we want to save the word for later attempts.
    should probably be rewritten so it doesn't open the file every time an append is needed.
    a bit of a redudant function but made it for readability
    """
    f_append(LEFTOVER_WORDS_FILE, word)
    


def f_append(f_name, vals):
    """basic file append function"""
    try:

        with open(f_name, 'a', encoding='utf-8') as f:
            for v in vals:
                f.write(v)

    except FileNotFoundError as e:
        print(e)


def read_def_json_f(f_name):
    """returns list of all json objs from a file"""
    try:

        with open(f_name, 'r', encoding='utf-8') as f:
            return [loads(line) for line in f if line.strip()]

    except FileNotFoundError as e:
        print(e)


def dict_vals_not_in_defns(f_name, b_two):
    """
        Returns all the values that are in the definitions file but not in the bible dictionary.
        Mostly for bug checking.
    """
    try:

        if f_name == DEFINITIONS_JSON_FILE:
            with open(f_name, 'r', encoding='utf-8') as f:
                return [loads(line)[0]['word'] for line in f if line.strip()
                        if loads(line)[0]['word'] not in b_two.keys()]

        return "File exists but not is valid for this function."
    except FileNotFoundError as e:
        print(e)


def defns_not_in_dict(f_name, b_two):
    """
        Returns all words that are in the given file
        but are not in the dict containing the words of the bible.
        Mostly for bug checking.
    """
    try:

        with open(f_name, 'r') as f:
            if f_name == DEFINITIONS_JSON_FILE:
                lst = [loads(line)[0]['word'] for line in f if line.strip()
                       if loads(line)[0]['word'] not in b_two.keys()]
                print(lst)

            if f_name == LEFTOVER_WORDS_FILE:
                lst = [l for line in f if (l := line.replace('\n', '')) not in b_two.keys()]
                print(lst)

        return lst if lst else None

    except FileNotFoundError as e:
        print(e)


def delete_leftover_duplicates(f_name):
    """Deletes left over duplicate lines in a given file"""
    try:

        with open(f_name, 'r+', encoding='utf-8') as f:
            no_dupes = set(f.readlines())
            f.seek(0)
            f.truncate()
            [f.write("{}".format(line)) for line in no_dupes]

    except FileNotFoundError as e:
        print(e)
