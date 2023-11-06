import os
import re
import json
from typing import Optional

with open(os.path.dirname(__file__)+'/../b_w_lists/cvr.json') as file:
    cvr_bw = json.load(file)
regex_string = r"\b(DK)?(\d{8})\b"
tag_name = "CVR"
category_guid = "224e2d5b-ca0c-4d59-99f1-d4824ffb4abf"
whitelist_words = set(cvr_bw["whitelist"])
blacklist_words = set(cvr_bw["blacklist"])
words_count = 4
whitelist_required = True

class CVR:
    def __init__(self) -> None:
        pass
    
    def match_regex(self, text: str, sensitive: Optional[bool] = True):
        if text:
            regex_compiled = re.compile(regex_string)
            for match_num, match in enumerate(regex_compiled.finditer(text), 1):
                result = match.group(2)
                start_index, end_index = match.span()
                
                # Getting surrounding text and words.
                proximate_text = text[max(start_index - 40, 0):end_index + 40]
                proximate_words = get_nearby_words(text, start_index, end_index, words_count)
                
                # Remove sensitive data from final result
                if sensitive:
                    result = result[0:4] + "XXXX"
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