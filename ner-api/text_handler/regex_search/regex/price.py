import os
import regex as re
import json
from typing import Optional

with open(os.path.dirname(__file__)+'/../b_w_lists/price.json') as file:
    price_bw = json.load(file)
regex_string = r"((\p{Sc}\s?[0-9,.]+)|([0-9,.]+\s?(DKK|USD|CNY|EUR|DKK|USD|BTC|XBT|ETC|LTC|XRP|USD|XMR|kr|dollar|dollars|euros|euro|kroner|yen|rubler|bitcoin|ethereum)[.,-]?)|([0-9,.]+,\-)|([0-9,.]{3,}))"
tag_name = "PRIS"
category_guid = "18f3ebfd-f5b9-48ef-987b-d4f32328db31"

whitelist_words = set(price_bw["whitelist"])
blacklist_words = set(price_bw["blacklist"])
words_count = 4
whitelist_required = True

class Price:
    def __init__(self) -> None:
        pass
    
    def match_regex(self, text: str, sensitive: Optional[bool] = True):
        if text:
            regex_compiled = re.compile(regex_string)
            for match_num, match in enumerate(regex_compiled.finditer(text), 1):
                result = match.group(1)
                price = result
                price_only = re.sub(r"([^0-9,.]*)([0-9,.]+)([^0-9,.]*)", r"\2", price)
                price_only = re.sub(r"([0-9,.]+)([.,]$)" ,r"\1" , price_only)
                price_only = re.sub(r"(^[.,])([0-9,.]+)" ,r"\2" , price_only)
                pre_price = re.sub(rf"([^0-9]*){price_only}([^0-9]*)", r"\1", price)
                post_price = re.sub(rf"([^0-9]*){price_only}([^0-9]*)", r"\2", price)
                if price_only == "." or price_only == ",    ":
                    continue
                if pre_price == None or pre_price == "":
                    pre_price = 0
                else:
                    pre_price = len(pre_price)
                if post_price == None or post_price == "":
                    post_price = 0
                else:
                    post_price = len(post_price)
                
                start_index, end_index = match.span()
                # Getting surrounding text and words.
                proximate_text = text[max(start_index - 40, 0):end_index + 40]
                proximate_words = get_nearby_words(text, start_index, end_index, words_count)
                
                # Remove sensitive data from final result
                if sensitive:
                    price_only = re.sub(r"\d", "X", price_only)
                    proximate_text = re.sub(r"\d", "0", proximate_text)
                is_valid = check_match(proximate_words, result, whitelist_required)
                if is_valid:
                    yield {
                        "offset": [start_index+pre_price, end_index+post_price],
                        "match": price_only,
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
def check_match(proximate_words, result, whitelist_required):
    for b_word in blacklist_words:
        for p_word in proximate_words:
            if b_word.lower() in p_word.lower():
                return False
    
    if whitelist_required:
        in_whitelist = False
        for w_word in whitelist_words:
            for p_word in proximate_words:
                if re.search(rf"\b{w_word.lower()}\b", p_word.lower()):
                    in_whitelist = True
            if w_word in result:
                in_whitelist = True
        if not in_whitelist:
            return False
    return True