import os
import re
import json
from typing import Optional


with open(os.path.dirname(__file__)+'/../b_w_lists/law.json') as file:
    law_bw = json.load(file)
regex_string = r"\b((\d{1,3}[,.] ?stk[,.]? ?\d{1,3}[,.] ?i? ?)?([Dd][Ii][Rr][Ee][Kk][Tt][Ii][Vv] ?)?(\d{1,4}[\/-\\., ]\d{1,4}[\/-\\., ][euføEUFØ]{2,3}))\b"
tag_name = "LAW"
category_guid = "ef4633af-ce48-442e-9d09-c7e7a4e5ca2a"


whitelist_words = set(law_bw["whitelist"])
blacklist_words = set(law_bw["blacklist"])
words_count = 4
whitelist_required = False

class Direktivnr:
    def __init__(self) -> None:
        pass
    
    def match_regex(self, text: str, sensitive: Optional[bool] = True):
        if text:
            regex_compiled = re.compile(regex_string)
            for match_num, match in enumerate(regex_compiled.finditer(text), 1):
                result = match.group(1)
                
                start_index, end_index = match.span()
                
                # Getting surrounding text and words.
                proximate_text = text[max(start_index - 40, 0):end_index + 40]
                proximate_words = get_nearby_words(text, start_index, end_index, words_count)
                
                # Remove sensitive data from final result
                if sensitive:
                    result = "XXXX/XX/XX"
                    proximate_text = re.sub(r"\d", "0", proximate_text)
                is_valid = check_match(proximate_words, whitelist_required)
                if is_valid:
                    yield {
                        "offset": [start_index, end_index],
                        "match": result,
                        "context": proximate_text,
                        "tag": tag_name,
                        "probability": 1.0,
                        "guid": category_guid,
                        "sensitivity": sensitive
                    }

# Validation method to get nearby content
def get_nearby_words(text, start, end, words_count):
    text_prev = text[max(start-60,0):start]
    text_next = text[end:end+60]
    words_prev = re.findall(r"\b\w+(?:[-'./@]\w+)*\b", text_prev) 
    words_next = re.findall(r"\b\w+(?:[-'./@]\w+)*\b", text_next)
    return words_prev[-words_count:] + words_next[:words_count]

# Validation method to match whitelist and blacklist words from surrounding text. (Important when matching numbers)
def check_match(proximate_words, whitelist_required):
    for b_word in blacklist_words:
        for p_word in proximate_words:
            if b_word.lower() in p_word.lower():
                return False
    
    if whitelist_required:
        in_whitelist = False
        for w_word in whitelist_words:
            for p_word in proximate_words:
                if w_word.lower() == p_word.lower():
                    in_whitelist = True
        if not in_whitelist:
            return False
    return True