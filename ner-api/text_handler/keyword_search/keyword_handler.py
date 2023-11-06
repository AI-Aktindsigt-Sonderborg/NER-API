from flashtext import KeywordProcessor
import json, os

# A custom class to define non-word boundaries using given predicates.
# This will assist in filtering and finding an optimal result for keywords.
class NonWordBoundaries:
    def __init__(self, *predicates):
        self.predicates = predicates
        
    def __contains__(self, ch):
        for predicate in self.predicates:
            if predicate(ch):
                return True
        return False

all_keyword_processor = KeywordProcessor()
all_keyword_processor.set_non_word_boundaries(NonWordBoundaries(str.isalpha, str.isdigit))

data_processors = []
path = os.path.dirname(__file__)+'/keyword_data/'

# Dictionary mapping categories to unique GUIDs.
category_guid = {
    "authority":"9cfc0cb9-3186-4e7c-bc86-b0762b110dd6",
    "commune":"44caa372-c0b6-48e6-ba80-2f6ff5972a4f",
    "complaint":"eccb2d7e-b255-41d4-af4a-b1c76a9c61ab",
    "crime":"e3d68e48-5f19-4e96-af56-0552cc368786",
    "diagnose":"b0eabf94-d4a1-442d-8c2f-f8c72b162ed6",
    "ethnicity":"3bd0e00d-d7ec-4f93-875a-cb960933324f",
    "gender":"0213894f-d3df-4862-825d-97f0cc1a2052",
    "medicine":"566a6a89-cc5b-459d-b001-84ca0a116d88",
    "nationality":"aa3f6cef-ff3b-4880-8baa-593c8400e23c",
    "region":"79b7f5b9-6992-44a0-9b74-5a33ab106bc1",
    "religion":"40aea378-28f3-412f-8384-0e1729060c0b",
    "religiouscommunity":"d46070fb-4a72-4edf-805d-e458462eb080",
    "sexuality":"fae355cd-9b83-40bb-88b0-92ee4ee0d181",
    "union":"9c1e3e55-9ad3-4c84-8be8-810dc46f1087",
}

# Loop through the files in the directory where the JSON keyword data files are located.
for file_name in [file for file in os.listdir(path) if file.endswith('.json')]:
    # Open each JSON file.
    with open(path + file_name) as json_file:
        # Load the data from the JSON file.
        data = json.load(json_file)
        
        # Create a new KeywordProcessor for each file and set non-word boundaries for the keyword processor.
        keyword_processor = KeywordProcessor()
        keyword_processor.set_non_word_boundaries(NonWordBoundaries(str.isalpha, str.isdigit))
        
        # Append a tuple containing the title and the keyword processor with data to the list.
        data_processors.append([data['title'], {"data": data['data'], "kw": keyword_processor}])

# Iterate over the data processors to add keywords to both the individual and the all-encompassing keyword processor.
for data_processor in data_processors:
    title = data_processor[0]
    for keyword in data_processor[1]['data']:
        # Add the keyword to the individual keyword processor with a tuple (tag, match).
        data_processor[1]['kw'].add_keyword(keyword, ({"tag": title, "match": keyword}))
        # Also add the keyword to the global keyword processor.
        all_keyword_processor.add_keyword(keyword, (title, keyword))

# Function to get the all-encompassing keyword processor.
def get_allkeywords():
    return all_keyword_processor

# Function to get a specific keyword processor by title.
def get_keyword_processor(title_get):
    for data_processor in data_processors:
        if title_get in data_processor[0]:
            return data_processor[1]['kw']
    return "no title found"

# Function to get match information based on matches, content, and sensitivity.
def provide_match_info(matches, content, sensitive, guid):
    matches_data = []
    for match in matches:
        if sensitive:
            # Replace the matched keyword with a placeholder if it's sensitive.
            keyword_match = "[SENSITIVE WORD]"
            keyword_context = None
        else:
            # If not sensitive, get the actual matched keyword and get the context of the keyword in the content
            keyword_match = match[0]['match']
            keyword_context = content[max(match[1] - 50, 0): match[2] + 50]
            
        # Append the match data to the list with a certain format.
        matches_data.append({
            "offset": [match[1], match[2]],  # The start and end indices of the match.
            "match": keyword_match,          # The matched keyword or placeholder.
            "context": keyword_context,      # The context of the keyword.
            "tag": match[0]["tag"],          # The tag associated with the keyword.
            "probability": 1.0,              # Assumed probability of the match. (useless for now. added for future validation development)
            "guid": guid,                    # The GUID associated with the category.
            "sensitivity": sensitive         # The sensitivity of the match.
        })
    return matches_data