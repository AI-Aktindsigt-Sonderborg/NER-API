import os
import re
import json
from typing import Optional

with open(os.path.dirname(__file__)+'/../b_w_lists/iban.json') as file:
    iban_bw = json.load(file)
regex_string = r"\b(([A-Za-z]{2})(\d{2})\s?([A-Za-z\d]{4}?\s?[A-Za-z\d]{0,4}\s?[A-Za-z\d]{0,4}\s?[A-Za-z\d]{0,}))\b"
tag_name = "IBAN"
category_guid = "15c2257d-d1f1-425e-b4d0-fcafecaea1e2"

whitelist_words = set(iban_bw["whitelist"])
blacklist_words = set(iban_bw["blacklist"])
words_count = 4
whitelist_required = False
iban_code_length = {
    "AD": 24, "AE": 23, "AT": 20, "AZ": 28, "BA": 20, "BE": 16, "BG": 22, "BH": 22, "BR": 29,
    "CH": 21, "CR": 21, "CY": 28, "CZ": 24, "DE": 22, "DK": 18, "DO": 28, "EE": 20, "ES": 24,
    "FI": 18, "FO": 18, "FR": 27, "GB": 22, "GI": 23, "GL": 18, "GR": 27, "GT": 28, "HR": 21,
    "HU": 28, "IE": 22, "IL": 23, "IS": 26, "IT": 27, "JO": 30, "KW": 30, "KZ": 20, "LB": 28,
    "LI": 21, "LT": 20, "LU": 20, "LV": 21, "MC": 27, "MD": 24, "ME": 22, "MK": 19, "MR": 27,
    "MT": 31, "MU": 30, "NL": 18, "NO": 15, "PK": 24, "PL": 28, "PS": 29, "PT": 25, "QA": 29,
    "RO": 24, "RS": 22, "SA": 24, "SE": 24, "SI": 19, "SK": 24, "SM": 27, "TN": 24, "TR": 26,   
    "AL": 28, "BY": 28, "CR": 22, "EG": 29, "GE": 22, "IQ": 23, "LC": 32, "SC": 31, "ST": 25,
    "SV": 28, "TL": 23, "UA": 29, "VA": 22, "VG": 24, "XK": 20
};

class IBAN:
    def __init__(self) -> None:
        pass
    
    def match_regex(self, text: str, sensitive: Optional[bool] = True):
       if text:
            regex_compiled = re.compile(regex_string)
            for match_num, match in enumerate(regex_compiled.finditer(text), 1):
                result = match.group(1)
                iban = result.replace(" ", "")
                # IBAN can have multiple different lengths depending on the country.
                if len(iban) != iban_code_length.get(match.group(2)):
                    continue
                
                start_index, end_index = match.span()
                
                # Getting surrounding text and words.
                proximate_text = text[max(start_index - 40, 0):end_index + 40]
                proximate_words = get_nearby_words(text, start_index, end_index, words_count)
                
                # Remove sensitive data from final result
                if sensitive:
                    result = result[0:6] + "XXXXXXXXXX"
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