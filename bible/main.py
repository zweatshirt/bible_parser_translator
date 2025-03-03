from bible_f_reading.bible_reading import *
from bible_to_dicts.DictOne import DictOne
from bible_to_dicts.DictTwo import DictTwo
from mem_mgmt.mem_mgmt import *
from defn_api_handling.defn_api_handling import *
from constants import *
import pickle  # will implement eventually
import json


# TODO:
# Complete the implementation of the dictionary. About 5000 words to find definitions for.
# Unfortunately this probably means using a different API.
# Add NLP phrase searching.


def main():
    bible = read_file(BIBLE_FILE)

    # bible lower cased and stripped of most punctuation
    cleaned_bible = clean_bible(bible)  # needs work

    # bible -> book -> chapter -> verse -> words
    # {str: {int: {int: [str]}}}
    b = DictOne(cleaned_bible)
    # word -> [word occurrence count, {[Strong's: Strong's occurrence count, [book, chapter, verse]]}]
    # # {str: [int, {str: int}]}
    b_two = DictTwo(cleaned_bible)
  

    # # List of JSON of as many words in the bible as possible with definitions
    dictionary_json = read_def_json_f(DEFINITIONS_JSON_FILE)
    # unreadable = read_file(LEFTOVER_WORDS_FILE)  # these words can't be understood by the API

    # delete_leftover_duplicates(LEFTOVER_WORDS_FILE)
    # delete_leftover_duplicates(DEFINITIONS_JSON_FILE)

    # # the elements in this list need to be fed to the API.
    # to_append_to_defns = dict_vals_not_in_defns(DEFINITIONS_JSON_FILE, b_two)

    # # for i in to_append_to_defns:
    # for i in to_append_to_defns:
    #     pass
    
    # # monitor process size. Currently around .4 GB which is a lot.
    # process = psutil.Process()
    # mem_size(process)
    print(b.get_key_list)

    # b_two = {k: v for k, v in b_two.items() if v is not None}
    with open('bible.json', 'w', encoding='utf-8') as fp:
        json.dump([dict(b), dict(b_two), dictionary_json], fp, indent=2)
    # with open('bible1.json', 'w', encoding='utf-8') as fp:
    #     json.dump(dict(b), fp, indent=2)
    # with open('bible2.json', 'w', encoding='utf-8') as fp:
    #     json.dump(dict(b_two), fp, indent=2)

        
if __name__ == '__main__':
    main()


# not working, I'm not sure why. Will work on later.
# It's (supposed to be) a recursive dictionaries val finding function
# def getpath(nested_dict, value, prepath=()):
#     for k, v in nested_dict.items():
#         path = prepath + (k,)
#         if v == value:  # found value
#             return path
#         elif hasattr(v, 'items'):  # v is a dict
#             p = getpath(v, value, path)  # recursive call
#             if p is not None:
#                 return p
